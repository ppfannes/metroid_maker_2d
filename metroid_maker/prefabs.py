import glm

from components.sprite_renderer import SpriteRenderer
from metroid_maker.game_object import GameObject
from metroid_maker.transform import Transform


class Prefabs:

    @classmethod
    def generate_sprite_object(cls, sprite, sprite_width, sprite_height):
        block = GameObject("Sprite_Object_Gen",
                           Transform(glm.fvec2(), glm.fvec2(sprite_width, sprite_height)),
                           0)
        sprite_renderer = SpriteRenderer()
        sprite_renderer.set_sprite(sprite)
        block.add_component(sprite_renderer)

        return block
