from abc import ABC
from enum import Enum
import imgui
import glm
from editor.mimgui import MImGui


class Component(ABC):
    _ID_COUNTER = 0

    def __init__(self):
        self._uid = -1
        self.game_object = None

    def editor_update(self, dt):
        pass

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
                value = MImGui.drag_int(name + ": ", field)
                setattr(self, name, value)

                continue

            if isinstance(field, float):
                value = MImGui.drag_float(name, field)
                setattr(self, name, value)

                continue

            if isinstance(field, glm.fvec2):
                value = MImGui.draw_vec2_control(name, field)
                setattr(self, name, value)

                continue

            if isinstance(field, glm.fvec3):
                value = MImGui.draw_vec3_control(name, field)
                setattr(self, name, value)

                continue

            if isinstance(field, glm.fvec4):
                changed, value = imgui.drag_float4(
                    name + ": ",
                    field.x,
                    field.y,
                    field.z,
                    field.w,
                    min_value=-100.0,
                    max_value=100.0,
                )

                if changed:
                    vec_value = glm.fvec4(*value)
                    setattr(self, name, vec_value)

                continue

            if isinstance(field, Enum):
                value_names = field.__class__._member_names_
                changed, current = imgui.combo(
                    name + ": ", value_names.index(field.name), value_names
                )

                if changed:
                    new_value = field.__class__._member_map_[value_names[current]]
                    setattr(self, name, new_value)

                continue

    def exposed_fields(self):
        fields = self.__dict__.copy()
        del fields["_uid"]
        return fields

    def get_uid(self):
        return self._uid

    def generate_id(self):
        self._uid = Component._ID_COUNTER
        Component._ID_COUNTER += 1

    def destroy(self):
        pass

    @classmethod
    def init(cls, max_id):
        cls._ID_COUNTER = max_id

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["game_object"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.game_object = None
