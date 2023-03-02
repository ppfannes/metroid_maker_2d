from components.component import Component
from metroid_maker.transform import Transform

class GameObject:
    def __init__(self, name: str, transform=Transform(), z_index=0):
        self._name = name
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
