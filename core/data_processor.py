# core/data_processor.py
import json
import logging
from collections import deque
from utils.file_manager import FileManager

class DataProcessor:
    """异步数据处理器"""
    def __init__(self, file_manager: FileManager):
        self.message_queue = deque(maxlen=1000)
        self.file_manager = file_manager

    async def process(self, raw_data: str):
        """处理原始消息数据"""
        try:
            data = json.loads(raw_data)
            self._validate(data)
            self.message_queue.append(data)
            await self.file_manager.add_message(data)
            print(data)
            # 此处调用业务处理模块
            # await business.handle(data)
        except json.JSONDecodeError:
            logging.error("JSON解析失败，原始数据：%s", raw_data[:100])
        except ValidationError as e:
            logging.warning(f"数据校验失败：{str(e)}")

    def _validate(self, data: dict):
        """数据基础校验"""
        if not isinstance(data, dict):
            raise ValidationError("数据格式错误")
        if 'post_type' not in data:
            raise ValidationError("缺少必要字段: post_type")

class ValidationError(Exception):
    pass
