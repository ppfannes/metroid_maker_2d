import glm
from components.component import Component
from renderer.debug_draw import DebugDraw


class Box2DCollider(Component):
    def __init__(self):
        super().__init__()
        self._half_size = glm.fvec2(1.0, 1.0)
        self._origin = glm.fvec2()
        self._offset = glm.fvec2()

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value

    @property
    def half_size(self):
        return self._half_size

    @half_size.setter
    def half_size(self, value):
        self._half_size = value

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value

    def editor_update(self, dt):
        center = glm.add(glm.fvec2(self.game_object.transform.position), self.offset)
        DebugDraw.add_box_2d(
            center, self._half_size, self.game_object.transform.rotation
        )
