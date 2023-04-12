import imgui
from glfw.GLFW import GLFW_MOUSE_BUTTON_LEFT
import typing
from components.non_pickable import NonPickable
from utils.mouse_listener import MouseListener
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.circle_collider import CircleCollider

if typing.TYPE_CHECKING:
    from typing import List
    from metroid_maker.game_object import GameObject


class PropertiesWindow:
    def __init__(self, picking_texture):
        self._active_game_objects: List[GameObject] = []
        self._active_game_object = None
        self._picking_texture = picking_texture
        self._debounce = 0.2

    def imgui(self):
        if (
            len(self._active_game_objects) == 1
            and self._active_game_objects[0] is not None
        ):
            self._active_game_object = self._active_game_objects[0]
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
        if len(self._active_game_objects) == 1:
            return self._active_game_objects[0]
        return None

    def get_active_game_objects(self):
        return self._active_game_objects

    def clear_selected(self):
        self._active_game_objects.clear()

    def set_active_game_object(self, game_object):
        if game_object is not None:
            self.clear_selected()
            self._active_game_objects.append(game_object)

    def add_active_game_object(self, game_object):
        self._active_game_objects.append(game_object)

    def get_picking_texture(self):
        return self._picking_texture
