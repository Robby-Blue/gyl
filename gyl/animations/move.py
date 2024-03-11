from animation import Animation
from animations.resize import Resize

class Move(Animation):

    def __init__(self, x, y, interpolation=None):
        super().__init__(interpolation)
        self.start_pos = None
        self.destination = (x, y)

    def apply_to_element(self, frame):
        if frame == 0:
            end_width = self.get_end_width()
            print(end_width)

            self.destination = self.element.normal_pos(self.destination, width=end_width)
            self.start_pos = self.element.normal_pos(self.element.position)

        time = frame/self.get_length()

        self.element.position = (
            self.interpolate(self.start_pos[0], self.destination[0], time),
            self.interpolate(self.start_pos[1], self.destination[1], time)
        )

    def get_end_width(self):
        for animation in self.scene.animations:
            print(animation)
            if animation["element"] != self.element:
                continue
            print(animation)
            if not isinstance(animation["animation"], Resize):
                continue
            return animation["animation"].destination_width
        return self.element.width

    def get_length(self):
        return 20