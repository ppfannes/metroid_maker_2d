from components.block import Block
from utils.asset_pool import AssetPool


class BreakableBrick(Block):
    def player_hit(self, player_controller):
        if not player_controller.is_small():
            if AssetPool.get_sound("assets/sounds/break_block.ogg").is_playing:
                AssetPool.get_sound("assets/sounds/break_block.ogg").stop()
            AssetPool.get_sound("assets/sounds/break_block.ogg").play()
            self.game_object.destroy()
