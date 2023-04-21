import glm
import jsonpickle

from components.component import Component
from components.transform import Transform
from metroid_maker.camera import Camera
from metroid_maker.game_object import GameObject
from physics2d.physics2d import Physics2D
from renderer.renderer import Renderer


class Scene:
    def __init__(self, scene_initializer):
        self._is_running = False
        self._camera = None
        self._game_objects = []
        self._pending_objects = []
        self._renderer = Renderer()
        self._active_game_object = None
        self._scene_initializer = scene_initializer
        self._physics2d = Physics2D()

    def get_physics(self):
        return self._physics2d

    def destroy(self):
        for game_object in self._game_objects:
            game_object.destroy()

    def init(self):
        self._camera = Camera(glm.fvec2(0.0))
        self._scene_initializer.load_resources(self)
        self._scene_initializer.init(self)

    def start(self):
        for game_object in self._game_objects:
            game_object.start()
            self._renderer.add_game_object(game_object)
            self._physics2d.add(game_object)
        self._is_running = True

    def add_game_object_to_scene(self, game_object: GameObject):
        if not self._is_running:
            self._game_objects.append(game_object)
        else:
            self._pending_objects.append(game_object)

    def editor_update(self, dt):
        self._camera.adjust_projection()

        self._game_objects[:] = [
            game_object
            for game_object in self._game_objects
            if not self._process_dead_game_object(game_object)
        ]

        for game_object in self._game_objects:
            game_object.editor_update(dt)

        for game_object in self._pending_objects:
            self._game_objects.append(game_object)
            game_object.start()
            self._renderer.add_game_object(game_object)
            self._physics2d.add(game_object)

        self._pending_objects.clear()

    def update(self, dt: float):
        self._camera.adjust_projection()
        self._physics2d.update(dt)

        self._game_objects[:] = [
            game_object
            for game_object in self._game_objects
            if not self._process_dead_game_object(game_object)
        ]

        for game_object in self._game_objects:
            game_object.update(dt)

        for game_object in self._pending_objects:
            self._game_objects.append(game_object)
            game_object.start()
            self._renderer.add_game_object(game_object)
            self._physics2d.add(game_object)

        self._pending_objects.clear()

    def _process_dead_game_object(self, game_object):
        if game_object.is_dead():
            self._renderer.destroy_game_object(game_object)
            self._physics2d.destroy_game_object(game_object)
            return True
        return False

    def render(self):
        self._renderer.render()

    def camera(self):
        return self._camera

    def imgui(self):
        self._scene_initializer.imgui()

    def get_game_object(self, game_object_id):
        return next(
            filter(
                lambda game_object: game_object.get_uid() == game_object_id,
                self._game_objects,
            ),
            None,
        )

    def get_game_objects(self):
        return self._game_objects

    def save(self):
        with open("serialized.pickle", "w+") as file:
            objects_to_serialize = [
                game_object
                for game_object in self._game_objects
                if game_object.do_serialize()
            ]
            file.write(jsonpickle.encode(objects_to_serialize, indent=4))

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

    def create_game_object(self, name):
        game_object = GameObject(name)
        game_object.add_component(Transform())
        game_object.transform = game_object.get_component(Transform)
        return game_object
