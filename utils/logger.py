# utils/logger.py
import logging
from logging.handlers import TimedRotatingFileHandler
from config.settings import LogConfig, PathConfig

def setup_logger():
    """配置全局日志记录器"""
    PathConfig.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    formatter = logging.Formatter(LogConfig.FORMAT)
    
    # 文件处理器（带日志轮转）
    file_handler = TimedRotatingFileHandler(
        filename=PathConfig.LOGS_DIR / "bot.log",
        when='midnight',
        backupCount=LogConfig.RETENTION,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # 控制台处理器
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(LogConfig.LEVEL)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
