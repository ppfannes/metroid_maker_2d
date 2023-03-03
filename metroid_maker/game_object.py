from components.component import Component
from metroid_maker.transform import Transform

class GameObject:

    _ID_COUNTER = 0

    def __init__(self, name: str, transform=Transform(), z_index=0):
        self._name = name
        self._uid = GameObject._ID_COUNTER
        GameObject._ID_COUNTER += 1
        self._components = []
        self.transform = transform
        self._z_index = z_index

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

    def z_index(self):
        return self._z_index

    def imgui(self):
        for component in self._components:
            component.imgui()

    def get_uid(self):
        return self._uid

    @classmethod
    def init(cls, max_id):
        cls._ID_COUNTER = max_id

    def get_all_components(self):
        return self._components
