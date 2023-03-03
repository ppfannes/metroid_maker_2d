from glfw.GLFW import GLFW_MOUSE_BUTTON_LEFT

from components.component import Component
from utils.mouse_listener import MouseListener


class MouseControls(Component):

    def __init__(self) -> None:
        super().__init__()
        self._holding_object = None

    def pickup_object(self, game_object):
        from metroid_maker.window import Window
        self._holding_object = game_object
        Window.get_scene().add_game_object_to_scene(game_object)

    def place(self):
        self._holding_object = None

    def update(self, dt):
        if self._holding_object is not None:
            self._holding_object.transform.position.x = MouseListener.get_ortho_x() - 32
            self._holding_object.transform.position.y = MouseListener.get_ortho_y() - 32

            if MouseListener.mouse_button_down(GLFW_MOUSE_BUTTON_LEFT):
                self.place()
