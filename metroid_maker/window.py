import time
import glfw
from glfw.GLFW import (
    GLFW_FALSE,
    GLFW_TRUE,
    GLFW_RESIZABLE,
    GLFW_VISIBLE,
    GLFW_MAXIMIZED,
)
import OpenGL.GL as gl
import openal.alc as alc
import openal.al as al

from metroid_maker.imgui_layer import ImGuiLayer
from observers.event_system import EventSystem
from observers.events.event_type import EventType
from observers.observer import Observer
from renderer.debug_draw import DebugDraw
from renderer.framebuffer import Framebuffer
from renderer.picking_texture import PickingTexture
from scenes.level_editor_scene_initializer import LevelEditorSceneInitializer
from scenes.scene import Scene
from utils.key_listener import KeyListener
from utils.mouse_listener import MouseListener


class Window(Observer):
    _instance = None

    def __init__(self):
        if Window._instance is not None:
            raise Exception("Singleton")
        else:
            Window._instance = self
        self._width = 1920
        self._height = 1080
        self._title = "Metroid Maker 2D"
        self._glfw_window = None

        self._imgui_layer = None
        self._framebuffer = None
        self._picking_texture = None

        self._current_scene = None
        self._runtime_playing = False
        EventSystem.add_observer(self)

    @staticmethod
    def get():
        if Window._instance is None:
            Window()
        return Window._instance

    @classmethod
    def get_width(cls):
        return cls.get()._width

    @classmethod
    def get_height(cls):
        return cls.get()._height

    def change_scene(self, scene_initializer):
        if self._current_scene is not None:
            self._current_scene.destroy()

        self.get_imgui_layer().get_properties_window().set_active_game_object(None)
        self._current_scene = Scene(scene_initializer)
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

    @classmethod
    def get_framebuffer(cls):
        return cls.get()._framebuffer

    @staticmethod
    def get_target_aspect_ratio():
        return 16.0 / 9.0

    @classmethod
    def get_imgui_layer(cls):
        return cls.get()._imgui_layer

    def on_notify(self, game_object, event):
        match event.type:
            case EventType.GAME_ENGINE_START_PLAYING:
                self._runtime_playing = True
                self._current_scene.save()
                self.change_scene(LevelEditorSceneInitializer())
            case EventType.GAME_ENGINE_STOP_PLAYING:
                self._runtime_playing = False
                self.change_scene(LevelEditorSceneInitializer())
            case EventType.SAVE_LEVEL:
                self._current_scene.save()
            case EventType.LOAD_LEVEL:
                self.change_scene(LevelEditorSceneInitializer())

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

        self._glfw_window = glfw.create_window(
            self._width, self._height, self._title, None, None
        )

        if not self._glfw_window:
            raise RuntimeError("Could not create the GLFW window.")

        glfw.make_context_current(self._glfw_window)
        glfw.set_cursor_pos_callback(
            self._glfw_window, MouseListener.cursor_pos_callback
        )
        glfw.set_mouse_button_callback(
            self._glfw_window, MouseListener.mouse_button_callback
        )
        glfw.set_scroll_callback(self._glfw_window, MouseListener.scroll_callback)
        glfw.set_key_callback(self._glfw_window, KeyListener.key_callback)
        glfw.set_window_size_callback(self._glfw_window, Window.resize_window_callback)

        glfw.swap_interval(1)

        glfw.show_window(self._glfw_window)

        default_device_name = None
        audio_device = alc.alcOpenDevice(default_device_name)

        attributes = None
        audio_context = alc.alcCreateContext(audio_device, attributes)
        alc.alcMakeContextCurrent(audio_context)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_ONE, gl.GL_ONE_MINUS_SRC_ALPHA)

        self._framebuffer = Framebuffer(1920, 1080)
        self._picking_texture = PickingTexture(1920, 1080)
        gl.glViewport(0, 0, 1920, 1080)

        self._imgui_layer = ImGuiLayer(self._glfw_window, self._picking_texture)
        self._imgui_layer.init_imgui()

        self.change_scene(LevelEditorSceneInitializer())

    def loop(self) -> None:
        from utils.asset_pool import AssetPool
        from renderer.renderer import Renderer

        start_time = time.perf_counter_ns() * 1e-9
        end_time = time.perf_counter_ns() * 1e-9
        dt = -1.0

        default_shader = AssetPool.get_shader("assets/shaders", "default")
        picking_shader = AssetPool.get_shader("assets/shaders", "picking")

        while not glfw.window_should_close(self._glfw_window):
            glfw.poll_events()
            self._imgui_layer.process_inputs()

            gl.glDisable(gl.GL_BLEND)
            self._picking_texture.enable_writing()

            gl.glViewport(0, 0, 1920, 1080)
            gl.glClearColor(0.0, 0.0, 0.0, 0.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

            Renderer.bind_shader(picking_shader)
            self._current_scene.render()

            self._picking_texture.disable_writing()
            gl.glEnable(gl.GL_BLEND)

            DebugDraw.begin_frame()

            self._framebuffer.bind()

            gl.glClearColor(1.0, 1.0, 1.0, 1.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            if dt >= 0:
                Renderer.bind_shader(default_shader)
                if self._runtime_playing:
                    self._current_scene.update(dt)
                else:
                    self._current_scene.editor_update(dt)
                self._current_scene.render()
                DebugDraw.draw()
            self._framebuffer.unbind()

            self._imgui_layer.update(dt, self._current_scene)
            MouseListener.end_frame()
            glfw.swap_buffers(self._glfw_window)

            end_time = time.perf_counter_ns() * 1e-9
            dt = end_time - start_time
            start_time = end_time

        self._imgui_layer.shutdown()
