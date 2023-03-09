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
            if isinstance(field, bool):
                changed, value = imgui.checkbox(name + ": ", field)

                if changed:
                    setattr(self, name, value)

                continue

            if isinstance(field, int):
                changed, value = imgui.drag_int(name + ": ", field, min_value=-100, max_value=100)

                if changed:
                    setattr(self, name, value)

                continue

            if isinstance(field, float):
                changed, value = imgui.drag_float(name + ": ", field, min_value=-100.0, max_value=100.0)

                if changed:
                    setattr(self, name, value)

                continue

            if isinstance(field, glm.fvec2):
                changed, value = imgui.drag_float2(name + ": ", field.x, field.y, min_value=-100.0, max_value=100.0)

                if changed:
                    vec_value = glm.fvec2(*value)
                    setattr(self, name, vec_value)

                continue

            if isinstance(field, glm.fvec3):
                changed, value = imgui.drag_float3(name + ": ", field.x, field.y, field.z, min_value=-100.0, max_value=100.0)

                if changed:
                    vec_value = glm.fvec3(*value)
                    setattr(self, name, vec_value)

                continue

            if isinstance(field, glm.fvec4):
                changed, value = imgui.drag_float4(name + ": ", field.x, field.y, field.z, field.w, min_value=-100.0, max_value=100.0)

                if changed:
                    vec_value = glm.fvec4(*value)
                    setattr(self, name, vec_value)

                continue

    def exposed_fields(self):
        fields = self.__dict__.copy()
        del fields["_uid"]
        return fields

    def get_uid(self):
        return self._uid

    def generate_id(self):
        if self._uid == -1:
            self._uid = Component._ID_COUNTER
            Component._ID_COUNTER += 1

    @classmethod
    def init(cls, max_id):
        cls._ID_COUNTER = max_id
