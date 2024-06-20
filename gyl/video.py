from gyl.scenes import AnimationScene, WaitScene
import subprocess
import os

class Video():

    elements = []
    scenes = []
    audio_path = None

    def __init__(self):
        self.add_scene()

        output_folder = "scenes"
        cache_folder = os.path.join(output_folder, ".cache")

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        if not os.path.exists(cache_folder):
            os.mkdir(cache_folder)

    def render(self, resolution=(1280, 720), fps=30, render_full=False):
        self.resolution = resolution
        self.fps = fps
        rendered = 0

        output_folder = "scenes"

        scenes_file = f"{output_folder}/scenes.txt"
        f = open(scenes_file, "w")
        for i, scene in enumerate(self.scenes):
            output_file = f"{output_folder}/{i}.mp4"
            f.write(f"file '{os.path.abspath(output_file)}'\n")

            did_render = scene.render(output_file, resolution, fps)

            if did_render:
                rendered+=1
        f.close()

        if len(self.scenes) > 1 and rendered > 0 and render_full:
            command = [
                "ffmpeg",
                "-y",
                "-safe", "0",
                "-r", str(fps),
                "-f", "concat",
                "-i", scenes_file
            ]

            if self.audio_path:
                command += ["-i", self.audio_path]

            command+=[
                "-pix_fmt", "yuv420p",
                "-loglevel", "error"
            ]

            command.append("full.mp4")

            p = subprocess.Popen(command)
            p.wait()

    def add_element(self, element):
        element.video = self
        self.elements.append(element)
        self.current_scene().elements.append(element)

    def animate(self, element, animation):
        self.current_scene().add_animation({
            "element": element,
            "animation": animation
        })

    def remove_element(self, element):
        self.elements.remove(element)
        self.current_scene().elements.remove(element)

    def clear(self):
        for element in list(self.elements):
            self.remove_element(element)

    def add_scene(self):
        self.scenes.append(AnimationScene(self.elements))

    def wait(self, seconds):
        self.scenes.append(WaitScene(self.elements, seconds))
        self.add_scene()

    def current_scene(self):
        return self.scenes[-1]
    
    def set_audio(self, path):
        self.audio_path = path