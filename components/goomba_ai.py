import glm
from components.component import Component
from components.player_controller import PlayerController
from components.state_machine import StateMachine
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.physics2d import Physics2D
from utils.asset_pool import AssetPool


class GoombaAI(Component):
    def __init__(self):
        super().__init__()
        self._going_right = False
        self._rigid_body = None
        self._walk_speed = 0.6
        self._velocity = glm.fvec2(0.0)
        self._acceleration = glm.fvec2(0.0)
        self._terminal_velocity = glm.fvec2(0.0)
        self._on_ground = False
        self._is_dead = False
        self._time_to_kill = 0.5
        self._state_machine = None

    def start(self):
        from metroid_maker.window import Window

        self._state_machine = self.game_object.get_component(StateMachine)
        self._rigid_body = self.game_object.get_component(RigidBody2D)
        self._acceleration.y = Window.get_physics().gravity.y * 0.7

    def update(self, dt):
        from metroid_maker.window import Window

        camera = Window.get_scene().camera()

        if (
            self.game_object.transform.position.x
            > camera.get_position().x
            + camera.get_projection_size().x * camera.get_zoom()
        ):
            return

        if self._is_dead:
            self._time_to_kill -= dt
            if self._time_to_kill <= 0:
                self.game_object.destroy()
            self._rigid_body.velocity = glm.fvec2(0.0)
            return

        if self._going_right:
            self._velocity.x = self._walk_speed
        else:
            self._velocity.x = -self._walk_speed

        self.check_on_ground()

        if self._on_ground:
            self._acceleration.y = 0.0
            self._velocity.y = 0.0
        else:
            self._acceleration.y = Window.get_physics().gravity.y * 0.7

        self._velocity.y += self._acceleration.y * dt
        self._velocity.y = max(
            min(self._velocity.y, self._terminal_velocity.y), -self._terminal_velocity.y
        )
        self._rigid_body.velocity = self._velocity

    def check_on_ground(self):
        inner_player_width = 0.25 * 0.7
        y_val = -0.14
        self._on_ground = Physics2D.check_on_ground(
            self.game_object, inner_player_width, y_val
        )

    def begin_collision(self, colliding_object, contact, collision_normal):
        if self._is_dead:
            return

        player_controller = colliding_object.get_component(PlayerController)
        if player_controller is not None:
            if (
                not player_controller.is_dead()
                and not player_controller.is_hurt_invincible()
                and collision_normal[1] > 0.58
            ):
                player_controller.enemy_bounce()
                self.stomp()
            elif (
                not player_controller.is_dead()
                and not player_controller.is_invincible()
            ):
                pass
                player_controller.die()
        elif abs(collision_normal[1]) < 0.1:
            self._going_right = collision_normal[0] < 0.0

    def stomp(self, play_sound=True):
        self._is_dead = True
        self._velocity = glm.fvec2(0.0)
        self._rigid_body.velocity = glm.fvec2(0.0)
        self._rigid_body.angular_velocity = 0.0
        self._rigid_body.gravity_scale = 0.0
        self._state_machine.trigger("getSquashed")
        self._rigid_body.is_sensor = True
        if play_sound:
            if AssetPool.get_sound("assets/sounds/bump.ogg").is_playing:
                AssetPool.get_sound("assets/sounds/bump.ogg").stop()
            AssetPool.get_sound("assets/sounds/bump.ogg").play()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_going_right"]
        del state["_rigid_body"]
        del state["_walk_speed"]
        del state["_velocity"]
        del state["_acceleration"]
        del state["_terminal_velocity"]
        del state["_on_ground"]
        del state["_is_dead"]
        del state["_time_to_kill"]
        del state["_state_machine"]
        return state

    def __setstate__(self, state):
        state["_going_right"] = False
        state["_rigid_body"] = None
        state["_walk_speed"] = 0.6
        state["_velocity"] = glm.fvec2(0.0)
        state["_acceleration"] = glm.fvec2(0.0)
        state["_terminal_velocity"] = glm.fvec2(0.0)
        state["_on_ground"] = False
        state["_is_dead"] = False
        state["_time_to_kill"] = 0.5
        state["_state_machine"] = None
        self.__dict__.update(state)
