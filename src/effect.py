from canvas import Canvas
from vector import Vector
from color import Color


class Effect:
    @staticmethod
    def perlin_noise(canves: Canvas, grid: Vector, seed: int = 0) -> None:
        """Creates a 2D Perlin noise"""

        pass

    @staticmethod
    def play_conway_game(canves: Canvas) -> None:
        """
        Simulates one step of Conway's Game of Life on the canvas.

        This method applies the rules of Conway's Game of Life to the current state of the canvas.
        Each pixel with a color is considered an "alive" cell, while blank pixels are considered "dead" cells.

        Rules:
        1. Any alive cell with fewer than two alive neighbors dies (underpopulation).
        2. Any alive cell with two or three alive neighbors survives to the next generation.
        3. Any alive cell with more than three alive neighbors dies (overpopulation).
        4. Any dead cell with exactly three alive neighbors becomes alive (reproduction).

        The canvas is updated in-place to reflect the new state after applying these rules.
        """

        # next_generation_pixels = deepcopy(canves.pixels)
        next_generation_pixels = canves.pixels.copy()

        for y in range(canves.h):
            for x in range(canves.w):
                is_alive = canves.get_at((x, y)) != Color.NULL_VALUE
                num_alive_neighbors = 0
                new_cell_color = Color(0)
                for offsetX in range(-1, 2):
                    for offsetY in range(-1, 2):
                        if not canves.is_inside(
                            (x + offsetX, y + offsetY)
                        ):  # not checking cells outside the canvas
                            continue

                        if offsetX == 0 and offsetY == 0:  # excluding the cell it self
                            continue

                        color = canves.get_at((x + offsetX, y + offsetY))
                        if color != Color.NULL_VALUE:
                            new_cell_color.blend(color, 0.5)
                            num_alive_neighbors += 1

                if is_alive:
                    if num_alive_neighbors < 2:  # underpopulation
                        next_generation_pixels[y, x] = Color.NULL_VALUE
                    elif num_alive_neighbors > 3:  # overpopulation
                        next_generation_pixels[y, x] = Color.NULL_VALUE
                    elif num_alive_neighbors in {2, 3}:
                        pass
                else:
                    if num_alive_neighbors == 3:
                        next_generation_pixels[y, x] = new_cell_color

        canves.pixels = next_generation_pixels
