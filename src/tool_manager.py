from app_context import AppContext
from color import Color
from color_table import ColorTable
from tools import *
from static import *


class ToolManager:
    def __init__(self, ctx: AppContext = None) -> None:
        self.ctx = ctx
        self.tools: dict[str, Tool] = {
            "hand": Hand(),
            "line": Line(),
            "circle": Circle(),
            "curve": Curve(),
            "fill": Fill(),
            "pincil": Pincil(),
            "eraser": Eraser(),
            "rectangle": Rectangle(),
            "shape": Shape(),
        }
        self.current_tool: Tool = self.tools["hand"]
        self.primary_color = Color(ColorTable.WHITE)
        self.secondary_color = Color(ColorTable.BLACK)

    def select_tool(self, name: str) -> None:
        self.current_tool = self.tools[name]

    def update(self) -> None:
        if self.current_tool:
            self.current_tool.update(self.ctx)
