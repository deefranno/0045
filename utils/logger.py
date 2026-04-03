import sys
import os
from loguru import logger

def setup_logging(log_dir="logs"):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "app.log")

    # Remove default handler
    logger.remove()

    # Add console handler
    logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

    # Add file handler with rotation
    logger.add(log_file, rotation="10 MB", retention="10 days", level="DEBUG")

    return logger
