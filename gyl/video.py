from scene import Scene

class Video():
    
    resolution = ()
    elements = []
    scenes = []
    backlog = []
    # eg to remember to remove once next scene starts if theres an animation

    def __init__(self, resolution=(1280, 720)):
        self.resolution = resolution
        self.add_scene()

    def render(self):
        for i, scene in enumerate(self.scenes):
            scene.render(f"{i}.mp4", self.resolution)

    def add_element(self, element):
        element.video = self
        self.elements.append(element)
        self.current_scene().elements.append(element)

    def animate(self, element, animation):
        self.current_scene().add_animation({
            "element": element,
            "animation": animation
        })

    def remove_element(self, element):
        self.elements.remove(element)
        self.current_scene().elements.remove(element)

    def add_scene(self):
        self.scenes.append(Scene(self.elements))    
        for event in self.backlog:
            self.current_scene().add_event(event)
        self.backlog.clear()

    def current_scene(self):
        return self.scenes[-1]