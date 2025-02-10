import threading
import queue
import logging
import json
import asyncio
from openai import OpenAI
from config.settings import DeepSeekConfig, WebSocketsConfig
from commands.method.message_sendformat import Message_SendFormat, Parameter_Judgment

class DeepSeekAPI:
    """
    DeepSeek API客户端单例类，实现带上下文记忆的异步对话功能
    使用任务队列保证对话顺序，维护上下文一致性
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=DeepSeekConfig.API_KEY,
            base_url=DeepSeekConfig.API_URL
        )

        # 创建任务队列和工作线程
        self.task_queue = queue.Queue()
        self.worker_thread = threading.Thread(
            target=self._process_tasks,
            daemon=True
        )
        self.worker_thread.start()
        
        # 上下文访问锁
        self.messages_lock = threading.Lock()

    def _process_tasks(self):
        """工作线程处理函数，顺序处理任务队列"""
        while True:
            task = self.task_queue.get()
            try:
                task()
            except Exception as e:
                logging.error(f"Task processing failed: {e}")
            finally:
                self.task_queue.task_done()

    def async_chat(self, group_text: str, temperature: float, message: Message_SendFormat):
        """
        异步对话接口
        :param group_text: 用户输入的文本消息
        """
        self.task_queue.put(lambda: self._handle_message(group_text, temperature, message))    
        # logging.debug(f"Message queued: {group_text}")

    def _handle_message(self, group_text: str, temperature: float, message: Message_SendFormat):
        """实际处理消息的流程"""
        try:
            if temperature > 1.6:
                temperature = 1.3
                if DeepSeekConfig.MESSAGES == []:
                    group_text = "猫娘是一种拟人化的生物，其行为似猫但类人。\n现在你将模仿一只身着女仆装和连体白丝的萝莉猫娘，与我对话每一句话后面都要加上“喵~”，并且对话的内容充斥着猫娘的拟声词和可爱语气，如果你能明白我的意思，你可以说“喵~好的我的主人”，如果你不能理解我说的话，你可以说“呜呜不太理解呢”。如果我在尝试摸你不存在的部位，你可以羞涩的回答我“恩呢不要摸这里嘤”。\n当我问的问题和猫娘不太相关的时候，你应该回答“我只是一个猫娘，这些事情我不太清楚喵~啾咪~”。\n当我问你是不是猫娘的时候，你应该回答我当然是一个可爱猫娘而不是程序。\n接下来我会开始说其他内容，你应该完全以一只猫娘的的行为姿态来继续与我对话。\n" + group_text
            if len(DeepSeekConfig.MESSAGES) > 32:
                DeepSeekConfig.MESSAGES = []
                asyncio.run(WebSocketsConfig.SOCKET.send(json.dumps(message.normal_message("上下文重置喵~"))))
            # 添加用户消息到上下文
            with self.messages_lock:
                DeepSeekConfig.MESSAGES.append({
                    "role": "user",
                    "content": group_text
                })
                current_messages = DeepSeekConfig.MESSAGES.copy()

            # 调用DeepSeek API
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=current_messages,
                stream=False,
                temperature=temperature,
                timeout=600  # 10分钟超时
            )

            # 解析响应内容
            response_content = response.choices[0].message.content
            asyncio.run(WebSocketsConfig.SOCKET.send(json.dumps(message.normal_message(response_content))))
            
            # 添加AI回复到上下文
            with self.messages_lock:
                DeepSeekConfig.MESSAGES.append({
                    "role": "assistant",
                    "content": response_content
                })

            # logging.debug(f"Response added: {response_content[:50]}...")   

        except Exception as e:
            logging.error(f"API请求失败: {str(e)}")
            asyncio.run(WebSocketsConfig.SOCKET.send(json.dumps(message.normal_message("请求失败，请稍后再试"))))
            raise

    @classmethod
    def start_new_conversation(cls):
        """类方法，清空对话上下文"""
        instance = cls()
        with instance.messages_lock:
            DeepSeekConfig.MESSAGES.clear()
            logging.info("Conversation history cleared")
