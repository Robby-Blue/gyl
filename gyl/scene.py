from PIL import Image, ImageDraw
import copy
from video_renderer import VideoRenderer

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

        for frame in self.plan_frames():
            img = Image.new("RGBA", resolution, color=(20, 20, 20))
            draw = ImageDraw.Draw(img)
            for element in frame:
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

                im = element.draw()
                res_im = im.resize((int(width), int(height)))

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
                animation.apply_to_element(i)

            frames.append([])
            for element in self.elements:
                frames[-1].append(copy.copy(element))

        return frames