from gyl.element import Element
from gyl.position import pos_of
from gyl.size import size_of
from PIL import Image, ImageDraw

class Striketrough(Element):

    def __init__(self, element, vertical=False):
        self.element = element
        
        self.position = pos_of(element)
        self.width = size_of(element)

        self.vertical = vertical

    def draw(self):
        size = self.get_size()

        x = size[0]
        y = size[1]

        linewidth = size[0]//50

        if self.vertical:
            shape = [(linewidth, y-linewidth),
                    (x-linewidth, linewidth)]
        else:
            shape = [(linewidth, y/2),
                    (x-linewidth, y/2)]

        img = Image.new("RGBA", size, (0, 0, 0, 0))

        draw = ImageDraw.Draw(img)
        draw.line(shape, fill=(255, 0, 0, 255), width=linewidth)

        return img

    def get_size(self):
        x, y = self.element.get_size()
        return x, y
    
    def get_cache(self):
        return {
            "type": "Text",
            "pos": self.normal_pos(),
            "size": self.normal_width(),
            "vertical": self.vertical
        }