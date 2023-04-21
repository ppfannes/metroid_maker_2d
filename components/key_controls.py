import copy
import glfw
import glm
from components.component import Component
from components.state_machine import StateMachine
from utils.settings import GRID_WIDTH


class KeyControls(Component):
    def editor_update(self, dt):
        from metroid_maker.window import Window
        from utils.key_listener import KeyListener

        properties_window = Window.get_imgui_layer().get_properties_window()
        active_game_object = properties_window.get_active_game_object()
        active_game_objects = properties_window.get_active_game_objects()

        if (
            KeyListener.is_key_pressed(glfw.KEY_LEFT_CONTROL)
            and KeyListener.key_begin_press(glfw.KEY_D)
            and active_game_object is not None
        ):
            new_object = active_game_object.copy()
            Window.get_scene().add_game_object_to_scene(new_object)
            new_object.transform.position = glm.add(
                new_object.transform.position, glm.fvec2(GRID_WIDTH, 0.0)
            )
            properties_window.set_active_game_object(new_object)
            if new_object.get_component(StateMachine) is not None:
                new_object.get_component(StateMachine).refresh_textures()
        elif (
            KeyListener.is_key_pressed(glfw.KEY_LEFT_CONTROL)
            and KeyListener.key_begin_press(glfw.KEY_D)
            and len(active_game_objects) > 1
        ):
            game_objects = copy.copy(active_game_objects)
            properties_window.clear_selected()
            for game_object in game_objects:
                game_object_copy = game_object.copy()
                Window.get_scene().add_game_object_to_scene(game_object_copy)
                properties_window.add_active_game_object(game_object_copy)
                if game_object_copy.get_component(StateMachine) is not None:
                    game_object_copy.get_component(StateMachine).refresh_textures()
        elif KeyListener.is_key_pressed(glfw.KEY_DELETE):
            for game_object in active_game_objects:
                game_object.destroy()
            properties_window.clear_selected()
