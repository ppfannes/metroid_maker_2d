import imgui
import pickle
from components.component import Component
from components.transform import Transform


class GameObject:
    _ID_COUNTER = 0

    def __init__(self, name: str):
        self.name = name
        self._uid = GameObject._ID_COUNTER
        GameObject._ID_COUNTER += 1
        self._components = []
        self.transform = None
        self._do_serialize = True
        self._is_dead = False

    def destroy(self):
        self._is_dead = True
        for component in self._components:
            component.destroy()

    def get_component(self, component_class: Component):
        for component in self._components:
            if issubclass(component_class, component.__class__):
                return component

        return None

    def is_dead(self):
        return self._is_dead

    def remove_component(self, component_class: Component):
        for component in self._components:
            if issubclass(component_class, component.__class__):
                self._components.remove(component)
                return

    def add_component(self, component: Component):
        component.generate_id()
        self._components.append(component)
        component.game_object = self

    def editor_update(self, dt):
        for component in self._components:
            component.editor_update(dt)

    def update(self, dt: float):
        for component in self._components:
            component.update(dt)

    def start(self):
        for component in self._components:
            component.start()

    def copy(self):
        from components.sprite_renderer import SpriteRenderer
        from utils.asset_pool import AssetPool

        pickled_object = pickle.dumps(self)
        new_object = pickle.loads(pickled_object)

        new_object.generate_uid()

        for component in new_object._components:
            component.generate_id()

        sprite_renderer = new_object.get_component(SpriteRenderer)
        if sprite_renderer is not None and sprite_renderer.get_texture() is not None:
            sprite_renderer.set_texture(
                AssetPool.get_texture(sprite_renderer.get_texture().get_file_path())
            )

        return new_object

    def imgui(self):
        for component in self._components:
            expanded, _ = imgui.collapsing_header(component.__class__.__name__)
            if expanded:
                component.imgui()

    def get_uid(self):
        return self._uid

    def generate_uid(self):
        self._uid = GameObject._ID_COUNTER
        GameObject._ID_COUNTER += 1

    @classmethod
    def init(cls, max_id):
        cls._ID_COUNTER = max_id

    def get_all_components(self):
        return self._components

    def set_no_serialize(self):
        self._do_serialize = False

    def do_serialize(self):
        return self._do_serialize

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["transform"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        components = self._components
        for component in components:
            component.game_object = self
        self.transform = self.get_component(Transform)
