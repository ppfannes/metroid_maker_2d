import glm
import imgui

from components.rigid_body import RigidBody
from components.sprite_renderer import SpriteRenderer
from components.spritesheet import Spritesheet
from components.sprite import Sprite
from metroid_maker.camera import Camera
from metroid_maker.game_object import GameObject
from metroid_maker.scene import Scene
from metroid_maker.transform import Transform
from utils.asset_pool import AssetPool
from utils.mouse_listener import MouseListener

class LevelEditorScene(Scene):

    sprites = None
    obj1 = None

    def __init__(self):
        self._camera = Camera(glm.vec2(-250.0, 0.0))
        super().__init__(self._camera)
        self._obj1_sprite = None

    def init(self):
        self._load_resources()
        self.sprites = AssetPool.get_spritesheet("assets/images/decorations_and_blocks.jpg")

        if self._level_loaded:
            print(self._game_objects)
            self._active_game_object = self._game_objects[0]
            return

        self.obj1 = GameObject("Object 1", Transform(glm.vec2(200.0, 100.0), glm.vec2(256.0, 256.0)), 2)
        self._obj1_sprite = SpriteRenderer(color=glm.vec4(1.0, 0.0, 0.0, 1.0))
        self.obj1.add_component(self._obj1_sprite)
        self.obj1.add_component(RigidBody())
        self.add_game_object_to_scene(self.obj1)
        self._active_game_object = self.obj1

        obj2 = GameObject("Object 2", Transform(glm.vec2(400.0, 100.0), glm.vec2(256.0, 256.0)), 2)
        obj2_sprite_renderer = SpriteRenderer(sprite=Sprite(
            AssetPool.get_texture("assets/images/blend_image_2.jpg")
        ))
        obj2.add_component(obj2_sprite_renderer)
        self.add_game_object_to_scene(obj2)

    def _load_resources(self):
        AssetPool.get_shader("assets/shaders", "default")

        AssetPool.add_sprite_sheet("assets/images/decorations_and_blocks.jpg",
                                    Spritesheet(AssetPool.get_texture("assets/images/decorations_and_blocks.jpg"), 16, 16, 81, 0))

    def update(self, dt: float):
        MouseListener.get_ortho_x()

        for game_object in self._game_objects:
            game_object.update(dt)

        self._renderer.render()

    def imgui(self):
        imgui.begin("Test window")

        window_position = glm.vec2(*imgui.get_window_position())
        window_size = glm.vec2(*imgui.get_window_size())
        item_spacing = glm.vec2(*imgui.get_style().item_spacing)

        window_x2 = window_position.x + window_size.x

        for i in range(self.sprites.size()):
            sprite = self.sprites.get_sprite(i)
            sprite_width = sprite.get_width() * 4
            sprite_height = sprite.get_height() * 4
            sprite_id = sprite.get_tex_id()
            tex_coords = sprite.get_tex_coords()

            imgui.push_id(str(i))
            if imgui.image_button(sprite_id, sprite_width, sprite_height, tex_coords[0].to_tuple(), tex_coords[2].to_tuple()):
                print(f"Button {i} clicked")
            imgui.pop_id()

            last_button_pos = glm.vec2(*imgui.get_item_rect_max())
            last_button_x2 = last_button_pos.x
            next_button_x2 = last_button_x2 + item_spacing.x + sprite_width

            if i < self.sprites.size() and next_button_x2 <= window_x2:
                imgui.same_line()

        imgui.end()
