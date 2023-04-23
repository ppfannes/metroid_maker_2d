import glm
from components.component import Component
from components.player_controller import PlayerController
from metroid_maker.direction import Direction
from glfw import KEY_W, KEY_A, KEY_S, KEY_D, KEY_DOWN, KEY_UP, KEY_LEFT, KEY_RIGHT


class Pipe(Component):
    def __init__(self, direction):
        self._direction = direction
        self._connecting_pipe_name = ""
        self._is_entrance = False
        self._connecting_pipe = None
        self._entrance_vector_tolerance = 0.9
        self._colliding_player = None

    def start(self):
        from metroid_maker.window import Window

        self._connecting_pipe = Window.get_scene().get_game_object_by_name(
            self._connecting_pipe_name
        )

    def update(self, dt):
        from utils.asset_pool import AssetPool
        from utils.key_listener import KeyListener

        if self._connecting_pipe is None:
            return

        if self._colliding_player is not None:
            player_entering = False

            match self._direction:
                case Direction.UP:
                    if (
                        KeyListener.is_key_pressed(KEY_DOWN)
                        or KeyListener.is_key_pressed(KEY_S)
                    ) and self._is_entrance:
                        player_entering = True
                case Direction.LEFT:
                    if (
                        KeyListener.is_key_pressed(KEY_RIGHT)
                        or KeyListener.is_key_pressed(KEY_D)
                    ) and self._is_entrance:
                        player_entering = True
                case Direction.RIGHT:
                    if (
                        KeyListener.is_key_pressed(KEY_LEFT)
                        or KeyListener.is_key_pressed(KEY_A)
                    ) and self._is_entrance:
                        player_entering = True
                case Direction.DOWN:
                    if (
                        KeyListener.is_key_pressed(KEY_UP)
                        or KeyListener.is_key_pressed(KEY_W)
                    ) and self._is_entrance:
                        player_entering = True

            if player_entering:
                self._colliding_player.set_position(
                    self._get_player_position(self._connecting_pipe)
                )
                AssetPool.get_sound("assets/sounds/pipe.ogg").play()

    def _get_player_position(self, pipe):
        pipe_component = pipe.get_component(Pipe)

        match pipe_component._direction:
            case Direction.UP:
                return glm.add(pipe.transform.position, glm.fvec2(0.0, 0.5))
            case Direction.LEFT:
                return glm.add(pipe.transform.position, glm.fvec2(-0.5, 0.0))
            case Direction.RIGHT:
                return glm.add(pipe.transform.position, glm.fvec2(0.5, 0.0))
            case Direction.DOWN:
                return glm.add(pipe.transform.position, glm.fvec2(0.0, -0.5))

    def begin_collision(self, colliding_object, contact, collision_normal):
        player_controller = colliding_object.get_component(PlayerController)

        if player_controller is not None:
            match self._direction:
                case Direction.UP:
                    if collision_normal.y < self._entrance_vector_tolerance:
                        return
                case Direction.RIGHT:
                    if collision_normal.x < self._entrance_vector_tolerance:
                        return
                case Direction.DOWN:
                    if collision_normal.y > -self._entrance_vector_tolerance:
                        return
                case Direction.LEFT:
                    if collision_normal.x > -self._entrance_vector_tolerance:
                        return

            self._colliding_player = player_controller

    def end_collision(self, colliding_object, contact, collision_normal):
        player_controller = colliding_object.get_component(PlayerController)

        if player_controller is not None:
            self._colliding_player = None

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_connecting_pipe"]
        del state["_entrance_vector_tolerance"]
        del state["_colliding_player"]
        return state

    def __setstate__(self, state):
        state["_connecting_pipe"] = None
        state["_entrance_vector_tolerance"] = 0.6
        state["_colliding_player"] = None
        self.__dict__.update(state)
