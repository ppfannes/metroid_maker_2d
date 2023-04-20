import glm
from components.component import Component
from renderer.debug_draw import DebugDraw


class CircleCollider(Component):
    def __init__(self):
        super().__init__()
        self._radius = 1.0
        self._offset = glm.fvec2(0.0)

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value

    def editor_update(self, dt):
        center = glm.add(self.game_object.transform.position, self.offset)
        DebugDraw.add_circle(center, self._radius)
