from PIL import Image
import copy
import json
import os
from gyl.video_renderer import subprocess
from gyl.scene import Scene

class WaitScene(Scene):

    elements = []

    def __init__(self, elements, time):
        self.elements = list(elements)
        self.time = time

    def render(self, file_name, resolution, fps):
        is_cached, write_cache = self.is_cached(file_name)
        if is_cached:
            return False

        img = Image.new("RGBA", resolution, color=(20, 20, 20))
        for element in self.elements:
            imwidth, imheight = element.get_size()

            normal_pos = element.normal_pos()

            x = normal_pos[0]*resolution[0]/100
            y = normal_pos[1]*resolution[1]/100

            width = element.normal_width()*resolution[0]/100
            if imwidth == 0:
                continue
            height = width/imwidth*imheight

            if imwidth < 0 or imheight < 0:
                continue

            im = copy.copy(element.draw())

            res_im = im.resize((int(width), int(height)), resample=Image.LANCZOS)

            img.paste(res_im, (int(x),int(y)),mask=res_im)

        write_cache()

        img.save(f"{file_name}.frame.png", "png")

        command = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-r", str(fps),
            "-i", f"{file_name}.frame.png",
            "-c:v", "libx264",
            "-t", str(self.time),
            "-pix_fmt", "yuv420p",
            "-loglevel", "error",
            file_name
        ]

        p = subprocess.Popen(command)
        p.wait()

        return True
    
    def is_cached(self, file_name):
        cache_obj = self.create_cache_obj()

        scenes_folder = os.path.dirname(file_name)
        cache_folder = os.path.join(scenes_folder, ".cache")
        cache_json_file = os.path.join(cache_folder,
            os.path.basename(file_name)+".json")
        
        def write_cache():
            with open(cache_json_file, "w", encoding="UTF8") as f:
                json.dump(cache_obj, f)
        
        if not os.path.exists(cache_json_file):
            return False, write_cache
        if not os.path.exists(file_name):
            return False, write_cache

        with open(cache_json_file, "r", encoding="UTF8") as f:
            cached_data = json.load(f)

        return cache_obj == cached_data, write_cache

    def create_cache_obj(self):
        cache_obj = []
        for element in self.elements:
            element_cache = element.get_cache()
            element_cache["pos"] = list(element_cache["pos"])

            cache_obj.append([
                element_cache
            ])
        return {
            "elements": cache_obj
        }