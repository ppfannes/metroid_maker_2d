import glm
from components.component import Component
from components.fireball import Fireball
from components.goomba_ai import GoombaAI
from components.state_machine import StateMachine
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.physics2d import Physics2D
from utils.asset_pool import AssetPool


class TurtleAI(Component):
    def __init__(self):
        super().__init__()
        self._going_right = False
        self._rigid_body = None
        self._walk_speed = 0.6
        self._velocity = glm.fvec2(0.0)
        self._acceleration = glm.fvec2(0.0)
        self._terminal_velocity = glm.fvec2(2.1, 3.1)
        self._on_ground = False
        self._is_dead = False
        self._is_moving = False
        self._state_machine = None
        self._moving_debounce = 0.32

    def start(self):
        from metroid_maker.window import Window

        self._state_machine = self.game_object.get_component(StateMachine)
        self._rigid_body = self.game_object.get_component(RigidBody2D)
        self._acceleration.y = Window.get_physics().gravity.y * 0.7

    def update(self, dt):
        from metroid_maker.window import Window

        self._moving_debounce -= dt
        camera = Window.get_scene().camera()

        if (
            self.game_object.transform.position.x
            > camera._position.x + camera.get_projection_size().x * camera.get_zoom()
        ):
            return

        if not self._is_dead or self._is_moving:
            if self._going_right:
                self.game_object.transform.scale.x = -0.25
                self._velocity.x = self._walk_speed
            else:
                self.game_object.transform.scale.x = 0.25
                self._velocity.x = -self._walk_speed
        else:
            self._velocity.x = 0.0

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

        if self.game_object.transform.position.x < camera._position.x - 0.5:
            self.game_object.destroy()

    def check_on_ground(self):
        inner_player_width = 0.25 * 0.7
        y_val = -0.2
        self._on_ground = Physics2D.check_on_ground(
            self.game_object, inner_player_width, y_val
        )

    def stomp(self):
        self._is_dead = True
        self._is_moving = False
        self._velocity = glm.fvec2(0.0)
        self._rigid_body.velocity = self._velocity
        self._rigid_body.angular_velocity = 0.0
        self._rigid_body.gravity_scale = 0.0
        self._state_machine.trigger("shellSpin")
        if AssetPool.get_sound("assets/sounds/bump.ogg").is_playing:
            AssetPool.get_sound("assets/sounds/bump.ogg").stop()
        AssetPool.get_sound("assets/sounds/bump.ogg").play()

    def pre_solve(self, colliding_object, contact, collision_normal):
        from components.player_controller import PlayerController

        goomba = colliding_object.get_component(GoombaAI)
        if self._is_dead and self._is_moving and goomba is not None:
            goomba.stomp()
            contact.enabled = False
            if AssetPool.get_sound("assets/sounds/kick.ogg").is_playing:
                AssetPool.get_sound("assets/sounds/kick.ogg").stop()
            AssetPool.get_sound("assets/sounds/kick.ogg").play()

        player_controller = colliding_object.get_component(PlayerController)
        if player_controller is not None:
            if (
                not self._is_dead
                and not player_controller.is_dead()
                and not player_controller.is_hurt_invincible()
                and collision_normal[1] > 0.58
            ):
                player_controller.enemy_bounce()
                self.stomp()
                self._walk_speed *= 3.0
            elif (
                self._moving_debounce < 0.0
                and not player_controller.is_dead()
                and not player_controller.is_hurt_invincible()
                and (self._is_moving or not self._is_dead)
                and collision_normal[1] < 0.58
            ):
                player_controller.die()
                if not player_controller.is_dead():
                    contact.enabled = False
            elif (
                not player_controller.is_dead()
                and not player_controller.is_hurt_invincible()
            ):
                if self._is_dead and collision_normal[1] > 0.58:
                    player_controller.enemy_bounce()
                    self._is_moving = not self._is_moving
                    self._going_right = collision_normal[0] < 0.0
                elif self._is_dead and not self._is_moving:
                    self._is_moving = True
                    self._going_right = collision_normal[0] < 0.0
                    self._moving_debounce = 0.32
                elif not player_controller.is_dead() and player_controller.is_hurt_invincible():
                    contact.enabled = False
        elif abs(collision_normal[1]) < 0.1 and not colliding_object.is_dead():
            self._going_right = collision_normal[0] < 0.0
            if self._is_moving and self._is_dead:
                if AssetPool.get_sound("assets/sounds/bump.ogg").is_playing:
                    AssetPool.get_sound("assets/sounds/bump.ogg").stop()
                AssetPool.get_sound("assets/sounds/bump.ogg").play()

        if colliding_object.get_component(Fireball) is not None:
            self.stomp()
            colliding_object.get_component(Fireball).disappear()

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
        del state["_is_moving"]
        del state["_state_machine"]
        return state

    def __setstate__(self, state):
        state["_going_right"] = False
        state["_rigid_body"] = None
        state["_walk_speed"] = 0.6
        state["_velocity"] = glm.fvec2(0.0)
        state["_acceleration"] = glm.fvec2(0.0)
        state["_terminal_velocity"] = glm.fvec2(2.1, 3.1)
        state["_on_ground"] = False
        state["_is_dead"] = False
        state["_is_moving"] = False
        state["_state_machine"] = None
        self.__dict__.update(state)
