def lineheight(height):
    # calculate the elements width such that it has a specific
    # line height
    def get_lineheight(text_element):
        imwidth, imheight = text_element.get_size()
        if imwidth == 0:
            return 0
        
        res = text_element.video.resolution
        video_aspect_ratio = res[0]/res[1]

        w = height/ video_aspect_ratio/imheight*imwidth
        return w
    return get_lineheight

def height(element):
    # calculate the elements width such that it has a specific
    # line height
    def get_height(text_element):
        _, imheight = text_element.get_size()
        if imheight == 0:
            return 0

        scale = text_element.get_size()[1]/element.get_size()[1]

        if not callable(element.width):
            first_type = type(element).__name__
            text_type = type(element).__name__
            raise ValueError(f"{text_type} Element set to height({first_type}), {first_type} needs to have a functional height")
        return element.width(text_element)*scale
    return get_height