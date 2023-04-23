import glm
from components.block_coin import BlockCoin
from components.flower import Flower
from components.goomba_ai import GoombaAI
from components.ground import Ground
from components.mushroom_ai import MushroomAI
from components.question_block import QuestionBlock
from components.sprite_renderer import SpriteRenderer
from components.state_machine import StateMachine
from components.animation_state import AnimationState
from components.player_controller import PlayerController
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.circle_collider import CircleCollider
from physics2d.components.pillbox_collider import PillboxCollider
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.enums.body_types import BodyType


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
        from components.state_machine import StateTrigger

        player_sprites = AssetPool.get_spritesheet("assets/images/spritesheet.jpg")
        big_player_sprites = AssetPool.get_spritesheet(
            "assets/images/big_spritesheet.jpg"
        )
        mario = cls.generate_sprite_object(player_sprites.get_sprite(0), 0.25, 0.25)

        # Little mario animations
        run = AnimationState()
        run.title = "Run"
        default_frame_time = 0.2
        run.add_frame(player_sprites.get_sprite(0), default_frame_time)
        run.add_frame(player_sprites.get_sprite(2), default_frame_time)
        run.add_frame(player_sprites.get_sprite(3), default_frame_time)
        run.add_frame(player_sprites.get_sprite(2), default_frame_time)
        run.does_loop = True

        switch_direction = AnimationState()
        switch_direction.title = "Switch Direction"
        switch_direction.add_frame(player_sprites.get_sprite(4), 0.1)
        switch_direction.does_loop = False

        idle = AnimationState()
        idle.title = "Idle"
        idle.add_frame(player_sprites.get_sprite(0), 0.1)
        idle.does_loop = False

        jump = AnimationState()
        jump.title = "Jump"
        jump.add_frame(player_sprites.get_sprite(5), 0.1)
        jump.does_loop = False

        # Big mario animations
        big_run = AnimationState()
        big_run.title = "big_run"
        big_run.add_frame(big_player_sprites.get_sprite(0), default_frame_time)
        big_run.add_frame(big_player_sprites.get_sprite(1), default_frame_time)
        big_run.add_frame(big_player_sprites.get_sprite(2), default_frame_time)
        big_run.add_frame(big_player_sprites.get_sprite(3), default_frame_time)
        big_run.add_frame(big_player_sprites.get_sprite(2), default_frame_time)
        big_run.add_frame(big_player_sprites.get_sprite(1), default_frame_time)
        big_run.does_loop = True

        big_switch_direction = AnimationState()
        big_switch_direction.title = "Big Switch Direction"
        big_switch_direction.add_frame(big_player_sprites.get_sprite(4), 0.1)
        big_switch_direction.does_loop = False

        big_idle = AnimationState()
        big_idle.title = "big_idle"
        big_idle.add_frame(big_player_sprites.get_sprite(0), 0.1)
        big_idle.does_loop = False

        big_jump = AnimationState()
        big_jump.title = "big_jump"
        big_jump.add_frame(big_player_sprites.get_sprite(5), 0.1)
        big_jump.does_loop = False

        # Fire mario animations
        fire_offset = 21
        fire_run = AnimationState()
        fire_run.title = "fire_run"
        fire_run.add_frame(
            big_player_sprites.get_sprite(fire_offset + 0), default_frame_time
        )
        fire_run.add_frame(
            big_player_sprites.get_sprite(fire_offset + 1), default_frame_time
        )
        fire_run.add_frame(
            big_player_sprites.get_sprite(fire_offset + 2), default_frame_time
        )
        fire_run.add_frame(
            big_player_sprites.get_sprite(fire_offset + 3), default_frame_time
        )
        fire_run.add_frame(
            big_player_sprites.get_sprite(fire_offset + 2), default_frame_time
        )
        fire_run.add_frame(
            big_player_sprites.get_sprite(fire_offset + 1), default_frame_time
        )
        fire_run.does_loop = True

        fireswitch_direction = AnimationState()
        fireswitch_direction.title = "Fire Switch Direction"
        fireswitch_direction.add_frame(
            big_player_sprites.get_sprite(fire_offset + 4), 0.1
        )
        fireswitch_direction.does_loop = False

        fire_idle = AnimationState()
        fire_idle.title = "fire_idle"
        fire_idle.add_frame(big_player_sprites.get_sprite(fire_offset + 0), 0.1)
        fire_idle.does_loop = False

        fire_jump = AnimationState()
        fire_jump.title = "fire_jump"
        fire_jump.add_frame(big_player_sprites.get_sprite(fire_offset + 5), 0.1)
        fire_jump.does_loop = False

        die = AnimationState()
        die.title = "Die"
        die.add_frame(player_sprites.get_sprite(6), 0.1)
        die.does_loop = False

        state_machine = StateMachine()
        state_machine.add_state(run)
        state_machine.add_state(idle)
        state_machine.add_state(switch_direction)
        state_machine.add_state(jump)
        state_machine.add_state(die)

        state_machine.add_state(big_run)
        state_machine.add_state(big_idle)
        state_machine.add_state(big_switch_direction)
        state_machine.add_state(big_jump)

        state_machine.add_state(fire_run)
        state_machine.add_state(fire_idle)
        state_machine.add_state(fireswitch_direction)
        state_machine.add_state(fire_jump)

        state_machine.set_default_state(idle.title)
        state_machine.add_state_trigger(
            run.title, switch_direction.title, "switchDirection"
        )
        state_machine.add_state_trigger(run.title, idle.title, "stopRunning")
        state_machine.add_state_trigger(run.title, jump.title, "jump")
        state_machine.add_state_trigger(
            switch_direction.title, idle.title, "stopRunning"
        )
        state_machine.add_state_trigger(
            switch_direction.title, run.title, "startRunning"
        )
        state_machine.add_state_trigger(switch_direction.title, jump.title, "jump")
        state_machine.add_state_trigger(idle.title, run.title, "startRunning")
        state_machine.add_state_trigger(idle.title, jump.title, "jump")
        state_machine.add_state_trigger(jump.title, idle.title, "stopJumping")

        state_machine.add_state_trigger(
            big_run.title, big_switch_direction.title, "switchDirection"
        )
        state_machine.add_state_trigger(big_run.title, big_idle.title, "stopRunning")
        state_machine.add_state_trigger(big_run.title, big_jump.title, "jump")
        state_machine.add_state_trigger(
            big_switch_direction.title, big_idle.title, "stopRunning"
        )
        state_machine.add_state_trigger(
            big_switch_direction.title, big_run.title, "startRunning"
        )
        state_machine.add_state_trigger(
            big_switch_direction.title, big_jump.title, "jump"
        )
        state_machine.add_state_trigger(big_idle.title, big_run.title, "startRunning")
        state_machine.add_state_trigger(big_idle.title, big_jump.title, "jump")
        state_machine.add_state_trigger(big_jump.title, big_idle.title, "stopJumping")

        state_machine.add_state_trigger(
            fire_run.title, fireswitch_direction.title, "switchDirection"
        )
        state_machine.add_state_trigger(fire_run.title, fire_idle.title, "stopRunning")
        state_machine.add_state_trigger(fire_run.title, fire_jump.title, "jump")
        state_machine.add_state_trigger(
            fireswitch_direction.title, fire_idle.title, "stopRunning"
        )
        state_machine.add_state_trigger(
            fireswitch_direction.title, fire_run.title, "startRunning"
        )
        state_machine.add_state_trigger(
            fireswitch_direction.title, fire_jump.title, "jump"
        )
        state_machine.add_state_trigger(fire_idle.title, fire_run.title, "startRunning")
        state_machine.add_state_trigger(fire_idle.title, fire_jump.title, "jump")
        state_machine.add_state_trigger(fire_jump.title, fire_idle.title, "stopJumping")

        state_machine.add_state_trigger(run.title, big_run.title, "powerup")
        state_machine.add_state_trigger(idle.title, big_idle.title, "powerup")
        state_machine.add_state_trigger(
            switch_direction.title, big_switch_direction.title, "powerup"
        )
        state_machine.add_state_trigger(jump.title, big_jump.title, "powerup")
        state_machine.add_state_trigger(big_run.title, fire_run.title, "powerup")
        state_machine.add_state_trigger(big_idle.title, fire_idle.title, "powerup")
        state_machine.add_state_trigger(
            big_switch_direction.title, fireswitch_direction.title, "powerup"
        )
        state_machine.add_state_trigger(big_jump.title, fire_jump.title, "powerup")

        state_machine.add_state_trigger(big_run.title, run.title, "damage")
        state_machine.add_state_trigger(big_idle.title, idle.title, "damage")
        state_machine.add_state_trigger(
            big_switch_direction.title, switch_direction.title, "damage"
        )
        state_machine.add_state_trigger(big_jump.title, jump.title, "damage")
        state_machine.add_state_trigger(fire_run.title, big_run.title, "damage")
        state_machine.add_state_trigger(fire_idle.title, big_idle.title, "damage")
        state_machine.add_state_trigger(
            fireswitch_direction.title, big_switch_direction.title, "damage"
        )
        state_machine.add_state_trigger(fire_jump.title, big_jump.title, "damage")

        state_machine.add_state_trigger(run.title, die.title, "die")
        state_machine.add_state_trigger(switch_direction.title, die.title, "die")
        state_machine.add_state_trigger(idle.title, die.title, "die")
        state_machine.add_state_trigger(jump.title, die.title, "die")
        state_machine.add_state_trigger(big_run.title, run.title, "die")
        state_machine.add_state_trigger(
            big_switch_direction.title, switch_direction.title, "die"
        )
        state_machine.add_state_trigger(big_idle.title, idle.title, "die")
        state_machine.add_state_trigger(big_jump.title, jump.title, "die")
        state_machine.add_state_trigger(fire_run.title, big_run.title, "die")
        state_machine.add_state_trigger(
            fireswitch_direction.title, big_switch_direction.title, "die"
        )
        state_machine.add_state_trigger(fire_idle.title, big_idle.title, "die")
        state_machine.add_state_trigger(fire_jump.title, big_jump.title, "die")
        mario.add_component(state_machine)

        pillbox_collider = PillboxCollider()
        pillbox_collider.width = 0.39
        pillbox_collider.height = 0.31
        rigid_body = RigidBody2D()
        rigid_body.body_type = BodyType.DYNAMIC
        rigid_body.continuous_collision = False
        rigid_body.fixed_rotation = True
        rigid_body.mass = 25.0

        mario.add_component(rigid_body)
        mario.add_component(pillbox_collider)
        mario.add_component(PlayerController())

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

        inactive = AnimationState()
        inactive.title = "Inactive"
        inactive.add_frame(item.get_sprite(3), default_frame_time)
        inactive.does_loop = False

        state_machine = StateMachine()
        state_machine.add_state(flicker)
        state_machine.add_state(inactive)
        state_machine.add_state_trigger(flicker.title, inactive.title, "setInactive")
        state_machine.set_default_state(flicker.title)
        question_block.add_component(state_machine)
        question_block.add_component(QuestionBlock())

        rigid_body = RigidBody2D()
        rigid_body.body_type = BodyType.STATIC
        question_block.add_component(rigid_body)
        box_2d_collider = Box2DCollider()
        box_2d_collider.half_size = glm.fvec2(0.25, 0.25)
        question_block.add_component(box_2d_collider)
        question_block.add_component(Ground())

        return question_block

    @classmethod
    def generate_block_coin(cls):
        from utils.asset_pool import AssetPool

        item = AssetPool.get_spritesheet("assets/images/items.jpg")
        coin = cls.generate_sprite_object(item.get_sprite(7), 0.25, 0.25)

        coin_flip = AnimationState()
        coin_flip.title = "CoinFlip"
        default_frame_time = 0.23
        coin_flip.add_frame(item.get_sprite(7), 0.57)
        coin_flip.add_frame(item.get_sprite(8), default_frame_time)
        coin_flip.add_frame(item.get_sprite(9), default_frame_time)
        coin_flip.does_loop = True

        state_machine = StateMachine()
        state_machine.add_state(coin_flip)
        state_machine.set_default_state(coin_flip.title)
        coin.add_component(state_machine)
        coin.add_component(QuestionBlock())

        coin.add_component(BlockCoin())

        return coin

    @classmethod
    def generate_mushroom(cls):
        from utils.asset_pool import AssetPool

        item = AssetPool.get_spritesheet("assets/images/items.jpg")
        mushroom = cls.generate_sprite_object(item.get_sprite(10), 0.25, 0.25)

        rigid_body = RigidBody2D()
        rigid_body.body_type = BodyType.DYNAMIC
        rigid_body.fixed_rotation = True
        rigid_body.continuous_collision = False
        mushroom.add_component(rigid_body)

        circle_collider = CircleCollider()
        circle_collider.radius = 0.14
        mushroom.add_component(circle_collider)
        mushroom.add_component(MushroomAI())

        return mushroom

    @classmethod
    def generate_flower(cls):
        from utils.asset_pool import AssetPool

        item = AssetPool.get_spritesheet("assets/images/items.jpg")
        flower = cls.generate_sprite_object(item.get_sprite(20), 0.25, 0.25)

        rigid_body = RigidBody2D()
        rigid_body.body_type = BodyType.STATIC
        rigid_body.fixed_rotation = True
        rigid_body.continuous_collision = False
        flower.add_component(rigid_body)

        flicker = AnimationState()
        flicker.title = "FlickerFlower"
        default_frame_time = 0.23
        flicker.add_frame(item.get_sprite(21), 0.57)
        flicker.add_frame(item.get_sprite(22), default_frame_time)
        flicker.add_frame(item.get_sprite(23), default_frame_time)
        flicker.does_loop = True

        state_machine = StateMachine()
        state_machine.add_state(flicker)
        state_machine.set_default_state(flicker.title)
        flower.add_component(state_machine)

        circle_collider = CircleCollider()
        circle_collider.radius = 0.14
        flower.add_component(circle_collider)
        flower.add_component(Flower())

        return flower

    @classmethod
    def generate_goomba(cls):
        from utils.asset_pool import AssetPool

        sprite = AssetPool.get_spritesheet("assets/images/spritesheet.jpg")
        goomba = cls.generate_sprite_object(sprite.get_sprite(14), 0.25, 0.25)

        walk = AnimationState()
        walk.title = "Walk"
        default_frame_time = 0.23
        walk.add_frame(sprite.get_sprite(14), default_frame_time)
        walk.add_frame(sprite.get_sprite(15), default_frame_time)
        walk.does_loop = True

        squashed = AnimationState()
        squashed.title = "Squashed"
        squashed.add_frame(sprite.get_sprite(16), 0.1)
        squashed.does_loop = False

        state_machine = StateMachine()
        state_machine.add_state(walk)
        state_machine.add_state(squashed)
        state_machine.add_state_trigger(walk.title, squashed.title, "getSquashed")
        state_machine.set_default_state(walk.title)
        goomba.add_component(state_machine)

        rigid_body = RigidBody2D()
        rigid_body.body_type = BodyType.DYNAMIC
        rigid_body.mass = 0.1
        rigid_body.fixed_rotation = True
        goomba.add_component(rigid_body)
        circle = CircleCollider()
        circle.radius = 0.12
        goomba.add_component(circle)

        goomba.add_component(GoombaAI())

        return goomba
