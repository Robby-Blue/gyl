def center(position_val):
    def f(width_val):
        return position_val-width_val/2
    return f