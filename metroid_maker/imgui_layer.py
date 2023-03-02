import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer
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
        io.fonts.clear()
        io.font_global_scale = 1.0 / font_scaling_factor

        io.fonts.add_font_from_file_ttf("assets/fonts/SEGOEUI.TTF", 20 * font_scaling_factor, io.fonts.get_glyph_ranges_latin())

        self._glfw_renderer.refresh_font_texture()

    def update(self, current_scene):
        imgui.new_frame()
        current_scene.scene_imgui()
        imgui.show_test_window()
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
