from elements.text import Text
from video import Video
from position import *
from animations.edittext import EditText

if __name__ == "__main__":
    video = Video()

    text = Text("test text", (1, 1))
    video.add_element(text)
    video.animate(text, EditText("other test"))

    video.render()