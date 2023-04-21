import typing
import glm
import math
from components.component import Component
from physics2d.enums.body_types import BodyType
from Box2D.b2 import vec2

if typing.TYPE_CHECKING:
    from Box2D.b2 import body


class RigidBody2D(Component):
    def __init__(self) -> None:
        super().__init__()
        self._velocity = glm.fvec2(1.0)
        self._angular_damping = 0.8
        self._linear_damping = 0.9
        self._mass = 0
        self._body_type = BodyType.DYNAMIC
        self._friction = 0.1
        self._angular_velocity = 0.0
        self._gravity_scale = 1.0
        self._is_sensor = False

        self._fixed_rotation = False
        self._continuous_collision = True

        self._raw_body: body = None

    @property
    def offset(self):
        return self._offset

    def apply_force(self, force):
        if self._raw_body is not None:
            self._raw_body.ApplyForceToCenter((force.x, force.y), True)

    def apply_impulse(self, impulse):
        if self._raw_body is not None:
            self._raw_body.ApplyLinearImpulse(
                (impulse.x, impulse.y), self._raw_body.worldCenter, True
            )

    def update(self, dt):
        if self._raw_body is not None:
            if (
                self._body_type == BodyType.DYNAMIC
                or self._body_type == BodyType.KINEMATIC
            ):
                self.game_object.transform.position = glm.fvec2(
                    self._raw_body.position.x, self._raw_body.position.y
                )
                self.game_object.transform.rotation = math.degrees(self._raw_body.angle)
                self._velocity = glm.fvec2(
                    self._raw_body.linearVelocity.x, self._raw_body.linearVelocity.y
                )
            elif self._body_type == BodyType.STATIC:
                self._raw_body.transform = (
                    vec2(
                        self.game_object.transform.position.x,
                        self.game_object.transform.position.y,
                    ),
                    self.game_object.transform.rotation,
                )

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity = value

        if self._raw_body is not None:
            self._raw_body.linearVelocity = value

    @property
    def angular_velocity(self):
        return self._angular_velocity

    @angular_velocity.setter
    def angular_velocity(self, value):
        self._angular_velocity = value

        if self._raw_body is not None:
            self._raw_body.angularVelocity = value

    @property
    def gravity_scale(self):
        return self._gravity_scale

    @gravity_scale.setter
    def gravity_scale(self, value):
        self._gravity_scale = value

        if self._raw_body is not None:
            self._raw_body.gravityScale = value

    @property
    def is_sensor(self):
        return self._is_sensor

    @is_sensor.setter
    def is_sensor(self, value):
        from metroid_maker.window import Window

        self._is_sensor = value

        if self._raw_body is not None:
            Window.get_physics().set_is_sensor(self, value)

    @property
    def friction(self):
        return self._friction

    @friction.setter
    def friction(self, value):
        self._friction = value

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

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_raw_body"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._raw_body = None
