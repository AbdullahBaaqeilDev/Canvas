import numpy as np
from typing import Generator, Literal, Callable
from static import *

"""
In Python, bitwise operations follow a specific order of precedence, just like arithmetic operations. Here's the order from highest to lowest precedence:

Bitwise NOT (~)
    This is a unary operator that inverts all the bits of its operand.

Bitwise AND (&)
    Performs a logical AND operation on each pair of corresponding bits.

Bitwise OR (|) and Bitwise XOR (^)
    OR (|) sets a bit to 1 if at least one of the corresponding bits is 1.
    XOR (^) sets a bit to 1 if the corresponding bits are different.

Bitwise Shift Operators (<<, >>)
    Left shift (<<) shifts bits to the left, filling with zeros.
    Right shift (>>) shifts bits to the right, discarding bits on the right.
"""

linear = lambda a, b, t: a + (b - a) * t


class Color:
    R_MASK = 0xFF000000
    G_MASK = 0x00FF0000
    B_MASK = 0x0000FF00
    A_MASK = 0x000000FF
    R_UNMASK = G_MASK | B_MASK | A_MASK
    G_UNMASK = R_MASK | B_MASK | A_MASK
    B_UNMASK = R_MASK | G_MASK | A_MASK
    A_UNMASK = R_MASK | G_MASK | B_MASK
    NULL_VALUE = 0x00000000

    @staticmethod
    def tuple_to_int(rgba: RGBA) -> int:
        """Convert a tuple of red, green, blue and alpha channels to an integer 0xRRGGBBAA"""

        r, g, b, a = rgba
        value = 0x00000000
        value = value | (r & 0xFF) << 24
        value = value | (g & 0xFF) << 16
        value = value | (b & 0xFF) << 8
        value = value | (a & 0xFF) << 0

        return value

    @staticmethod
    def int_to_tuple(value: int) -> RGBA:
        """Convert a integer value of 0xRRGGBBAA channels to a tuple of red, green, blue and alpha"""

        r = (value & Color.R_MASK) >> 24
        g = (value & Color.G_MASK) >> 16
        b = (value & Color.B_MASK) >> 8
        a = (value & Color.A_MASK) >> 0

        return (r, g, b, a)

    def __init__(self, value: np.int32) -> None:
        self.value = value

    def __getitem__(self, *args, **kwargs) -> tuple | int:
        if len(args) == 1:
            i = args[0]
            match i:
                case 0:
                    return self.r
                case 1:
                    return self.g
                case 2:
                    return self.b
                case 3:
                    return self.a

    def __iter__(self) -> Generator[int]:
        yield self.r
        yield self.g
        yield self.b
        yield self.a

    def __add__(self, other: "Color") -> "Color":
        if isinstance(other, Color):
            r = (self.r + other.r) & 0xFF
            g = (self.g + other.g) & 0xFF
            b = (self.b + other.b) & 0xFF
            a = (self.a + other.a) & 0xFF
            return Color.fromRGBA(r, g, b, a)

    def __sub__(self, other: "Color") -> "Color":
        if isinstance(other, Color):
            r = (self.r - other.r) & 0xFF
            g = (self.g - other.g) & 0xFF
            b = (self.b - other.b) & 0xFF
            a = (self.a - other.a) & 0xFF
            return Color.fromRGBA(r, g, b, a)

    def __mul__(self, other: int) -> "Color":
        if isinstance(other, Color):
            r = (self.r * other.r) & 0xFF
            g = (self.g * other.g) & 0xFF
            b = (self.b * other.b) & 0xFF
            a = (self.a * other.a) & 0xFF
            return Color.fromRGBA(r, g, b, a)

    def __hash__(self) -> int:
        return hash((self.r, self.g, self.b, self.a))

    def __eq__(self, other):
        if isinstance(other, Color):
            return (
                self.r == other.r
                and self.g == other.g
                and self.b == other.b
                and self.a == other.a
            )

    def __repr__(self) -> str:
        return f"{self.r, self.g, self.b, self.a}"

    def __str__(self) -> str:
        return f"{self.r, self.g, self.b, self.a}"

    @classmethod
    def fromRGBA(cls, r: int, g: int, b: int, a: int) -> "Color":
        return Color(Color.tuple_to_int((r, g, b, a)))

    @property
    def r(self) -> int:
        return (self.value & Color.R_MASK) >> 24

    @r.setter
    def r(self, value: int) -> None:
        self.value &= Color.R_UNMASK
        self.value |= (value & 0xFF) << 24

    @property
    def g(self) -> int:
        return (self.value & Color.G_MASK) >> 16

    @g.setter
    def g(self, value: int) -> None:
        self.value &= Color.G_UNMASK
        self.value |= (value & 0xFF) << 16

    @property
    def b(self) -> int:
        return (self.value & Color.B_MASK) >> 8

    @b.setter
    def b(self, value: int) -> None:
        self.value &= Color.B_UNMASK
        self.value |= (value & 0xFF) << 8

    @property
    def a(self) -> int:
        return self.value & Color.A_MASK

    @a.setter
    def a(self, value: int) -> None:
        self.value &= Color.A_UNMASK
        self.value |= value & 0xFF

    @property
    def rgb(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)

    @property
    def rgba(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b, self.a)

    def blend(self, color_b: "Color", percentage: float) -> None:
        r0, g0, b0, a0 = self.rgba
        r1, g1, b1, a1 = color_b.rgba

        self.r = int(linear(r0, r1, percentage))
        self.g = int(linear(g0, g1, percentage))
        self.b = int(linear(b0, b1, percentage))
        self.a = int(linear(a0, a1, percentage))

    def blended(self, color_b: "Color", percentage: float) -> "Color":
        r0, g0, b0, a0 = self.rgba
        r1, g1, b1, a1 = color_b.rgba

        r = int(linear(r0, r1, percentage))
        g = int(linear(g0, g1, percentage))
        b = int(linear(b0, b1, percentage))
        a = int(linear(a0, a1, percentage))

        return Color.fromRGBA(r, g, b, a)

    def invert(self) -> None:
        self.r = -(self.r - 127) + 127
        self.g = -(self.g - 127) + 127
        self.b = -(self.b - 127) + 127

    def inverted(self) -> "Color":
        r, g, b = self.rgb

        r = -(r - 127) + 127
        g = -(g - 127) + 127
        b = -(b - 127) + 127

        return Color.fromRGBA(r, g, b, self.a)
