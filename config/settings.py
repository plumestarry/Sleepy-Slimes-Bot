# config/settings.py
from pathlib import Path
from dataclasses import dataclass

@dataclass
class PathConfig:
    PROJECT_ROOT = Path(__file__).parent.parent
    DATABASE_DIR = PROJECT_ROOT / "database"
    LOGS_DIR = DATABASE_DIR / "logs"
    TEMP_JSON = DATABASE_DIR / "received_messages.json"
    CONFIG_JSON = DATABASE_DIR / "config.json"

@dataclass
class LogConfig:
    FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    FILE_NAME = PathConfig.LOGS_DIR / "bot.log"
    LEVEL = "INFO"
    ROTATION = "00:00"
    RETENTION = 7

@dataclass
class PerfParams:
    QUEUE_SIZE = 1000
    BATCH_SIZE = 100
    FLUSH_INTERVAL = 60