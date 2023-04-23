import glm
import imgui

from components.breakable_brick import BreakableBrick
from components.editor_camera import EditorCamera
from components.gizmo_system import GizmoSystem
from components.ground import Ground
from components.grid_lines import GridLines
from components.key_controls import KeyControls
from components.mouse_controls import MouseControls
from components.sprite_renderer import SpriteRenderer
from components.spritesheet import Spritesheet
from components.state_machine import StateMachine
from metroid_maker.direction import Direction
from metroid_maker.prefabs import Prefabs
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.enums.body_types import BodyType
from scenes.scene_initializer import SceneInitializer
from utils.asset_pool import AssetPool


class LevelEditorSceneInitializer(SceneInitializer):
    def __init__(self):
        super().__init__()
        self.sprites = None
        self.level_editor_object = None

    def init(self, scene):
        self.sprites = AssetPool.get_spritesheet(
            "assets/images/decorations_and_blocks.jpg"
        )
        gizmos = AssetPool.get_spritesheet("assets/images/gizmos.jpg")

        self.level_editor_object = scene.create_game_object("Level Editor")
        self.level_editor_object.set_no_serialize()
        self.level_editor_object.add_component(KeyControls())
        self.level_editor_object.add_component(MouseControls())
        self.level_editor_object.add_component(GridLines())
        self.level_editor_object.add_component(EditorCamera(scene.camera()))
        self.level_editor_object.add_component(GizmoSystem(gizmos))
        scene.add_game_object_to_scene(self.level_editor_object)

    def load_resources(self, scene):
        AssetPool.get_shader("assets/shaders", "default")

        AssetPool.add_sprite_sheet(
            "assets/images/decorations_and_blocks.jpg",
            Spritesheet(
                AssetPool.get_texture("assets/images/decorations_and_blocks.jpg"),
                16,
                16,
                81,
                0,
            ),
        )
        AssetPool.add_sprite_sheet(
            "assets/images/spritesheet.jpg",
            Spritesheet(
                AssetPool.get_texture("assets/images/spritesheet.jpg"),
                16,
                16,
                26,
                0,
            ),
        )
        AssetPool.add_sprite_sheet(
            "assets/images/items.jpg",
            Spritesheet(
                AssetPool.get_texture("assets/images/items.jpg"),
                16,
                16,
                43,
                0,
            ),
        )
        AssetPool.add_sprite_sheet(
            "assets/images/gizmos.jpg",
            Spritesheet(
                AssetPool.get_texture("assets/images/gizmos.jpg"), 24, 48, 3, 0
            ),
        )
        AssetPool.add_sprite_sheet(
            "assets/images/big_spritesheet.jpg",
            Spritesheet(
                AssetPool.get_texture("assets/images/big_spritesheet.jpg"),
                16,
                32,
                42,
                0,
            ),
        )
        AssetPool.add_sprite_sheet(
            "assets/images/pipes.jpg",
            Spritesheet(AssetPool.get_texture("assets/images/pipes.jpg"), 32, 32, 4, 0),
        )
        AssetPool.get_texture("assets/images/blend_image_2.jpg")

        AssetPool.add_sound("assets/sounds/main-theme-overworld.ogg", True)
        AssetPool.add_sound("assets/sounds/flagpole.ogg", False)
        AssetPool.add_sound("assets/sounds/break_block.ogg", False)
        AssetPool.add_sound("assets/sounds/bump.ogg", False)
        AssetPool.add_sound("assets/sounds/coin.ogg", False)
        AssetPool.add_sound("assets/sounds/gameover.ogg", False)
        AssetPool.add_sound("assets/sounds/jump-small.ogg", False)
        AssetPool.add_sound("assets/sounds/mario_die.ogg", False)
        AssetPool.add_sound("assets/sounds/pipe.ogg", False)
        AssetPool.add_sound("assets/sounds/powerup.ogg", False)
        AssetPool.add_sound("assets/sounds/powerup_appears.ogg", False)
        AssetPool.add_sound("assets/sounds/stage_clear.ogg", False)
        AssetPool.add_sound("assets/sounds/stomp.ogg", False)
        AssetPool.add_sound("assets/sounds/kick.ogg", False)
        AssetPool.add_sound("assets/sounds/invincible.ogg", False)

        for game_object in scene.get_game_objects():
            if game_object.get_component(SpriteRenderer) is not None:
                sprite_renderer = game_object.get_component(SpriteRenderer)

                if sprite_renderer.get_texture() is not None:
                    sprite_renderer.set_texture(
                        AssetPool.get_texture(
                            sprite_renderer.get_texture().get_file_path()
                        )
                    )

            if game_object.get_component(StateMachine) is not None:
                state_machine = game_object.get_component(StateMachine)
                state_machine.refresh_textures()

    def imgui(self):
        imgui.begin("Level Editor Debug")
        self.level_editor_object.imgui()
        imgui.end()

        imgui.begin("Objects")

        if imgui.begin_tab_bar("WindowTabBar"):
            if imgui.begin_tab_item("Blocks").selected:
                window_position = glm.fvec2(*imgui.get_window_position())
                window_size = glm.fvec2(*imgui.get_window_size())
                item_spacing = glm.fvec2(*imgui.get_style().item_spacing)

                window_x2 = window_position.x + window_size.x

                for i in range(self.sprites.size()):
                    if i == 34:
                        continue
                    if i >= 38 and i < 61:
                        continue

                    sprite = self.sprites.get_sprite(i)
                    sprite_width = sprite.get_width() * 2
                    sprite_height = sprite.get_height() * 2
                    sprite_id = sprite.get_tex_id()
                    tex_coords = sprite.get_tex_coords()

                    imgui.push_id(str(i))
                    if imgui.image_button(
                        sprite_id,
                        sprite_width,
                        sprite_height,
                        (tex_coords[2].x, tex_coords[0].y),
                        (tex_coords[0].x, tex_coords[2].y),
                    ):
                        game_object = Prefabs.generate_sprite_object(sprite, 0.25, 0.25)
                        rigid_body = RigidBody2D()
                        rigid_body.body_type = BodyType.STATIC
                        game_object.add_component(rigid_body)
                        box_2d_collider = Box2DCollider()
                        box_2d_collider.half_size = glm.fvec2(0.25, 0.25)
                        game_object.add_component(box_2d_collider)
                        game_object.add_component(Ground())

                        if i == 12:
                            game_object.add_component(BreakableBrick())

                        self.level_editor_object.get_component(
                            MouseControls
                        ).pickup_object(game_object)
                    imgui.pop_id()

                    last_button_pos = glm.fvec2(*imgui.get_item_rect_max())
                    last_button_x2 = last_button_pos.x
                    next_button_x2 = last_button_x2 + item_spacing.x + sprite_width

                    if i < self.sprites.size() and next_button_x2 <= window_x2:
                        imgui.same_line()

                imgui.end_tab_item()

            if imgui.begin_tab_item("Decoration Blocks").selected:
                window_position = glm.fvec2(*imgui.get_window_position())
                window_size = glm.fvec2(*imgui.get_window_size())
                item_spacing = glm.fvec2(*imgui.get_style().item_spacing)

                window_x2 = window_position.x + window_size.x

                for i in range(34, 61):
                    if i >= 35 and i < 38:
                        continue
                    if i >= 42 and i < 45:
                        continue

                    sprite = self.sprites.get_sprite(i)
                    sprite_width = sprite.get_width() * 2
                    sprite_height = sprite.get_height() * 2
                    sprite_id = sprite.get_tex_id()
                    tex_coords = sprite.get_tex_coords()

                    imgui.push_id(str(i))
                    if imgui.image_button(
                        sprite_id,
                        sprite_width,
                        sprite_height,
                        (tex_coords[2].x, tex_coords[0].y),
                        (tex_coords[0].x, tex_coords[2].y),
                    ):
                        game_object = Prefabs.generate_sprite_object(sprite, 0.25, 0.25)
                        self.level_editor_object.get_component(
                            MouseControls
                        ).pickup_object(game_object)
                    imgui.pop_id()

                    last_button_pos = glm.fvec2(*imgui.get_item_rect_max())
                    last_button_x2 = last_button_pos.x
                    next_button_x2 = last_button_x2 + item_spacing.x + sprite_width

                    if i < self.sprites.size() and next_button_x2 <= window_x2:
                        imgui.same_line()

                imgui.end_tab_item()

            if imgui.begin_tab_item("Prefabs").selected:
                uid = 0
                player_sprite = AssetPool.get_spritesheet(
                    "assets/images/spritesheet.jpg"
                )
                sprite = player_sprite.get_sprite(0)
                sprite_width = sprite.get_width() * 2
                sprite_height = sprite.get_height() * 2
                sprite_id = sprite.get_tex_id()
                tex_coords = sprite.get_tex_coords()

                imgui.push_id(str(uid))
                uid += 1
                if imgui.image_button(
                    sprite_id,
                    sprite_width,
                    sprite_height,
                    (tex_coords[2].x, tex_coords[0].y),
                    (tex_coords[0].x, tex_coords[2].y),
                ):
                    game_object = Prefabs.generate_mario()
                    self.level_editor_object.get_component(MouseControls).pickup_object(
                        game_object
                    )
                imgui.pop_id()
                imgui.same_line()

                item = AssetPool.get_spritesheet("assets/images/items.jpg")
                sprite = item.get_sprite(0)
                sprite_id = sprite.get_tex_id()
                tex_coords = sprite.get_tex_coords()

                imgui.push_id(str(uid))
                uid += 1
                if imgui.image_button(
                    sprite_id,
                    sprite_width,
                    sprite_height,
                    (tex_coords[2].x, tex_coords[0].y),
                    (tex_coords[0].x, tex_coords[2].y),
                ):
                    game_object = Prefabs.generate_question_block()
                    self.level_editor_object.get_component(MouseControls).pickup_object(
                        game_object
                    )
                imgui.pop_id()
                imgui.same_line()

                sprite = player_sprite.get_sprite(14)
                sprite_id = sprite.get_tex_id()
                tex_coords = sprite.get_tex_coords()

                imgui.push_id(str(uid))
                uid += 1
                if imgui.image_button(
                    sprite_id,
                    sprite_width,
                    sprite_height,
                    (tex_coords[2].x, tex_coords[0].y),
                    (tex_coords[0].x, tex_coords[2].y),
                ):
                    game_object = Prefabs.generate_goomba()
                    self.level_editor_object.get_component(MouseControls).pickup_object(
                        game_object
                    )
                imgui.pop_id()
                imgui.same_line()

                pipes = AssetPool.get_spritesheet("assets/images/pipes.jpg")
                sprite = pipes.get_sprite(0)
                sprite_id = sprite.get_tex_id()
                tex_coords = sprite.get_tex_coords()

                imgui.push_id(str(uid))
                uid += 1
                if imgui.image_button(
                    sprite_id,
                    sprite_width,
                    sprite_height,
                    (tex_coords[2].x, tex_coords[0].y),
                    (tex_coords[0].x, tex_coords[2].y),
                ):
                    game_object = Prefabs.generate_pipe(Direction.DOWN)
                    self.level_editor_object.get_component(MouseControls).pickup_object(
                        game_object
                    )
                imgui.pop_id()
                imgui.same_line()

                sprite = pipes.get_sprite(1)
                sprite_id = sprite.get_tex_id()
                tex_coords = sprite.get_tex_coords()

                imgui.push_id(str(uid))
                uid += 1
                if imgui.image_button(
                    sprite_id,
                    sprite_width,
                    sprite_height,
                    (tex_coords[2].x, tex_coords[0].y),
                    (tex_coords[0].x, tex_coords[2].y),
                ):
                    game_object = Prefabs.generate_pipe(Direction.UP)
                    self.level_editor_object.get_component(MouseControls).pickup_object(
                        game_object
                    )
                imgui.pop_id()
                imgui.same_line()

                sprite = pipes.get_sprite(2)
                sprite_id = sprite.get_tex_id()
                tex_coords = sprite.get_tex_coords()

                imgui.push_id(str(uid))
                uid += 1
                if imgui.image_button(
                    sprite_id,
                    sprite_width,
                    sprite_height,
                    (tex_coords[2].x, tex_coords[0].y),
                    (tex_coords[0].x, tex_coords[2].y),
                ):
                    game_object = Prefabs.generate_pipe(Direction.RIGHT)
                    self.level_editor_object.get_component(MouseControls).pickup_object(
                        game_object
                    )
                imgui.pop_id()
                imgui.same_line()

                sprite = pipes.get_sprite(3)
                sprite_id = sprite.get_tex_id()
                tex_coords = sprite.get_tex_coords()

                imgui.push_id(str(uid))
                uid += 1
                if imgui.image_button(
                    sprite_id,
                    sprite_width,
                    sprite_height,
                    (tex_coords[2].x, tex_coords[0].y),
                    (tex_coords[0].x, tex_coords[2].y),
                ):
                    game_object = Prefabs.generate_pipe(Direction.LEFT)
                    self.level_editor_object.get_component(MouseControls).pickup_object(
                        game_object
                    )
                imgui.pop_id()

                imgui.end_tab_item()

            if imgui.begin_tab_item("Sounds").selected:
                sounds = AssetPool.get_all_sounds()
                for sound in sounds:
                    if imgui.button(sound.file_path):
                        if not sound.is_playing:
                            sound.play()
                        else:
                            sound.stop()

                    if imgui.get_content_region_available()[0] > 100:
                        imgui.same_line()
                imgui.end_tab_item()

            imgui.end_tab_bar()

        imgui.end()
