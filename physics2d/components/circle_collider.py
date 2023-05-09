import glm
from components.component import Component
from physics2d.components.rigid_body_2d import RigidBody2D
from renderer.debug_draw import DebugDraw


class CircleCollider(Component):
    def __init__(self):
        super().__init__()
        self._radius = 1.0
        self._reset_fixture_next_frame = False
        self._offset = glm.fvec2(0.0)

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._reset_fixture_next_frame = True
        self._radius = value

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value

    def editor_update(self, dt):
        center = glm.add(self.game_object.transform.position, self.offset)
        DebugDraw.add_circle(center, self._radius)

        if self._reset_fixture_next_frame:
            self.reset_fixture()

    def update(self, dt):
        if self._reset_fixture_next_frame:
            self.reset_fixture()

    def reset_fixture(self):
        from metroid_maker.window import Window

        if Window.get_physics().is_locked():
            self._reset_fixture_next_frame = True
            return

        self._reset_fixture_next_frame = False

        if self.game_object is not None:
            rigid_body = self.game_object.get_component(RigidBody2D)

            if rigid_body is not None:
                Window.get_physics().reset_circle_collider(rigid_body, self)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_reset_fixture_next_frame"]
        return state

    def __setstate__(self, state):
        state["_reset_fixture_next_frame"] = False
        self.__dict__.update(state)
