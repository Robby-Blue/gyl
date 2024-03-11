from animation import Animation

class Resize(Animation):

    def __init__(self, dest, interpolation=None):
        super().__init__(interpolation)
        self.start_width = None
        self.destination_width = dest

    def apply_to_element(self, frame):
        if frame == 0:
            self.start_width = self.element.width

        time = frame/self.get_length()

        self.element.width = self.interpolate(self.start_width, self.destination_width, time)

    def get_length(self):
        return 20