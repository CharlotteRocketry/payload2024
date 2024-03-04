import json
from glob import glob
from flask import Flask, request, redirect, render_template, send_file
from src import camera
from src.recording import Recording

app = Flask(__name__)

recording = None
name = ""

@app.route("/")
def main():
    return render_template('pages/main.html', main_active=True, recording=recording, name=name)


# start a recording if a valid name is given
@app.route('/start', methods=["POST"])
def start():
    global recording, name
    name = request.form.get("name", "")
    if name != "":
        recording = Recording(name)
        recording.write_metadata()
        recording.start_video()
    return redirect("/")


# stop a recording
@app.route('/stop', methods=["POST"])
def stop():
    camera.stop_video()
    global recording, name
    recording.stop_video()
    recording = None
    name = ""
    return redirect("/")


# get settings page
@app.route('/config')
def config():
    return render_template('pages/config.html', config_active=True, recording=recording)


# get flights page
@app.route('/flights')
def flights():
    flights_list = []
    for metadata_file in glob('data/*/meta.json'):
        flights_list.append(json.load(open(metadata_file)))
    flights_list.sort(key=lambda x: x['name'])
    return render_template('pages/flights.html', flights_list=flights_list, flights_active=True)


@app.route("/preview.jpg")
def camera_preview():
    camera.generate_preview("data/preview.jpg")
    return send_file("data/preview.jpg")

