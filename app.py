from flask import Flask, request, redirect, render_template, send_file
from src.camera import Camera

app = Flask(__name__)

recording = False
name = ""

camera = Camera()

@app.route("/")
def main():
    return render_template('pages/main.html', main_active=True, recording=recording, name=name)


# start a recording if a valid name is given
@app.route('/start', methods=["POST"])
def start():
    global recording, name
    name = request.form.get("name", "")
    if name != "":
        camera.start_video('test.mp4')
        recording = True
    return redirect("/")


# stop a recording
@app.route('/stop', methods=["POST"])
def stop():
    camera.stop_video()
    global recording, name
    recording = False
    name = ""
    return redirect("/")


# get settings page
@app.route('/config')
def config():
    return render_template('pages/config.html', config_active=True, recording=recording)


# get flights page
@app.route('/flights')
def flights():
    return render_template('pages/flights.html', flights_active=True)


@app.route("/preview.jpg")
def camera_preview():
    camera.generate_preview("data/preview.jpg")
    return send_file("data/preview.jpg")


@app.route("/video.mp4")
def video():
    return send_file("test.mp4")

