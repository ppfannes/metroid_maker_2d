import glm
import imgui

from components.grid_lines import GridLines
from components.mouse_controls import MouseControls
from components.rigid_body import RigidBody
from components.sprite_renderer import SpriteRenderer
from components.spritesheet import Spritesheet
from components.sprite import Sprite
from metroid_maker.camera import Camera
from metroid_maker.game_object import GameObject
from metroid_maker.prefabs import Prefabs
from metroid_maker.transform import Transform
from renderer.debug_draw import DebugDraw
from scenes.scene import Scene
from utils.asset_pool import AssetPool

class LevelEditorScene(Scene):

    sprites = None
    obj1 = None
    level_editor_object = GameObject("Level Editor")

    def __init__(self):
        self._camera = Camera(glm.fvec2(-250.0, 0.0))
        super().__init__(self._camera)
        self._obj1_sprite = None

    def init(self):
        self.level_editor_object.add_component(MouseControls())
        self.level_editor_object.add_component(GridLines())
        self._load_resources()
        self.sprites = AssetPool.get_spritesheet("assets/images/decorations_and_blocks.jpg")

        if self._level_loaded:
            if len(self._game_objects) > 0:
                print(self._game_objects)
                self._active_game_object = self._game_objects[0]
            return

        # self.obj1 = GameObject("Object 1", Transform(glm.fvec2(200.0, 100.0), glm.fvec2(256.0, 256.0)), 2)
        # self._obj1_sprite = SpriteRenderer(color=glm.fvec4(1.0, 0.0, 0.0, 1.0))
        # self.obj1.add_component(self._obj1_sprite)
        # self.obj1.add_component(RigidBody())
        # self.add_game_object_to_scene(self.obj1)
        # self._active_game_object = self.obj1

        # obj2 = GameObject("Object 2", Transform(glm.fvec2(400.0, 100.0), glm.fvec2(256.0, 256.0)), 2)
        # obj2_sprite_renderer = SpriteRenderer(sprite=Sprite(
        #     texture=AssetPool.get_texture("assets/images/blend_image_2.jpg")
        # ))
        # obj2.add_component(obj2_sprite_renderer)
        # self.add_game_object_to_scene(obj2)

    def _load_resources(self):
        AssetPool.get_shader("assets/shaders", "default")

        AssetPool.add_sprite_sheet("assets/images/decorations_and_blocks.jpg",
                                    Spritesheet(AssetPool.get_texture("assets/images/decorations_and_blocks.jpg"), 16, 16, 81, 0))
        AssetPool.get_texture("assets/images/blend_image_2.jpg")

        for game_object in self._game_objects:
            if game_object.get_component(SpriteRenderer) is not None:
                sprite_renderer = game_object.get_component(SpriteRenderer)
                
                if sprite_renderer.get_texture() is not None:
                    sprite_renderer.set_texture(AssetPool.get_texture(sprite_renderer.get_texture().get_file_path()))

    def update(self, dt: float):
        self.level_editor_object.update(dt)

        for game_object in self._game_objects:
            game_object.update(dt)

        self._renderer.render()

    def imgui(self):
        imgui.begin("Test window")

        window_position = glm.fvec2(*imgui.get_window_position())
        window_size = glm.fvec2(*imgui.get_window_size())
        item_spacing = glm.fvec2(*imgui.get_style().item_spacing)

        window_x2 = window_position.x + window_size.x

        for i in range(self.sprites.size()):
            sprite = self.sprites.get_sprite(i)
            sprite_width = sprite.get_width() * 2
            sprite_height = sprite.get_height() * 2
            sprite_id = sprite.get_tex_id()
            tex_coords = sprite.get_tex_coords()

            imgui.push_id(str(i))
            if imgui.image_button(sprite_id, sprite_width, sprite_height, (tex_coords[2].x, tex_coords[0].y), (tex_coords[0].x, tex_coords[2].y)):
                game_object = Prefabs.generate_sprite_object(sprite, 32, 32)
                self.level_editor_object.get_component(MouseControls).pickup_object(game_object)
            imgui.pop_id()

            last_button_pos = glm.fvec2(*imgui.get_item_rect_max())
            last_button_x2 = last_button_pos.x
            next_button_x2 = last_button_x2 + item_spacing.x + sprite_width

            if i < self.sprites.size() and next_button_x2 <= window_x2:
                imgui.same_line()

        imgui.end()
