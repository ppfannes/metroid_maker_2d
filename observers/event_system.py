class EventSystem:

    _observers = []

    @classmethod
    def add_observer(cls, observer):
        cls._observers.append(observer)

    @classmethod
    def notify(cls, game_object, event):
        for observer in cls._observers:
            observer.on_notify(game_object, event)
