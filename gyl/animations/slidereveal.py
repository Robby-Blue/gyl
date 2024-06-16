from PIL import Image
from gyl.animation import Animation

class SlideReveal(Animation):

    def __init__(self, appear=True, interpolation=None, start_frame=0):
        self.appear = appear
        super().__init__(interpolation, start_frame)

    def apply_to_img(self, im, frame):
        width, height = im.size

        if self.appear:
            shown_width = int(self.interpolate(0, width, frame))
        else:
            shown_width = int(self.interpolate(width, 0, frame))

        transparent_img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        im.paste(transparent_img, (shown_width, 0))

        return im

    def get_animation_type(self):
        return "EDITIMG"

    def get_length(self):
        return 0.3
       
    def get_cache(self):
        return {
            "type": "Slide",
            "length": self.get_length(),
            "interpolation": self.interpolator.__name__
        }