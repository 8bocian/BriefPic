import logging
import os
import uuid
from sys import stdout


def createLogger():
    logger = logging.getLogger(f'logger{str(uuid.uuid4())}')
    logger.propagate = False
    logFormatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
    level = logging.getLevelName(os.getenv("LOG_LEVEL"))
    logger.setLevel(level)
    consoleHandler = logging.StreamHandler(stdout)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    return logger