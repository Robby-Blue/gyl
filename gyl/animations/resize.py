from gyl.animation import Animation

class Resize(Animation):

    def __init__(self, dest, interpolation=None):
        super().__init__(interpolation)
        self.start_width = None
        self.destination_width = dest
        self.normed_destination_width = None

    def apply_to_element(self, frame):
        if frame == 0:
            self.start_width = self.element.width
            self.normed_destination_width = self.element.normal_width(self.destination_width)

        time = frame/self.get_length()

        self.element.width = self.interpolate(self.start_width, self.normed_destination_width, time)

        if frame == self.get_length():
            self.element.width = self.destination_width

    def get_length(self):
        return 20