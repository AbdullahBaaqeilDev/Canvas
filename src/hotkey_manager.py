from typing import Literal, Callable
from app_context import AppContext
from static import *


class HotkeyManager:
    def __init__(
        self,
        ctx: AppContext = None,
        trigger_mode: Literal["strict", "depth"] = "strict",
    ) -> None:
        self.ctx: AppContext = ctx
        self.mode = trigger_mode
        self.bindings: dict[frozenset, str] = {}  # Combo: Name
        self.actions: dict[str, Callable] = {}  # Name: Action

    def register_binding(self, name: str, combo: tuple) -> None:
        self.bindings[frozenset({STRING_TO_KEY_ID[key] for key in combo})] = name

    def register_action(self, name: str, action: Callable) -> None:
        self.actions[name] = action

    def trigger_action(self, name: str | None) -> None:
        if not name:
            raise LookupError(f"None is not a vaild name")

        if name not in self.actions:
            raise NotImplementedError(
                f"The action with name {name} hasn't been implemented"
            )

        self.actions[name](self.ctx)

    def update(self) -> None:
        # keys_down include held key and both keys pressed just now
        keys_down = self.ctx.input_manager.keys_held.copy()
        keys_down.update(self.ctx.input_manager.keys_pressed)
        keys_down = frozenset(keys_down)

        # would trigger the action if the only keys pressed are the action combo
        if self.mode == "strict":
            action_name = self.bindings.get(keys_down)
            if action_name != None and action_name in self.actions:
                self.trigger_action(action_name)
        # would trigger the action with more keys in the combo
        # e.g. when (ctrl + shift + s) is pressed it will trigger (ctrl + shift + s) over (ctrl + s)
        else:
            combos: tuple[frozenset] = sorted(
                self.bindings.keys(), key=lambda combo: -len(combo)
            )

            for combo in combos:
                if combo.issubset(keys_down):
                    action_name = self.bindings.get(combo)
                    if action_name and action_name in self.actions:
                        self.trigger_action(action_name)
