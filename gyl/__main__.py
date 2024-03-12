from elements.text import Text, lineheight
from video import Video
from position import *

if __name__ == "__main__":
    video = Video()

    text = Text("test text", (1, 1))
    video.add_element(text)
    text2 = Text("test", (1, 11))
    video.add_element(text2)
    text3 = Text("really long test text goes here", (1, 21))
    video.add_element(text3)

    video.render()