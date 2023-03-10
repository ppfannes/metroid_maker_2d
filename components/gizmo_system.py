import glfw
from components.component import Component
from components.scale_gizmo import ScaleGizmo
from components.translate_gizmo import TranslateGizmo
from utils.key_listener import KeyListener

class GizmoSystem(Component):

    def __init__(self, gizmos_sprite_sheet):
        super().__init__()
        self._gizmos = gizmos_sprite_sheet
        self._using_gizmo = 0

    def start(self):
        from metroid_maker.window import Window
        self.game_object.add_component(TranslateGizmo(self._gizmos.get_sprite(1), Window.get_imgui_layer().get_properties_window()))
        self.game_object.add_component(ScaleGizmo(self._gizmos.get_sprite(2), Window.get_imgui_layer().get_properties_window()))

    def update(self, dt):
        if self._using_gizmo == 0:
            self.game_object.get_component(TranslateGizmo).set_using()
            self.game_object.get_component(ScaleGizmo).set_not_using()
        elif self._using_gizmo == 1:
            self.game_object.get_component(TranslateGizmo).set_not_using()
            self.game_object.get_component(ScaleGizmo).set_using()

        if KeyListener.is_key_pressed(glfw.KEY_E):
            self._using_gizmo = 0
        elif KeyListener.is_key_pressed(glfw.KEY_R):
            self._using_gizmo = 1
