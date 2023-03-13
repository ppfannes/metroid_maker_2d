from abc import ABC, abstractmethod

class SceneInitializer(ABC):

    @abstractmethod
    def init(self, scene):
        raise NotImplementedError

    @abstractmethod
    def load_resources(self, scene):
        raise NotImplementedError

    @abstractmethod
    def imgui(self):
        raise NotImplementedError
