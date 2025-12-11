from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from canvas import Canvas
    from camera import Camera
    from font_table import FontTable
    from color_table import ColorTable
    from input_manager import InputManager
    from hotkey_manager import HotkeyManager
    from tool_manager import ToolManager
    from debugging_tool import DebuggingTool


class AppContext:
    def __init__(
        self,
        canvas: Canvas | None = None,
        camera: Camera | None = None,
        font_table: FontTable | None = None,
        color_table: ColorTable | None = None,
        input_manager: InputManager | None = None,
        hotkey_manager: HotkeyManager | None = None,
        tool_manager: ToolManager | None = None,
        debugging_tool: DebuggingTool | None = None,
    ):
        self.canves = canvas
        self.camera = camera
        self.font_table = font_table
        self.color_table = color_table
        self.input_manager = input_manager
        self.hotkey_manager = hotkey_manager
        self.tool_manager = tool_manager
        self.debugging_tool = debugging_tool
