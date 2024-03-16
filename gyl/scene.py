from PIL import Image, ImageDraw
import copy
from gyl.video_renderer import VideoRenderer

class Scene():

    elements = []
    animations = []

    def __init__(self, elements):
        self.elements = list(elements)
        self.animations = []

    def add_animation(self, animation):
        self.animations.append(animation)

    def render(self, file_name, resolution):
        renderer = VideoRenderer(file_name, resolution)

        for frame_count, frame in enumerate(self.plan_frames()):
            img = Image.new("RGBA", resolution, color=(20, 20, 20))
            draw = ImageDraw.Draw(img)
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
                    res_im = animation.apply_to_img(res_im, frame_count)

                draw.bitmap((x, y), res_im)

            renderer.add_frame(img)
        
        renderer.done()

    def plan_frames(self):
        frame_count = 0
        animations = []

        for event in self.animations:
            animation = event["animation"]

            animation.element = event["element"]
            animation.scene = self
            animations.append(animation)
            if animation.get_length() > frame_count:
                frame_count = animation.get_length()

        frames = []
         
        for i in range(frame_count+1):
            for animation in animations:
                if i > animation.get_length():
                    continue
                if animation.get_animation_type() != "EDITATTR":
                    continue
                animation.apply_to_element(i)

            frames.append([])
            for element in self.elements:

                post_draw_anims = []
                for animation in animations:
                    if animation.element != element:
                        continue
                    if i > animation.get_length():
                        continue
                    if animation.get_animation_type() != "EDITIMG":
                        continue
                    post_draw_anims.append(animation)

                frames[-1].append((copy.copy(element), post_draw_anims))

        return frames