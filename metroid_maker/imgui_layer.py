import glfw
import imgui
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer
from editor.game_view_window import GameViewWindow
from editor.menu_bar import MenuBar
from editor.properties_window import PropertiesWindow
from editor.scene_hierarchy_window import SceneHierarchyWindow


class ImGuiLayer:
    def __init__(self, glfw_window: int, picking_texture):
        self._glfw_window = glfw_window
        self._glfw_renderer = None
        self._game_view_window = GameViewWindow()
        self._properties_window = PropertiesWindow(picking_texture)
        self._menu_bar = MenuBar()
        self._scene_hierarchy_window = SceneHierarchyWindow()

    def _fb_to_window_factor(self):
        window_width, window_height = glfw.get_window_size(self._glfw_window)
        framebuffer_width, framebuffer_height = glfw.get_framebuffer_size(
            self._glfw_window
        )
        return max(
            float(framebuffer_width) / window_width,
            float(framebuffer_height) / window_height,
        )

    def _keyboard_callback(self, window, key, scancode, action, mods):
        from utils.key_listener import KeyListener

        io: imgui._IO = self._glfw_renderer.io

        if action == glfw.PRESS:
            io.keys_down[key] = True
        elif action == glfw.RELEASE:
            io.keys_down[key] = False

        io.key_ctrl = (
            io.keys_down[glfw.KEY_LEFT_CONTROL] or io.keys_down[glfw.KEY_RIGHT_CONTROL]
        )

        io.key_alt = io.keys_down[glfw.KEY_LEFT_ALT] or io.keys_down[glfw.KEY_RIGHT_ALT]

        io.key_shift = (
            io.keys_down[glfw.KEY_LEFT_SHIFT] or io.keys_down[glfw.KEY_RIGHT_SHIFT]
        )

        io.key_super = (
            io.keys_down[glfw.KEY_LEFT_SUPER] or io.keys_down[glfw.KEY_RIGHT_SUPER]
        )

        if not io.want_capture_keyboard:
            KeyListener.key_callback(window, key, scancode, action, mods)

    def _char_callback(self, window, char):
        io: imgui._IO = imgui.get_io()

        if 0 < char < 0x10000:
            io.add_input_character(char)

    def _mouse_callback(self, window, button, action, mods):
        from utils.mouse_listener import MouseListener

        io: imgui._IO = self._glfw_renderer.io

        io.mouse_down[0] = button == glfw.MOUSE_BUTTON_1 and not action == glfw.RELEASE
        io.mouse_down[1] = button == glfw.MOUSE_BUTTON_2 and not action == glfw.RELEASE
        io.mouse_down[2] = button == glfw.MOUSE_BUTTON_3 and not action == glfw.RELEASE
        io.mouse_down[3] = button == glfw.MOUSE_BUTTON_4 and not action == glfw.RELEASE
        io.mouse_down[4] = button == glfw.MOUSE_BUTTON_5 and not action == glfw.RELEASE

        if not io.want_capture_mouse and io.mouse_down[1]:
            imgui.set_window_focus(None)

        if not io.want_capture_mouse or self._game_view_window.want_capture_mouse():
            MouseListener.mouse_button_callback(window, button, action, mods)

    def _scroll_callback(self, window, x_offset, y_offset):
        from utils.mouse_listener import MouseListener

        io = self._glfw_renderer.io
        io.mouse_wheel_horizontal = x_offset
        io.mouse_wheel = y_offset

        if not io.want_capture_mouse or self._game_view_window.want_capture_mouse():
            MouseListener.scroll_callback(window, x_offset, y_offset)

    def init_imgui(self):
        imgui.create_context()
        self._glfw_renderer = GlfwRenderer(self._glfw_window, False)
        font_scaling_factor = self._fb_to_window_factor()

        io = self._glfw_renderer.io
        io.config_flags |= imgui.CONFIG_DOCKING_ENABLE | imgui.CONFIG_VIEWPORTS_ENABLE

        glfw.set_key_callback(self._glfw_window, self._keyboard_callback)
        glfw.set_mouse_button_callback(self._glfw_window, self._mouse_callback)
        glfw.set_char_callback(self._glfw_window, self._char_callback)
        glfw.set_scroll_callback(self._glfw_window, self._scroll_callback)

        io.fonts.clear()
        io.font_global_scale = 1.0 / font_scaling_factor

        io.fonts.add_font_from_file_ttf(
            "assets/fonts/SEGOEUI.TTF",
            20 * font_scaling_factor,
            glyph_ranges=io.fonts.get_glyph_ranges_latin(),
        )

        self._glfw_renderer.refresh_font_texture()

    def update(self, dt, current_scene):
        imgui.new_frame()

        self.setup_dockspace()
        current_scene.imgui()
        self._game_view_window.imgui()
        self._properties_window.update(dt, current_scene)
        self._properties_window.imgui()
        self._scene_hierarchy_window.imgui()

        self.end_frame()

    def end_frame(self):
        from metroid_maker.window import Window

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        gl.glViewport(0, 0, Window.get_width(), Window.get_height())
        gl.glClearColor(0, 0, 0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        self._glfw_renderer.render(imgui.get_draw_data())

        backup_window_ptr = glfw.get_current_context()
        imgui.update_platform_windows()
        glfw.make_context_current(backup_window_ptr)

    def shutdown(self):
        self._glfw_renderer.shutdown()

    def process_inputs(self):
        self._glfw_renderer.process_inputs()

    def setup_dockspace(self):
        from metroid_maker.window import Window

        window_flags = imgui.WINDOW_MENU_BAR | imgui.WINDOW_NO_DOCKING

        main_viewport: imgui._ImGuiViewport = imgui.get_main_viewport()
        imgui.set_next_window_position(
            main_viewport.work_pos.x, main_viewport.work_pos.y
        )
        imgui.set_next_window_size(main_viewport.work_size.x, main_viewport.work_size.y)
        imgui.set_next_window_viewport(main_viewport.id)
        imgui.set_next_window_position(0.0, 0.0, imgui.ALWAYS)
        imgui.set_next_window_size(Window.get_width(), Window.get_height())
        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0.0)
        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0.0)
        window_flags |= (
            imgui.WINDOW_NO_TITLE_BAR
            | imgui.WINDOW_NO_COLLAPSE
            | imgui.WINDOW_NO_RESIZE
            | imgui.WINDOW_NO_MOVE
            | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
            | imgui.WINDOW_NO_NAV_FOCUS
        )

        imgui.begin("Dockspace Demo", True, window_flags)
        imgui.pop_style_var(2)

        imgui.dockspace(imgui.get_id("Dockspace"))

        self._menu_bar.imgui()

        imgui.end()

    def get_properties_window(self):
        return self._properties_window
