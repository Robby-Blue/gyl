from gyl.scene import Scene
import subprocess
import os

class Video():
    
    resolution = ()
    elements = []
    scenes = []

    def __init__(self, resolution=(1280, 720), render_full=False):
        self.resolution = resolution
        self.render_full = render_full
        self.add_scene()

        output_folder = "scenes"
        cache_folder = os.path.join(output_folder, ".cache")

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        if not os.path.exists(cache_folder):
            os.mkdir(cache_folder)

    def render(self):
        rendered = 0

        output_folder = "scenes"

        scenes_file = f"{output_folder}/scenes.txt"
        f = open(scenes_file, "w")
        for i, scene in enumerate(self.scenes):
            output_file = f"{output_folder}/{i}.mp4"
            f.write(f"file '{os.path.abspath(output_file)}'\n")

            did_render = scene.render(output_file)

            if did_render:
                rendered+=1
        f.close()

        if len(self.scenes) > 1 and rendered > 0 and self.render_full:
            command = [
                "ffmpeg",
                "-y",
                "-safe", "0",
                "-f", "concat",
                "-i", scenes_file,
                "-loglevel", "error",
                "full.mp4"
            ]

            subprocess.Popen(command)

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
        self.scenes.append(Scene(self.elements, self.resolution))

    def current_scene(self):
        return self.scenes[-1]