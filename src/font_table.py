import pygame
from static import *


class FontTable:
    def __init__(self) -> None:
        # A map indecating which sizes of this font are avaliable (e.g. Arail: [16, 18, 32])
        self.sizes_map: dict[str, list[int]] = {}

        # A map with a font name and font object
        self.table: dict[str, list[pygame.font.Font]] = {}

    def load(self, name: str, size: int) -> pygame.font.Font:
        if not self.is_loaded(name, size):
            font = pygame.font.SysFont(name, size)

            if name not in self.sizes_map.keys():
                self.sizes_map[name] = []
                self.table[name] = []

            self.sizes_map[name].append(size)
            self.table[name].append(font)
        else:
            for i, stored_size in enumerate(self.sizes_map[name]):
                if stored_size == size:
                    font = self.table[name][i]

        return font

    def unload(self, name: str, size: int | None) -> None:
        # if the size is None remove all the fonts from that family
        if size == None:
            self.sizes_map.pop(name)
            self.table.pop(name)
            return

        for i, stored_size in enumerate(self.sizes_map[name]):
            if stored_size == size:
                self.sizes_map[name].pop(i)
                self.table[name].pop(i)
                break

    def is_loaded(self, name: str, size: int) -> bool:
        if name in self.sizes_map.keys():
            if size in self.sizes_map[name]:
                return True
