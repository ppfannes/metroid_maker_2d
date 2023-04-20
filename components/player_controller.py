from enum import Enum
import glm
from glfw import KEY_D, KEY_RIGHT, KEY_A, KEY_LEFT, KEY_SPACE
from components.component import Component
from components.ground import Ground
from components.state_machine import StateMachine
from physics2d.components.rigid_body_2d import RigidBody2D
from utils.asset_pool import AssetPool
from utils.key_listener import KeyListener
from openal import *


class PlayerState(Enum):
    SMALL = 0
    BIG = 1
    FIRE = 2
    INVINCIBLE = 3


class PlayerController(Component):
    def __init__(self) -> None:
        super().__init__()

        self.walk_speed = 1.9
        self.jump_boost = 1.0
        self.jump_impulse = 3.0
        self.slow_down_force = 0.05
        self.terminal_velocity = glm.fvec2(2.1, 3.1)
        self._player_state = PlayerState.SMALL

        self.on_ground = False
        self._ground_debounce = 0.0
        self._ground_debounce_time = 0.1
        self._rigid_body = None
        self._state_machine = None
        self._big_jump_boost_factor = 1.05
        self._player_width = 0.25
        self._jump_time = 0.0
        self._acceleration = glm.fvec2(0.0)
        self._velocity = glm.fvec2(0.0)
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

        self.check_on_ground()

        if KeyListener.is_key_pressed(KEY_SPACE) and (
            self._jump_time > 0 or self.on_ground or self._ground_debounce > 0
        ):
            if (self.on_ground or self._ground_debounce > 0) and self._jump_time == 0:
                if AssetPool.get_sound("assets/sounds/jump-small.ogg").is_playing:
                    AssetPool.get_sound("assets/sounds/jump-small.ogg").stop()
                AssetPool.get_sound("assets/sounds/jump-small.ogg").play()
                self._jump_time = 28
                self._velocity.y = self.jump_impulse
            elif self._jump_time > 0:
                self._jump_time -= 1
                self._velocity.y = (self._jump_time / 2.2) * self.jump_boost
            else:
                self._velocity.y = 0
            self._ground_debounce = 0
        elif not self.on_ground:
            if self._jump_time > 0:
                self._velocity.y *= 0.35
                self._jump_time = 0
            self._ground_debounce -= dt
            self._acceleration.y = Window.get_physics().gravity.y * 0.7
        else:
            self._velocity.y = 0
            self._acceleration.y = 0
            self._ground_debounce = self._ground_debounce_time

        self._velocity += self._acceleration * dt
        self._velocity.x = max(
            min(self._velocity.x, self.terminal_velocity.x), -self.terminal_velocity.x
        )
        self._velocity.y = max(
            min(self._velocity.y, self.terminal_velocity.y), -self.terminal_velocity.y
        )
        self._rigid_body.velocity = self._velocity
        self._rigid_body.angular_velocity = 0.0

        if not self.on_ground:
            self._state_machine.trigger("jump")
        else:
            self._state_machine.trigger("stopJumping")

    def check_on_ground(self):
        from metroid_maker.window import Window
        from renderer.debug_draw import DebugDraw

        raycast_begin = glm.fvec2(self.game_object.transform.position)
        inner_player_width = self._player_width * 0.6
        raycast_begin = glm.sub(raycast_begin, glm.fvec2(inner_player_width / 2.0, 0.0))
        y_val = 0.0

        if self._player_state == PlayerState.SMALL:
            y_val = -0.14
        else:
            y_val = -0.24

        raycast_end = glm.add(raycast_begin, glm.fvec2(0.0, y_val))

        info = Window.get_physics().raycast(
            self.game_object, raycast_begin, raycast_end
        )

        raycast2_begin = glm.add(raycast_begin, glm.fvec2(inner_player_width, 0.0))
        raycast2_end = glm.add(raycast_end, glm.fvec2(inner_player_width, 0.0))
        info2 = Window.get_physics().raycast(
            self.game_object, raycast2_begin, raycast2_end
        )

        self.on_ground = (
            info.hit
            and info.hit_object is not None
            and info.hit_object.get_component(Ground)
            or info2.hit
            and info2.hit_object is not None
            and info2.hit_object.get_component(Ground)
        )

    def begin_collision(self, colliding_object, contact, collision_normal):
        if self._is_dead:
            return

        if colliding_object.get_component(Ground) is not None:
            if abs(collision_normal[0]) > 0.8:
                self._velocity.x = 0
            elif collision_normal[1] > 0.8:
                self._velocity.y = 0
                self._acceleration.y = 0
                self._jump_time = 0

    def is_small(self):
        return self._player_state == PlayerState.SMALL

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["on_ground"]
        del state["_ground_debounce"]
        del state["_ground_debounce_time"]
        del state["_rigid_body"]
        del state["_state_machine"]
        del state["_big_jump_boost_factor"]
        del state["_player_width"]
        del state["_jump_time"]
        del state["_acceleration"]
        del state["_velocity"]
        del state["_is_dead"]
        del state["_enemy_bounce"]
        return state

    def __setstate__(self, state):
        state["on_ground"] = False
        state["_ground_debounce"] = 0.0
        state["_ground_debounce_time"] = 0.1
        state["_rigid_body"] = None
        state["_state_machine"] = None
        state["_big_jump_boost_factor"] = 1.05
        state["_player_width"] = 0.25
        state["_jump_time"] = 0.0
        state["_acceleration"] = glm.fvec2(0.0)
        state["_velocity"] = glm.fvec2(0.0)
        state["_is_dead"] = False
        state["_enemy_bounce"] = 0.0
        self.__dict__.update(state)
