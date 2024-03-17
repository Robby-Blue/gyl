from gyl.scene import Scene
import subprocess
import os

class Video():
    
    resolution = ()
    elements = []
    scenes = []
    backlog = []
    # eg to remember to remove once next scene starts if theres an animation

    def __init__(self, resolution=(1280, 720)):
        self.resolution = resolution
        self.add_scene()

    def render(self):
        output_folder = "scenes"

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        rendered = 0

        scenes_file = f"{output_folder}/scenes.txt"
        f = open(scenes_file, "w")
        for i, scene in enumerate(self.scenes):
            output_file = f"{output_folder}/{i}.mp4"
            f.write(f"file '{os.path.abspath(output_file)}'\n")

            did_render = scene.render(output_file, self.resolution)

            if did_render:
                rendered+=1
        f.close()

        if len(self.scenes) > 1 and rendered > 0:
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

    def add_scene(self):
        self.scenes.append(Scene(self.elements))    
        for event in self.backlog:
            self.current_scene().add_event(event)
        self.backlog.clear()

    def current_scene(self):
        return self.scenes[-1]