import glm
from components.component import Component
from editor.mimgui import MImGui


class Transform(Component):
    def __init__(self, position=glm.fvec2(), scale=glm.fvec2()):
        super().__init__()
        self.position = position
        self.scale = scale
        self.rotation = 0.0
        self.z_index = 0

    def copy(self):
        return Transform(glm.fvec2(self.position), glm.fvec2(self.scale))

    def imgui(self):
        self.game_object.name = MImGui.input_text("Name: ", self.game_object.name)
        MImGui.draw_vec2_control("Position", self.position)
        MImGui.draw_vec2_control("Scale", self.scale)
        self.rotation = MImGui.drag_float("Rotation", self.rotation)
        self.z_index = MImGui.drag_int("Z-Index", self.z_index)

    def copy_to(self, transform: "Transform"):
        transform.position.xy = self.position.xy
        transform.scale.xy = self.scale.xy

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Transform):
            return (
                self.position == other.position
                and self.scale == other.scale
                and self.rotation == other.rotation
                and self.z_index == other.z_index
            )
        return NotImplementedError
