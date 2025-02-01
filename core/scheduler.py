# core/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import settings
import logging
import json

class Scheduler:
    """定时任务管理器"""
    def __init__(self, file_manager):
        self.scheduler = AsyncIOScheduler()
        self.file_manager = file_manager

    async def start(self):
        """启动定时任务"""
        config = self._load_clear_time()
        self.scheduler.add_job(
            self._clear_temp_file,
            'cron',
            hour=config['hour'],
            minute=config['minute']
        )
        self.scheduler.start()
        logging.info("定时任务已启动")

    async def _clear_temp_file(self):
        """执行文件清理"""
        await self.file_manager.clear_temp_file()
        logging.info("已执行每日数据清理")

    def _load_clear_time(self):
        """加载清理时间配置"""
        with open(settings.PathConfig.CONFIG_JSON) as f:
            return json.load(f)['clear_time']