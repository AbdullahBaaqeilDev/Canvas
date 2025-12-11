import pygame
import numpy as np
from vector import Vector
from color import Color
from static import *


class Canvas:
    def __init__(self, size: WH = WINDOW_SIZE) -> None:
        self.surf = pygame.Surface(WINDOW_SIZE)
        self.rect = self.surf.get_rect()
        self.pixels: np.ndarray = np.zeros(size[::-1], dtype=np.int64)

    @property
    def w(self) -> int:
        return self.pixels.shape[0]

    @property
    def h(self) -> int:
        return self.pixels.shape[1]

    def is_inside(self, pos: Vector) -> bool:
        return 0 <= pos[0] < self.w and 0 <= pos[1] < self.h

    def get_at(self, pos: XY) -> RGBA:
        return self.pixels[pos[1]][pos[0]]

    def set_at(self, pos: XY, color: RGBA) -> None:
        """Change the color of the pixel with given position to the given color"""

        # assert self.is_inside(pos), f"The position given {pos} doesn't exist inside the canves"
        if not self.is_inside(pos):
            return

        col, row = pos
        self.pixels[row, col] = Color.tuple_to_int(color)

    def reset_pixels(self) -> None:
        """Resets all of the pixels colors to 0x00000000"""

        self.pixels: np.ndarray = np.zeros((self.h, self.w), dtype=np.int64)
