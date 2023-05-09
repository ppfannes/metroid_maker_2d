import glm
import imgui
from observers.event_system import EventSystem
from observers.events.event_type import EventType
from observers.events.event import Event
from utils.mouse_listener import MouseListener


class GameViewWindow:
    def __init__(self):
        self._is_playing = False
        self._window_is_hovered = False

    def imgui(self):
        from metroid_maker.window import Window

        imgui.begin(
            "Game Viewport",
            flags=imgui.WINDOW_NO_SCROLLBAR
            | imgui.WINDOW_NO_SCROLL_WITH_MOUSE
            | imgui.WINDOW_MENU_BAR,
        )

        if imgui.begin_menu_bar():
            clicked_start, _ = imgui.menu_item(
                "Play", "", self._is_playing, not self._is_playing
            )
            clicked_stop, _ = imgui.menu_item(
                "Stop", "", not self._is_playing, self._is_playing
            )

            if clicked_start:
                self._is_playing = True
                EventSystem.notify(None, Event(EventType.GAME_ENGINE_START_PLAYING))

            if clicked_stop:
                self._is_playing = False
                EventSystem.notify(None, Event(EventType.GAME_ENGINE_STOP_PLAYING))

            imgui.end_menu_bar()

        window_size = self._get_largest_size_for_viewport()
        window_pos = self._get_centered_position_for_viewport(window_size)

        imgui.set_cursor_pos(window_pos)

        top_left = imgui.get_cursor_screen_pos()

        texture_id = Window.get_framebuffer().get_texture_id()
        imgui.image_button(texture_id, window_size[0], window_size[1], (0, 1), (1, 0))
        self._window_is_hovered = imgui.is_item_hovered()

        MouseListener.set_game_viewport_pos(glm.fvec2(*top_left))
        MouseListener.set_game_viewport_size(glm.fvec2(*window_size))

        imgui.end()

    def want_capture_mouse(self):
        return self._window_is_hovered

    def _get_largest_size_for_viewport(self):
        from metroid_maker.window import Window

        window_size = imgui.get_content_region_available()

        aspect_width = window_size.x
        aspect_height = aspect_width / Window.get_target_aspect_ratio()

        if aspect_height > window_size.y:
            aspect_height = window_size.y
            aspect_width = aspect_height * Window.get_target_aspect_ratio()

        return (aspect_width, aspect_height)

    def _get_centered_position_for_viewport(self, aspect_size):
        window_size = imgui.get_content_region_available()

        viewport_x = (window_size.x / 2.0) - (aspect_size[0] / 2.0)
        viewport_y = (window_size.y / 2.0) - (aspect_size[1] / 2.0)

        return (
            viewport_x + imgui.get_cursor_pos_x(),
            viewport_y + imgui.get_cursor_pos_y(),
        )
