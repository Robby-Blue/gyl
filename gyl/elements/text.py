from gyl.element import Element
from gyl.size import lineheight
from PIL import Image, ImageDraw, ImageFont
import os

FONT_FILE = os.path.dirname(__file__)+"/../fonts/Roboto-Black.ttf"

if not os.path.exists(FONT_FILE):
    raise FileNotFoundError(f"Font file {FONT_FILE} not found")

text_font = ImageFont.truetype(FONT_FILE, 200)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
heightbbox = text_font.getbbox(alphabet)
text_height = heightbbox[3]

class Text(Element):

    text_color = (230, 230, 230)
    outline_color = (0, 0, 0)
    outline_width = 0

    def __init__(self, text, position, width=None, *, outline_width=0):
        if not width:
            width = lineheight(10)
        self.outline_width = outline_width
        super().__init__(position, width)
        self.text = text

    def draw(self):
        bbox = text_font.getbbox(self.text)
        
        text_width = bbox[2]

        margin = +self.outline_width
        img = Image.new('RGBA', (text_width+margin, text_height+margin))
        draw = ImageDraw.Draw(img)

        draw.text((0, 0), self.text, fill=self.text_color, font=text_font, stroke_fill=self.outline_color, stroke_width=self.outline_width)

        return img
    
    def get_size(self):
        bbox = text_font.getbbox(self.text)
        return bbox[2], text_height
    
    def get_cache(self):
        return {
            "type": "Text",
            "pos": self.normal_pos(),
            "size": self.normal_width(),
            "text": self.text,
            "color": self.text_color,
            "outline": {
                "color": self.outline_color,
                "width": self.outline_width
            }
        }