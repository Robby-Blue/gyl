from element import Element
from PIL import Image, ImageDraw, ImageFont
import os

FONT_FILE = "gyl/fonts/Roboto-Black.ttf"

if not os.path.exists(FONT_FILE):
    raise FileNotFoundError(f"Font file {FONT_FILE} not found")

text_font = ImageFont.truetype(FONT_FILE, 200)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
heightbbox = text_font.getbbox(alphabet)
text_height = heightbbox[3]

class Text(Element):

    def __init__(self, text, position, width=None):
        if not width:
            width = lineheight(10)
        super().__init__(position, width)
        self.text = text

    def draw(self):
        bbox = text_font.getbbox(self.text)
        
        text_width = bbox[2]

        img = Image.new('RGBA', (text_width, text_height))
        draw = ImageDraw.Draw(img)

        draw.text((0, 0), self.text, fill=(230, 230, 230), font=text_font)

        return img
    
    def get_size(self):
        bbox = text_font.getbbox(self.text)
        return bbox[2], text_height
    
def lineheight(height):
    # calculate the elements width such that it has a specific
    # line height
    def f(text_element):
        imwidth, imheight = text_element.get_size()
        if imwidth == 0:
            return 0
        
        res = text_element.video.resolution
        video_aspect_ratio = res[0]/res[1]

        w = (height*imwidth/imheight*video_aspect_ratio)
        w = height/ video_aspect_ratio/imheight*imwidth
        return w
    return f