class Element():

    video = None

    def __init__(self, position, width):
        self.position = position
        self.width = width

    def draw(self):
        raise NotImplementedError()
    
    def normal_pos(self, position=None):
        if not position:
            position = self.position

        x = position[0]
        if callable(x):
            x = x(self.width)

        # hope that its easy to draw
        im = self.draw()

        res = self.video.resolution
        video_aspect_ratio = res[0]/res[1]
        height = self.width/im.width*im.height * video_aspect_ratio

        y = position[1]
        if callable(y):
            y = y(height)

        return (x, y)