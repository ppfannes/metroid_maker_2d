from Box2D.b2 import rayCastCallback, vec2, fixture
from metroid_maker.game_object import GameObject


class RaycastInfo(rayCastCallback):
    def __init__(self, requesting_object):
        super().__init__()
        self.fixture: fixture = None
        self.point: vec2 = vec2()
        self.normal: vec2 = vec2()
        self.fraction: float = 0.0
        self.hit: bool = False
        self.hit_object: GameObject = None
        self._requesting_object: GameObject = requesting_object

    def ReportFixture(self, fixture, point, normal, fraction):
        if fixture.userData == self._requesting_object:
            return 1

        self.fixture = fixture
        self.point = point
        self.normal = normal
        self.fraction = fraction
        self.hit = fraction != 0.0
        self.hit_object = fixture.userData

        return fraction
