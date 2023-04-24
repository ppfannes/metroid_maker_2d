import sys
import glm
from components.component import Component
from components.player_controller import PlayerController


class GameCamera(Component):
    def __init__(self, game_camera):
        self._player = None
        self._game_camera = game_camera
        self._highest_x = sys.float_info.min
        self._underground_y_level = 0.0
        self._camera_buffer = 1.5
        self._player_buffer = 0.25

        self._sky_color = glm.fvec4(92.9 / 255.0, 148.0 / 255.0, 252.0 / 255.0, 1.0)
        self._underground_color = glm.fvec4(0.0, 0.0, 0.0, 1.0)

    def start(self):
        from metroid_maker.window import Window

        self._player = Window.get_scene().get_game_object_with_component(
            PlayerController
        )
        self._game_camera.clear_color = self._sky_color
        self._underground_y_level = (
            self._game_camera._position.y
            - self._game_camera.get_projection_size().y
            - self._camera_buffer
        )

    def update(self, dt):
        if (
            self._player is not None
            and not self._player.get_component(PlayerController).has_won()
        ):
            self._game_camera._position.x = max(
                self._player.transform.position.x - 2.5, self._highest_x
            )
            self._highest_x = max(self._highest_x, self._game_camera._position.x)

            if self._player.transform.position.y < -self._player_buffer:
                self._game_camera._position.y = self._underground_y_level
                self._game_camera.clear_color = self._underground_color
            elif self._player.transform.position.y >= 0.0:
                self._game_camera._position.y = 0.0
                self._game_camera.clear_color = self._sky_color
