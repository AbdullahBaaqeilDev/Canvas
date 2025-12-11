from static import *


class Vector:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int) -> "Vector":
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)

    def __getitem__(self, index: int) -> int:
        return self.x if not index else self.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y

    def __iter__(self):
        # yield is a keyword in python means that this function is going to be a generator
        # so next(__iter__) will be self.x and next(__iter__) again will be self.y
        yield self.x
        yield self.y

    def __repr__(self) -> str:
        return f"{self.x, self.y}"

    def __str__(self) -> str:
        return f"{self.x, self.y}"

    @property
    def xy(self) -> "Vector":
        return self.x, self.y

    @property
    def w(self) -> int:
        return self.x

    @property
    def h(self) -> int:
        return self.y

    @property
    def wh(self) -> "Vector":
        return self.x, self.y

    @staticmethod
    def north() -> "Vector":
        return Vector(0, -1)

    @staticmethod
    def east() -> "Vector":
        return Vector(1, 0)

    @staticmethod
    def south() -> "Vector":
        return Vector(0, 1)

    @staticmethod
    def west() -> "Vector":
        return Vector(-1, 0)
