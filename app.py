import json
import numpy as np
from fastapi import HTTPException
from flask import Flask, request, jsonify, HTTPException
from flask_restful import Resource, Api, abort
from flask_cors import CORS
from pipeline import Pipeline
import cv2
from utils import createLogger


app = Flask(__name__)
app.config['TIMEOUT'] = 120
app.config['DEBUG'] = True
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



class BadResource(Resource):
    def get(self):
        # Raise a bad request exception
        abort(400, message="Bad request")

@app.errorhandler(Exception)
def handle_error(error):
    if isinstance(error, HTTPException):
        # Return a custom error message for HTTP exceptions
        return jsonify({"error": str(error)})
    else:
        # Return a generic error message for other exceptions
        return jsonify({"error": "Internal server error"})

api.add_resource(BadResource, "/bad")

class Summarizer(Resource):
    def post(self):
        print(request.form)
        mask = json.loads(request.form['mask'])
        print(mask)
        mask = [{'x': 22, 'y': 4.171875},
                {'x': 363, 'y': 8.171875},
                {'x': 372, 'y': 364.171875},
                {'x': 14, 'y': 366.171875}]
        # widthRatio = request.form['widthRatio']
        # heightRatio = request.form['heighthRatio']
        # print(widthRatio, heightRatio)
        image_stream = request.files['image'].stream

        widthRatio = 8.042553191489361
        heightRatio = 8.032432432432433
        prefix = "Stwórz 4 krótkie punkty na podstawie tekstu ale nie kończ podanego tekstu: "

        image_stream.seek(0)
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        text = pip.fullRun(image, widthRatio, heightRatio, prefix, mask)
        logger.info(text)
        return createResponse(text, 200)

api.add_resource(Summarizer, '/summarize')

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=80, debug=True)