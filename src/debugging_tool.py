import pygame
from typing import Any
from color_table import ColorTable
from app_context import AppContext
from vector import Vector
from static import *


def draw_marker(surf: pygame.Surface, center: Vector, radius: int, color: RGB) -> None:
    """The pos is window pixels coordinates"""

    pygame.draw.circle(surf, color, (center.x, center.y), radius)


def draw_ruler(
    surf: pygame.Surface, point_a: Vector, point_b: Vector, color: RGB
) -> None:
    """The points A & B is window pixels coordinates"""

    # A line between the points
    pygame.draw.line(
        surf,
        color,
        (point_a.x, point_a.y),
        (point_b.x, point_b.y),
    )

    # A marker at point A
    pygame.draw.circle(
        surf,
        color,
        (point_a.x, point_a.y),
        RULER_POINT_RADIUS,
    )

    # A marker at point B
    pygame.draw.circle(
        surf,
        color,
        (point_b.x, point_b.y),
        RULER_POINT_RADIUS,
    )


def debug(info: Any = None, x: int = 0, y: int = 0) -> None:
    font = pygame.font.Font(None, 24)
    surf = font.render(info.__str__(), True, "white", "black")
    rect = surf.get_rect(topleft=(x, y))

    screen = pygame.display.get_surface()
    screen.blit(surf, rect)


class DebuggingTool:
    def __init__(self, color_table: ColorTable, ctx: AppContext = None) -> None:
        self.ctx = ctx
        self.screen = pygame.display.get_surface()

        self.markers: set[Vector] = set()
        self.ruler: list[Vector | None, Vector | None] = [None, None]
        self.ruler_ready = False

        # Color
        self.markers_colors = color_table["fg_highlight"]
        self.ruler_color = color_table["fg_highlight"]

        self.show_markers = True
        self.show_ruler = True

    def mark(self, pos: Vector) -> None:
        if not self.ctx.canves.is_inside(pos):
            return

        if pos not in self.markers:
            self.markers.add(pos)

    def unmark(self, pos: Vector) -> None:
        self.markers.discard(pos)

    def set_ruler_anchor(self, anchor: Vector) -> None:
        self.ruler[0] = anchor

    def set_ruler_point(self, point: Vector) -> None:
        if not self.ctx.canves.is_inside(point):
            return

        self.ruler[1] = point

    def remove_ruler(self) -> None:
        self.ruler = [None, None]
        self.ruler_ready = False

    def draw(self) -> None:
        # Drawing the markers
        for i, marker in enumerate(self.markers):
            center = self.ctx.camera.to_world(marker)
            draw_marker(
                self.screen,
                center,
                self.ctx.camera.cell_size // 2 * self.ctx.camera.zoom,
                self.markers_colors[i % len(self.markers_colors)],
            )

        if None not in self.ruler:
            anchor = self.ctx.camera.to_world(self.ruler[0])
            endpoint = self.ctx.camera.to_world(self.ruler[1])
            draw_ruler(self.screen, anchor, endpoint, self.ruler_color)
