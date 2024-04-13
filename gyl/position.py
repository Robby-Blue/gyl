def center(position_val):
    def get_center(width_val):
        return position_val-width_val/2
    return get_center

def right(position_val):
    def get_right(width_val):
        return position_val-width_val
    return get_right

def x_of(element):
    def get_x_of(_):
        return element.normal_pos()[0]
    return get_x_of

def y_of(element):
    def get_y_of(_):
        return element.normal_pos()[1]
    return get_y_of

def pos_of(element):
    return (x_of(element), y_of(element))