from flask import Flask, send_file
from picamera2 import Picamera2

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<body><img src=\"/preview.jpg\" width=\"auto\" height=\"200px\"></body>"

@app.route("/preview.jpg")
def camera_preview():
    picam2.capture_file("preview.jpg")
    return send_file("preview.jpg")