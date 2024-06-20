from PIL import Image
import copy
import json
import os
from gyl.video_renderer import VideoRenderer
from gyl.scene import Scene

class AnimationScene(Scene):

    elements = []
    animations = []

    def __init__(self, elements):
        self.elements = list(elements)
        self.animations = []

    def add_animation(self, animation):
        self.animations.append(animation)

    def render(self, file_name, resolution, fps):
        frames = self.plan_frames(fps)

        is_cached, write_cache = self.is_cached(file_name, frames)
        if is_cached:
            return False

        last_frame = None
        renderer = VideoRenderer(file_name, resolution, fps)

        for frame_count, frame in enumerate(frames):
            img = Image.new("RGBA", resolution, color=(20, 20, 20))
            for element, post_draw_animations in frame:
                # add var to whether it stays the same, no need to redraw
                # if it stays the same

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

                for animation in post_draw_animations:
                    res_im = animation.apply_to_img(res_im, frame_count/fps)

                img.paste(res_im, (int(x),int(y)),mask=res_im)

            if frame_count < len(frames)-1:
                renderer.add_frame(img)
            else:
                last_frame = img
        
        renderer.done()
        write_cache()

        last_frame.save(f"{file_name}.last.png", "png")

        return True

    def plan_frames(self, fps):
        frame_count = 0
        animations = []

        for event in self.animations:
            animation = event["animation"]

            animation.element = event["element"]
            animation.scene = self
            animations.append(animation)
            if animation.get_end_time()*fps > frame_count:
                frame_count = animation.get_end_time()*fps

        frames = []
        
        if frame_count < 1:
            frame_count = 1

        for i in range(int(frame_count)):
            for animation in animations:
                if i > animation.get_end_time()*fps:
                    continue
                if animation.get_animation_type() != "EDITATTR":
                    continue
                animation.apply_to_element(i/fps)

            frames.append([])
            for element in self.elements:

                post_draw_anims = []
                for animation in animations:
                    if animation.element != element:
                        continue
                    if i > animation.get_end_time()*fps:
                        continue
                    if animation.get_animation_type() != "EDITIMG":
                        continue
                    post_draw_anims.append(animation)

                frames[-1].append((copy.copy(element), post_draw_anims))

        return frames
    
    def is_cached(self, file_name, frames):
        cache_obj = self.create_cache_obj(frames)

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

    def create_cache_obj(self, frames):
        cache_obj = []
        for frame in frames:
            elements = []
            for element in frame:
                element_cache = element[0].get_cache()
                element_cache["pos"] = list(element_cache["pos"])

                animations = []
                for animation in element[1]:
                    animations.append(animation.get_cache())
                elements.append([
                    element_cache,
                    animations
                ])
            cache_obj.append(elements)
        return {
            "frames": cache_obj
        }