import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer
from editor.game_view_window import GameViewWindow
import OpenGL.GL as gl

class ImGuiLayer:

    def __init__(self, glfw_window: int):
        self._glfw_window = glfw_window
        self._glfw_renderer = None

    def init_imgui(self):
        imgui.create_context()
        self._glfw_renderer = GlfwRenderer(self._glfw_window, False)
        font_scaling_factor = self._fb_to_window_factor()

        io = self._glfw_renderer.io
        io.config_flags |= imgui.CONFIG_DOCKING_ENABLE
        io.fonts.clear()
        io.font_global_scale = 1.0 / font_scaling_factor

        io.fonts.add_font_from_file_ttf("assets/fonts/SEGOEUI.TTF", 20 * font_scaling_factor, glyph_ranges=io.fonts.get_glyph_ranges_latin())

        self._glfw_renderer.refresh_font_texture()

    def update(self, current_scene):
        imgui.new_frame()
        self.setup_dockspace()
        current_scene.scene_imgui()
        imgui.show_test_window()
        GameViewWindow.imgui()
        imgui.end()
        imgui.render()
        self._glfw_renderer.render(imgui.get_draw_data())

    def shutdown(self):
        self._glfw_renderer.shutdown()

    def process_inputs(self):
        self._glfw_renderer.process_inputs()

    def _fb_to_window_factor(self):
        window_width, window_height = glfw.get_window_size(self._glfw_window)
        framebuffer_width, framebuffer_height = glfw.get_framebuffer_size(self._glfw_window)
        return max(float(framebuffer_width) / window_width, float(framebuffer_height) / window_height)
    
    def setup_dockspace(self):
        from metroid_maker.window import Window
        window_flags = imgui.WINDOW_MENU_BAR | imgui.WINDOW_NO_DOCKING

        imgui.set_next_window_position(0.0, 0.0, imgui.ALWAYS)
        imgui.set_next_window_size(Window.get_width(), Window.get_height())
        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0.0)
        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0.0)
        window_flags |= imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE | \
                        imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_NAV_FOCUS
        
        imgui.begin("Dockspace Demo", True, window_flags)
        imgui.pop_style_var(2)

        imgui.dockspace(imgui.get_id("Dockspace"))
