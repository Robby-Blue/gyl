class Scene():

    elements = []
    animations = []

    def __init__(self, elements):
        self.elements = list(elements)
        self.animations = []

    def add_animation(self, animation):
        self.animations.append(animation)

    def render(self, file_name, resolution, fps):
        raise NotImplementedError()