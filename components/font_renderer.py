from components.sprite_renderer import SpriteRenderer
from metroid_maker.component import Component

class FontRenderer(Component):

    def start(self):
        if self.game_object.get_component(SpriteRenderer)is not None:
            print("Found Font Renderer!")
    
    def update(self, dt: float):
        pass
