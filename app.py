import json
import cv2.cv2 as cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from pipeline import Pipeline
from fastapi import FastAPI, UploadFile, File
from starlette.requests import Request
import io
import cv2

from pydantic import BaseModel

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
        image_stream = request.files['image'].stream

        # if request.files['type'] == "bulletpoints":
        #     prefix = "Stwórz punkty na podstawie tekstu: "
        # else:
        #     prefix = "Podsumuj tekst: "
        prefix = "Podsumuj tekst: "
        # image_bytes.save("image.jpg")
        # image = cv2.imread("image.jpg")
        # image_stream = io.BytesIO(image_bytes)
        image_stream.seek(0)
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        text = pip.fullRun(image, widthRatio, heightRatio, prefix, mask)
        print(text)
        return createResponse(text, 200)


app = FastAPI()


class ImageType(BaseModel):
    url: str


@app.post("/predict/")
def prediction(request: Request, file: bytes = File):
    if request.method == "POST":
        image_stream = io.BytesIO(file)
        image_stream.seek(0)
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        widthRatio = 0
        heightRatio = 0
        prefix = ""
        mask = None
        text = pip.fullRun(image, widthRatio, heightRatio, prefix, mask)

        return text
    return "Method Not Allowed"
