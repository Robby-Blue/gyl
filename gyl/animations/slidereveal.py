from PIL import Image
from gyl.animation import Animation

class SlideReveal(Animation):

    def __init__(self, appear=True, inverse=False, interpolation=None, start_time=0):
        self.appear = appear
        self.inverse = inverse
        super().__init__(interpolation, start_time)

    def apply_to_img(self, im, frame):
        width, height = im.size

        if self.appear:
            shown_width = int(self.interpolate(0, width, frame))
        else:
            shown_width = int(self.interpolate(width, 0, frame))

        transparent_img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        
        if self.inverse:
            im.paste(transparent_img, (-shown_width, 0))
        else:
            im.paste(transparent_img, (shown_width, 0))

        return im

    def get_animation_type(self):
        return "EDITIMG"
       
    def get_cache(self):
        return {
            "type": "Slide",
            "length": self.get_length(),
            "appear": self.appear,
            "inverse": self.inverse,
            "interpolation": self.interpolator.__name__
        }