from abc import ABC, abstractmethod
import imgui
import jsonpickle

from metroid_maker.game_object import GameObject
from renderer.renderer import Renderer

class Scene(ABC):

    def __init__(self, camera):
        self._is_running = False
        self._camera = camera
        self._game_objects = []
        self._renderer = Renderer(camera)
        self._active_game_object = None
        self._level_loaded = False

    def init(self):
        pass

    def start(self):
        for game_object in self._game_objects:
            game_object.start()
            self._renderer.add_game_object(game_object)
        self._is_running = True

    def add_game_object_to_scene(self, game_object: GameObject):
        if not self._is_running:
            self._game_objects.append(game_object)
        else:
            self._game_objects.append(game_object)
            game_object.start()
            self._renderer.add_game_object(game_object)
    
    @abstractmethod
    def update(self, dt: float):
        raise NotImplementedError

    def camera(self):
        return self._camera

    def scene_imgui(self):
        if self._active_game_object is not None:
            imgui.begin("Inspector")
            self._active_game_object.imgui()
            imgui.end()

        self.imgui()

    def imgui(self):
        pass

    def save_exit(self):
        with open("serialized.pickle", "w+") as file:
            file.write(jsonpickle.encode(self._game_objects, indent=4))

    def load(self):
        loaded_objects = None

        try:
            with open("serialized.pickle", "r") as file:
                loaded_objects = jsonpickle.decode(file.read())
        except IOError:
            return

        for obj in loaded_objects:
            self.add_game_object_to_scene(obj)

        self._level_loaded = True