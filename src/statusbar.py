import pygame
from app_context import AppContext
from camera import Camera
from canvas import Canvas
from static import *


class Statusbar:
    def __init__(self, ctx: AppContext, width: int | None = None) -> None:
        self.ctx = ctx
        self.screen = pygame.display.get_surface()
        self.num_lines = 1
        self.width = self.ctx.canves.surf.get_width() if not width else width
        self.surf = pygame.Surface(
            (
                self.width,
                self.num_lines * (STATUS_BAR_LINE_HEIGHT + STATUS_BAR_LINES_GAP)
                + (STATUS_BAR_PADDING_Y * 2),
            )
        )
        self.rect = self.surf.get_rect(bottomleft=self.ctx.canves.rect.bottomleft)

        self.font = self.ctx.font_table.load("Consolas", STATUS_BAR_FONT_SIZE)

        self.shown_items: dict[str, bool] = {
            "mouse_pos": True,
            "grid_size": True,
            "cell_size": True,
            "camera_zoom": True,
            "camera_offset": True,
            "markers_visibility": True,
            "ruler_visibility": True,
        }

        self.items: list[str] = []

    def resize(self) -> None:
        self.surf = pygame.Surface(
            (
                self.width,
                self.num_lines * (STATUS_BAR_LINE_HEIGHT + STATUS_BAR_LINES_GAP)
                + (STATUS_BAR_PADDING_Y * 2),
            )
        )
        self.rect = self.surf.get_rect(bottomleft=self.ctx.canves.rect.bottomleft)

    def update(self) -> None:
        self.items.clear()

        if self.shown_items["mouse_pos"]:
            self.items.append(
                f"MousePos: {self.ctx.camera.to_local(self.ctx.input_manager.mouse_pos)}"
            )

        if self.shown_items["camera_zoom"]:
            self.items.append(f"Zoom: {int(self.ctx.camera.zoom * 100)}%")

        if self.shown_items["camera_offset"]:
            self.items.append(f"Offset: {self.ctx.camera.offset}")

        if self.shown_items["grid_size"]:
            self.items.append(f"GridSize: {self.ctx.canves.w}x{self.ctx.canves.h}")

        if self.shown_items["cell_size"]:
            size = int(self.ctx.camera.cell_size * self.ctx.camera.zoom)
            self.items.append(f"CellSize: {size}x{size}")

        if self.shown_items["markers_visibility"]:
            self.items.append(f"ShowMarkers: {self.ctx.debugging_tool.show_markers}")

        if self.shown_items["ruler_visibility"]:
            self.items.append(f"ShowRuler: {self.ctx.debugging_tool.show_ruler}")

    def draw(self) -> None:
        self.surf.fill(self.ctx.color_table["bg_secondary"].rgb)

        # Drawing the info
        line_index = 0
        line_width = STATUS_BAR_PADDING_X

        for item in self.items:
            item_surf = self.font.render(
                item, True, self.ctx.color_table["fg_primary"].rgb
            )
            item_rect = item_surf.get_rect(
                topleft=(
                    line_width,
                    line_index * (STATUS_BAR_LINE_HEIGHT + STATUS_BAR_LINES_GAP)
                    + STATUS_BAR_PADDING_Y,
                )
            )

            # making sure no item is wider than the statusbar
            while item_rect.w > self.rect.w:
                item = item[: (len(item) >> 1)]

            line_width += item_rect.w + STATUS_BAR_ITEMS_GAP

            if line_width > self.rect.w:
                line_index += 1
                line_width = STATUS_BAR_PADDING_X

                item_rect.topleft = (
                    line_width,
                    line_index * (STATUS_BAR_LINE_HEIGHT + STATUS_BAR_LINES_GAP)
                    + STATUS_BAR_PADDING_Y,
                )

                line_width += item_rect.w + STATUS_BAR_ITEMS_GAP

            self.surf.blit(item_surf, item_rect)

        if line_index + 1 != self.num_lines:
            self.num_lines = line_index + 1
            self.resize()

        pygame.draw.rect(
            self.surf,
            self.ctx.color_table["fg_primary"].rgb,
            [0, 0, *self.rect.size],
            2,
        )
        self.screen.blit(self.surf, self.rect)
