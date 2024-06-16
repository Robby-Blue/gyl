from gyl.interpolation import smooth

class Animation():

    element = None
    interpolator = None
    scene = None
    length = 0.5

    def __init__(self, interpolator, start_time=0):
        if not interpolator:
            interpolator = smooth()

        self.interpolator = interpolator
        self.start_time = start_time

    def interpolate(self, val1, val2, frame):
        if frame < self.start_time:
            return val1
        if frame > self.start_time+self.get_length():
            return val2
        return self.interpolator(val1, val2, (frame-self.start_time)/self.get_length())

    def get_end_time(self):
        return self.start_time + self.get_length()

    def get_length(self):
        return self.length
    
    def set_length(self, length):
        self.length = length
        return self

    def apply_to_element(self, frame, element):
        raise NotImplementedError()