import logging
import os
from logging.handlers import RotatingFileHandler
from app.utils.config import Config

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))

    os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)

    file_handler = RotatingFileHandler(
        Config.LOG_FILE, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
