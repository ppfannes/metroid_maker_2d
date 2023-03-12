import glm
import imgui
from observers.event_system import EventSystem
from observers.events.event_type import EventType
from observers.events.event import Event
from utils.mouse_listener import MouseListener

class GameViewWindow:

    left_x = 0.0
    bottom_y = 0.0
    top_y = 0.0
    right_x = 0.0
    _is_playing = False

    def imgui(self):
        from metroid_maker.window import Window
        imgui.begin("Game Viewport", flags=imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE | imgui.WINDOW_MENU_BAR)

        if imgui.begin_menu_bar():
            clicked_start, _ = imgui.menu_item("Play", "", GameViewWindow._is_playing, not GameViewWindow._is_playing)
            clicked_stop, _ = imgui.menu_item("Stop", "", not GameViewWindow._is_playing, GameViewWindow._is_playing)
            
            if clicked_start:
                GameViewWindow._is_playing = True
                EventSystem.notify(None, Event(EventType.GAME_ENGINE_START_PLAYING))

            if clicked_stop:
                GameViewWindow._is_playing = False
                EventSystem.notify(None, Event(EventType.GAME_ENGINE_STOP_PLAYING))
            
            imgui.end_menu_bar()

        window_size = self._get_largest_size_for_viewport()
        window_pos = self._get_centered_position_for_viewport(window_size)

        imgui.set_cursor_pos(window_pos)

        tmp = imgui.get_cursor_screen_pos()
        top_left = (tmp.x - imgui.get_scroll_x(), tmp.y - imgui.get_scroll_y())
        GameViewWindow.left_x = top_left[0]
        GameViewWindow.bottom_y = top_left[1]
        GameViewWindow.right_x = top_left[0] + window_size[0]
        GameViewWindow.top_y = top_left[1] + window_size[1]

        texture_id = Window.get_framebuffer().get_texture_id()
        imgui.image(texture_id, window_size[0], window_size[1], (0, 1), (1, 0))

        MouseListener.set_game_viewport_pos(glm.fvec2(*top_left))
        MouseListener.set_game_viewport_size(glm.fvec2(*window_size))

        imgui.end()

    def want_capture_mouse(self):
        from utils.mouse_listener import MouseListener
        return MouseListener.get_x_pos() >= GameViewWindow.left_x and MouseListener.get_x_pos() <= GameViewWindow.right_x and \
                MouseListener.get_y_pos() >= GameViewWindow.bottom_y and MouseListener.get_y_pos() <= GameViewWindow.top_y

    def _get_largest_size_for_viewport(self):
        from metroid_maker.window import Window#
        window_size = imgui.get_content_region_available()
        region_x, region_y = window_size.x - imgui.get_scroll_x(), window_size.y - imgui.get_scroll_y()

        aspect_width = region_x
        aspect_height = aspect_width / Window.get_target_aspect_ratio()

        if aspect_height > region_y:
            aspect_height = region_y
            aspect_width = aspect_height * Window.get_target_aspect_ratio()

        return (aspect_width, aspect_height)

    
    def _get_centered_position_for_viewport(self, aspect_size):
        window_size = imgui.get_content_region_available()
        region_x, region_y = window_size.x - imgui.get_scroll_x(), window_size.y - imgui.get_scroll_y()

        viewport_x = (region_x / 2.0) - (aspect_size[0] / 2.0)
        viewport_y = (region_y / 2.0) - (aspect_size[1] / 2.0)

        return (viewport_x + imgui.get_cursor_pos_x(), viewport_y + imgui.get_cursor_pos_y())
