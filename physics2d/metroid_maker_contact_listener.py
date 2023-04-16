from Box2D.b2 import (
    contactListener,
    vec2,
    manifold,
    contact,
    contactImpulse,
    worldManifold,
)
from metroid_maker.game_object import GameObject


class MetroidMakerContactListener(contactListener):
    def __init__(self):
        super().__init__()

    def BeginContact(self, contact: contact):
        object_a: GameObject = contact.fixtureA.userData
        object_b: GameObject = contact.fixtureB.userData
        world_manifold: worldManifold = contact.worldManifold
        a_normal: vec2 = world_manifold.normal
        b_normal: vec2 = -a_normal

        for component in object_a.get_all_components():
            component.begin_collision(object_b, contact, a_normal)

        for component in object_b.get_all_components():
            component.begin_collision(object_a, contact, b_normal)

    def EndContact(self, contact: contact):
        object_a: GameObject = contact.fixtureA.userData
        object_b: GameObject = contact.fixtureB.userData
        world_manifold: worldManifold = contact.worldManifold
        a_normal: vec2 = world_manifold.normal
        b_normal: vec2 = -a_normal

        for component in object_a.get_all_components():
            component.end_collision(object_b, contact, a_normal)

        for component in object_b.get_all_components():
            component.end_collision(object_a, contact, b_normal)

    def PreSolve(self, contact: contact, manifold: manifold):
        object_a: GameObject = contact.fixtureA.userData
        object_b: GameObject = contact.fixtureB.userData
        world_manifold: worldManifold = contact.worldManifold
        a_normal: vec2 = world_manifold.normal
        b_normal: vec2 = -a_normal

        for component in object_a.get_all_components():
            component.pre_solve(object_b, contact, a_normal)

        for component in object_b.get_all_components():
            component.pre_solve(object_a, contact, b_normal)

    def PostSolve(self, contact: contact, impulse: contactImpulse):
        object_a: GameObject = contact.fixtureA.userData
        object_b: GameObject = contact.fixtureB.userData
        world_manifold: worldManifold = contact.worldManifold
        a_normal: vec2 = world_manifold.normal
        b_normal: vec2 = -a_normal

        for component in object_a.get_all_components():
            component.post_solve(object_b, contact, a_normal)

        for component in object_b.get_all_components():
            component.post_solve(object_a, contact, b_normal)
