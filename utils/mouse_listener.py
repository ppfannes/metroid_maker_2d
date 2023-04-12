import glm
from glfw.GLFW import GLFW_PRESS, GLFW_RELEASE


class MouseListener:
    _x_pos = 0.0
    _y_pos = 0.0
    _scroll_x = 0.0
    _scroll_y = 0.0
    _last_x = 0.0
    _last_y = 0.0
    _world_x = 0.0
    _world_y = 0.0
    _last_world_x = 0.0
    _last_world_y = 0.0
    _mouse_button_pressed = [False for _ in range(9)]
    _is_dragging = False
    _mouse_button_down = 0
    _game_viewport_pos = glm.fvec2(1.0)
    _game_viewport_size = glm.fvec2(1.0)

    @classmethod
    def cursor_pos_callback(cls, window: int, x_pos: float, y_pos: float) -> None:
        from metroid_maker.window import Window

        if not Window.get_imgui_layer().get_game_view_window().want_capture_mouse():
            cls.clear()

        if cls._mouse_button_down > 0:
            cls._is_dragging = True

        cls._last_x, cls._last_y = cls._x_pos, cls._y_pos
        cls._last_world_x, cls._last_world_y = cls._world_x, cls._world_y
        cls._x_pos, cls._y_pos = x_pos, y_pos

    @classmethod
    def mouse_button_callback(
        cls, window: int, button: int, action: int, mods: int
    ) -> None:
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

    @classmethod
    def get_x_pos(cls) -> float:
        return float(cls._x_pos)

    @classmethod
    def get_y_pos(cls) -> float:
        return float(cls._y_pos)

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
    def get_screen(cls):
        current_x = cls.get_x_pos() - cls._game_viewport_pos.x
        current_x = (current_x / cls._game_viewport_size.x) * 1920.0
        current_y = cls.get_y_pos() - cls._game_viewport_pos.y
        current_y = (1.0 - (current_y / cls._game_viewport_size.y)) * 1080.0

        return glm.fvec2(current_x, current_y)

    @classmethod
    def screen_to_world(cls, screen_coords):
        from metroid_maker.window import Window

        normalized_screen_coords = glm.fvec2(
            screen_coords.x / Window.get_width(), screen_coords.y / Window.get_height()
        )
        normalized_screen_coords = glm.sub(
            glm.mul(2.0, normalized_screen_coords), glm.fvec2(1.0)
        )
        camera = Window.get_scene().camera()
        tmp = glm.fvec4(
            normalized_screen_coords.x, normalized_screen_coords.y, 0.0, 1.0
        )
        inverse_view = glm.fmat4(camera.get_inverse_view())
        inverse_projection = glm.fmat4(camera.get_inverse_projection())
        tmp = glm.mul(glm.mul(inverse_view, inverse_projection), tmp)
        return glm.fvec2(tmp)

    @classmethod
    def world_to_screen(cls, world_coords):
        from metroid_maker.window import Window

        camera = Window.get_scene().camera()
        ndc_space_pos = glm.fvec4(world_coords.x, world_coords.y, 0.0, 1.0)
        view = camera.get_view_matrix()
        projection = camera.get_projection_matrix()
        ndc_space_pos = glm.mul(glm.mul(ndc_space_pos, projection), view)
        window_space = glm.mul(
            glm.fvec2(ndc_space_pos.x, ndc_space_pos.x), 1.0 / ndc_space_pos.w
        )
        window_space = glm.mul(glm.add(window_space, glm.fvec2(1.0)), 0.5)
        window_space = glm.mul(
            window_space, glm.fvec2(Window.get_width(), Window.get_height())
        )
        return glm.fvec2(window_space)

    @classmethod
    def get_screen_x(cls):
        return cls.get_screen().x

    @classmethod
    def get_screen_y(cls):
        return cls.get_screen().y

    @classmethod
    def get_world(cls):
        from metroid_maker.window import Window

        current_x = cls.get_x_pos() - cls._game_viewport_pos.x
        current_x = (current_x / cls._game_viewport_size.x) * 2.0 - 1.0
        current_y = cls.get_y_pos() - cls._game_viewport_pos.y
        current_y = (1.0 - (current_y / cls._game_viewport_size.y)) * 2.0 - 1.0
        tmp = glm.fvec4(current_x, current_y, 0.0, 1.0)

        camera = Window.get_scene().camera()
        inverse_view = glm.fmat4(camera.get_inverse_view())
        inverse_projection = glm.fmat4(camera.get_inverse_projection())
        tmp = glm.mul(glm.mul(inverse_view, inverse_projection), tmp)

        return glm.fvec2(tmp)

    @classmethod
    def get_world_x(cls):
        return cls.get_world().x

    @classmethod
    def get_world_y(cls):
        return cls.get_world().y

    @classmethod
    def set_game_viewport_pos(cls, game_viewport_pos):
        cls._game_viewport_pos = game_viewport_pos

    @classmethod
    def set_game_viewport_size(cls, game_viewport_size):
        cls._game_viewport_size = game_viewport_size

    @classmethod
    def clear(cls):
        cls._x_pos, cls._y_pos = 0.0, 0.0
        cls._scroll_x, cls._scroll_y = 0.0, 0.0
        cls._last_x, cls._last_y = 0.0, 0.0
        cls._mouse_button_down = 0
        cls._is_dragging = False
        cls._mouse_button_pressed[:] = [False for _ in cls._mouse_button_pressed]
