from abc import ABC, abstractmethod

class Observer(ABC):

    @abstractmethod
    def on_notify(self, game_object, event):
        raise NotImplementedError
