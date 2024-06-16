import subprocess

class VideoRenderer():
    def __init__(self, file_name, resolution, fps):
        command = [
            "ffmpeg",
            "-y",  # overwrite output file if it exists
            "-f", "rawvideo",
            "-s", f"{resolution[0]}x{resolution[1]}", # resolution
            "-pix_fmt", "rgba",
            "-r", str(fps),  # fps
            "-i", "-",  # input is pipe
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
        self.process.wait()