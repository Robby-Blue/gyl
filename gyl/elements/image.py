import PIL.Image
from gyl.element import Element
import PIL

class Img(Element):

    def __init__(self, path, position, width=None):
        if not width:
            width = 50
        super().__init__(position, width)
        self.image = PIL.Image.open(path)
        self.path = path

    def draw(self):
        return self.image
    
    def get_size(self):
        return self.image.size
    
    def get_cache(self):
        return {
            "type": "Text",
            "pos": self.normal_pos(),
            "size": self.normal_width(),
            "path": self.path
        }