from dataclasses import dataclass
from typing import Dict

import imgui
from components.component import Component


@dataclass(eq=True, order=True, frozen=True)
class StateTrigger:
    state: str
    trigger: str


class StateMachine(Component):
    def __init__(self):
        super().__init__()
        self._state_transfers: Dict[StateTrigger, str] = {}
        self._states = []
        self._current_state = None
        self._default_state_title = ""

    def refresh_textures(self):
        for animation_state in self._states:
            animation_state.refresh_textures()

    def add_state_trigger(self, state_from, state_to, on_trigger):
        new_state_trigger = StateTrigger(state_from, on_trigger)
        self._state_transfers[new_state_trigger] = state_to

    def add_state(self, state):
        self._states.append(state)

    def set_default_state(self, animation_title):
        for animation_state in self._states:
            if animation_state.title == animation_title:
                self._default_state_title = animation_title

                if self._current_state is None:
                    self._current_state = animation_state
                    return

        print(f"Unable to find state {animation_title} in set default state.")

    def trigger(self, trigger: str):
        state_triggers = [
            state_trigger
            for state_trigger in self._state_transfers.keys()
            if state_trigger.state.title == self._current_state.title
            and state_trigger.trigger == trigger
        ]

        if len(state_triggers):
            if self._state_transfers.get(state_triggers[0]):
                for index, animation_state in enumerate(self._states):
                    if animation_state.title == self._state_transfers.get(
                        state_triggers[0]
                    ):
                        self._current_state = self._states[index]

        return

    def start(self):
        for animation_state in self._states:
            if animation_state.title == self._default_state_title:
                self._current_state = animation_state
                break

    def update(self, dt):
        from components.sprite_renderer import SpriteRenderer

        if self._current_state is not None:
            self._current_state.update(dt)
            sprite_renderer = self.game_object.get_component(SpriteRenderer)

            if sprite_renderer is not None:
                sprite_renderer.set_sprite(self._current_state.current_sprite)

    def editor_update(self, dt):
        from components.sprite_renderer import SpriteRenderer

        if self._current_state is not None:
            self._current_state.update(dt)
            sprite_renderer = self.game_object.get_component(SpriteRenderer)

            if sprite_renderer is not None:
                sprite_renderer.set_sprite(self._current_state.current_sprite)

    def imgui(self):
        for animation_state in self._states:
            changed, text = imgui.input_text("State: ", animation_state.title, 256)
            if changed:
                animation_state.title = text

            changed, ticked = imgui.checkbox("Does loop?", animation_state.does_loop)
            if changed:
                animation_state.does_loop = ticked

            for frame in animation_state.animation_frames:
                changed, value = imgui.drag_float(
                    f"Frame({animation_state.animation_frames.index(frame)}): ",
                    frame.frame_time,
                    0.01,
                )
                if changed:
                    frame.frame_time = value

    def __getstate__(self):
        state = self.__dict__.copy()
        state["_state_transfers_keys"] = list(state["_state_transfers"].keys())
        state["_state_transfers_values"] = list(state["_state_transfers"].values())
        state["_state_transfers"].clear()
        return state

    def __setstate__(self, state):
        state["_state_transfers"].update(
            list(zip(state["_state_transfers_keys"], state["_state_transfers_values"]))
        )
        del state["_state_transfers_keys"]
        del state["_state_transfers_values"]
        self.__dict__.update(state)
