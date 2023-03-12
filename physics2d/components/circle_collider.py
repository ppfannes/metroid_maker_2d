from components.component import Component

class CircleCollider(Component):

    def __init__(self):
        super().__init__()
        self._radius = 1.0

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
