from gyl.interpolation import smooth

class Animation():

    element = None
    interpolator = None
    scene = None

    def __init__(self, interpolator, start_frame=0):
        if not interpolator:
            interpolator = smooth()

        self.interpolator = interpolator
        self.start_frame = start_frame

    def interpolate(self, val1, val2, frame):
        if frame < self.start_frame:
            return val1
        if frame > self.start_frame+self.get_length():
            return val2
        return self.interpolator(val1, val2, (frame-self.start_frame)/self.get_length())

    def get_last_frame(self):
        return self.start_frame + self.get_length()

    def get_length(self):
        raise NotImplementedError()

    def apply_to_element(self, frame, element):
        raise NotImplementedError()