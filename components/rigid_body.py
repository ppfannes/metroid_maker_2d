import glm
from metroid_maker.component import Component

class RigidBody(Component):

    def __init__(self):
        super().__init__()
        self._collider_type = 0
        self._friction = 0.8
        self.velocity = glm.vec3(0.0, 0.5, 0.0)
        self._tmp = glm.vec4(0.0, 0.0, 0.0, 0.0)

    def imgui(self):
        super().imgui()

    def exposed_fields(self):
        exposed_fields = self.__dict__.copy()
        del exposed_fields["_tmp"]
        return exposed_fields
