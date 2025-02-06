# main.py
import asyncio
import platform
import logging
from utils import logger, file_manager
from core.websocket_server import WebSocketServer
from core.data_processor import DataProcessor
from core.scheduler import Scheduler
from commands.method.deepseek import DeepSeekAPI

async def main():
    """程序主入口"""
    # 初始化系统组件
    log = logger.setup_logger()
    fm = file_manager.FileManager()
    await fm.initialize()

    # 创建核心组件
    processor = DataProcessor(fm)
    server = WebSocketServer(processor.process)
    scheduler = Scheduler(fm)
    # deepseek = DeepSeekAPI()

    # 启动系统
    await asyncio.gather(
        server.start(),
        scheduler.start(),
        # deepseek.start()
    )

    # 保持运行
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        await shutdown(server, scheduler)

async def shutdown(server: WebSocketServer, scheduler: Scheduler):
    """优雅关闭系统"""
    logging.info("正在关闭服务...")
    # 关闭WebSocket服务器
    if server.server:
        server.server.close()
        await server.server.wait_closed()
    # 关闭定时任务
    if scheduler.scheduler.running:
        scheduler.scheduler.shutdown()
    # 确保文件缓冲区刷新
    await file_manager.FileManager()._flush_buffer()
    logging.info("服务已安全退出")
    # 停止事件循环
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [t.cancel() for t in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    # Windows事件循环策略设置
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt")
        
