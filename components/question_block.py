import glm
from enum import Enum
from components.block import Block
from components.state_machine import StateMachine


class BlockType(Enum):
    COIN = 0
    POWERUP = 1
    INVINCIBILITY = 2


class QuestionBlock(Block):
    def __init__(self):
        super().__init__()
        self.block_type = BlockType.COIN

    def player_hit(self, player_controller):
        match self.block_type:
            case BlockType.COIN:
                self.do_coin(player_controller)
            case BlockType.POWERUP:
                self.do_powerup(player_controller)
            case BlockType.INVINCIBILITY:
                self.do_invincibility(player_controller)

        state_machine = self.game_object.get_component(StateMachine)
        if state_machine is not None:
            state_machine.trigger("setInactive")
            self._active = False

    def do_invincibility(self, player_controller):
        pass

    def do_powerup(self, player_controller):
        if player_controller.is_small():
            self.spawn_mushroom()
        else:
            self.spawn_flower()

    def do_coin(self, player_controller):
        from metroid_maker.window import Window
        from metroid_maker.prefabs import Prefabs

        coin = Prefabs.generate_block_coin()
        coin.transform.position = glm.fvec2(self.game_object.transform.position)
        coin.transform.position.y += 0.25
        Window.get_scene().add_game_object_to_scene(coin)

    def spawn_mushroom(self):
        from metroid_maker.window import Window
        from metroid_maker.prefabs import Prefabs

        mushroom = Prefabs.generate_mushroom()
        mushroom.transform.position = glm.fvec2(self.game_object.transform.position)
        mushroom.transform.position.y += 0.25
        Window.get_scene().add_game_object_to_scene(mushroom)

    def spawn_flower(self):
        from metroid_maker.window import Window
        from metroid_maker.prefabs import Prefabs

        flower = Prefabs.generate_flower()
        flower.transform.position = glm.fvec2(self.game_object.transform.position)
        flower.transform.position.y += 0.25
        Window.get_scene().add_game_object_to_scene(flower)
