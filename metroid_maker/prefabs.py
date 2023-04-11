import glm
from components.sprite_renderer import SpriteRenderer
from components.state_machine import StateMachine
from components.animation_state import AnimationState


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

    @classmethod
    def generate_mario(cls):
        from utils.asset_pool import AssetPool

        player_sprite = AssetPool.get_spritesheet("assets/images/spritesheet.jpg")
        mario = cls.generate_sprite_object(player_sprite.get_sprite(0), 0.25, 0.25)

        run = AnimationState()
        run.title = "Run"
        default_frame_time = 0.23
        run.add_frame(player_sprite.get_sprite(0), default_frame_time)
        run.add_frame(player_sprite.get_sprite(2), default_frame_time)
        run.add_frame(player_sprite.get_sprite(3), default_frame_time)
        run.add_frame(player_sprite.get_sprite(2), default_frame_time)
        run.does_loop = True

        state_machine = StateMachine()
        state_machine.add_state(run)
        state_machine.set_default_state(run.title)
        mario.add_component(state_machine)

        return mario

    @classmethod
    def generate_question_block(cls):
        from utils.asset_pool import AssetPool

        item = AssetPool.get_spritesheet("assets/images/items.jpg")
        question_block = cls.generate_sprite_object(item.get_sprite(0), 0.25, 0.25)

        flicker = AnimationState()
        flicker.title = "Flicker"
        default_frame_time = 0.23
        flicker.add_frame(item.get_sprite(0), 0.57)
        flicker.add_frame(item.get_sprite(1), default_frame_time)
        flicker.add_frame(item.get_sprite(2), default_frame_time)
        flicker.does_loop = True

        state_machine = StateMachine()
        state_machine.add_state(flicker)
        state_machine.set_default_state(flicker.title)
        question_block.add_component(state_machine)

        return question_block
