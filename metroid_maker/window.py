import glfw
from glfw.GLFW import GLFW_FALSE, GLFW_TRUE, GLFW_RESIZABLE, GLFW_VISIBLE, GLFW_MAXIMIZED
import OpenGL.GL as gl

from metroid_maker.imgui_layer import ImGuiLayer
from renderer.debug_draw import DebugDraw
from scenes.level_editor_scene import LevelEditorScene
from scenes.level_scene import LevelScene
from utils.key_listener import KeyListener
from utils.mouse_listener import MouseListener
from utils.singleton import Singleton
from utils.time import Time


class Window(metaclass=Singleton):

    r, g, b, a, = 1, 1, 1, 1

    def __init__(self):
        self._width = 1920
        self._height = 1080
        self._title = "Metroid Maker 2D"
        self._glfw_window = None

        self._imgui_layer = None

        self._current_scene = None

    @staticmethod
    def get() -> 'Window':
        return Window()
    
    @classmethod
    def get_width(cls):
        return cls.get()._width
    
    @classmethod
    def get_height(cls):
        return cls.get()._height

    
    def change_scene(self, new_scene: int) -> None | ValueError:
        match new_scene:
            case 0:
                self._current_scene = LevelEditorScene()
            case 1:
                self._current_scene = LevelScene()
            case _:
                raise ValueError("Unknown scene '" + str(new_scene) +"'")
            
        self._current_scene.load()
        self._current_scene.init()
        self._current_scene.start()

    @classmethod
    def get_scene(cls):
        return cls.get()._current_scene
    
    @classmethod
    def set_height(cls, new_height):
        cls.get()._height = new_height

    @classmethod
    def set_width(cls, new_width):
        cls.get()._width = new_width

    @classmethod
    def resize_window_callback(cls, window, new_width, new_height):
        cls.get().set_width(new_width)
        cls.get().set_height(new_height)

    def run(self) -> None:
        self.init()
        self.loop()

        glfw.destroy_window(self._glfw_window)

        glfw.terminate()


    def init(self) -> None:

        if not glfw.init():
            raise RuntimeError("Unable to initialize GLFW.")
        
        glfw.default_window_hints()
        glfw.window_hint(GLFW_VISIBLE, GLFW_FALSE)
        glfw.window_hint(GLFW_RESIZABLE, GLFW_TRUE)
        glfw.window_hint(GLFW_MAXIMIZED, GLFW_TRUE)

        self._glfw_window = glfw.create_window(self._width, self._height, self._title, None, None)

        if not self._glfw_window:
            raise RuntimeError("Could not create the GLFW window.")

        glfw.make_context_current(self._glfw_window)
        glfw.set_cursor_pos_callback(self._glfw_window, MouseListener.cursor_pos_callback)
        glfw.set_mouse_button_callback(self._glfw_window, MouseListener.mouse_button_callback)
        glfw.set_scroll_callback(self._glfw_window, MouseListener.scroll_callback)
        glfw.set_key_callback(self._glfw_window, KeyListener.key_callback)
        glfw.set_window_size_callback(self._glfw_window, Window.resize_window_callback)

        glfw.swap_interval(1)

        glfw.show_window(self._glfw_window)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_ONE, gl.GL_ONE_MINUS_SRC_ALPHA)

        self._imgui_layer = ImGuiLayer(self._glfw_window)
        self._imgui_layer.init_imgui()

        self.change_scene(0)


    def loop(self) -> None:
        start_time = Time.get_time()
        end_time = Time.get_time()
        dt = -1.0

        while not glfw.window_should_close(self._glfw_window):
            glfw.poll_events()
            self._imgui_layer.process_inputs()

            DebugDraw.begin_frame()

            gl.glClearColor(self.r, self.g, self.b, self.a)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            if dt >= 0:
                DebugDraw.draw()
                self._current_scene.update(dt)

            self._imgui_layer.update(self._current_scene)
            glfw.swap_buffers(self._glfw_window)

            end_time = Time.get_time()
            dt = end_time - start_time
            start_time = end_time

        self._current_scene.save_exit()
        self._imgui_layer.shutdown()
