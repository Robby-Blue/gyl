from gyl.elements.text import Text
from gyl.video import Video
from gyl.position import *
from gyl.animations.slidereveal import SlideReveal

if __name__ == "__main__":
    video = Video()

    text = Text("test text", (1, 1))
    video.add_element(text)
    video.animate(text, SlideReveal())

    video.render()