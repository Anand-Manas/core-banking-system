import logging
import os
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
APP_LOG_PATH = os.path.join(LOG_DIR, "app", "app.log")

os.makedirs(os.path.dirname(APP_LOG_PATH), exist_ok=True)

logger = logging.getLogger("core_banking_app")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = RotatingFileHandler(
        APP_LOG_PATH,
        maxBytes=5_000_000,
        backupCount=3
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
