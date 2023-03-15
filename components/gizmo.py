import copy
import glfw
import glm
from components.component import Component
from components.non_pickable import NonPickable
from components.sprite_renderer import SpriteRenderer
from metroid_maker.prefabs import Prefabs

class Gizmo(Component):

    def __init__(self, arrow_sprite, properties_window):
        from metroid_maker.window import Window
        super().__init__()
        self._using = False
        self._x_axis_color = glm.fvec4(1.0, 0.3, 0.3, 1.0)
        self._x_axis_color_hover = glm.fvec4(1.0, 0.0, 0.0, 1.0)
        self._y_axis_color = glm.fvec4(0.3, 1.0, 0.3, 1.0)
        self._y_axis_color_hover = glm.fvec4(0.0, 1.0, 0.0, 1.0)

        self._gizmo_width = 16 / 80.0
        self._gizmo_height = 48 / 80.0
        self._x_axis_game_object = Prefabs.generate_sprite_object(arrow_sprite, self._gizmo_width, self._gizmo_height)
        self._y_axis_game_object = Prefabs.generate_sprite_object(arrow_sprite, self._gizmo_width, self._gizmo_height)
        self._x_axis_game_object.add_component(NonPickable())
        self._y_axis_game_object.add_component(NonPickable())
        self._x_axis_sprite = self._x_axis_game_object.get_component(SpriteRenderer)
        self._y_axis_sprite = self._y_axis_game_object.get_component(SpriteRenderer)
        self._x_axis_offset = glm.fvec2(32.0 / 80.0, 0.0)
        self._y_axis_offset = glm.fvec2(0.0, 32.0 / 80.0)
        self._active_game_object = None
        self._x_axis_active = False
        self._y_axis_active = False
        self._properties_window = properties_window

        Window.get_scene().add_game_object_to_scene(self._x_axis_game_object)
        Window.get_scene().add_game_object_to_scene(self._y_axis_game_object)

    def start(self):
        self._x_axis_game_object.transform.rotation = 90.0
        self._y_axis_game_object.transform.rotation = 180.0
        self._x_axis_game_object.transform.z_index = 100
        self._y_axis_game_object.transform.z_index = 100
        self._x_axis_game_object.set_no_serialize()
        self._y_axis_game_object.set_no_serialize()

    def update(self, dt):
        if self._using:
            self.set_inactive()

    def editor_update(self, dt):
        if not self._using:
            return
        from metroid_maker.window import Window
        from utils.mouse_listener import MouseListener
        from utils.key_listener import KeyListener
        from utils.asset_pool import AssetPool
        self._active_game_object = self._properties_window.get_active_game_object()
        if self._active_game_object is not None:
            self.set_active()
            if KeyListener.is_key_pressed(glfw.KEY_LEFT_CONTROL) and KeyListener.key_begin_press(glfw.KEY_D):
                new_object = copy.deepcopy(self._active_game_object)

                new_object.generate_uid()
                for component in new_object.get_all_components():
                    component.generate_id()
                sprite_renderer = new_object.get_component(SpriteRenderer)
                if sprite_renderer is not None and sprite_renderer.get_texture() is not None:
                    sprite_renderer.set_texture(AssetPool.get_texture(sprite_renderer.get_texture().get_file_path()))
                
                Window.get_scene().add_game_object_to_scene(new_object)
                glm.add(new_object.transform.position, glm.fvec2(0.1, 0.1))
                self._properties_window.set_active_game_object(new_object)
                return
        else:
            self.set_inactive()
            return
        
        x_axis_hot = self.check_x_hover_state()
        y_axis_hot = self.check_y_hover_state()

        if (x_axis_hot or self._x_axis_active) and MouseListener.get_is_dragging() and MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_LEFT):
            self._x_axis_active = True
            self._y_axis_active = False
        elif (y_axis_hot or self._y_axis_active) and MouseListener.get_is_dragging() and MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_LEFT):
            self._x_axis_active = False
            self._y_axis_active = True
        else:
            self._x_axis_active = False
            self._y_axis_active = False

        if self._active_game_object is not None:
            self._x_axis_game_object.transform.position = self._active_game_object.transform.position + self._x_axis_offset
            self._y_axis_game_object.transform.position = self._active_game_object.transform.position + self._y_axis_offset

    def set_active(self):
        self._x_axis_sprite.set_color(self._x_axis_color)
        self._y_axis_sprite.set_color(self._y_axis_color)

    def set_inactive(self):
        self._active_game_object = None
        self._x_axis_sprite.set_color(glm.fvec4(0.0, 0.0, 0.0, 0.0))
        self._y_axis_sprite.set_color(glm.fvec4(0.0, 0.0, 0.0, 0.0))

    def check_x_hover_state(self):
        from utils.mouse_listener import MouseListener
        mouse_pos = glm.fvec2(MouseListener.get_ortho_x(), MouseListener.get_ortho_y())

        if mouse_pos.x <= self._x_axis_game_object.transform.position.x + (self._gizmo_height / 2.0) and \
            mouse_pos.x >= self._x_axis_game_object.transform.position.x - (self._gizmo_height / 2.0) and \
            mouse_pos.y >= self._x_axis_game_object.transform.position.y - (self._gizmo_width / 2.0) and \
            mouse_pos.y <= self._x_axis_game_object.transform.position.y + (self._gizmo_width / 2.0):

            self._x_axis_sprite.set_color(self._x_axis_color_hover)
            return True

        self._x_axis_sprite.set_color(self._x_axis_color)
        return False
    
    def check_y_hover_state(self):
        from utils.mouse_listener import MouseListener
        mouse_pos = glm.fvec2(MouseListener.get_ortho_x(), MouseListener.get_ortho_y())

        if mouse_pos.x <= self._y_axis_game_object.transform.position.x + (self._gizmo_width / 2.0) and \
            mouse_pos.x >= self._y_axis_game_object.transform.position.x - (self._gizmo_width / 2.0) and \
            mouse_pos.y <= self._y_axis_game_object.transform.position.y + (self._gizmo_height / 2.0) and \
            mouse_pos.y >= self._y_axis_game_object.transform.position.y - (self._gizmo_height / 2.0):

            self._y_axis_sprite.set_color(self._y_axis_color_hover)
            return True

        self._y_axis_sprite.set_color(self._y_axis_color)
        return False
    
    def set_using(self):
        self._using = True

    def set_not_using(self):
        self._using = False
        self.set_inactive()
