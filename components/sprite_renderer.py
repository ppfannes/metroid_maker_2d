import glm
import imgui
from components.sprite import Sprite
from components.component import Component

class SpriteRenderer(Component):

    def __init__(self, color=glm.fvec4(1.0, 1.0, 1.0, 1.0), sprite=Sprite()):
        super().__init__()
        self._color = color
        self._sprite = sprite
        self._last_transform = None
        self._is_dirty = True

    def start(self):
        self._last_transform = self.game_object.transform.copy()

    def update(self, dt: float):
        if not self._last_transform == self.game_object.transform:
            self.game_object.transform.copy_to(self._last_transform)
            self._is_dirty = True

    def imgui(self):
        current_color = (self._color.x, self._color.y, self._color.z, self._color.w)
        changed, color = imgui.color_edit4("Color Picker: ", *current_color)
            
        if changed:
            self._color = glm.fvec4(*color)
            self._is_dirty = True

    def get_color(self):
        return self._color

    def get_texture(self):
        return self._sprite.get_texture()

    def get_tex_coords(self):
        return self._sprite.get_tex_coords()

    def set_sprite(self, sprite):
        self._sprite = sprite
        self._is_dirty = True

    def set_color(self, color):
        if self._color != color:
            self._is_dirty = True
            self._color.xyzw = color.xyzw

    def is_dirty(self):
        return self._is_dirty

    def set_clean(self):
        self._is_dirty = False

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_is_dirty']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._is_dirty = True