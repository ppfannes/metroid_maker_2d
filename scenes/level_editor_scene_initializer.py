import glm
import imgui

from components.editor_camera import EditorCamera
from components.gizmo_system import GizmoSystem
from components.grid_lines import GridLines
from components.mouse_controls import MouseControls
from components.sprite_renderer import SpriteRenderer
from components.spritesheet import Spritesheet
from metroid_maker.prefabs import Prefabs
from scenes.scene_initializer import SceneInitializer
from utils.asset_pool import AssetPool

class LevelEditorSceneInitializer(SceneInitializer):

    def __init__(self):
        super().__init__()
        self.sprites = None
        self.level_editor_object = None

    def init(self, scene):
        self.sprites = AssetPool.get_spritesheet("assets/images/decorations_and_blocks.jpg")
        gizmos = AssetPool.get_spritesheet("assets/images/gizmos.jpg")

        self.level_editor_object = scene.create_game_object("Level Editor")
        self.level_editor_object.set_no_serialize()
        self.level_editor_object.add_component(MouseControls())
        self.level_editor_object.add_component(GridLines())
        self.level_editor_object.add_component(EditorCamera(scene.camera()))
        self.level_editor_object.add_component(GizmoSystem(gizmos))
        scene.add_game_object_to_scene(self.level_editor_object)

    def load_resources(self, scene):
        AssetPool.get_shader("assets/shaders", "default")

        AssetPool.add_sprite_sheet("assets/images/decorations_and_blocks.jpg",
                                    Spritesheet(AssetPool.get_texture("assets/images/decorations_and_blocks.jpg"), 16, 16, 81, 0))
        AssetPool.add_sprite_sheet("assets/images/gizmos.jpg",
                                   Spritesheet(AssetPool.get_texture("assets/images/gizmos.jpg"), 24, 48, 3, 0))
        AssetPool.get_texture("assets/images/blend_image_2.jpg")

        for game_object in scene.get_game_objects():
            if game_object.get_component(SpriteRenderer) is not None:
                sprite_renderer = game_object.get_component(SpriteRenderer)
                
                if sprite_renderer.get_texture() is not None:
                    sprite_renderer.set_texture(AssetPool.get_texture(sprite_renderer.get_texture().get_file_path()))

    def imgui(self):
        imgui.begin("Level Editor Debug")
        self.level_editor_object.imgui()
        imgui.end()

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
                game_object = Prefabs.generate_sprite_object(sprite, 0.25, 0.25)
                self.level_editor_object.get_component(MouseControls).pickup_object(game_object)
            imgui.pop_id()

            last_button_pos = glm.fvec2(*imgui.get_item_rect_max())
            last_button_x2 = last_button_pos.x
            next_button_x2 = last_button_x2 + item_spacing.x + sprite_width

            if i < self.sprites.size() and next_button_x2 <= window_x2:
                imgui.same_line()

        imgui.end()
