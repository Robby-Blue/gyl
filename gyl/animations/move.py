from animation import Animation

class Move(Animation):

    def __init__(self, x, y, interpolation=None):
        super().__init__(interpolation)
        self.start_pos = None
        self.destination = (x, y)

    def apply_to_element(self, frame):
        if frame == 0:
            self.destination = self.element.normal_pos(self.destination)
            self.start_pos = self.element.normal_pos(self.element.position)

        time = frame/self.get_length()

        self.element.position = (
            self.interpolate(self.start_pos[0], self.destination[0], time),
            self.interpolate(self.start_pos[1], self.destination[1], time)
        )

    def get_length(self):
        return 20