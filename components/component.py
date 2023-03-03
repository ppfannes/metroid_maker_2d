from abc import ABC
import imgui
import glm

class Component(ABC):

    _ID_COUNTER = 0

    def __init__(self):
        self._uid = -1
        self.game_object = None

    def update(self, dt: float):
        pass

    def start(self):
        pass

    def imgui(self):
        fields = self.exposed_fields()

        for name, field in fields.items():
            if isinstance(field, int):
                changed, value = imgui.drag_int(name + ": ", field, min_value=-5, max_value=5)

                if changed:
                    setattr(self, name, value)

            if isinstance(field, float):
                changed, value = imgui.drag_float(name + ": ", field, min_value=-5.0, max_value=5.0)

                if changed:
                    setattr(self, name, value)

            if isinstance(field, glm.fvec3):
                changed, value = imgui.drag_float3(name + ": ", field.x, field.y, field.z, min_value=-5.0, max_value=5.0)

                if changed:
                    vec_value = glm.fvec3(*value)
                    setattr(self, name, vec_value)

    def exposed_fields(self):
        return self.__dict__

    def get_uid(self):
        return self._uid

    def generate_id(self):
        if self._uid == -1:
            self._uid = Component._ID_COUNTER
            Component._ID_COUNTER += 1

    @classmethod
    def init(cls, max_id):
        cls._ID_COUNTER = max_id
