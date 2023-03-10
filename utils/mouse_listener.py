import glm
from glfw.GLFW import GLFW_PRESS, GLFW_RELEASE

class MouseListener:

    _x_pos = 0.0
    _y_pos = 0.0
    _last_x = 0.0
    _last_y = 0.0
    _scroll_x = 0.0
    _scroll_y = 0.0
    _world_x = 0.0
    _world_y = 0.0
    _last_world_x = 0.0
    _last_world_y = 0.0
    _mouse_button_pressed = [False for _ in range(9)]
    _is_dragging = False
    _mouse_button_down = 0
    _game_viewport_pos = glm.fvec2()
    _game_viewport_size = glm.fvec2()

    @classmethod
    def cursor_pos_callback(cls, window: int, x_pos: float, y_pos: float) -> None:
        if cls._mouse_button_down > 0:
            cls._is_dragging = True

        cls._last_x, cls._last_y = cls._x_pos, cls._y_pos
        cls._last_world_x, cls._last_world_y = cls._world_x, cls._world_y
        cls._x_pos, cls._y_pos = x_pos, y_pos
        cls.calc_ortho_x()
        cls.calc_ortho_y()

    @classmethod
    def mouse_button_callback(cls, window: int, button: int, action: int, mods: int) -> None:
        if action == GLFW_PRESS:
            cls._mouse_button_down += 1
            if button < len(cls._mouse_button_pressed):
                cls._mouse_button_pressed[button] = True
        elif action == GLFW_RELEASE:
            cls._mouse_button_down -= 1
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
        cls._last_world_x, cls._last_world_y = cls._world_x, cls._world_y

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
    def get_world_dx(cls):
        return float(cls._last_world_x - cls._world_x)

    @classmethod
    def get_dy(cls) -> float:
        return float(cls._last_y - cls._y_pos)
    
    @classmethod
    def get_world_dy(cls):
        return float(cls._last_world_y - cls._world_y)

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
    def get_screen_x(cls):
        assert cls._game_viewport_size.x > 0.0
        current_x = cls.get_x_pos() - cls._game_viewport_pos.x
        current_x = (current_x / cls._game_viewport_size.x) * 1920.0

        return current_x
    
    @classmethod
    def get_screen_y(cls):
        assert cls._game_viewport_size.y > 0.0
        current_y = cls.get_y_pos() - cls._game_viewport_pos.y
        current_y = 1080.0 - (current_y / cls._game_viewport_size.y) * 1080.0

        return current_y
    
    @classmethod
    def calc_ortho_x(cls):
        from metroid_maker.window import Window
        assert cls._game_viewport_pos.x > 0.0
        current_x = cls.get_x_pos() - cls._game_viewport_pos.x
        current_x = (current_x / cls._game_viewport_size.x) * 2.0 - 1.0
        tmp = glm.fvec4(current_x, 0.0, 0.0, 1.0)

        camera = Window.get_scene().camera()
        view_projection = glm.mul(camera.get_inverse_view(), camera.get_inverse_projection())
        cls._world_x = (glm.mul(view_projection, tmp)).x
    
    @classmethod
    def get_ortho_x(cls):
        return cls._world_x
    
    @classmethod
    def calc_ortho_y(cls):
        from metroid_maker.window import Window
        assert cls._game_viewport_pos.y > 0.0
        current_y = cls.get_y_pos() - cls._game_viewport_pos.y
        current_y = (current_y / cls._game_viewport_size.y) * 2.0 - 1.0
        tmp = glm.fvec4(0.0, -current_y, 0.0, 1.0)
        
        camera = Window.get_scene().camera()
        view_projection = glm.mul(camera.get_inverse_view(), camera.get_inverse_projection())
        cls._world_y = (glm.mul(view_projection, tmp)).y

    @classmethod
    def get_ortho_y(cls):
        return cls._world_y
    
    @classmethod
    def set_game_viewport_pos(cls, game_viewport_pos):
        cls._game_viewport_pos = game_viewport_pos

    @classmethod
    def set_game_viewport_size(cls, game_viewport_size):
        cls._game_viewport_size = game_viewport_size
