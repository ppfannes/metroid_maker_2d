from components.gizmo import Gizmo

class ScaleGizmo(Gizmo):

    def __init__(self, arrow_sprite, properties_window):
        super().__init__(arrow_sprite, properties_window)

    def editor_update(self, dt):
        from utils.mouse_listener import MouseListener
        if self._active_game_object is not None:
            if self._x_axis_active and not self._y_axis_active:
                self._active_game_object.transform.scale.x -= MouseListener.get_world_dx()
            elif self._y_axis_active:
                self._active_game_object.transform.scale.y -= MouseListener.get_world_dy()

        super().editor_update(dt)
