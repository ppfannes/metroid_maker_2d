import glm
from components.component import Component
from components.player_controller import PlayerController
from physics2d.components.rigid_body_2d import RigidBody2D
from utils.asset_pool import AssetPool


class MushroomAI(Component):
    def __init__(self):
        super().__init__()
        self._going_right = True
        self._rigid_body = None
        self._speed = glm.fvec2(1.0, 0.0)
        self._max_speed = 0.8
        self._hit_player = False

    def start(self):
        self._rigid_body = self.game_object.get_component(RigidBody2D)
        if AssetPool.get_sound("assets/sounds/powerup_appears.ogg").is_playing:
            AssetPool.get_sound("assets/sounds/powerup_appears.ogg").play()
        AssetPool.get_sound("assets/sounds/powerup_appears.ogg").play()

    def update(self, dt):
        if self._going_right and abs(self._rigid_body.velocity.x) < self._max_speed:
            self._rigid_body.apply_force(self._speed)
        elif (
            not self._going_right and abs(self._rigid_body.velocity.x) < self._max_speed
        ):
            self._rigid_body.apply_force(glm.fvec2(-self._speed.x, self._speed.y))

    def pre_solve(self, colliding_object, contact, collision_normal):
        player_controller = colliding_object.get_component(PlayerController)
        if player_controller is not None:
            contact.enabled = False
            if not self._hit_player:
                player_controller.powerup()
                self.game_object.destroy()
                self._hit_player = True

        if abs(collision_normal[1] < 0.1):
            self._going_right = collision_normal[0] < 0
