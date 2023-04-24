from components.game_camera import GameCamera
from components.spritesheet import Spritesheet
from components.sprite_renderer import SpriteRenderer
from components.state_machine import StateMachine
from scenes.scene_initializer import SceneInitializer
from utils.asset_pool import AssetPool


class LevelSceneInitializer(SceneInitializer):
    def __init__(self):
        super().__init__()
        self.sprites = None
        self.camera_object = None

    def init(self, scene):
        self.sprites = AssetPool.get_spritesheet(
            "assets/images/decorations_and_blocks.jpg"
        )

        self.camera_object = scene.create_game_object("Game Camera")
        self.camera_object.add_component(GameCamera(scene.camera()))
        self.camera_object.start()
        scene.add_game_object_to_scene(self.camera_object)

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
        pass
