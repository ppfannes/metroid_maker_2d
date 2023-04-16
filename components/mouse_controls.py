import glm
from glfw.GLFW import GLFW_MOUSE_BUTTON_LEFT, GLFW_KEY_ESCAPE

from components.component import Component
from components.non_pickable import NonPickable
from components.state_machine import StateMachine
from renderer.debug_draw import DebugDraw
from utils.mouse_listener import MouseListener
from utils.key_listener import KeyListener
from utils.settings import GRID_WIDTH, GRID_HEIGHT


class MouseControls(Component):
    def __init__(self) -> None:
        super().__init__()
        self._holding_object = None
        self._debounce_time = 0.2
        self._debounce = self._debounce_time
        self._box_select_set = False
        self._box_select_start = glm.fvec2()
        self._box_select_end = glm.fvec2()

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

        if new_game_object.get_component(StateMachine) is not None:
            new_game_object.get_component(StateMachine).refresh_textures()

        new_game_object.get_component(SpriteRenderer).set_color(
            glm.fvec4(1.0, 1.0, 1.0, 1.0)
        )
        new_game_object.remove_component(NonPickable)
        Window.get_scene().add_game_object_to_scene(new_game_object)

    def editor_update(self, dt):
        from metroid_maker.window import Window

        self._debounce -= dt
        picking_texture = (
            Window.get_imgui_layer().get_properties_window().get_picking_texture()
        )
        current_scene = Window.get_scene()

        if self._holding_object is not None:
            x = MouseListener.get_world_x()
            y = MouseListener.get_world_y()

            self._holding_object.transform.position.x = (
                int((x // GRID_WIDTH)) * GRID_WIDTH
            ) + GRID_WIDTH / 2.0
            self._holding_object.transform.position.y = (
                int((y // GRID_HEIGHT)) * GRID_HEIGHT
            ) + GRID_HEIGHT / 2.0

            if MouseListener.mouse_button_down(GLFW_MOUSE_BUTTON_LEFT):
                half_width = GRID_WIDTH / 2.0
                half_height = GRID_HEIGHT / 2.0

                if MouseListener.get_is_dragging() and not self._block_in_square(
                    self._holding_object.transform.position.x - half_width,
                    self._holding_object.transform.position.y - half_height,
                ):
                    self.place()
                elif (
                    not MouseListener.get_is_dragging()
                    and not self._block_in_square(
                        self._holding_object.transform.position.x - half_width,
                        self._holding_object.transform.position.y - half_height,
                    )
                    and self._debounce < 0
                ):
                    self.place()
                    self._debounce = self._debounce_time

            if KeyListener.is_key_pressed(GLFW_KEY_ESCAPE):
                self._holding_object.destroy()
                self._holding_object = None

        elif (
            not MouseListener.get_is_dragging()
            and MouseListener.mouse_button_down(GLFW_MOUSE_BUTTON_LEFT)
            and self._debounce < 0
        ):
            x = MouseListener.get_screen_x()
            y = MouseListener.get_screen_y()
            game_object_id = picking_texture.read_pixel(x, y)
            picked_object = current_scene.get_game_object(game_object_id)
            if (
                picked_object is not None
                and picked_object.get_component(NonPickable) is None
            ):
                Window.get_imgui_layer().get_properties_window().set_active_game_object(
                    picked_object
                )
            elif picked_object is None and not MouseListener.get_is_dragging():
                Window.get_imgui_layer().get_properties_window().clear_selected()
            self._debounce = 0.2

        elif MouseListener.get_is_dragging() and MouseListener.mouse_button_down(
            GLFW_MOUSE_BUTTON_LEFT
        ):
            if not self._box_select_set:
                Window.get_imgui_layer().get_properties_window().clear_selected()
                self._box_select_start = MouseListener.get_screen()
                self._box_select_set = True

            self._box_select_end = MouseListener.get_screen()
            box_select_start_world = MouseListener.screen_to_world(
                self._box_select_start
            )
            box_select_end_world = MouseListener.screen_to_world(self._box_select_end)
            half_size = glm.mul(
                glm.sub(box_select_end_world, box_select_start_world), 0.5
            )
            DebugDraw.add_box_2d(
                glm.add(box_select_start_world, half_size), glm.mul(half_size, 2.0), 0.0
            )

        elif self._box_select_set:
            self._box_select_set = False
            screen_start_x, screen_start_y = int(self._box_select_start.x), int(
                self._box_select_start.y
            )
            screen_end_x, screen_end_y = int(self._box_select_end.x), int(
                self._box_select_end.y
            )
            self._box_select_start = glm.fvec2(0.0)
            self._box_select_end = glm.fvec2(0.0)

            if screen_end_x < screen_start_x:
                screen_end_x, screen_start_x = screen_start_x, screen_end_x

            if screen_end_y < screen_start_y:
                screen_end_y, screen_start_y = screen_start_y, screen_end_y

            game_object_ids = picking_texture.read_pixels(
                glm.ivec2(screen_start_x, screen_start_y),
                glm.ivec2(screen_end_x, screen_end_y),
            )

            for object_id in game_object_ids:
                picked_obj = Window.get_scene().get_game_object(object_id)
                if (
                    picked_obj is not None
                    and picked_obj.get_component(NonPickable) is None
                ):
                    Window.get_imgui_layer().get_properties_window().add_active_game_object(
                        picked_obj
                    )

    def _block_in_square(self, x, y):
        from metroid_maker.window import Window

        properties_window = Window.get_imgui_layer().get_properties_window()
        start = glm.fvec2(x, y)
        end = glm.add(start, glm.fvec2(GRID_WIDTH, GRID_HEIGHT))
        start_screenf = MouseListener.world_to_screen(start)
        end_screenf = MouseListener.world_to_screen(end)
        start_screen = glm.ivec2(int(start_screenf.x + 2), int(start_screenf.y + 2))
        end_screen = glm.ivec2(int(end_screenf.x - 2), int(end_screenf.y - 2))
        game_object_ids = properties_window.get_picking_texture().read_pixels(
            start_screen, end_screen
        )

        for game_object_id in game_object_ids:
            if game_object_id >= 0:
                picked_obj = Window.get_scene().get_game_object(game_object_id)
                if picked_obj.get_component(NonPickable) is None:
                    return True

        return False
