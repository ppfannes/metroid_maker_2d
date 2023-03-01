import glm
from glfw.GLFW import GLFW_PRESS, GLFW_RELEASE
import metroid_maker.window

class MouseListener:

    _x_pos = 0.0
    _y_pos = 0.0
    _last_x = 0.0
    _last_y = 0.0
    _scroll_x = 0.0
    _scroll_y = 0.0
    _mouse_button_pressed = [False for _ in range(5)]
    _is_dragging = False

    @classmethod
    def cursor_pos_callback(cls, window: int, x_pos: float, y_pos: float) -> None:
        cls._last_x, cls._last_y = cls._x_pos, cls._y_pos
        cls._x_pos, cls._y_pos = x_pos, y_pos
        cls._is_dragging = cls._mouse_button_pressed[0] or cls._mouse_button_pressed[1] or cls._mouse_button_pressed[2]

    @classmethod
    def mouse_button_callback(cls, window: int, button: int, action: int, mods: int) -> None:
        if action == GLFW_PRESS:
            if button < len(cls._mouse_button_pressed):
                cls._mouse_button_pressed[button] = True
        elif action == GLFW_RELEASE:
            if button < len(cls._mouse_button_pressed):
                cls._mouse_button_pressed[button] = False
                cls._is_dragging = False

    @classmethod
    def scroll_callback(cls, window: int, x_offset: float, y_offset: float) -> None:
        cls._scroll_x, cls._scroll_y = x_offset, y_offset

    @classmethod
    def end_frame(cls) -> None:
        cls._scroll_x, cls._scroll_y = 0, 0
        cls._last_x, cls._last_y = cls._x_pos, cls._y_pos

    @classmethod
    def get_x_pos(cls) -> float:
        return float(cls._x_pos)

    @classmethod
    def get_y_pos(cls) -> float:
        return float(cls._y_pos)

    @classmethod
    def get_dx(cls) -> float:
        return float(cls._last_x - cls._x_pos)

    @classmethod
    def get_dy(cls) -> float:
        return float(cls._last_y - cls._y_pos)

    @classmethod
    def get_scroll_x(cls) -> float:
        return float(cls._scroll_x)

    @classmethod
    def get_scroll_y(cls) -> float:
        return float(cls._scroll_y)

    @classmethod
    def get_is_dragging(cls) -> bool:
        return cls._is_dragging

    @classmethod
    def mouse_button_down(cls, button: int):
        return cls._mouse_button_pressed[button]
    
    @classmethod
    def get_ortho_x(cls):
        from metroid_maker.window import Window
        current_x = cls.get_x_pos()
        current_x = (current_x / Window.get_width()) * 2.0 - 1.0
        tmp = glm.vec4(current_x, 0.0, 0.0, 1.0)
        tmp2 = tmp * Window.get_scene().camera().get_inverse_projection()
        tmp3 = tmp2 * Window.get_scene().camera().get_inverse_view()
        current_x = tmp3.x
        print(current_x)

    @classmethod
    def get_ortho_y(cls):
        pass
