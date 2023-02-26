FROM python:3.8

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install poppler-utils -y
RUN apt install tesseract-ocr -y
RUN apt install libtesseract-dev -y
COPY . .

#CMD ["python", "main.py"]
CMD gunicorn --bind 0.0.0.0:8080 --access-logfile=- app:app