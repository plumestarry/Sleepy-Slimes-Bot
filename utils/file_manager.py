# utils/file_manager.py
import json
import asyncio
import aiofiles
import logging
from config.settings import PathConfig, PerfParams

class FileManager:
    """带缓冲的异步文件管理器"""
    _instance = None
    lock = None
    buffer = None
    temp_path = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.buffer = []
            cls._instance.lock = asyncio.Lock()
            cls._instance.temp_path = PathConfig.TEMP_JSON
        return cls._instance

    async def initialize(self):
        """初始化时加载现有数据"""
        async with self.lock:
            if await self._file_exists():
                async with aiofiles.open(self.temp_path, 'r') as f:
                    content = await f.read()
                    self.buffer = json.loads(content) if content.strip() else []
            asyncio.create_task(self._auto_flush())

    async def add_message(self, data: dict):
        """异步添加消息到缓冲区"""
        async with self.lock:
            self.buffer.append(data)
            if len(self.buffer) >= PerfParams.BATCH_SIZE:
                await self._flush_buffer()

    async def clear_temp_file(self):
        """清空临时文件"""
        async with self.lock:
            self.buffer = []
            async with aiofiles.open(self.temp_path, 'w') as f:
                await f.write('[]')

    async def _auto_flush(self):
        """定时刷新缓冲区"""
        while True:
            await asyncio.sleep(PerfParams.FLUSH_INTERVAL)
            await self._flush_buffer()

    async def _flush_buffer(self):
        """批量写入文件"""
        if not self.buffer:
            return
        async with self.lock:
            try:
                async with aiofiles.open(self.temp_path, 'a') as f:
                    for buffer_data in self.buffer:
                        await f.write(json.dumps(buffer_data) + ',\n')
                self.buffer = []
            except Exception as e:
                logging.error(f"文件写入失败: {e}")

    async def _file_exists(self) -> bool:
        """异步检查文件是否存在"""
        try:
            return await aiofiles.os.path.exists(self.temp_path)
        except:
            return False
