import matplotlib.pyplot as plt
import numpy as np
import pytesseract as ts
import cv2.cv2 as cv2
import re
from transformers import BartTokenizer, BartForConditionalGeneration
from deep_translator import GoogleTranslator


class Pipeline:
    def __init__(self):
        self.tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        self.model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    def extractText(self, image):
        text = ts.image_to_data(image, config="--psm 3 --oem 2", lang='pol', output_type='dict')
        # text = text[['conf', 'text']]
        # text = text[text['conf'] > 60]
        print(text['text'])
        text = " ".join(text['text'])
        return text

    def summary(self, text):
        translated = GoogleTranslator(source='auto', target='en').translate(text)

        input_ids = self.tokenizer.encode(translated, return_tensors='pt')
        summary_ids = self.model.generate(input_ids, max_length=500, num_beams=4, early_stopping=True)
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        final = GoogleTranslator(source='auto', target='pl').translate(summary)

        return final

    def preproces(self, image, widthRatio, heightRatio, points=None):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 30)

        plt.imshow(image)
        plt.show()

        if points is not None:
            print(points)
            mask = np.zeros(image.shape[:2], dtype=np.uint8)

            mask_points = np.array([(float(p["x"])*float(widthRatio), float(p["y"])*float(heightRatio)) for p in points], dtype=np.int32)
            inverse_image = (np.ones_like(image) * 255) - image

            cv2.fillPoly(mask, [mask_points], (255, 255, 255))

            mask_combined = cv2.bitwise_and(inverse_image, mask)
            image = (np.ones_like(image) * 255) - mask_combined


        return image

    def processResult(self, text):


        pattern = r'(\S)—\s*'
        result = re.sub(pattern, r"\1", text, flags=re.MULTILINE)

        pattern = r'\s+'
        result = re.sub(pattern, r" ", result, flags=re.MULTILINE)

        return result

    def fullRun(self, image, widthRatio, heightRatio, points=None):
        image = self.preproces(image, widthRatio, heightRatio, points)

        text = self.extractText(image)

        processedText = self.processResult(text)
        print(processedText)
        cv2.imwrite("test.jpg", image)
        summary = self.summary(processedText)

        return summary

    def trimText(self, text):
        low = None
        for i, char in enumerate(text):
            if char.isupper():
                low = i
                break

        high = min(-text[::-1].index("."), -1)

        return text[low:high]

# pip = Pipeline()
# image = cv2.imread("../images/IMG_2743.jpg")
# s = pip.fullRun(image)
# print(s)



