import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer

class ImGuiLayer:

    def __init__(self, glfw_window: int):
        self._glfw_window = glfw_window
        self._impl = None

    def init_imgui(self):
        imgui.create_context()
        self._impl = GlfwRenderer(self._glfw_window, False)
        font_scaling_factor = self._fb_to_window_factor()

        io = self._impl.io
        io.fonts.clear()
        io.font_global_scale = 1.0 / font_scaling_factor

        io.fonts.add_font_from_file_ttf("assets/fonts/SEGOEUI.TTF", 20 * font_scaling_factor, io.fonts.get_glyph_ranges_latin())

        self._impl.refresh_font_texture()

    def update(self, current_scene):
        imgui.new_frame()
        current_scene.scene_imgui()
        imgui.show_test_window()
        imgui.render()
        self._impl.render(imgui.get_draw_data())

    def shutdown(self):
        self._impl.shutdown()

    def process_inputs(self):
        self._impl.process_inputs()

    def _fb_to_window_factor(self):
        window_width, window_height = glfw.get_window_size(self._glfw_window)
        framebuffer_width, framebuffer_height = glfw.get_framebuffer_size(self._glfw_window)
        return max(float(framebuffer_width) / window_width, float(framebuffer_height) / window_height)
