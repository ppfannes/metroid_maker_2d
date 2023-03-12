import glm
import math
from Box2D.b2 import (vec2, world, bodyDef, kinematicBody, dynamicBody, staticBody, polygonShape)
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.circle_collider import CircleCollider
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.enums.body_types import BodyType

class Physics2D:

    def __init__(self) -> None:
        self._gravity = vec2(0, -10.0)
        self._world = world(self._gravity)
        self._physics_time = 0.0
        self._physics_time_step = 1.0 / 60.0
        self._velocity_iterations = 8
        self._position_iterations = 3

    def add(self, game_object):
        rigid_body = game_object.get_component(RigidBody2D)
        if rigid_body is not None and rigid_body.raw_body is None:
            transform = game_object.transform

            body_def = bodyDef()
            body_def.angle = math.radians(transform.rotation)
            body_def.position = (transform.position.x, transform.position.y)
            body_def.angular_damping = rigid_body.angular_damping
            body_def.linear_damping = rigid_body.linear_damping
            body_def.fixed_rotation = rigid_body.fixed_rotation
            body_def.bullet = rigid_body.continuous_collision

            match rigid_body.body_type:
                case BodyType.KINEMATIC:
                    body_def.type = kinematicBody
                case BodyType.STATIC:
                    body_def.type = staticBody
                case BodyType.DYNAMIC:
                    body_def.type = dynamicBody

            shape = polygonShape()
            
            if game_object.get_component(CircleCollider) is not None:
                circle_collider = game_object.get_component(CircleCollider)
                shape.radius = circle_collider.radius
            elif game_object.get_component(Box2DCollider) is not None:
                box_collider = game_object.get_component(Box2DCollider)
                half_size = glm.mul(glm.fvec2(box_collider.half_size), 0.5)
                offset = box_collider.offset
                origin = glm.fvec2(box_collider.origin)
                shape.box = (half_size.x, half_size.y, vec2(origin.x, origin.y), 0)

                pos = body_def.position
                x_pos = pos.x + offset.x
                y_pos = pos.y + offset.y
                body_def.position = vec2(x_pos, y_pos)

            body = self._world.CreateBody(body_def)
            rigid_body.raw_body = body
            body.CreateFixture(shape=shape, density=rigid_body.mass)



    def update(self, dt):
        self._physics_time += dt

        if self._physics_time >= 0.0:
            self._physics_time -= self._physics_time_step
            self._world.Step(self._physics_time_step, self._velocity_iterations, self._position_iterations)
