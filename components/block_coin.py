import glm
from math import fmod
from components.component import Component
from utils.asset_pool import AssetPool


class BlockCoin(Component):
    def __init__(self):
        super().__init__()
        self._top_y = glm.fvec2(0.0)
        self._coin_speed = 1.0

    def start(self):
        self._top_y = glm.add(
            glm.fvec2(self.game_object.transform.position.y), glm.fvec2(0.0, 0.5)
        )
        if AssetPool.get_sound("assets/sounds/coin.ogg").is_playing:
            AssetPool.get_sound("assets/sounds/coin.ogg").stop()
        AssetPool.get_sound("assets/sounds/coin.ogg").play()

    def update(self, dt):
        if self.game_object.transform.position.y < self._top_y.y:
            self.game_object.transform.position.y += self._coin_speed * dt
            self.game_object.transform.scale.x -= fmod(0.5 * dt, -1.0)
        else:
            self.game_object.destroy()
