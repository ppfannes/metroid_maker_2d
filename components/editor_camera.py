import glfw
import glm
import math
from components.component import Component

class EditorCamera(Component):

    def __init__(self, camera):
        super().__init__()
        self._drag_debounce = 0.032
        self._level_editor_camera = camera
        self._click_origin = glm.fvec2()
        self._drag_sensitivity = 30.0
        self._scroll_sensitivity = 0.1
        self._lerp_time = 0.0
        self._reset = False

    def editor_update(self, dt):
        from utils.key_listener import KeyListener
        from utils.mouse_listener import MouseListener
        if MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_MIDDLE) and self._drag_debounce > 0:
            self._click_origin = glm.fvec2(MouseListener.get_ortho_x(), MouseListener.get_ortho_y())
            self._drag_debounce -= dt
            return
        
        if MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_MIDDLE):
            mouse_pos = glm.fvec2(MouseListener.get_ortho_x(), MouseListener.get_ortho_y())
            delta = glm.sub(glm.fvec2(mouse_pos), self._click_origin)
            self._level_editor_camera._position = glm.sub(self._level_editor_camera._position, glm.mul(glm.mul(delta, dt), self._drag_sensitivity))
            self._click_origin = glm.lerp(self._click_origin, mouse_pos, dt)

        if self._drag_debounce <= 0.0 and not MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_MIDDLE):
            self._drag_debounce = 0.1

        if MouseListener.get_scroll_y() != 0.0:
            add_zoom = pow(abs(MouseListener.get_scroll_y() * self._scroll_sensitivity), 1 / self._level_editor_camera.get_zoom())
            add_zoom *= -self._sign(MouseListener.get_scroll_y())
            self._level_editor_camera.add_zoom(add_zoom)

        if KeyListener.is_key_pressed(glfw.KEY_KP_DECIMAL):
            self._reset = True

        if self._reset:
            self._level_editor_camera._position = glm.lerp(self._level_editor_camera._position, glm.fvec2(), self._lerp_time)
            self._level_editor_camera.set_zoom(self._level_editor_camera.get_zoom() + \
                                               ((1.0 - self._level_editor_camera.get_zoom()) * self._lerp_time))
            self._lerp_time += 0.1 * dt

            if abs(self._level_editor_camera._position.x) <= 5.0 and abs(self._level_editor_camera._position.y) <= 5.0:
                self._lerp_time = 0.0
                self._level_editor_camera._position = glm.fvec2(0.0, 0.0)
                self._level_editor_camera.set_zoom(1.0)
                self._reset = False

    def _sign(self, value):
        return 0.0 if abs(value) == 0 else value / abs(value)
