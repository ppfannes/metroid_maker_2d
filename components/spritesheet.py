import glm
from components.sprite import Sprite

class Spritesheet:
    def __init__(self, texture, sprite_width, sprite_height, num_sprites, spacing):
        self._sprites = []
        self._texture = texture

        current_x = 0
        current_y = texture.get_height() - sprite_height

        for _ in range(num_sprites):
            top_y = (current_y + sprite_height) / texture.get_height()
            right_x = (current_x + sprite_width) / texture.get_width()
            left_x = current_x / texture.get_width()
            bottom_y = current_y / texture.get_height()

            tex_coords = [
                glm.vec2(right_x, top_y),
                glm.vec2(right_x, bottom_y),
                glm.vec2(left_x, bottom_y),
                glm.vec2(left_x, top_y)
            ]

            sprite = Sprite(sprite_width, sprite_height, self._texture, tex_coords)
            self._sprites.append(sprite)

            current_x += sprite_width + spacing

            if current_x >= texture.get_width():
                current_x = 0
                current_y -= sprite_height + spacing

    def get_sprite(self, index):
        return self._sprites[index]
    
    def size(self):
        return len(self._sprites)
