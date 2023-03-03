import json
import numpy as np
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from pipeline import Pipeline
import cv2
from utils import createLogger


app = Flask(__name__)
app.config['TIMEOUT'] = 120
CORS(app)
api = Api(app)
pip = Pipeline()
logger = createLogger()


def createResponse(message, code, file=False):
    if file:
        response = message
    else:
        response = jsonify(message)
    response.status_code = code
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Max-Age', '1200')
    return response


class Summarizer(Resource):
    def post(self):
        logger.info(request.form)
        logger.info(request.values)
        logger.info(request.files)
        logger.info(request.data)
        mask = json.loads(request.form['mask'])
        widthRatio = request.form['widthRatio']
        heightRatio = request.form['heighthRatio']
        image_stream = request.files['image'].stream

        prefix = "Stwórz 4 krótkie punkty na podstawie tekstu ale nie kończ podanego tekstu: "

        image_stream.seek(0)
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        text = pip.fullRun(image, widthRatio, heightRatio, prefix, mask)
        logger.info(text)
        return createResponse(text, 200)

api.add_resource(Summarizer, '/summarize/submit-form')

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=80, debug=True)