import imgui
from glfw.GLFW import GLFW_MOUSE_BUTTON_LEFT
from components.non_pickable import NonPickable
from utils.mouse_listener import MouseListener

class PropertiesWindow:

    def __init__(self, picking_texture):
        self._active_game_object = None
        self._picking_texture = picking_texture
        self._debounce = 0.2

    def update(self, dt, current_scene):
        self._debounce -= dt
        if MouseListener.mouse_button_down(GLFW_MOUSE_BUTTON_LEFT) and self._debounce < 0:
            x = MouseListener.get_screen_x()
            y = MouseListener.get_screen_y()
            game_object_id = self._picking_texture.read_pixel(x, y)
            picked_object = current_scene.get_game_object(game_object_id)
            if picked_object is not None and picked_object.get_component(NonPickable) is None:
                self._active_game_object = picked_object
            elif picked_object is None and not MouseListener.get_is_dragging():
                self._active_game_object = None
            self._debounce = 0.2

    def imgui(self):
        if self._active_game_object is not None:
            imgui.begin("Properties")
            self._active_game_object.imgui()
            imgui.end()

    def get_active_game_object(self):
        return self._active_game_object
