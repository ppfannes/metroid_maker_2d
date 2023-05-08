import glm
from components.component import Component
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.physics2d import Physics2D


class Fireball(Component):
    _fireball_count = 0

    def __init__(self):
        super().__init__()
        self._going_right = False
        self._rigid_body = None
        self._fireball_speed = 1.7
        self._velocity = glm.fvec2(0.0)
        self._acceleration = glm.fvec2(0.0)
        self._terminal_velocity = glm.fvec2(2.1, 3.1)
        self._on_ground = False
        self._lifetime = 4.0

    @classmethod
    def can_spawn(cls):
        return cls._fireball_count < 4

    def start(self):
        from metroid_maker.window import Window

        self._rigid_body = self.game_object.get_component(RigidBody2D)
        self._acceleration.y = Window.get_physics().gravity.y * 0.7
        Fireball._fireball_count += 1

    def update(self, dt: float):
        from metroid_maker.window import Window

        self._lifetime -= dt
        if self._lifetime < 0:
            self.disappear()
            return

        if self._going_right:
            self._velocity.x = self._fireball_speed
        else:
            self._velocity.x = -self._fireball_speed

        self.check_on_ground()

        if self._on_ground:
            self._acceleration.y = 1.5
            self._velocity.y = 2.5
        else:
            self._acceleration.y = Window.get_physics().gravity.y * 0.7

        self._velocity.y += self._acceleration.y * dt
        self._velocity.y = max(min(self._velocity.y, self._terminal_velocity.y), -self._terminal_velocity.y)
        self._rigid_body.velocity = self._velocity

    def check_on_ground(self):
        inner_player_width = 0.25 * 0.7
        y_val = -0.09
        self._on_ground = Physics2D.check_on_ground(self.game_object, inner_player_width, y_val)

    def begin_collision(self, colliding_object, contact, collision_normal):
        if abs(collision_normal[0]) > 0.8:
            self._going_right = collision_normal[0] < 0.0

    def pre_solve(self, colliding_object, contact, collision_normal):
        from components.player_controller import PlayerController

        if colliding_object.get_component(PlayerController) is not None or colliding_object.get_component(Fireball) is not None:
            contact.enabled = False

    def disappear(self):
        Fireball._fireball_count -= 1
        self.game_object.destroy()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_going_right"]
        del state["_rigid_body"]
        del state["_fireball_speed"]
        del state["_velocity"]
        del state["_acceleration"]
        del state["_terminal_velocity"]
        del state["_on_ground"]
        del state["_lifetime"]
        return state

    def __setstate__(self, state):
        state["_going_right"] = False
        state["_rigid_body"] = None
        state["_fireball_speed"] = 1.7
        state["_velocity"] = glm.fvec2(0.0)
        state["_acceleration"] = glm.fvec2(0.0)
        state["_terminal_velocity"] = glm.fvec2(2.1, 3.1)
        state["_on_ground"] = False
        state["_lifetime"] = 4.0
        self.__dict__.update(state)
