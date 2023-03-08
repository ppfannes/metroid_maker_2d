from components.sprite_renderer import SpriteRenderer
from metroid_maker.game_object import GameObject
from renderer.render_batch import RenderBatch

class Renderer:

    _current_shader = None

    def __init__(self) -> None:
        self._MAX_BATCH_SIZE = 1000
        self._batches = []

    def add_game_object(self, game_object: GameObject):
        sprite_renderer: SpriteRenderer = game_object.get_component(SpriteRenderer)
        if sprite_renderer is not None:
            self._add_sprite_renderer(sprite_renderer)

    def _add_sprite_renderer(self, sprite_renderer):
        added = False

        for render_batch in self._batches:
            if render_batch.has_room() and render_batch.z_index() == sprite_renderer.game_object.z_index():
                texture = sprite_renderer.get_texture()

                if render_batch.has_texture(texture) or render_batch.has_texture_room() or texture is None:
                    render_batch.add_sprite(sprite_renderer)
                    added = True
                    break

        if not added:
            new_batch = RenderBatch(self._MAX_BATCH_SIZE, sprite_renderer.game_object.z_index())
            new_batch.start()
            self._batches.append(new_batch)
            new_batch.add_sprite(sprite_renderer)
            self._batches.sort()

    def render(self):
        Renderer._current_shader.use()
        for render_batch in self._batches:
            render_batch.render()

    @classmethod
    def bind_shader(cls, shader):
        cls._current_shader = shader

    @classmethod
    def get_bound_shader(cls):
        return cls._current_shader