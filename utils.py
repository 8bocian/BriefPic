import logging
import os
import uuid
from sys import stdout
from dotenv import load_dotenv

load_dotenv()

def createLogger():
    logger = logging.getLogger(f'logger{str(uuid.uuid4())}')
    logger.propagate = False
    logFormatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
    level = logging.getLevelName("INFO")
    logger.setLevel(level)
    consoleHandler = logging.StreamHandler(stdout)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    return logger

def convertPoints(points, ratioV, ratioH):
    points = [{"x": point["x"] * ratioV, "y": point["y"] * ratioH} for point in points]
    print(points)
    return points