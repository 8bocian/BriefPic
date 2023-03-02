import io
import json

import matplotlib.pyplot as plt
import numpy as np
import pytesseract as ts
import cv2.cv2 as cv2
from PIL.Image import Image
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from transformers import pipeline
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from pipeline import Pipeline

app = Flask(__name__)
app.config['TIMEOUT'] = 120
CORS(app)
api = Api(app)
pip = Pipeline()

def createResponse(message, code, file=False):
    if file:
        response = message
    else:
        response = jsonify(message)
    response.status_code = code
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Max-Age', '120000')
    return response

class Summarizer(Resource):
    def post(self):
        mask = json.loads(request.form['mask'])
        widthRatio = request.form['widthRatio']
        heightRatio = request.form['heighthRatio']
        image_bytes = request.files['image']

        # if request.files['type'] == "bulletpoints":
        #     prefix = "Stwórz punkty na podstawie tekstu: "
        # else:
        #     prefix = "Podsumuj tekst: "
        prefix = "Podsumuj tekst: "
        image_bytes.save("image.jpg")
        image = cv2.imread("image.jpg")
        text = pip.fullRun(image, widthRatio, heightRatio, prefix, mask)
        print(text)
        return createResponse(text, 200)


api.add_resource(Summarizer, "/summarize")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)