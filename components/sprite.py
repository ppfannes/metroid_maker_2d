import glm


class Sprite:
    def __init__(self, sprite_width=0, sprite_height=0, texture=None, tex_coords=None):
        self._texture = texture
        self._tex_coords = (
            tex_coords
            if tex_coords is not None
            else [
                glm.fvec2(1.0, 1.0),
                glm.fvec2(1.0, 0.0),
                glm.fvec2(0.0, 0.0),
                glm.fvec2(0.0, 1.0),
            ]
        )
        self._width = sprite_width
        self._height = sprite_height

    def get_texture(self):
        return self._texture

    def set_texture(self, texture):
        self._texture = texture

    def get_tex_coords(self):
        return self._tex_coords

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_tex_id(self):
        if self._texture is not None:
            return self._texture.get_id()
        return -1
