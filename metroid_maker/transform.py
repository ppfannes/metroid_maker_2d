import glm

class Transform:
    def __init__(self, position=glm.fvec2(), scale=glm.fvec2(), rotation=0.0):
        self.position = position
        self.scale = scale
        self.rotation = rotation

    def copy(self):
        return Transform(glm.fvec2(self.position), glm.fvec2(self.scale))

    def copy_to(self, transform: 'Transform'):
        transform.position.xy = self.position.xy
        transform.scale.xy = self.scale.xy

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Transform):
            return self.position == other.position and self.scale == other.scale
        return NotImplementedError
