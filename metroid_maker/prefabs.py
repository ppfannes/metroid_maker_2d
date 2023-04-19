import glm
from components.sprite_renderer import SpriteRenderer
from components.state_machine import StateMachine
from components.animation_state import AnimationState
from components.player_controller import PlayerController
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
        big_player_sprites = AssetPool.get_spritesheet("assets/images/big_spritesheet.jpg")
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
        fire_run.add_frame(big_player_sprites.get_sprite(fire_offset + 0), default_frame_time)
        fire_run.add_frame(big_player_sprites.get_sprite(fire_offset + 1), default_frame_time)
        fire_run.add_frame(big_player_sprites.get_sprite(fire_offset + 2), default_frame_time)
        fire_run.add_frame(big_player_sprites.get_sprite(fire_offset + 3), default_frame_time)
        fire_run.add_frame(big_player_sprites.get_sprite(fire_offset + 2), default_frame_time)
        fire_run.add_frame(big_player_sprites.get_sprite(fire_offset + 1), default_frame_time)
        fire_run.does_loop = True

        fireswitch_direction = AnimationState()
        fireswitch_direction.title = "Fire Switch Direction"
        fireswitch_direction.add_frame(big_player_sprites.get_sprite(fire_offset + 4), 0.1)
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
        state_machine.add_state_trigger(run.title, switch_direction.title, "switch_direction")
        state_machine.add_state_trigger(run.title, idle.title, "stopRunning")
        state_machine.add_state_trigger(run.title, jump.title, "jump")
        state_machine.add_state_trigger(switch_direction.title, idle.title, "stopRunning")
        state_machine.add_state_trigger(switch_direction.title, run.title, "startRunning")
        state_machine.add_state_trigger(switch_direction.title, jump.title, "jump")
        state_machine.add_state_trigger(idle.title, run.title, "startRunning")
        state_machine.add_state_trigger(idle.title, jump.title, "jump")
        state_machine.add_state_trigger(jump.title, idle.title, "stopJumping")

        state_machine.add_state_trigger(big_run.title, big_switch_direction.title, "switch_direction")
        state_machine.add_state_trigger(big_run.title, big_idle.title, "stopRunning")
        state_machine.add_state_trigger(big_run.title, big_jump.title, "jump")
        state_machine.add_state_trigger(big_switch_direction.title, big_idle.title, "stopRunning")
        state_machine.add_state_trigger(big_switch_direction.title, big_run.title, "startRunning")
        state_machine.add_state_trigger(big_switch_direction.title, big_jump.title, "jump")
        state_machine.add_state_trigger(big_idle.title, big_run.title, "startRunning")
        state_machine.add_state_trigger(big_idle.title, big_jump.title, "jump")
        state_machine.add_state_trigger(big_jump.title, big_idle.title, "stopJumping")

        state_machine.add_state_trigger(fire_run.title, fireswitch_direction.title, "switch_direction")
        state_machine.add_state_trigger(fire_run.title, fire_idle.title, "stopRunning")
        state_machine.add_state_trigger(fire_run.title, fire_jump.title, "jump")
        state_machine.add_state_trigger(fireswitch_direction.title, fire_idle.title, "stopRunning")
        state_machine.add_state_trigger(fireswitch_direction.title, fire_run.title, "startRunning")
        state_machine.add_state_trigger(fireswitch_direction.title, fire_jump.title, "jump")
        state_machine.add_state_trigger(fire_idle.title, fire_run.title, "startRunning")
        state_machine.add_state_trigger(fire_idle.title, fire_jump.title, "jump")
        state_machine.add_state_trigger(fire_jump.title, fire_idle.title, "stopJumping")

        state_machine.add_state_trigger(run.title, big_run.title, "powerup")
        state_machine.add_state_trigger(idle.title, big_idle.title, "powerup")
        state_machine.add_state_trigger(switch_direction.title, big_switch_direction.title, "powerup")
        state_machine.add_state_trigger(jump.title, big_jump.title, "powerup")
        state_machine.add_state_trigger(big_run.title, fire_run.title, "powerup")
        state_machine.add_state_trigger(big_idle.title, fire_idle.title, "powerup")
        state_machine.add_state_trigger(big_switch_direction.title, fireswitch_direction.title, "powerup")
        state_machine.add_state_trigger(big_jump.title, fire_jump.title, "powerup")

        state_machine.add_state_trigger(big_run.title, run.title, "damage")
        state_machine.add_state_trigger(big_idle.title, idle.title, "damage")
        state_machine.add_state_trigger(big_switch_direction.title, switch_direction.title, "damage")
        state_machine.add_state_trigger(big_jump.title, jump.title, "damage")
        state_machine.add_state_trigger(fire_run.title, big_run.title, "damage")
        state_machine.add_state_trigger(fire_idle.title, big_idle.title, "damage")
        state_machine.add_state_trigger(fireswitch_direction.title, big_switch_direction.title, "damage")
        state_machine.add_state_trigger(fire_jump.title, big_jump.title, "damage")

        state_machine.add_state_trigger(run.title, die.title, "die")
        state_machine.add_state_trigger(switch_direction.title, die.title, "die")
        state_machine.add_state_trigger(idle.title, die.title, "die")
        state_machine.add_state_trigger(jump.title, die.title, "die")
        state_machine.add_state_trigger(big_run.title, run.title, "die")
        state_machine.add_state_trigger(big_switch_direction.title, switch_direction.title, "die")
        state_machine.add_state_trigger(big_idle.title, idle.title, "die")
        state_machine.add_state_trigger(big_jump.title, jump.title, "die")
        state_machine.add_state_trigger(fire_run.title, big_run.title, "die")
        state_machine.add_state_trigger(fireswitch_direction.title, big_switch_direction.title, "die")
        state_machine.add_state_trigger(fire_idle.title, big_idle.title, "die")
        state_machine.add_state_trigger(fire_jump.title, big_jump.title, "die")
        mario.add_component(state_machine)

        test_trigger = StateTrigger("fire_run", "jump")
        print(state_machine._state_transfers[test_trigger])

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

        state_machine = StateMachine()
        state_machine.add_state(flicker)
        state_machine.set_default_state(flicker.title)
        question_block.add_component(state_machine)

        return question_block
