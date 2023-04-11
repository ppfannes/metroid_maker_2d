import glm
from glfw.GLFW import GLFW_MOUSE_BUTTON_LEFT, GLFW_KEY_ESCAPE

from components.component import Component
from components.non_pickable import NonPickable
from components.state_machine import StateMachine
from utils.mouse_listener import MouseListener
from utils.key_listener import KeyListener
from utils.settings import GRID_WIDTH, GRID_HEIGHT


class MouseControls(Component):
    def __init__(self) -> None:
        super().__init__()
        self._holding_object = None
        self._debounce_time = 0.05
        self._debounce = self._debounce_time

    def pickup_object(self, game_object):
        from metroid_maker.window import Window
        from components.sprite_renderer import SpriteRenderer

        if self._holding_object is not None:
            self._holding_object.destroy()

        self._holding_object = game_object
        self._holding_object.get_component(SpriteRenderer).set_color(
            glm.fvec4(0.8, 0.8, 0.8, 0.5)
        )
        self._holding_object.add_component(NonPickable())
        Window.get_scene().add_game_object_to_scene(game_object)

    def place(self):
        from metroid_maker.window import Window
        from components.sprite_renderer import SpriteRenderer

        new_game_object = self._holding_object.copy()

        if new_game_object.get_component(StateMachine):
            new_game_object.get_component(StateMachine).refresh_textures()

        new_game_object.get_component(SpriteRenderer).set_color(
            glm.fvec4(1.0, 1.0, 1.0, 1.0)
        )
        new_game_object.remove_component(NonPickable)
        Window.get_scene().add_game_object_to_scene(new_game_object)

    def editor_update(self, dt):
        self._debounce -= dt
        if self._holding_object is not None and self._debounce <= 0.0:
            self._holding_object.transform.position = MouseListener.get_world()

            self._holding_object.transform.position = glm.fvec2(
                (
                    int((self._holding_object.transform.position.x // GRID_WIDTH))
                    * GRID_WIDTH
                )
                + GRID_WIDTH / 2.0,
                (
                    int((self._holding_object.transform.position.y // GRID_HEIGHT))
                    * GRID_HEIGHT
                )
                + GRID_HEIGHT / 2.0,
            )

            if MouseListener.mouse_button_down(GLFW_MOUSE_BUTTON_LEFT):
                self.place()
                self._debounce = self._debounce_time

            if KeyListener.is_key_pressed(GLFW_KEY_ESCAPE):
                self._holding_object.destroy()
                self._holding_object = None
