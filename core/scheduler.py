# core/scheduler.py
from commands.method.message_sendformat import Message_SendFormat, Parameter_Judgment
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from commands.whitelist import WhiteList
from config.settings import PathConfig, WebSocketsConfig
import logging
import json

class Scheduler:
    """定时任务管理器"""
    def __init__(self, file_manager):
        self.scheduler = AsyncIOScheduler()
        self.file_manager = file_manager
        self.group_list = WhiteList.special_manage()["special"]

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
        await self._group_list()
        logging.info("已执行每日数据清理")

    def _load_clear_time(self):
        """加载清理时间配置"""
        with open(PathConfig.CONFIG_JSON) as f:
            return json.load(f)['clear_time']
        
    async def _group_list(self):
        """发送群组消息"""
        message_send_init = Message_SendFormat("send_group_msg", "group_id", 0).normal_message("让我看看还有哪个小可爱没睡觉喵~没睡觉的小心晚上被我抓到喵~呵呵呵哈哈哈~🤤🤤🤤")
        for group_id in self.group_list:
            message_send_init["params"]["group_id"] = group_id
            await WebSocketsConfig.SOCKET.send(json.dumps(message_send_init))
            