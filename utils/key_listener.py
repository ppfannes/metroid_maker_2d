from glfw.GLFW import GLFW_PRESS, GLFW_RELEASE

class KeyListener:

    _key_pressed = [False for _ in range(350)]

    @classmethod
    def key_callback(cls, window: int, key: int, scancode: int, action: int, mods: int):
        if action == GLFW_PRESS:
            cls._key_pressed[key] = True
        elif action == GLFW_RELEASE:
            cls._key_pressed[key] = False

    @classmethod
    def is_key_pressed(cls, key: int):
        return cls._key_pressed[key]
