from element import Element
from PIL import Image, ImageDraw, ImageFont
import os

FONT_FILE = "gyl/fonts/Roboto-Black.ttf"

if not os.path.exists(FONT_FILE):
    raise FileNotFoundError(f"Font file {FONT_FILE} not found")

text_font = ImageFont.truetype(FONT_FILE, 200)

class Text(Element):

    def __init__(self, text, position):
        super().__init__(position, 25)
        self.text = text

    def draw(self):
        bbox = text_font.getbbox(self.text)
        
        text_width = bbox[2]-bbox[0]
        text_height = bbox[3]-bbox[1]

        img = Image.new('RGBA', (text_width, text_height))
        draw = ImageDraw.Draw(img)

        draw.text((-bbox[0], -bbox[1]), self.text, fill=(230, 230, 230), font=text_font)

        return img