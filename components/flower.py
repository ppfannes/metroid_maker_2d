from components.component import Component
from physics2d.components.rigid_body_2d import RigidBody2D
from utils.asset_pool import AssetPool


class Flower(Component):
    def __init__(self):
        super().__init__()
        self._rigid_body = None

    def start(self):
        self._rigid_body = self.game_object.get_component(RigidBody2D)
        if AssetPool.get_sound("assets/sounds/powerup_appears.ogg").is_playing:
            AssetPool.get_sound("assets/sounds/powerup_appears.ogg").stop()
        AssetPool.get_sound("assets/sounds/powerup_appears.ogg").play()
        self._rigid_body.is_sensor = True

    def begin_collision(self, colliding_object, contact, collision_normal):
        from components.player_controller import PlayerController

        player_controller = colliding_object.get_component(PlayerController)
        if player_controller is not None:
            player_controller.powerup()
            self.game_object.destroy()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_rigid_body"]
        return state

    def __setstate__(self, state):
        state["_rigid_body"] = None
        self.__dict__.update(state)
