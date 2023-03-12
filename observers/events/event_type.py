from enum import Enum

class EventType(Enum):
    GAME_ENGINE_START_PLAYING = 0
    GAME_ENGINE_STOP_PLAYING = 1
    SAVE_LEVEL = 2
    LOAD_LEVEL = 3
    USER_EVENT = 4
