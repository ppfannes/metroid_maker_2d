import glm
from glfw.GLFW import GLFW_MOUSE_BUTTON_LEFT

from components.component import Component
from utils.mouse_listener import MouseListener
from utils.settings import GRID_WIDTH, GRID_HEIGHT


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

    def editor_update(self, dt):
        if self._holding_object is not None:
            self._holding_object.transform.position = glm.fvec2(MouseListener.get_ortho_x(),
                                                                MouseListener.get_ortho_y())

            self._holding_object.transform.position = glm.fvec2(int((self._holding_object.transform.position.x // GRID_WIDTH) * GRID_WIDTH),
                                                                int((self._holding_object.transform.position.y // GRID_HEIGHT) * GRID_HEIGHT))

            if MouseListener.mouse_button_down(GLFW_MOUSE_BUTTON_LEFT):
                self.place()
