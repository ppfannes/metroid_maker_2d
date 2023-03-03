class Line2D:

    def __init__(self, start, end, color, lifetime):
        self._start = start
        self._end = end
        self._color = color
        self._lifetime = lifetime

    def begin_frame(self):
        self._lifetime -= 1
        return self._lifetime

    def get_start(self):
        return self._start
    
    def get_end(self):
        return self._end
    
    def get_color(self):
        return self._color
