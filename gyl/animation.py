from interpolation import smooth

class Animation():

    element = None
    interpolate = None

    def __init__(self, interpolate):
        if not interpolate:
            interpolate = smooth()

        self.interpolate = interpolate

    def get_length(self):
        raise NotImplementedError()

    def apply_to_element(self, frame, element):
        raise NotImplementedError()