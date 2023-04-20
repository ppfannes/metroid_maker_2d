import glm
from Box2D.b2 import rayCastCallback, fixture
from metroid_maker.game_object import GameObject


class RaycastInfo(rayCastCallback):
    def __init__(self, requesting_object):
        super().__init__()
        self.fixture: fixture = None
        self.point: glm.fvec2 = glm.fvec2()
        self.normal: glm.fvec2 = glm.fvec2()
        self.fraction: float = 0.0
        self.hit: bool = False
        self.hit_object: GameObject = None
        self._requesting_object: GameObject = requesting_object

    def ReportFixture(self, fixture, point, normal, fraction):
        if fixture.userData == self._requesting_object:
            return 1

        self.fixture = fixture
        self.point = glm.fvec2(*point)
        self.normal = glm.fvec2(*normal)
        self.fraction = fraction
        self.hit = fraction != 0.0
        self.hit_object = fixture.userData

        return fraction
