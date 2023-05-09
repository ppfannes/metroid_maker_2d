import math
import glm
from Box2D.b2 import (
    vec2,
    world,
    bodyDef,
    kinematicBody,
    dynamicBody,
    staticBody,
    polygonShape,
    fixtureDef,
    circleShape,
)
from components.ground import Ground
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.circle_collider import CircleCollider
from physics2d.components.pillbox_collider import PillboxCollider
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.enums.body_types import BodyType
from physics2d.metroid_maker_contact_listener import MetroidMakerContactListener
from physics2d.raycast_info import RaycastInfo


class Physics2D:
    def __init__(self) -> None:
        self._gravity = vec2(0, -10.0)
        self._world = world(self._gravity)
        self._physics_time = 0.0
        self._physics_time_step = 1.0 / 60.0
        self._velocity_iterations = 8
        self._position_iterations = 3

        self._world.contactListener = MetroidMakerContactListener()

    def add(self, game_object):
        rigid_body = game_object.get_component(RigidBody2D)
        if rigid_body is not None and rigid_body.raw_body is None:
            transform = game_object.transform

            body_def = bodyDef()
            body_def.angle = math.radians(transform.rotation)
            body_def.position = (transform.position.x, transform.position.y)
            body_def.angularDamping = rigid_body.angular_damping
            body_def.linearDamping = rigid_body.linear_damping
            body_def.fixedRotation = rigid_body.fixed_rotation
            body_def.gravityScale = rigid_body.gravity_scale
            body_def.angularVelocity = rigid_body.angular_velocity
            body_def.userData = rigid_body.game_object
            body_def.bullet = rigid_body.continuous_collision

            match rigid_body.body_type:
                case BodyType.KINEMATIC:
                    body_def.type = kinematicBody
                case BodyType.STATIC:
                    body_def.type = staticBody
                case BodyType.DYNAMIC:
                    body_def.type = dynamicBody

            body = self._world.CreateBody(body_def)
            body.mass = rigid_body.mass
            rigid_body.raw_body = body

            if game_object.get_component(CircleCollider) is not None:
                circle_collider = game_object.get_component(CircleCollider)
                self.add_circle_collider(rigid_body, circle_collider)

            if game_object.get_component(Box2DCollider) is not None:
                box_collider = game_object.get_component(Box2DCollider)
                self.add_box_2d_collider(rigid_body, box_collider)

            if game_object.get_component(PillboxCollider) is not None:
                pillbox_collider = game_object.get_component(PillboxCollider)
                self.add_pillbox_collider(rigid_body, pillbox_collider)

    def destroy_game_object(self, game_object):
        rigid_body = game_object.get_component(RigidBody2D)

        if rigid_body is not None:
            if rigid_body.raw_body is not None:
                self._world.DestroyBody(rigid_body.raw_body)
                rigid_body.raw_body = None

    def update(self, dt):
        self._physics_time += dt

        if self._physics_time >= 0.0:
            self._physics_time -= self._physics_time_step
            self._world.Step(
                self._physics_time_step,
                self._velocity_iterations,
                self._position_iterations,
            )

    def set_is_sensor(self, rigid_body, is_sensor):
        body = rigid_body.raw_body

        if body is None:
            return

        for fixture in body.fixtures:
            fixture.sensor = is_sensor

    def reset_box_collider(self, rigid_body, box_collider):
        body = rigid_body.raw_body

        if body is None:
            return

        for fixture in reversed(body.fixtures):
            body.DestroyFixture(fixture)

        self.add_box_2d_collider(rigid_body, box_collider)
        body.ResetMassData()

    def add_box_2d_collider(self, rigid_body, box_collider):
        body = rigid_body.raw_body

        shape = polygonShape()
        half_size = 0.5 * vec2(box_collider.half_size)
        offset = box_collider.offset
        shape.box = (half_size.x, half_size.y, vec2(offset.x, offset.y), 0)

        fixture_def = fixtureDef()
        fixture_def.shape = shape
        fixture_def.density = 1.0
        fixture_def.friction = rigid_body.friction
        fixture_def.userData = box_collider.game_object
        fixture_def.isSensor = rigid_body.is_sensor
        body.CreateFixture(fixture_def)

    def reset_circle_collider(self, rigid_body, circle_collider):
        body = rigid_body.raw_body

        if body is None:
            return

        for fixture in reversed(body.fixtures):
            body.DestroyFixture(fixture)

        self.add_circle_collider(rigid_body, circle_collider)
        body.ResetMassData()

    def add_circle_collider(self, rigid_body, circle_collider):
        body = rigid_body.raw_body

        shape = circleShape()
        shape.radius = circle_collider.radius
        shape.pos = vec2(circle_collider.offset.x, circle_collider.offset.y)

        fixture_def = fixtureDef()
        fixture_def.shape = shape
        fixture_def.density = 1.0
        fixture_def.friction = rigid_body.friction
        fixture_def.userData = circle_collider.game_object
        fixture_def.isSensor = rigid_body.is_sensor
        body.CreateFixture(fixture_def)

    def reset_pillbox_collider(self, rigid_body, pillbox_collider):
        body = rigid_body.raw_body
        if body is None:
            return

        for fixture in reversed(body.fixtures):
            body.DestroyFixture(fixture)

        self.add_pillbox_collider(rigid_body, pillbox_collider)
        body.ResetMassData()

    def add_pillbox_collider(self, rigid_body, pillbox_collider):
        body = rigid_body.raw_body
        if body is None:
            return

        self.add_box_2d_collider(rigid_body, pillbox_collider.box)
        self.add_circle_collider(rigid_body, pillbox_collider.bottom_circle)

    def raycast(self, requesting_object, point1, point2):
        callback = RaycastInfo(requesting_object)
        self._world.RayCast(
            callback, vec2(point1.x, point1.y), vec2(point2.x, point2.y)
        )
        return callback

    def is_locked(self):
        return self._world.locked

    @property
    def gravity(self):
        return self._gravity

    @gravity.setter
    def gravity(self, value):
        self._gravity = value

    @classmethod
    def check_on_ground(cls, game_object, inner_player_width, height):
        from metroid_maker.window import Window

        raycast_begin = glm.fvec2(game_object.transform.position)
        raycast_begin = glm.sub(raycast_begin, glm.fvec2(inner_player_width / 2.0, 0.0))

        raycast_end = glm.add(raycast_begin, glm.fvec2(0.0, height))

        info = Window.get_physics().raycast(game_object, raycast_begin, raycast_end)

        raycast2_begin = glm.add(raycast_begin, glm.fvec2(inner_player_width, 0.0))
        raycast2_end = glm.add(raycast_end, glm.fvec2(inner_player_width, 0.0))
        info2 = Window.get_physics().raycast(game_object, raycast2_begin, raycast2_end)

        return (
            info.hit
            and info.hit_object is not None
            and info.hit_object.get_component(Ground)
            or info2.hit
            and info2.hit_object is not None
            and info2.hit_object.get_component(Ground)
        )
