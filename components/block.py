import glm
from abc import abstractmethod
from components.component import Component
from components.player_controller import PlayerController
from utils.asset_pool import AssetPool


class Block(Component):
    def __init__(self):
        super().__init__()
        self._bop_going_up = True
        self._do_bop_animation = False
        self._bop_start = glm.fvec2(0.0)
        self._top_bop_location = glm.fvec2(0.0)
        self._active = True

        self.bop_speed = 0.4

    def start(self):
        self._bop_start = glm.fvec2(self.game_object.transform.position)
        self._top_bop_location = glm.add(self._bop_start, glm.fvec2(0.0, 0.02))

    def update(self, dt):
        if self._do_bop_animation:
            if self._bop_going_up:
                if self.game_object.transform.position.y < self._top_bop_location.y:
                    self.game_object.transform.position.y += self.bop_speed * dt
                else:
                    self._bop_going_up = False
            else:
                if self.game_object.transform.position.y > self._bop_start.y:
                    self.game_object.transform.position.y -= self.bop_speed * dt
                else:
                    self.game_object.transform.position.y = self._bop_start.y
                    self._bop_going_up = True
                    self._do_bop_animation = False

    def begin_collision(self, colliding_object, contact, collision_normal):
        player_controller = colliding_object.get_component(PlayerController)
        if (
            self._active
            and player_controller is not None
            and collision_normal[1] < -0.8
        ):
            self._do_bop_animation = True
            if AssetPool.get_sound("assets/sounds/bump.ogg").is_playing:
                AssetPool.get_sound("assets/sounds/bump.ogg").stop()
            AssetPool.get_sound("assets/sounds/bump.ogg").play()
            self.player_hit(player_controller)

    @abstractmethod
    def player_hit(self, player_controller):
        raise NotImplementedError

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value