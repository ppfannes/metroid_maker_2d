import glm
from components.sprite_renderer import SpriteRenderer

class Prefabs:

    @classmethod
    def generate_sprite_object(cls, sprite, sprite_width, sprite_height):
        from metroid_maker.window import Window
        block = Window.get_scene().create_game_object("Sprite_Object_Gen")
        block.transform.scale = glm.fvec2(sprite_width, sprite_height)
        sprite_renderer = SpriteRenderer()
        sprite_renderer.set_sprite(sprite)
        block.add_component(sprite_renderer)

        return block
