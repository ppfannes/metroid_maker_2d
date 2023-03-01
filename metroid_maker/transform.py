import glm

class Transform:
    def __init__(self, position=glm.vec2(), scale=glm.vec2()):
        self.position = position
        self.scale = scale

    def copy(self):
        return Transform(glm.vec2(self.position), glm.vec2(self.scale))

    def copy_to(self, transform: 'Transform'):
        transform.position.xy = self.position.xy
        transform.scale.xy = self.scale.xy

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Transform):
            return self.position == other.position and self.scale == other.scale
        return NotImplementedError
