import logging
from logging.handlers import RotatingFileHandler


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    date_format = "%Y-%m-%d %H:%M:%S,%f"[:-3]
    formatter = logging.Formatter(log_format, datefmt=date_format)

    file_handler = RotatingFileHandler(
        "app.log", maxBytes=2 * 1024 * 1024, backupCount=2, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
