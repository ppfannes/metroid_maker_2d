import glm
from glfw import KEY_D, KEY_RIGHT, KEY_A, KEY_LEFT
from components.component import Component
from components.state_machine import StateMachine
from physics2d.components.rigid_body_2d import RigidBody2D
from utils.key_listener import KeyListener


class PlayerController(Component):
    def __init__(self) -> None:
        super().__init__()

        self.walk_speed = 1.9
        self.jump_boost = 1.0
        self.jump_impulse = 3.0
        self.slow_down_force = 0.05
        self.terminal_velocity = glm.fvec2(2.1, 3.1)

        self.on_ground = False
        self._ground_debounce = 0.0
        self._ground_debounce_time = 0.1
        self._rigid_body = None
        self._state_machine = None
        self._big_jump_boos_factor = 1.05
        self._player_width = 0.25
        self._jump_time = 0.0
        self._acceleration = glm.fvec2(1.0)
        self._velocity = glm.fvec2(1.0)
        self._is_dead = False
        self._enemy_bounce = 0.0

    def start(self):
        self._rigid_body = self.game_object.get_component(RigidBody2D)
        self._state_machine = self.game_object.get_component(StateMachine)
        self._rigid_body.gravity_scale = 0.0

    def update(self, dt):
        from metroid_maker.window import Window

        if KeyListener.is_key_pressed(KEY_RIGHT) or KeyListener.is_key_pressed(KEY_D):
            self.game_object.transform.scale.x = self._player_width
            self._acceleration.x = self.walk_speed

            if self._velocity.x < 0:
                self._state_machine.trigger("switchDirection")
                self._velocity.x += self.slow_down_force
            else:
                self._state_machine.trigger("startRunning")

        elif KeyListener.is_key_pressed(KEY_LEFT) or KeyListener.is_key_pressed(KEY_A):
            self.game_object.transform.scale.x = -self._player_width
            self._acceleration.x = -self.walk_speed

            if self._velocity.x > 0:
                self._state_machine.trigger("switchDirection")
                self._velocity.x -= self.slow_down_force
            else:
                self._state_machine.trigger("startRunning")

        else:
            self._acceleration.x = 0

            if self._velocity.x > 0:
                self._velocity.x = max(0, self._velocity.x - self.slow_down_force)

            elif self._velocity.x < 0:
                self._velocity.x = min(0, self._velocity.x + self.slow_down_force)

            if self._velocity.x == 0:
                self._state_machine.trigger("stopRunning")

        self._acceleration.y = Window.get_physics().gravity.y * 0.7

        self._velocity = self._acceleration * dt
        self._velocity.x = max(min(self._velocity.x, self.terminal_velocity.x), -self.terminal_velocity.x)
        self._velocity.y = max(min(self._velocity.y, self.terminal_velocity.y), -self.terminal_velocity.y)
        self._rigid_body.velocity = self._velocity
        self._rigid_body.angular_velocity = 0.0

