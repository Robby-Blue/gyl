from gyl.animation import Animation
from gyl.interpolation import linear
from fast_diff_match_patch import diff

class EditText(Animation):

    def __init__(self, text, interpolation=None, start_frame=0):
        if not interpolation:
            interpolation = linear()
        super().__init__(interpolation, start_frame)
        self.start_string = None
        self.end_string = text
        self.steps = None

    def apply_to_element(self, frame):
        if frame == 0:
            start_string = self.element.text
            self.steps = self.plan_steps(start_string, self.end_string)

        timed_index = self.interpolate(0, len(self.steps)-1, frame)
        self.element.text = self.steps[int(timed_index)]

    def plan_steps(self, start_str, end_str):
        changes = diff(start_str, end_str)

        idx = 0
        current_text = str(start_str)
        texts = []

        for op, length in changes:
            if op == "-":
                for _ in range(length):
                    texts.append(str(current_text))
                    current_text = current_text[:idx]+current_text[idx+1:]
            if op == "=":
                idx += length
            if op == "+":
                for _ in range(length):
                    texts.append(str(current_text))
                    current_text = current_text[:idx]+end_str[idx]+current_text[idx:]
                    idx+=1

        texts.append(str(current_text))
        return texts
    
    def get_animation_type(self):
        return "EDITATTR"

    def get_length(self):
        return 50