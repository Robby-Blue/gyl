from elements.text import Text
from video import Video
from position import *
from animations.move import Move
from interpolation import smooth

if __name__ == "__main__":
    video = Video()

    text = Text("test", (center(50), center(50)))
    video.add_element(text)
    video.animate(text, Move(0, 0, interpolation=smooth()))

    video.render()