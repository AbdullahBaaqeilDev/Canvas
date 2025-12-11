import pygame
from typing import Literal
from vector import Vector
from static import *


class InputManager:
    def __init__(self) -> None:
        # keyboard keys
        self.keys_pressed: set[int] = set()
        self.keys_held: set[int] = set()
        self.keys_released: set[int] = set()

        # mouse buttons
        self.mouse_pressed: set[int] = set()
        self.mouse_held: set[int] = set()
        self.mouse_released: set[int] = set()

        # mouse motion
        self.mouse_pos: Vector = Vector(0, 0)
        self.mouse_rel: Vector = Vector(0, 0)
        self.mouse_whl: Vector = Vector(0, 0)

    def is_mod_held(self, modifier: Literal["ctrl", "shift", " alt"]) -> bool:
        return STRING_TO_KEY_ID.get(modifier) in self.keys_held

    def is_mouse_button_pressed(self, button: Literal[0, 1, 2]) -> bool:
        return button in self.mouse_pressed

    def is_mouse_button_held(self, button: Literal[0, 1, 2]) -> bool:
        return button in self.mouse_held

    def is_mouse_button_released(self, button: Literal[0, 1, 2]) -> bool:
        return button in self.mouse_released

    def is_mouse_moved(self) -> bool:
        return self.mouse_rel.x or self.mouse_rel.y

    def is_key_pressed(self, key: str) -> bool:
        return STRING_TO_KEY_ID[key] in self.keys_pressed

    def is_key_held(self, key: str) -> bool:
        return STRING_TO_KEY_ID[key] in self.keys_held

    def is_key_released(self, key: str) -> bool:
        return STRING_TO_KEY_ID[key] in self.keys_released

    def keys_new_input(self) -> bool:
        return self.keys_pressed or self.keys_released

    def update(self):
        # Reset per-frame states
        self.keys_pressed.clear()
        self.keys_released.clear()
        self.mouse_pressed.clear()
        self.mouse_released.clear()
        self.mouse_rel = Vector(0, 0)
        self.mouse_wheel = Vector(0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            elif event.type == pygame.KEYDOWN:
                sc = event.scancode
                self.keys_pressed.add(sc)
                self.keys_held.add(sc)

            elif event.type == pygame.KEYUP:
                sc = event.scancode
                self.keys_released.add(sc)
                self.keys_held.discard(sc)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed.add(event.button)
                self.mouse_held.add(event.button)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_released.add(event.button)
                self.mouse_held.discard(event.button)

            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = Vector(*event.pos)
                self.mouse_rel = Vector(*event.rel)

            elif event.type == pygame.MOUSEWHEEL:
                self.mouse_wheel = Vector(event.x, event.y)
