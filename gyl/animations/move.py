from gyl.animation import Animation
from gyl.animations.resize import Resize

class Move(Animation):

    def __init__(self, x, y, interpolation=None):
        super().__init__(interpolation)
        self.start_pos = None
        self.destination = (x, y)
        self.normal_destination = None

    def apply_to_element(self, frame):
        if frame == 0:
            end_width = self.get_end_width()

            self.normal_destination = self.element.normal_pos(self.destination, width=end_width)
            self.start_pos = self.element.normal_pos(self.element.position)

        time = frame/self.get_length()

        self.element.position = (
            self.interpolate(self.start_pos[0], self.normal_destination[0], time),
            self.interpolate(self.start_pos[1], self.normal_destination[1], time)
        )

        if frame == self.get_length():
            self.element.position = self.destination

    def get_end_width(self):
        for animation in self.scene.animations:
            if animation["element"] != self.element:
                continue
            if not isinstance(animation["animation"], Resize):
                continue
            return animation["animation"].destination_width
        return self.element.width
    
    def get_animation_type(self):
        return "EDITATTR"

    def get_length(self):
        return 20