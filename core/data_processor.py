# core/data_processor.py
import json
import logging
import websockets
from collections import deque
from utils.file_manager import FileManager
from commands.message_distribution import Distribution

class DataProcessor:
    """异步数据处理器"""
    def __init__(self, file_manager: FileManager):
        self.message_queue = deque(maxlen=100)
        self.file_manager = file_manager

    async def process(self, raw_data: str, websocket: websockets.ServerConnection, manage_dict: dict[str, list[int]]):
        """处理原始消息数据"""
        try:
            if raw_data[-22:-1] != '"post_type":"message"' and raw_data[-21:-1] != '"post_type":"notice"':
                return
            data = json.loads(raw_data)
            self._validate(data)
            self.message_queue.append(data)
            await self.file_manager.add_message(data)

            # 调用加工所要的方法
            message_send = ""
            try:
                message_send = Distribution().function_selection(data, data["post_type"], manage_dict)
            except Exception as e:
                logging.error(f"调用加工所要的方法失败：{str(e)}")
            if message_send:
                await websocket.send(json.dumps(message_send))
            
        except json.JSONDecodeError:
            logging.error("JSON解析失败，原始数据：%s", raw_data[:100])
        except ValidationError as e:
            logging.warning(f"数据校验失败：{str(e)}")

    def _validate(self, data: dict):
        """数据基础校验"""
        if not isinstance(data, dict):
            raise ValidationError("数据格式错误")
        # if 'post_type' not in data:
        #     raise ValidationError("缺少必要字段: post_type")

class ValidationError(Exception):
    pass
