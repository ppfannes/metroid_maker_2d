import glm
from components.component import Component

class Collider(Component):

    def __init__(self) -> None:
        super().__init__()
        self._offset = glm.fvec2()

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
