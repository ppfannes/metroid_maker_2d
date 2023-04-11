from components.frame import Frame
from components.sprite import Sprite


class AnimationState:
    def __init__(self):
        self.title = ""
        self.animation_frames = []
        self._default_sprite = Sprite()
        self._time_tracker = 0.0
        self._current_sprite = 0
        self._does_loop = False

    def refresh_textures(self):
        from utils.asset_pool import AssetPool

        for frame in self.animation_frames:
            frame.sprite.set_texture(
                AssetPool.get_texture(frame.sprite.get_texture().get_file_path())
            )

    def add_frame(self, sprite, frame_time):
        self.animation_frames.append(Frame(sprite, frame_time))

    @property
    def does_loop(self):
        return self._does_loop

    @does_loop.setter
    def does_loop(self, does_loop):
        self._does_loop = does_loop

    def update(self, dt):
        if self._current_sprite < len(self.animation_frames):
            self._time_tracker -= dt

            if self._time_tracker <= 0:
                if (
                    not self._current_sprite == len(self.animation_frames) - 1
                    or self._does_loop
                ):
                    self._current_sprite = (self._current_sprite + 1) % len(
                        self.animation_frames
                    )

                self._time_tracker = self.animation_frames[
                    self._current_sprite
                ].frame_time

    @property
    def current_sprite(self):
        if self._current_sprite < len(self.animation_frames):
            return self.animation_frames[self._current_sprite].sprite

        return self._default_sprite
