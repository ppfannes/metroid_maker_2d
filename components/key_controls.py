import copy
import glfw
import glm
from components.component import Component
from components.sprite_renderer import SpriteRenderer
from utils.settings import GRID_WIDTH


class KeyControls(Component):
    def editor_update(self, dt):
        from metroid_maker.window import Window
        from utils.asset_pool import AssetPool
        from utils.key_listener import KeyListener

        properties_window = Window.get_imgui_layer().get_properties_window()
        active_game_object = properties_window.get_active_game_object()
        active_game_objects = properties_window.get_active_game_objects()

        if (
            KeyListener.is_key_pressed(glfw.KEY_LEFT_CONTROL)
            and KeyListener.key_begin_press(glfw.KEY_D)
            and active_game_object is not None
        ):
            new_object = copy.deepcopy(active_game_object)

            new_object.generate_uid()
            for component in new_object.get_all_components():
                component.generate_id()
            sprite_renderer = new_object.get_component(SpriteRenderer)
            if (
                sprite_renderer is not None
                and sprite_renderer.get_texture() is not None
            ):
                sprite_renderer.set_texture(
                    AssetPool.get_texture(sprite_renderer.get_texture().get_file_path())
                )

            Window.get_scene().add_game_object_to_scene(new_object)
            new_object.transform.position = glm.add(
                new_object.transform.position, glm.fvec2(GRID_WIDTH, 0.0)
            )
            properties_window.set_active_game_object(new_object)
        elif (
            KeyListener.is_key_pressed(glfw.KEY_LEFT_CONTROL)
            and KeyListener.key_begin_press(glfw.KEY_D)
            and len(active_game_objects) > 1
        ):
            game_objects = copy.copy(active_game_objects)
            properties_window.clear_selected()
            for game_object in game_objects:
                game_object_copy = copy.deepcopy(game_object)
                Window.get_scene().add_game_object_to_scene(game_object_copy)
                properties_window.add_active_game_object(game_object_copy)
        elif KeyListener.is_key_pressed(glfw.KEY_DELETE):
            for game_object in active_game_objects:
                game_object.destroy()
            properties_window.clear_selected()
