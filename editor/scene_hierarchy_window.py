import imgui
import pickle

import typing


if typing.TYPE_CHECKING:
    from typing import List

    from metroid_maker.game_object import GameObject


class SceneHierarchyWindow:
    _payload_drag_drop_type = "SceneHierarchy"

    def imgui(self):
        from metroid_maker.window import Window

        imgui.begin("Scene Hierarchy")

        game_objects: List[GameObject] = Window.get_scene().get_game_objects()

        index = 0

        for game_object in game_objects:
            if not game_object.do_serialize():
                continue

            tree_node_open = self._do_tree_node(game_object, index)

            if tree_node_open:
                imgui.tree_pop()

            index += 1

        imgui.end()

    def _do_tree_node(self, game_object, index):
        imgui.push_id(str(index))

        tree_node_open: bool = imgui.tree_node(
            game_object.name,
            imgui.TREE_NODE_DEFAULT_OPEN
            | imgui.TREE_NODE_FRAME_PADDING
            | imgui.TREE_NODE_OPEN_ON_ARROW
            | imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH,
        )

        imgui.pop_id()

        if imgui.begin_drag_drop_source():
            imgui.set_drag_drop_payload("itemtype", pickle.dumps(game_object))
            imgui.text(game_object.name)
            imgui.end_drag_drop_source()

        if imgui.begin_drag_drop_target():
            payload = imgui.accept_drag_drop_payload("itemtype")
            if payload is not None:
                depickled_payload = pickle.loads(payload)
                print(f"Payload accepted '{depickled_payload.name}'")
            imgui.end_drag_drop_target()

        return tree_node_open
