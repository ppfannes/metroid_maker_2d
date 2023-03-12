import glm
import math
from components.component import Component
from physics2d.enums.body_types import BodyType

class RigidBody2D(Component):

    def __init__(self) -> None:
        super().__init__()
        self._velocity = glm.fvec2()
        self._angular_damping = 0.8
        self._linear_damping = 0.9
        self._mass = 0
        self._body_type = BodyType.DYNAMIC

        self._fixed_rotation = False
        self._continuous_collision = True

        self._raw_body = None

    def update(self, dt):
        if self._raw_body is not None:
            self.game_object.transform.position = glm.fvec2(self._raw_body.position.x, self._raw_body.position.y)
            self.game_object.transform.rotation = math.degrees(self._raw_body.angle)

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    @property
    def angular_damping(self):
        return self._angular_damping

    @angular_damping.setter
    def angular_damping(self, value):
        self._angular_damping = value

    @property
    def linear_damping(self):
        return self._linear_damping

    @linear_damping.setter
    def linear_damping(self, value):
        self._linear_damping = value

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        self._mass = value

    @property
    def body_type(self):
        return self._body_type

    @body_type.setter
    def body_type(self, value):
        self._body_type = value

    @property
    def fixed_rotation(self):
        return self._fixed_rotation

    @fixed_rotation.setter
    def fixed_rotation(self, value):
        self._fixed_rotation = value

    @property
    def continuous_collision(self):
        return self._continuous_collision

    @continuous_collision.setter
    def continuous_collision(self, value):
        self._continuous_collision = value

    @property
    def raw_body(self):
        return self._raw_body

    @raw_body.setter
    def raw_body(self, value):
        self._raw_body = value
