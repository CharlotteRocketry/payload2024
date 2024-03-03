import subprocess
from picamera2 import Picamera2
from picamera2.outputs import FileOutput
from picamera2.encoders import H264Encoder

class Camera:
    def __init__(self):
        self.picam = Picamera2()
        self.picam.configure(self.picam.create_video_configuration())
        self.picam.start()
        self.ffmpeg = None


    def start_video(self, output):
        general_options = [
#            '-loglevel', 'warning',
            '-y' # -y means overwrite output without asking
        ]
        video_input = [
            '-use_wallclock_as_timestamps', '1',
            '-thread_queue_size', '64', # necessary to prevent warnings
            '-i', '-'
        ]
        video_codec = ['-c:v', 'copy']
        audio_input = [
#            '-itsoffset', '-0.3',
            '-f', 'alsa',
            '-channels', '1',
            '-sample_rate', '48000',
            '-thread_queue_size', '1024', # necessary to prevent warnings
            '-i', 'hw:CARD=Device,DEV=0'
        ]
        audio_codec = [
            '-b:a', '128000',
            '-c:a', 'aac'
        ]

        command = ['ffmpeg'] + general_options + audio_input + video_input + audio_codec + video_codec + output.split()
        self.ffmpeg = subprocess.Popen(command, stdin=subprocess.PIPE, shell=False)
        self.picam.start_recording(encoder=H264Encoder(bitrate=2000000), output=FileOutput(self.ffmpeg.stdin))


    def stop_video(self):
        self.ffmpeg.stdin.close()
        self.ffmpeg.terminate()
        self.picam.stop_recording()
        self.picam.start()


    def generate_preview(self, output):
        request = self.picam.capture_request()
        request.save("main", output)
        request.release()
