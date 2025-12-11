from canvas import Canvas
from camera import Camera
from vector import Vector
from color import Color
from color_table import ColorTable
from static import *


class Draw:
    @staticmethod
    def line(canves: Canvas, a: Vector, b: Vector, color: RGB, width: int = 1) -> None:
        """Using Bresenham's line algorithm to draw a line from pointA to pointB"""

        x0, y0 = a
        x1, y1 = b

        # if the change in x is greater then the change in y (a horizontal line)
        if abs(x1 - x0) > abs(y1 - y0):
            # if the line is going from right to left
            if x0 > x1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0

            dx = x1 - x0
            dy = y1 - y0

            dir = -1 if dy < 0 else 1
            dy *= dir

            y = y0
            d = dy * 2 - dx

            for i in range(dx + 1):
                for stroke in range(width):
                    canves.set_at((x0 + i, y + stroke - width // 2), color)

                if d >= 0:
                    d += -2 * dx
                    y += dir

                d += 2 * dy
        # if the change in y is greater then the change in x (a vertical line)
        else:
            # if the line is going from top to bottom
            if y0 > y1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0

            dx = x1 - x0
            dy = y1 - y0

            dir = -1 if dx < 0 else 1
            dx *= dir

            x = x0
            d = dx * 2 - dy

            for i in range(dy + 1):
                for stroke in range(width):
                    canves.set_at((x + stroke - width // 2, y0 + i), color)

                if d >= 0:
                    d += -2 * dy
                    x += dir

                d += 2 * dx

    @staticmethod
    def aaline(canves: Canvas, a: Vector, b: Vector, color: RGB) -> None:
        """Using Xiolin Wu algorithm it will draw an Anti-Aliased line"""

        x0, y0 = a
        x1, y1 = b

        if abs(x1 - x0) > abs(y1 - y0):
            if x0 > x1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0

            dx = x1 - x0
            dy = y1 - y0
            m = dy / dx if dx != 0 else 1

            # handling the start pixel brightness
            overlap = 1 - ((x0 + 0.5) - int(x0 + 0.5))
            dist_start = y0 - int(y0)
            canves.set_at((int(x0 + 0.5), int(y0)), color, (1 - dist_start) * overlap)

            # handling the end pixel brightness
            overlap = (x1 - 0.5) - int(x1 - 0.5)
            distEnd = y1 - int(y1)
            canves.set_at((int(x1 + 0.5), int(y1)), color, (1 - distEnd) * overlap)

            for i in range(1, int(dx)):
                x = x0 + i
                y = y0 + m * i

                ix = int(x)
                iy = int(y)

                dist = y - iy

                canves.set_at((ix, iy), color, 1 - dist)
                canves.set_at((ix, iy + 1), color, dist)
        else:
            if y0 > y1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0

            dx = x1 - x0
            dy = y1 - y0
            m = dx / dy if dy != 0 else 1

            # handling the start pixel brightness
            overlap = 1 - ((y0 + 0.5) - int(y0 + 0.5))
            dist_start = x0 - int(x0)
            canves.set_at((int(x0 + 0.5), int(y0)), color, (1 - dist_start) * overlap)

            # handling the end pixel brightness
            overlap = (y1 - 0.5) - int(y1 - 0.5)
            distEnd = x1 - int(x1)
            canves.set_at((int(x1 + 0.5), int(y1)), color, (1 - distEnd) * overlap)

            for i in range(1, int(dy)):
                x = x0 + m * i
                y = y0 + i

                ix = int(x)
                iy = int(y)

                dist = x - ix

                canves.set_at((ix, iy), color, 1 - dist)
                canves.set_at((ix + 1, iy), color, dist)

    @staticmethod
    def circle(
        canves: Canvas, c: Vector, r: int, color: RGB, filled: bool = False
    ) -> None:
        """Using the Mid-Point Circle algorithm it will draw a circle."""

        # y_value: (x_min, x_max)
        spans: dict[int, (int, int)] = {}
        r = r

        x = 0
        y = -r
        d = (
            -r + 0.25
        )  # the 0.25 could be removed for slightly faster performence but woth slight different circle

        while x <= -y:
            if d > 0:
                y += 1
                d += 2 * y
            d += 2 * x + 1

            # Draw the circle points 8 times since the circle is identical in 8 sides
            canves.set_at(Vector(c.x + x, c.y + y), color)  # 0-45 deg
            canves.set_at(Vector(c.x - y, c.y - x), color)  # 45-90 deg
            canves.set_at(Vector(c.x - y, c.y + x), color)  # 90-135 deg
            canves.set_at(Vector(c.x + x, c.y - y), color)  # 135-180 deg
            canves.set_at(Vector(c.x - x, c.y - y), color)  # 180-225 deg
            canves.set_at(Vector(c.x + y, c.y + x), color)  # 225-270 deg
            canves.set_at(Vector(c.x + y, c.y - x), color)  # 270-315 deg
            canves.set_at(Vector(c.x - x, c.y + y), color)  # 315-360 deg
            spans[c.y + y] = (c.x - x, c.x + x)
            spans[c.y - x] = (c.x - y, c.x + y)
            spans[c.y + x] = (c.x - y, c.x + y)
            spans[c.y - y] = (c.x - x, c.x + x)

            x += 1

        if not filled:
            return

        # drawing the pixels
        for y, xs in spans.items():
            x0, x1 = xs

            dx = abs(x1 - x0)
            x_min = min(x0, x1)

            for j in range(1, dx):
                canves.set_at((x_min + j, y), color)

    @staticmethod
    def aacircle(
        canves: Canvas, c: Vector, r: int, color: RGB, filled: bool = False
    ) -> None:
        """Using the Mid-Point Circle algorithm it will draw a circle."""

        # y_value: (x_min, x_max)
        spans: dict[int, (int, int)] = {}
        r = r

        x = 0
        y = -r
        d = (
            -r + 0.25
        )  # the 0.25 could be removed for slightly faster performence but woth slight different circle

        while x <= -y:
            if d > 0:
                y += 1
                d += 2 * y
            d += 2 * x + 1

            # Draw the circle points 8 times since the circle is identical in 8 sides
            canves.set_at(Vector(c.x + x, c.y + y), color)  # 0-45 deg
            canves.set_at(Vector(c.x - y, c.y - x), color)  # 45-90 deg
            canves.set_at(Vector(c.x - y, c.y + x), color)  # 90-135 deg
            canves.set_at(Vector(c.x + x, c.y - y), color)  # 135-180 deg
            canves.set_at(Vector(c.x - x, c.y - y), color)  # 180-225 deg
            canves.set_at(Vector(c.x + y, c.y + x), color)  # 225-270 deg
            canves.set_at(Vector(c.x + y, c.y - x), color)  # 270-315 deg
            canves.set_at(Vector(c.x - x, c.y + y), color)  # 315-360 deg
            spans[c.y + y] = (c.x - x, c.x + x)
            spans[c.y - x] = (c.x - y, c.x + y)
            spans[c.y + x] = (c.x - y, c.x + y)
            spans[c.y - y] = (c.x - x, c.x + x)

            x += 1

        if not filled:
            return

        # drawing the pixels
        for y, xs in spans.items():
            x0, x1 = xs

            dx = abs(x1 - x0)
            x_min = min(x0, x1)

            for j in range(1, dx):
                canves.set_at((x_min + j, y), color)

    @staticmethod
    def arc(
        canves: Canvas,
        center: Vector,
        radius: int,
        radians: tuple[float, float],
        color: RGB,
        filled: bool = False,
    ) -> None:
        pass

    @staticmethod
    def rectangle(
        canves: Canvas, topleft: Vector, size: Vector, color: RGB, filled: bool = False
    ) -> None:
        x, y = topleft
        w, h = size

        for dy in (0, h):
            for dx in (0, w):
                canves.set_at((x + dx, y + dy), color)

        if not filled:
            return

        for dy in range(1, h - 1):
            for dx in range(1, w - 1):
                canves.set_at((x + dx, y + dy), color)

    @staticmethod
    def polygon(
        canves: Canvas, vertices: tuple[Vector], color: RGB, filled: bool = False
    ) -> None:
        pass

    @staticmethod
    def vertex_array(
        canves: Canvas, vertex_array: tuple[Vector], color: RGB, filled: bool = False
    ) -> None:
        pass

    @staticmethod
    def bezier(
        canves: Canvas, points: tuple[Vector], color: RGB, filled: bool = False
    ) -> None:
        pass

    @staticmethod
    def fill(canves: Canvas, pos: Vector, color: RGB) -> None:
        """Using the Flood-Fill algorithm it will fill the whole area that pos lies in"""

        stack: list[Vector] = [Vector(pos)]
        base_color = canves.get_at(pos)

        while stack:
            cell = stack.pop()

            if canves.is_inside(cell) and canves.get_at(cell) == base_color:
                stack.append(cell + Vector.north())
                stack.append(cell + Vector.east())
                stack.append(cell + Vector.south())
                stack.append(cell + Vector.west())

                canves.set_at((int(cell.x), int(cell.y)), color)

    def draw_canvas(
        surf: pygame.Surface,
        canves: Canvas,
        camera: Camera,
        color_table: ColorTable,
        show_grid: bool = True,
    ) -> None:
        ct = color_table
        zoom = camera.zoom
        offset = camera.offset
        cell_size = camera.cell_size

        top = canves.rect.top + offset.y
        left = canves.rect.left + offset.x
        bottom = canves.h * cell_size * zoom + offset.y
        right = canves.w * cell_size * zoom + offset.x

        canves.surf.fill(ct["bg_primary"].rgb)

        # ---------- Draw pixels ----------
        for row in range(canves.h):
            for col in range(canves.w):
                color = Color(canves.get_at((col, row)))
                if not color.a:
                    continue

                pygame.draw.rect(
                    canves.surf,
                    color.rgb,
                    (
                        col * cell_size * zoom + offset.x,
                        row * cell_size * zoom + offset.y,
                        cell_size * zoom,
                        cell_size * zoom,
                    ),
                )

        # ---------- Draw the grid ----------
        color = (
            color_table["fg_secondary"]
            .blended(color_table["fg_primary"], min(zoom / (ZOOM_MAX), 1))
            .rgb
        )

        # Top & Left & Bottom & Right Borders
        pygame.draw.line(canves.surf, color, (left, top), (right, top))
        pygame.draw.line(canves.surf, color, (left, top), (left, bottom))
        pygame.draw.line(
            canves.surf,
            color,
            (left, bottom),
            (right, bottom),
        )
        pygame.draw.line(
            canves.surf,
            color,
            (right, top),
            (right, bottom),
        )

        if show_grid and cell_size * zoom > UNSHOWING_THE_GRID_THRESHOLD:
            for row in range(1, canves.h):
                y = row * cell_size * zoom + offset.y
                pygame.draw.line(canves.surf, color, (left, y), (right, y))

            for column in range(1, canves.w):
                offsetX = cell_size * column * zoom + offset.x
                pygame.draw.line(canves.surf, color, (offsetX, top), (offsetX, bottom))

        surf.blit(canves.surf, canves.rect)
