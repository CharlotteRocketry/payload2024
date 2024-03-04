import os
import uuid
import json
from . import camera

class Recording:
    def __init__(self, name, video_h=1080, video_w=1920):
        self.id = str(uuid.uuid4())
        self.name = name
        self.video_h = video_h
        self.video_w = video_w
        os.mkdir('data/' + self.id)


    def start_video(self):
        camera.start_video('data/' + self.id + '/video.mp4')


    def stop_video(self):
        camera.stop_video()


    def write_metadata(self):
        metadata = {
            "id": self.id,
            "name": self.name
        }
        outfile = open('data/' + self.id + '/meta.json', "w")
        json.dump(metadata, outfile, indent=4, sort_keys=True)

