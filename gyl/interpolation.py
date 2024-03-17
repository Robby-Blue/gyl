import math

def linear():
    def get_linear(val1, val2, time):
        return val1 + (val2-val1)*time
    return get_linear

def smooth():
    def get_smooth(val1, val2, time):
        return val1 + (val2-val1)*(1+math.sin(math.pi * (time-0.5)))/2
    
    return get_smooth