import imgui

class GameViewWindow:

    @staticmethod
    def imgui():
        from metroid_maker.window import Window
        imgui.begin("Game Viewport", imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE)

        window_size = GameViewWindow.get_largest_size_for_viewport()
        window_pos = GameViewWindow.get_centered_position_for_viewport(window_size)

        imgui.set_cursor_pos(window_pos)
        texture_id = Window.get_framebuffer().get_texture_id()
        imgui.image(texture_id, window_size[0], window_size[1], (0, 1), (1, 0))

        imgui.end()

    @staticmethod
    def get_largest_size_for_viewport():
        from metroid_maker.window import Window#
        window_size = imgui.get_content_region_available()
        region_x, region_y = window_size.x - imgui.get_scroll_x(), window_size.y - imgui.get_scroll_y()

        aspect_width = region_x
        aspect_height = aspect_width / Window.get_target_aspect_ratio()

        if aspect_height > region_y:
            aspect_height = region_y
            aspect_width = aspect_height * Window.get_target_aspect_ratio()

        return (aspect_width, aspect_height)

    @staticmethod
    def get_centered_position_for_viewport(aspect_size):
        window_size = imgui.get_content_region_available()
        region_x, region_y = window_size.x - imgui.get_scroll_x(), window_size.y - imgui.get_scroll_y()

        viewport_x = (region_x / 2.0) - (aspect_size[0] / 2.0)
        viewport_y = (region_y / 2.0) - (aspect_size[1] / 2.0)

        return (viewport_x + imgui.get_cursor_pos_x(), viewport_y + imgui.get_cursor_pos_y())
