from components.sprite import Sprite


class Frame:
    def __init__(self, sprite=Sprite(), frame_time=0.0):
        self.sprite = sprite
        self.frame_time = frame_time
