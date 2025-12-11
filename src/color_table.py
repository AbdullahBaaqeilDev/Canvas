from color import Color


class ColorTable:
    WHITE = 0xFFFFFFFF
    BLACK = 0x000000FF
    RED = 0xFF0000FF
    GREEN = 0x00FF00FF
    BLUE = 0x0000FFFF
    YELLOW = 0xFFFF00FF
    CYAN = 0x00FFFFFF
    MAGENTA = 0xFF00FFFF
    GRAY = 0x7F7F7FFF
    ORANGE = 0xFF7F00FF
    PURPLE = 0x7F00FFFF

    def __init__(self) -> None:
        self.data: dict[str, Color] = {}

    def __getitem__(self, name: str) -> Color:
        return self.data.get(name, Color.NULL_VALUE)

    def __setitem__(self, name: str, value: int) -> None:
        self.data[name] = Color(value)

    def clear(self) -> None:
        self.data.clear()
