import pygame
from typing import *
from json import load

# Types
type XY = tuple[int, int]
type WH = tuple[int, int]
type RGB = tuple[int, int, int]
type RGBA = tuple[int, int, int, int]
type Key = int
type Anchor = Literal["nw", "n", "ne", "w", "c", "e", "sw", "s", "se"]

# Constants
MAX_FPS = 0  # 60
WINDOW_SIZE = (500, 500)
WINDOW_CENTER = (250, 250)
ZOOM_MIN = 0.5
ZOOM_MAX = 10
ZOOM_STEP = 0.5
MAX_KEYS_IN_SHORTCUT = 3
RULER_POINT_RADIUS = 5
STATUS_BAR_FONT_SIZE = 12
STATUS_BAR_LINE_HEIGHT = STATUS_BAR_FONT_SIZE
STATUS_BAR_PADDING_Y = 10
STATUS_BAR_PADDING_X = 10
STATUS_BAR_LINES_GAP = 0
STATUS_BAR_ITEMS_GAP = 20
UNSHOWING_THE_GRID_THRESHOLD = 5

TOOLS = (
    "hand",
    "line",
    "circle",
    "fill",
    "rectangle",
    "shape",
    "curve",
    "pincil",
    "eraser",
)

with open("hotkeys.json", "r") as file:
    HOTKEYS: dict[str, list[int]] = load(file)

STRING_TO_KEY_ID: dict[str, int] = {
    # for SOME UNKOWN reason we have to use KSCAN_LCTRL instead of K_LCTRL 🤬
    "ctrl": pygame.KSCAN_LCTRL,
    "shift": pygame.KSCAN_LSHIFT,
    "alt": pygame.KSCAN_LALT,
    "a": pygame.KSCAN_A,
    "b": pygame.KSCAN_B,
    "c": pygame.KSCAN_C,
    "d": pygame.KSCAN_D,
    "e": pygame.KSCAN_E,
    "f": pygame.KSCAN_F,
    "g": pygame.KSCAN_G,
    "h": pygame.KSCAN_H,
    "i": pygame.KSCAN_I,
    "j": pygame.KSCAN_J,
    "k": pygame.KSCAN_K,
    "l": pygame.KSCAN_L,
    "m": pygame.KSCAN_M,
    "n": pygame.KSCAN_N,
    "o": pygame.KSCAN_O,
    "p": pygame.KSCAN_P,
    "q": pygame.KSCAN_Q,
    "r": pygame.KSCAN_R,
    "s": pygame.KSCAN_S,
    "t": pygame.KSCAN_T,
    "u": pygame.KSCAN_U,
    "v": pygame.KSCAN_V,
    "w": pygame.KSCAN_W,
    "x": pygame.KSCAN_X,
    "y": pygame.KSCAN_Y,
    "z": pygame.KSCAN_Z,
    "0": pygame.KSCAN_0,
    "1": pygame.KSCAN_1,
    "2": pygame.KSCAN_2,
    "3": pygame.KSCAN_3,
    "4": pygame.KSCAN_4,
    "5": pygame.KSCAN_5,
    "6": pygame.KSCAN_6,
    "7": pygame.KSCAN_7,
    "8": pygame.KSCAN_8,
    "9": pygame.KSCAN_9,
    "-": pygame.KSCAN_MINUS,
    "=": pygame.KSCAN_EQUALS,
    "f1": pygame.KSCAN_F1,
    "f2": pygame.KSCAN_F2,
    "f3": pygame.KSCAN_F3,
    "f4": pygame.KSCAN_F4,
    "f5": pygame.KSCAN_F5,
    "f6": pygame.KSCAN_F6,
    "f7": pygame.KSCAN_F7,
    "f8": pygame.KSCAN_F8,
    "f9": pygame.KSCAN_F9,
    "f10": pygame.KSCAN_F10,
    "f11": pygame.KSCAN_F11,
    "f12": pygame.KSCAN_F12,
    "f13": pygame.KSCAN_F13,
    "home": pygame.KSCAN_HOME,
    "end": pygame.KSCAN_END,
    "escape": pygame.KSCAN_ESCAPE,
    "tap": pygame.KSCAN_TAB,
    "delete": pygame.KSCAN_DELETE,
    "backspace": pygame.KSCAN_BACKSPACE,
    "space": pygame.KSCAN_SPACE,
    "up": pygame.KSCAN_UP,
    "right": pygame.KSCAN_RIGHT,
    "down": pygame.KSCAN_DOWN,
    "left": pygame.KSCAN_LEFT,
}
