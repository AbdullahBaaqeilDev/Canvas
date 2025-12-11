from canvas import Canvas
from vector import Vector
from static import *


class Camera:
    def __init__(self, canves: Canvas) -> None:
        self.canves = canves
        self.zoom = 1
        self.offset = Vector(0, 0)
        self.cell_size = min(
            WINDOW_SIZE[0] / self.canves.w, WINDOW_SIZE[1] / self.canves.h
        )

    def adjust_zoom(self, value: int | float) -> None:
        new_zoom = self.zoom + value
        if new_zoom >= ZOOM_MIN and new_zoom <= ZOOM_MAX:
            self.zoom = new_zoom

    def move(self, value: Vector) -> None:
        self.offset += value

    def move_h(self, value: int) -> None:
        self.offset.x += value

    def move_v(self, value: int) -> None:
        self.offset.y += value

    def recenter(self) -> None:
        self.zoom = 1
        self.offset.x = 0
        self.offset.y = 0

    def to_local(self, pos: Vector) -> Vector:
        """Translate the given position to coordinates of a pixel in the canves"""

        x, y = pos
        x -= self.canves.rect.left + self.offset.x
        y -= self.canves.rect.top + self.offset.y

        x //= self.cell_size * self.zoom
        y //= self.cell_size * self.zoom

        return Vector(x, y)

    def to_world(self, pos: Vector, anchor: Anchor = "c") -> Vector:
        """Translate the given pixel position to coordinates relative to the window"""

        world_pos = Vector(*pos)

        # ---------- Handling the anchor ----------
        # Adding half of the cell size to one of the access
        # Scine if the anchor is one letter that means one of the (x, y) will be half the cell as a default
        if len(anchor) == 1:
            if anchor in {"n", "s", "c"}:
                world_pos.x += 0.5
            if anchor in {"e", "w", "c"}:
                world_pos.y += 0.5
        else:
            # I "n" in anchor the y value will be 0 (relative to the topleft of the cell) by default
            if "e" in anchor:
                world_pos.x += 1
            if "s" in anchor:
                world_pos.y += 1
            # If "w" in anchor the x value will be 0 (relative to the topleft of the cell) by default

        # ---------- Translating the space ----------
        world_pos.x = int(world_pos.x * self.cell_size * self.zoom + self.offset.x)
        world_pos.y = int(world_pos.y * self.cell_size * self.zoom + self.offset.y)

        return world_pos
