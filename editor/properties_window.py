import imgui
from glfw.GLFW import GLFW_MOUSE_BUTTON_LEFT
from utils.mouse_listener import MouseListener

class PropertiesWindow():

    def __init__(self, picking_texture):
        self._active_game_object = None
        self._picking_texture = picking_texture

    def update(self, dt, current_scene):
        if MouseListener.mouse_button_down(GLFW_MOUSE_BUTTON_LEFT):
            x = MouseListener.get_screen_x()
            y = MouseListener.get_screen_y()
            game_object_id = self._picking_texture.read_pixel(x, y)
            self._active_game_object = current_scene.get_game_object(game_object_id)

    def imgui(self):
        if self._active_game_object is not None:
            imgui.begin("Properties")
            self._active_game_object.imgui()
            imgui.end()

    def get_active_game_object(self):
        return self._active_game_object
