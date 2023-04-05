import imgui
from glfw.GLFW import GLFW_MOUSE_BUTTON_LEFT
from components.non_pickable import NonPickable
from utils.mouse_listener import MouseListener
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.circle_collider import CircleCollider


class PropertiesWindow:
    def __init__(self, picking_texture):
        self._active_game_object = None
        self._picking_texture = picking_texture
        self._debounce = 0.2

    def update(self, dt, current_scene):
        self._debounce -= dt

        if (
            not MouseListener.is_dragging()
            and MouseListener.mouse_button_down(GLFW_MOUSE_BUTTON_LEFT)
            and self._debounce < 0
        ):
            x = MouseListener.get_screen_x()
            y = MouseListener.get_screen_y()
            game_object_id = self._picking_texture.read_pixel(x, y)
            picked_object = current_scene.get_game_object(game_object_id)
            if (
                picked_object is not None
                and picked_object.get_component(NonPickable) is None
            ):
                self._active_game_object = picked_object
            elif picked_object is None and not MouseListener.get_is_dragging():
                self._active_game_object = None
            self._debounce = 0.2

    def imgui(self):
        if self._active_game_object is not None:
            imgui.begin("Properties")

            if imgui.begin_popup_context_window("ColliderAdder"):
                clicked_rb, _ = imgui.menu_item("Add Rigid Body")
                clicked_bc, _ = imgui.menu_item("Add Box Collider")
                clicked_cc, _ = imgui.menu_item("Add Circle Collider")

                if (
                    clicked_rb
                    and self._active_game_object.get_component(RigidBody2D) is None
                ):
                    self._active_game_object.add_component(RigidBody2D())

                if (
                    clicked_bc
                    and self._active_game_object.get_component(Box2DCollider) is None
                    and self._active_game_object.get_component(CircleCollider) is None
                ):
                    self._active_game_object.add_component(Box2DCollider())

                if (
                    clicked_cc
                    and self._active_game_object.get_component(Box2DCollider) is None
                    and self._active_game_object.get_component(CircleCollider) is None
                ):
                    self._active_game_object.add_component(CircleCollider())

                imgui.end_popup()

            self._active_game_object.imgui()
            imgui.end()

    def get_active_game_object(self):
        return self._active_game_object

    def set_active_game_object(self, game_object):
        self._active_game_object = game_object
