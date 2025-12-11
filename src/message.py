import pygame
from app_context import AppContext
from vector import Vector
from static import *


class Message:
    def __init__(
        self,
        ctx: AppContext,
        text: str,
        pos: Vector,
        anchor: Anchor = "nw",
        max_width: int | None = None,
        title: str | None = None,
        icon: pygame.Surface | None = None,
        font_name: str = "Consolas",
        font_size: int = STATUS_BAR_FONT_SIZE,
    ) -> None:
        self.surf: pygame.Surface | None = None
        self.rect: pygame.Rect | None = None

        self.text = text
        self.pos = pos
        self.anchor = anchor
        self.max_width = max_width
        self.title = title
        self.icon = icon
        self.font = ctx.font_table.load(font_name, font_size)

    def _render(self) -> None:
        pass

    def draw(self, surf: pygame.Surface) -> None:
        pass
