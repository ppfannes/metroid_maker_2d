from abc import ABC, abstractmethod
import glm
import imgui
import jsonpickle

from components.component import Component
from metroid_maker.camera import Camera
from metroid_maker.game_object import GameObject
from renderer.renderer import Renderer

class Scene(ABC):

    def __init__(self):
        self._is_running = False
        self._camera = Camera(glm.fvec2(-250.0, 0.0))
        self._game_objects = []
        self._renderer = Renderer()
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
    
    @abstractmethod
    def render(self):
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
        max_game_object_id = -1
        max_component_id = -1

        try:
            with open("serialized.pickle", "r") as file:
                loaded_objects = jsonpickle.decode(file.read())
        except IOError:
            return

        for obj in loaded_objects:
            self.add_game_object_to_scene(obj)

            for component in obj.get_all_components():
                if component.get_uid() > max_component_id:
                    max_component_id = component.get_uid()

            if obj.get_uid() > max_game_object_id:
                max_game_object_id = obj.get_uid()

        max_game_object_id += 1
        max_component_id += 1
        GameObject.init(max_game_object_id)
        Component.init(max_component_id)
        self._level_loaded = True
