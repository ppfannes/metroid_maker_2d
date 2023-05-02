from enum import Enum
import glm
from glfw import KEY_D, KEY_RIGHT, KEY_A, KEY_LEFT, KEY_SPACE
from components.component import Component
from components.ground import Ground
from components.sprite_renderer import SpriteRenderer
from components.state_machine import StateMachine
from physics2d.physics2d import Physics2D
from physics2d.enums.body_types import BodyType
from physics2d.components.pillbox_collider import PillboxCollider
from physics2d.components.rigid_body_2d import RigidBody2D
from utils.asset_pool import AssetPool
from utils.key_listener import KeyListener


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

        self._hurt_invincibility_time_left = 0.0
        self._hurt_invincibility_time = 1.4
        self._dead_max_height = 0.0
        self._dead_min_height = 0.0
        self._dead_going_up = True
        self._blink_time = 0.0
        self._sprite_renderer = None

        self._play_win_animation = False
        self._time_to_castle = 4.5
        self._walk_time = 2.2

    def has_won(self):
        return False

    def start(self):
        self._sprite_renderer = self.game_object.get_component(SpriteRenderer)
        self._rigid_body = self.game_object.get_component(RigidBody2D)
        self._state_machine = self.game_object.get_component(StateMachine)
        self._rigid_body.gravity_scale = 0.0

    def update(self, dt):
        from metroid_maker.window import Window
        from scenes.level_scene_initializer import LevelSceneInitializer
        from scenes.level_editor_scene_initializer import LevelEditorSceneInitializer

        if self._play_win_animation:
            self.check_on_ground()
            if not self.on_ground:
                self.game_object.transform.scale.x = -0.25
                self.game_object.transform.position.y -= dt
                self._state_machine.trigger("stopRunning")
                self._state_machine.trigger("stopJumping")
            else:
                if self._walk_time > 0.0:
                    self.game_object.transform.scale.x = 0.25
                    self.game_object.transform.position.x += dt
                    self._state_machine.trigger("startRunning")
                if not AssetPool.get_sound("assets/sounds/stage_clear.ogg").is_playing:
                    AssetPool.get_sound("assets/sounds/stage_clear.ogg").play()
                self._time_to_castle -= dt
                self._walk_time -= dt

                if self._time_to_castle <= 0.0:
                    Window.change_scene(LevelEditorSceneInitializer())

            return

        if self._is_dead:
            if (
                self.game_object.transform.position.y < self._dead_max_height
                and self._dead_going_up
            ):
                self.game_object.transform.position.y += dt * self.walk_speed / 2.0
            elif (
                self.game_object.transform.position.y >= self._dead_max_height
                and self._dead_going_up
            ):
                self._dead_going_up = False
            elif (
                not self._dead_going_up
                and self.game_object.transform.position.y > self._dead_min_height
            ):
                self._rigid_body.body_type = BodyType.KINEMATIC
                self._acceleration.y = Window.get_physics().gravity.y * 0.7
                self._velocity.y += self._acceleration.y * dt
                self._velocity.y = max(
                    min(self._velocity.y, self.terminal_velocity.y),
                    -self.terminal_velocity.y,
                )
                self._rigid_body.velocity = self._velocity
                self._rigid_body.angular_velocity = 0.0
            elif (
                not self._dead_going_up
                and self.game_object.transform.position.y <= self._dead_min_height
            ):
                Window.change_scene(LevelSceneInitializer())
            return

        if self._hurt_invincibility_time_left > 0:
            self._hurt_invincibility_time_left -= dt
            self._blink_time -= dt

            if self._blink_time <= 0:
                self._blink_time = 0.2
                if self._sprite_renderer.get_color().w == 1:
                    self._sprite_renderer.set_color(glm.fvec4(1.0, 1.0, 1.0, 0.0))
                else:
                    self._sprite_renderer.set_color(glm.fvec4(1.0, 1.0, 1.0, 1.0))
            else:
                if self._sprite_renderer.get_color().w == 0:
                    self._sprite_renderer.set_color(glm.fvec4(1.0, 1.0, 1.0, 1.0))

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
        elif self._enemy_bounce > 0:
            self._enemy_bounce -= 1
            self._velocity.y = (self._enemy_bounce / 2.2) * self.jump_boost
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
        inner_player_width = self._player_width * 0.6
        y_val = 0.0

        if self._player_state == PlayerState.SMALL:
            y_val = -0.14
        else:
            y_val = -0.24

        self.on_ground = Physics2D.check_on_ground(
            self.game_object, inner_player_width, y_val
        )

    def set_position(self, new_pos):
        self.game_object.transform.position = new_pos
        self._rigid_body.set_position(new_pos)

    def powerup(self):
        if self._player_state == PlayerState.SMALL:
            self._player_state = PlayerState.BIG
            if AssetPool.get_sound("assets/sounds/powerup.ogg").is_playing:
                AssetPool.get_sound("assets/sounds/powerup.ogg").stop()
            AssetPool.get_sound("assets/sounds/powerup.ogg").play()
            self.game_object.transform.scale.y = 0.42
            pillbox_collider = self.game_object.get_component(PillboxCollider)
            if pillbox_collider is not None:
                self.jump_boost *= self._big_jump_boost_factor
                self.walk_speed *= self._big_jump_boost_factor
                pillbox_collider.height = 0.63
        elif self._player_state == PlayerState.BIG:
            self._player_state = PlayerState.FIRE
            if AssetPool.get_sound("assets/sounds/powerup.ogg").is_playing:
                AssetPool.get_sound("assets/sounds/powerup.ogg").stop()
            AssetPool.get_sound("assets/sounds/powerup.ogg").play()

        self._state_machine.trigger("powerup")

    def play_win_animation(self, flagpole):
        if not self._play_win_animation:
            self._play_win_animation = True
            self._velocity = glm.fvec2(0.0)
            self._acceleration = glm.fvec2(0.0)
            self._rigid_body.velocity = self._velocity
            self._rigid_body.is_sensor = True
            self._rigid_body.body_type = BodyType.STATIC
            self.game_object.transform.position.x = flagpole.transform.position.x
            AssetPool.get_sound("assets/sounds/flagpole.ogg").play()

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

    def enemy_bounce(self):
        self._enemy_bounce = 8

    def is_small(self):
        return self._player_state == PlayerState.SMALL

    def is_dead(self):
        return self._is_dead

    def is_hurt_invincible(self):
        return self._hurt_invincibility_time_left > 0 or self._play_win_animation

    def is_invincible(self):
        return (
            self._player_state == PlayerState.INVINCIBLE
            or self._hurt_invincibility_time_left > 0 or self._play_win_animation
        )

    def die(self):
        self._state_machine.trigger("die")
        if self._player_state == PlayerState.SMALL:
            self._velocity = glm.fvec2(0.0)
            self._acceleration = glm.fvec2(0.0)
            self._rigid_body.velocity = glm.fvec2(0.0)
            self._is_dead = True
            self._rigid_body.is_sensor = True
            AssetPool.get_sound("assets/sounds/mario_die.ogg").play()
            self._dead_max_height = self.game_object.transform.position.y + 0.3
            self._rigid_body.body_type = BodyType.STATIC
            if self.game_object.transform.position.y > 0:
                self._dead_min_height = -0.25
        elif self._player_state == PlayerState.BIG:
            self._player_state = PlayerState.SMALL
            self.game_object.transform.scale.y = 0.25
            pillbox_collider = self.game_object.get_component(PillboxCollider)
            if pillbox_collider is not None:
                self.jump_boost /= self._big_jump_boost_factor
                self.walk_speed /= self._big_jump_boost_factor
                pillbox_collider.height = 0.31
            self._hurt_invincibility_time_left = self._hurt_invincibility_time
            if AssetPool.get_sound("assets/sounds/pipe.ogg").is_playing:
                AssetPool.get_sound("assets/sounds/pipe.ogg").stop()
            AssetPool.get_sound("assets/sounds/pipe.ogg").play()
        elif self._player_state == PlayerState.FIRE:
            self._player_state = PlayerState.BIG
            self._hurt_invincibility_time_left = self._hurt_invincibility_time
            if AssetPool.get_sound("assets/sounds/pipe.ogg").is_playing:
                AssetPool.get_sound("assets/sounds/pipe.ogg").stop()
            AssetPool.get_sound("assets/sounds/pipe.ogg").play()

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
        del state["_hurt_invincibility_time_left"]
        del state["_hurt_invincibility_time"]
        del state["_dead_max_height"]
        del state["_dead_min_height"]
        del state["_dead_going_up"]
        del state["_blink_time"]
        del state["_sprite_renderer"]
        del state["_play_win_animation"]
        del state["_time_to_castle"]
        del state["_walk_time"]
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
        state["_hurt_invincibility_time_left"] = 0.0
        state["_hurt_invincibility_time"] = 1.4
        state["_dead_max_height"] = 0.0
        state["_dead_min_height"] = 0.0
        state["_dead_going_up"] = True
        state["_blink_time"] = 0.0
        state["_sprite_renderer"] = None
        state["_play_win_animation"] = False
        state["_time_to_castle"] = 4.5
        state["_walk_time"] = 2.2
        self.__dict__.update(state)
