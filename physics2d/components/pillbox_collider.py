import glm
from components.component import Component
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.circle_collider import CircleCollider


class PillboxCollider(Component):
    def __init__(self):
        super().__init__()
        self._top_circle: CircleCollider = CircleCollider()
        self._bottom_circle: CircleCollider = CircleCollider()
        self._box: Box2DCollider = Box2DCollider()
        self._reset_fixture_next_frame: bool = False
        self.width: float = 0.1
        self.height: float = 0.25
        self.offset: glm.fvec2 = glm.fvec2(0.0)

    def start(self):
        self._top_circle.game_object = self.game_object
        self._bottom_circle.game_object = self.game_object
        self._box.game_object = self.game_object
        self.recalculate_colliders()

    def editor_update(self, dt):
        self._top_circle.editor_update(dt)
        self._bottom_circle.editor_update(dt)
        self._box.editor_update(dt)

        if self._reset_fixture_next_frame:
            self.reset_fixture()

    def update(self, dt):
        if self._reset_fixture_next_frame:
            self.reset_fixture()

    @property
    def top_circle(self):
        return self._top_circle

    @top_circle.setter
    def top_circle(self, value):
        self._top_circle = value

    @property
    def bottom_circle(self):
        return self._bottom_circle

    @bottom_circle.setter
    def bottom_circle(self, value):
        self._bottom_circle = value

    @property
    def box(self):
        return self._box

    @box.setter
    def box(self, value):
        self._box = value

    def reset_fixture(self):
        from metroid_maker.window import Window

        if Window.get_physics().is_locked():
            self._reset_fixture_next_frame = True
            return

        self._reset_fixture_next_frame = False

        if self.game_object is not None:
            rigid_body = self.game_object.get_component(RigidBody2D)

            if rigid_body is not None:
                Window.get_physics().reset_pillbox_collider(rigid_body, self)

    def recalculate_colliders(self):
        circle_radius = self.width / 4.0
        box_height = self.height - 2 * circle_radius
        self._top_circle.radius = circle_radius
        self._bottom_circle.radius = circle_radius
        self._top_circle.offset = glm.add(
            glm.fvec2(self.offset), glm.fvec2(0.0, box_height / 4.0)
        )
        self._bottom_circle.offset = glm.sub(
            glm.fvec2(self.offset), glm.fvec2(0.0, box_height / 4.0)
        )
        self._box.half_size = glm.fvec2(self.width / 2.0, box_height / 2.0)
        self._box.offset = self.offset
