import subprocess

class VideoRenderer():
    def __init__(self, file_name, resolution):
        command = [
            "ffmpeg",
            "-y",  # overwrite output file if it exists
            "-f", "rawvideo",
            "-s", f"{resolution[0]}x{resolution[1]}", # resolution
            "-pix_fmt", "rgba",
            "-r", "30",  # fps
            "-i", "-",  # input is pioe
            "-an",
            "-loglevel", "error",
            file_name
        ]

        self.process = subprocess.Popen(command, stdin=subprocess.PIPE)

    def add_frame(self, img):
        raw_frame = img.tobytes()
        self.process.stdin.write(raw_frame)
            
    def done(self):
        self.process.stdin.close()