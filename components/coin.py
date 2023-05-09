import glm
from math import fmod
from components.component import Component
from utils.asset_pool import AssetPool


class Coin(Component):
    def __init__(self):
        self._top_y = glm.fvec2(0.0)
        self._coin_speed = 1.4
        self._play_animation = False

    def start(self):
        self._top_y = glm.add(glm.fvec2(self.game_object.transform.position.y), 0.5)

    def update(self, dt):
        if self._play_animation:
            if self.game_object.transform.position.y < self._top_y.y:
                self.game_object.transform.position.y += self._coin_speed * dt
                self.game_object.transform.scale.x -= fmod(0.5 * dt, -1.0)
            else:
                self.game_object.destroy()

    def pre_solve(self, colliding_object, contact, collision_normal):
        from components.player_controller import PlayerController

        if colliding_object.get_component(PlayerController) is not None:
            if AssetPool.get_sound("assets/sounds/coin.ogg").is_playing:
                AssetPool.get_sound("assets/sounds/coin.ogg").stop()
            AssetPool.get_sound("assets/sounds/coin.ogg").play()
            self._play_animation = True
            contact.enabled = False

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_play_animation"]
        return state

    def __setstate__(self, state):
        state["_play_animation"] = False
        self.__dict__.update(state)
