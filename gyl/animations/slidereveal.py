from PIL import Image
from gyl.animation import Animation

class SlideReveal(Animation):

    def __init__(self, interpolation=None):
        super().__init__(interpolation)

    def apply_to_img(self, im, frame):
        width, height = im.size

        time = frame/self.get_length()
        percent = self.interpolate(0, 1, time)
        shown_width = int(width*percent)

        transparent_img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        im.paste(transparent_img, (shown_width, 0))

        return im

    def get_animation_type(self):
        return "EDITIMG"

    def get_length(self):
        return 20