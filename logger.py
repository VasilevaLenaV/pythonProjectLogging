import os
import logging


def init(name):
    if not os.path.exists("logs"):
        os.mkdir("logs")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    log_handler = logging.FileHandler(f"logs\\{name}.log", mode='a', encoding='cp1251')
    log_formatter = logging.Formatter("%(asctime)s %(name)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
    return logger
