import tracemalloc
import matplotlib.pyplot as plt
import os
import numpy as np
import pytesseract as ts
import cv2
import re
from openaiapi import getKey, gpt3Completion
from dotenv import load_dotenv

load_dotenv()
class Pipeline:

    def __init__(self):
        self.kernel_size = 40
        ts.pytesseract.tesseract_cmd =  os.getenv("TESSERACT_PATH")
        getKey()

    def extractText(self, image):
        text = ts.image_to_data(image, config="--psm 3 --oem 3", lang='pol', output_type='dict')
        # text = text[['conf', 'text']]
        # text = text[text['conf'] > 60]
        text = " ".join(text['text'])
        return text

    def summary(self, text, prefix):

        summary = gpt3Completion(f"{prefix} {text}")


        return summary

    def preproces(self, image, points):
        imageGray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        imageThresh = cv2.adaptiveThreshold(imageGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 30)
        imageInv = cv2.bitwise_not(imageThresh)

        plt.imshow(image)
        plt.show()

        boxes = self.getTextBoxes(imageInv)

        boxesSelected = []

        for box in boxes:
            x1, y1, x2, y2 = box
            for point in points:
                if x1 <= point[0] <= x2 and y1 <= point[1] <= y2:
                    boxesSelected.append(box)

        mask = np.zeros_like(image)

        # draw each bounding box onto the mask
        for box in boxes:
            cv2.rectangle(mask, (box[0], box[1]), (box[2], box[3]), color=255, thickness=-1)

        # use the mask to zero out pixels in the input image
        imageMasked = cv2.bitwise_and(image, mask)

        plt.imshow(imageMasked)
        plt.show()

        return imageMasked

    def getTextBoxes(self, image):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.kernel_size, self.kernel_size))

        # imageMorph = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

        imageDilated = cv2.dilate(image, kernel, iterations=1)

        contours, hierarchy = cv2.findContours(imageDilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        boxes = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            boxes.append([x, y, x + w, y + h])

        return boxes
    def processResult(self, text):

        pattern = r'(\S)—\s*'
        result = re.sub(pattern, r"\1", text, flags=re.MULTILINE)

        pattern = r'\s+'
        result = re.sub(pattern, r" ", result, flags=re.MULTILINE)

        return result

    def fullRun(self, image, prefix, points=None):
        image = self.preproces(image, points)

        text = self.extractText(image)

        processedText = self.processResult(text)
        # cv2.imwrite("test.jpg", image)
        summary = self.summary(processedText, prefix)

        return summary

    def trimText(self, text):
        low = None
        for i, char in enumerate(text):
            if char.isupper():
                low = i
                break

        high = min(-text[::-1].index("."), -1)

        return text[low:high]

# tracemalloc.start()
# pip = Pipeline()
# image = cv2.imread("../images/IMG_2743.jpg")
# s = pip.fullRun(image, 0, 0, "")
# print(tracemalloc.get_traced_memory())
# tracemalloc.stop()
