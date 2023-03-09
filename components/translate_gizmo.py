import glm
from components.component import Component
from components.sprite_renderer import SpriteRenderer
from metroid_maker.prefabs import Prefabs

class TranslateGizmo(Component):

    def __init__(self, arrow_sprite, properties_window):
        from metroid_maker.window import Window
        super().__init__()
        self._x_axis_color = glm.fvec4(1.0, 0.0, 0.0, 1.0)
        self._x_axis_color_hover = glm.fvec4()
        self._y_axis_color = glm.fvec4(0.0, 1.0, 0.0, 1.0)
        self._y_axis_color_hover = glm.fvec4()

        self._x_axis_game_object = Prefabs.generate_sprite_object(arrow_sprite, 16.0, 48.0)
        self._y_axis_game_object = Prefabs.generate_sprite_object(arrow_sprite, 16.0, 48.0)
        self._x_axis_sprite = self._x_axis_game_object.get_component(SpriteRenderer)
        self._y_axis_sprite = self._y_axis_game_object.get_component(SpriteRenderer)
        self._active_game_object = None
        self._properties_window = properties_window

        Window.get_scene().add_game_object_to_scene(self._x_axis_game_object)
        Window.get_scene().add_game_object_to_scene(self._y_axis_game_object)

    def start(self):
        self._x_axis_game_object.transform.rotation = 90.0

    def update(self, dt):
        if self._active_game_object is not None:
            self._x_axis_game_object.transform.position = self._active_game_object.transform.position
            self._y_axis_game_object.transform.position = self._active_game_object.transform.position

        self._active_game_object = self._properties_window.get_active_game_object()

        if self._active_game_object is not None:
            self.set_active()
        else:
            self.set_inactive()

    def set_active(self):
        self._x_axis_sprite.set_color(self._x_axis_color)
        self._y_axis_sprite.set_color(self._y_axis_color)

    def set_inactive(self):
        self._active_game_object = None
        self._x_axis_sprite.set_color(glm.fvec4(0.0, 0.0, 0.0, 0.0))
        self._y_axis_sprite.set_color(glm.fvec4(0.0, 0.0, 0.0, 0.0))
