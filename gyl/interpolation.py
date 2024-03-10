import math

def linear():
    def f(val1, val2, time):
        return val1 + (val2-val1)*time
    return f

def smooth():
    def f(val1, val2, time):
        return val1 + (val2-val1)*(1+math.sin(math.pi * (time-0.5)))/2
    
    return f