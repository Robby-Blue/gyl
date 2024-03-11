from elements.text import Text
from video import Video
from position import *
from animations.move import Move
from animations.resize import Resize

if __name__ == "__main__":
    video = Video()

    text = Text("test", (center(50), center(50)))
    video.add_element(text)
    video.animate(text, Move(0, 0))
    video.animate(text, Resize(10))
    
    video.add_scene()
    video.animate(text, Move(center(50), center(50)))
    video.animate(text, Resize(20))

    video.render()