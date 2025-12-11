from vector import Vector
from app_context import AppContext
from input_manager import InputManager
from static import *


class Tool:
    def __init__(self) -> None: ...
    def update(self, ctx: AppContext, *args, **kwargs) -> None: ...


class Hand(Tool):
    def update(self, ctx: AppContext):
        im = ctx.input_manager

        if (
            im.is_key_held("space")
            and im.is_mouse_button_held(pygame.BUTTON_LEFT)
            and im.is_mouse_moved()
        ):
            ctx.camera.move(im.mouse_rel)


class Select(Tool):
    pass


class Line(Tool):
    def __init__(self):
        self.thickness: int = 1
        self.anti_aliased: bool = False
        self.a: Vector | None = None
        self.b: Vector | None = None

    def isReady(self) -> bool:
        return self.a != None and self.b != None

    def reset(self) -> None:
        self.a = None
        self.b = None


class Circle(Tool):
    def __init__(self) -> None:
        self.anti_aliased: bool = False
        self.radius: int = 5
        self.center: Vector | None = None


class Rectangle(Tool):
    def __init__(self) -> None:
        self.a: Vector | None = None
        self.b: Vector | None = None


class Fill(Tool):
    def __init__(self) -> None:
        self.p: Vector | None = None


class Shape(Tool):
    def __init__(self) -> None:
        self.vertices: list[Vector] = []


class Curve(Tool):
    def __init__(self) -> None:
        self.curve_type: str = "bezier"


class Pincil(Tool):
    def __init__(self) -> None:
        self.radius: int = 1


class Eraser(Tool):
    def __init__(self) -> None:
        self.radius: int = 1
