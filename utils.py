import logging
import os
import uuid
from sys import stdout
from dotenv import load_dotenv

load_dotenv()

def createLogger():
    logging.basicConfig(
                        filemode='a',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    logging.info("Started logger")

    logger = logging.getLogger('logger')
    logger.propagate = False

    return logger

def convertPoints(points, ratioV, ratioH):
    points = [{"x": point["x"] * ratioV, "y": point["y"] * ratioH} for point in points]
    print(points)
    return points