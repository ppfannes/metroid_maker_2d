import imgui
from components.component import Component
from components.transform import Transform

class GameObject:

    _ID_COUNTER = 0

    def __init__(self, name: str):
        self._name = name
        self._uid = GameObject._ID_COUNTER
        GameObject._ID_COUNTER += 1
        self._components = []
        self.transform = None
        self._do_serialize = True

    def get_component(self, component_class: Component):
        for component in self._components:
            if issubclass(component_class, component.__class__):
                return component

        return None

    def remove_component(self, component_class: Component):
        for component in self._components:
            if issubclass(component_class, component.__class__):
                self._components.remove(component)
                return

    def add_component(self, component: Component):
        component.generate_id()
        self._components.append(component)
        component.game_object = self

    def update(self, dt: float):
        for component in self._components:
            component.update(dt)

    def start(self):
        for component in self._components:
            component.start()

    def imgui(self):
        for component in self._components:
            expanded, _ = imgui.collapsing_header(component.__class__.__name__)
            if expanded:
                component.imgui()

    def get_uid(self):
        return self._uid

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
        self.transform = self.get_component(Transform)
