from components.component import Component


class Flagpole(Component):
    def __init__(self, is_top):
        super().__init__()
        self._is_top = is_top

    def begin_collision(self, colliding_object, contact, collision_normal):
        from components.player_controller import PlayerController

        player_controller = colliding_object.get_component(PlayerController)
        if player_controller is not None:
            player_controller.play_win_animation(self.game_object)
