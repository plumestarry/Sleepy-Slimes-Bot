# config/settings.py
from pathlib import Path
from dataclasses import dataclass
import json

@dataclass
class PathConfig: 
    # PROJECT_ROOT = Path(__file__).parent.parent
    # DATABASE_DIR = PROJECT_ROOT / "database"
    DATABASE_DIR = "database/"
    LOGS_DIR = DATABASE_DIR + "logs/"
    TEMP_JSON = DATABASE_DIR + "received_messages.json"
    CONFIG_JSON = DATABASE_DIR + "config.json"
    HELP_JSON = DATABASE_DIR + "help.json"

@dataclass
class LogConfig:
    FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    FILE_NAME = PathConfig.LOGS_DIR + "bot.log"
    LEVEL = "INFO"
    ROTATION = "00:00"
    RETENTION = 7

@dataclass
class PerfParams:
    QUEUE_SIZE = 1000
    BATCH_SIZE = 100
    FLUSH_INTERVAL = 60

@dataclass
class PokeConfig:
    POKE_COUNT = 0

@dataclass
class WebSocketsConfig:
    SOCKET = None
    
@dataclass
class DeepSeekConfig:
    API_KEY = "<DeepSeek API Key>"
    API_URL = "https://api.deepseek.com"
    MESSAGES = []
