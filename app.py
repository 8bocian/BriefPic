import json
import os
import numpy as np
from flask import Flask, request, jsonify, Response, make_response
from flask_cors import CORS
from pipeline import Pipeline
import cv2
from utils import createLogger, convertPoints
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config['TIMEOUT'] = 120
app.config['DEBUG'] = True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv("GMAIL_ADDR")
app.config['MAIL_PASSWORD'] = os.getenv("GMAIL_PASSWD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_SUPPRESS_SEND'] = True


CORS(app)
mail = Mail(app)

pip = Pipeline()
logger = createLogger()


def createResponse(message, code):
    response = jsonify(message)
    response.status_code = code
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers', 'Authenticate')
    response.headers.add('Access-Control-Max-Age', '1200')
    return response


@app.route("/robots.txt", methods=["GET"])
def robots():
    robotsTxt = "User-agent: * \nDisallow: /"
    return Response(robotsTxt, mimetype='text/plain')


@app.route("/summarize", methods=["POST"])
def summarize():
    image_stream = request.files['image'].stream
    image_stream.seek(0)
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    print(image.shape)
    points = json.loads(request.form['points'])
    print(points)
    ratioV = json.loads(request.form['ratio'])['ratioV']
    ratioH = json.loads(request.form['ratio'])['ratioH']

    mask = convertPoints(points, ratioV, ratioH)

    prefix = "Stwórz 4 krótkie punkty na podstawie tekstu ale nie kończ podanego tekstu: "

    text = pip.fullRun(image, prefix, mask)
    app.logger.info(text)
    app.logger.debug(request.data)
    app.logger.debug(request.headers)
    app.logger.debug(request.remote_addr)
    with app.app_context():
        msg = Message('Summarize request', sender=os.getenv("GMAIL_ADDR"), recipients=[os.getenv("GMAIL_ADDR")])
        msg.body = f'''
            request.data: {request.data}\n
            request.headers: {request.headers}\n
            request.remote_addr: {request.remote_addr}\n
            request.path: {request.path}\n
            '''
        mail.send(msg)
    return jsonify(text)




@app.errorhandler(404)
def handle_bad_request(error):
    app.logger.info(request.data)
    app.logger.info(request.headers)
    app.logger.info(request.remote_addr)
    with app.app_context():
        msg = Message('Bad request', sender=os.getenv("GMAIL_ADDR"), recipients=[os.getenv("GMAIL_ADDR")])
        msg.body = f'''
        request.data: {request.data}\n
        request.headers: {request.headers}\n
        request.remote_addr: {request.remote_addr}\n
        request.path: {request.path}\n
        error: {error}\n
        '''
        mail.send(msg)
    return jsonify({"error": "Pls, don't do this"}), 400

@app.errorhandler(500)
def handle_bad_request(error):
    app.logger.info(request.data)
    app.logger.info(request.headers)
    app.logger.info(request.remote_addr)
    with app.app_context():
        msg = Message('Bad request', sender=os.getenv("GMAIL_ADDR"), recipients=[os.getenv("GMAIL_ADDR")])
        msg.body = f'''
        request.data: {request.data}\n
        request.headers: {request.headers}\n
        request.remote_addr: {request.remote_addr}\n
        request.path: {request.path}\n
        error: {error}\n
        '''
        mail.send(msg)
    return jsonify({"error": "Pls, don't do this"}), 400

@app.errorhandler(400)
def handle_bad_request(error):
    app.logger.info(request.data)
    app.logger.info(request.headers)
    app.logger.info(request.remote_addr)
    with app.app_context():
        msg = Message('Bad request', sender=os.getenv("GMAIL_ADDR"), recipients=[os.getenv("GMAIL_ADDR")])
        msg.body = f'''
        request.data: {request.data}\n
        request.headers: {request.headers}\n
        request.remote_addr: {request.remote_addr}\n
        request.path: {request.path}\n
        error: {error}\n
        '''
        mail.send(msg)
    return jsonify({"error": "Pls, don't do this"}), 400

if __name__ == '__main__':
    with app.app_context():
        msg = Message('Log', sender=os.getenv("GMAIL_ADDR"), recipients=[os.getenv("GMAIL_ADDR")])
        msg.body = 'Service started'
        mail.send(msg)
    app.run(host="0.0.0.0", port=80, debug=True)