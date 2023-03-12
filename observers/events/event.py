from observers.events.event_type import EventType

class Event:

    def __init__(self, event_type=EventType.USER_EVENT) -> None:
        self.type = event_type
