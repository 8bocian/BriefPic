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
        # print(os.getenv("TESSERACT_PATH"))
        # ts.pytesseract.tesseract_cmd =  os.getenv("TESSERACT_PATH")
        getKey()

    def extractText(self, images):
        fullText = ""
        for image in images:
            text = ts.image_to_data(image, config="--psm 3 --oem 3", lang='pol', output_type='dict')
            # text = text[['conf', 'text']]
            # text = text[text['conf'] > 60]
            text = " ".join(text['text'])
            fullText += text + " "
        return fullText

    def summary(self, text, prefix):

        summary = gpt3Completion(f"{prefix} {text}")


        return summary

    def preproces(self, image, points):
        imageGray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        imageThresh = cv2.adaptiveThreshold(imageGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 30)
        imageInv = cv2.bitwise_not(imageThresh)



        boxes = self.getTextBoxes(imageInv)

        boxesSelected = []

        print(points)

        for box in boxes:
            x1, y1, x2, y2 = box
            for point in points:
                print(point)
                cv2.circle(image, (int(point["x"]), int(point["y"])), 40, (0, 0, 255), -1)
                if x1 <= point["x"] <= x2 and y1 <= point["y"] <= y2:
                    boxesSelected.append(box)

        # plt.imshow(image)
        # plt.show()

        masks = [np.zeros_like(imageInv) for _ in range(len(boxesSelected))]

        # draw each bounding box onto the mask
        for idx in range(len(boxesSelected)):
            box = boxesSelected[idx]
            mask = masks[idx]
            cv2.rectangle(mask, (box[0], box[1]), (box[2], box[3]), color=255, thickness=-1)

            # use the mask to zero out pixels in the input image
            imageMasked = cv2.bitwise_and(imageInv, mask)
            masks[idx] = imageMasked
            # plt.imshow(imageMasked, cmap='gray')
            # plt.show()


        return masks

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

    def fullRun(self, image, prefix, points):
        image = self.preproces(image, points)

        text = self.extractText(image)
        print(f"Text: {text}")

        processedText = self.processResult(text)
        print(f"Processed: {processedText}")

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
