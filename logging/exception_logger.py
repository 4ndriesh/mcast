import logging


def create_logger():
    logger = logging.getLogger("asyncio")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(r"logging.log")
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
logger = create_logger()
