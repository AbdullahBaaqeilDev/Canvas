import pygame
from functools import partial
from flatten_dict import flatten
from app_context import AppContext
from canvas import Canvas
from camera import Camera
from draw import Draw
from effect import Effect
from timer import Timer
from font_table import FontTable
from color_table import ColorTable
from tool_manager import ToolManager
from hotkey_manager import HotkeyManager
from input_manager import InputManager
from statusbar import Statusbar
from debugging_tool import *
from static import *


"""
Controls
--------
Mouse:
    - Scroll up       : Zoom out by 50%
    - Scroll down     : Zoom in by 50%
    - Space + LMB hold: Pan the canvas
    - Shift + LMB     : Add a marker
    - Shift + RMB     : Remove a marker
    - Alt + LMB hold  : Set ruler anchor/point
    - Alt + RMB       : Remove the ruler

Keys:
    - Esc                         : Quit the app
    - Up / Right / Down / Left    : Offset the canvas by one cellSize
    - Ctrl + S                    : Save canvas as BMP
    - Ctrl + R                    : Recenter (offset -> (0,0), zoom -> 100%)
    - Ctrl + Delete               : Clear all pixels
    - Ctrl + Shift + M            : Toggle mouse position in status bar
    - Ctrl + Shift + G            : Toggle grid size in status bar
    - Ctrl + Shift + Z            : Toggle zoom percentage in status bar
    - Ctrl + Shift + O            : Toggle offset in status bar
    - Ctrl + Shift + C            : Toggle cell size (pixels) in status bar
    - Ctrl + Shift + P            : Toggle plotted pixels count in status bar
    - Ctrl + Shift + K            : Toggle markers in status bar
    - Ctrl + Shift + R            : Toggle ruler in status bar
    - Ctrl + Shift + Alt + C      : Start/Stop Conway game

Tools (usage summary):
    - Circle   : LMB -> unfilled, RMB -> filled (radius +/-)
    - Curve    : LMB -> add point
    - Fill     : LMB -> fill
    - Line     : LMB -> set A, release -> set B
    - Pincil   : LMB + move -> draw
    - Rectangle: LMB -> set A, release -> set B
    - Shape    : LMB -> add vertex, RMB -> close & draw, Ctrl -> fill
    - Hand     : LMB + move -> pan the canvas
    - Eraser   : LMB + move -> erase
"""


class DrawingCanvas:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Drawing Canvas")
        self.clock = pygame.time.Clock()
        self.since_last_frame_ticks = 0

        # Create context first (empty)
        self.ctx = AppContext()

        # Create subsystems (don’t pass ctx yet) ctx will be patched later
        self.font_table = FontTable()
        self.color_table = ColorTable()
        self.init_font_table()
        self.init_color_table()

        self.canvas = Canvas((100, 100))
        self.camera = Camera(self.canvas)
        self.input_manager = InputManager()
        self.hotkey_manager = HotkeyManager()
        self.tool_manager = ToolManager()
        self.debugging_tool = DebuggingTool(self.color_table)
        self.conway_timer = Timer(
            partial(Effect.play_conway_game, self.canvas), 0.2, False
        )
        self._fps_timer = 0

        # Fill context
        self.ctx.canves = self.canvas
        self.ctx.camera = self.camera
        self.ctx.font_table = self.font_table
        self.ctx.color_table = self.color_table
        self.ctx.input_manager = self.input_manager
        self.ctx.hotkey_manager = self.hotkey_manager
        self.ctx.tool_manager = self.tool_manager
        self.ctx.debugging_tool = self.debugging_tool

        # Patch back references
        self.hotkey_manager.ctx = self.ctx
        self.tool_manager.ctx = self.ctx
        self.debugging_tool.ctx = self.ctx

        # Create components that depend on ctx
        self.statusbar = Statusbar(self.ctx)

        # Finish hotkey_manager setup
        self.register_hotkey_bindings()
        self.register_hotkey_actions()

    def delta_time(self) -> float:
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.since_last_frame_ticks) / 1000
        self.since_last_frame_ticks = current_time

        return delta_time

    def fps(self) -> float:
        return 1 / (self.delta_time() + 1e-3)

    def init_font_table(self) -> None:
        self.font_table.load("Consolas", STATUS_BAR_FONT_SIZE)

    def init_color_table(self) -> None:
        # the foreground (e.g. text, grid, selected)
        self.color_table["fg_primary"] = 0xCCCCCCFF
        self.color_table["fg_secondary"] = 0x868686FF
        self.color_table["fg_highlight"] = 0xE2C07EFF
        self.color_table["fg_highlight2"] = 0x317CD6FF
        self.color_table["fg_warning"] = 0xF88061FF

        # the background (e.g. canvas, statusbar)
        self.color_table["bg_primary"] = 0x224F8FFF
        self.color_table["bg_secondary"] = 0x224F8FFF

    def register_hotkey_actions(self) -> None:
        self.hotkey_manager.register_action(
            "camera.move.up", partial(self.camera_move, direction=Vector.south())
        )
        self.hotkey_manager.register_action(
            "camera.move.right", partial(self.camera_move, direction=Vector.west())
        )
        self.hotkey_manager.register_action(
            "camera.move.down", partial(self.camera_move, direction=Vector.north())
        )
        self.hotkey_manager.register_action(
            "camera.move.left", partial(self.camera_move, direction=Vector.east())
        )
        self.hotkey_manager.register_action("camera.recenter", self.camera_recenter)
        for i in range(len(TOOLS)):
            self.hotkey_manager.register_action(
                f"toolbox.select.{i}", partial(self.select_tool, name=TOOLS[i])
            )
        for info_name in self.statusbar.shown_items.keys():
            self.hotkey_manager.register_action(
                f"statusbar.toggle.{info_name}",
                partial(self.toggle_statusbar_info, info_name=info_name),
            )
        self.hotkey_manager.register_action("canves.clear", self.canves_clear)
        self.hotkey_manager.register_action("output.save_as_bmp", lambda ctx: None)
        self.hotkey_manager.register_action("conway_play", self.toggle_conway_game)

    def register_hotkey_bindings(self) -> None:
        for binding in flatten(HOTKEYS):
            # go through the flatten the keys to reach the combo and translate it to pygame key ids then register it to the hotkey manager
            node = HOTKEYS
            for key in binding:
                if key == binding[-1]:
                    combo = node[key]
                    self.hotkey_manager.register_binding(".".join(binding), combo)
                    break

                node = node[key]

    def camera_move(self, ctx: AppContext, direction: Vector) -> None:
        offset = self.camera.cell_size * self.camera.zoom
        self.camera.move(
            Vector(
                offset * (direction.x // abs(direction.x)) if direction.x != 0 else 0,
                offset * (direction.y // abs(direction.y)) if direction.y != 0 else 0,
            )
        )

    def camera_recenter(self, ctx: AppContext) -> None:
        self.camera.recenter()

    def select_tool(self, ctx: AppContext, name: str) -> None:
        self.tool_manager.select_tool(name)

    def toggle_statusbar_info(self, ctx: AppContext, info_name: str) -> None:
        self.statusbar.shown_items[info_name] = not self.statusbar.shown_items[
            info_name
        ]

    def toggle_debugging_tool_markers(self, ctx: AppContext) -> None:
        self.debugging_tool.show_markers = not self.debugging_tool.show_markers

    def toggle_debugging_tool_ruler(self, ctx: AppContext) -> None:
        self.debugging_tool.show_ruler = not self.debugging_tool.show_ruler

    def canves_clear(self, ctx: AppContext) -> None:
        self.canvas.reset_pixels()

    def toggle_conway_game(self, ctx: AppContext) -> None:
        if self.conway_timer.is_running:
            self.conway_timer.stop()
        else:
            self.conway_timer.start()

    def handle_debugging_input(self) -> None:
        im = self.input_manager
        dbg = self.debugging_tool

        if im.is_mouse_button_pressed(pygame.BUTTON_LEFT):
            if im.is_mod_held("shift"):
                dbg.mark(self.camera.to_local(im.mouse_pos))
            elif im.is_mod_held("alt"):
                dbg.remove_ruler()
                dbg.set_ruler_anchor(self.camera.to_local(im.mouse_pos))

        if im.is_mouse_button_held(pygame.BUTTON_RIGHT):
            if im.is_mod_held("shift"):
                dbg.unmark(self.camera.to_local(im.mouse_pos))
            elif im.is_mod_held("alt"):
                dbg.remove_ruler()

        if im.is_mouse_button_released(pygame.BUTTON_LEFT):
            if im.is_mod_held("alt"):
                dbg.set_ruler_point(self.camera.to_local(im.mouse_pos))
                dbg.ruler_ready = True

        if im.is_mouse_moved() and not dbg.ruler_ready:
            if im.is_mod_held("alt"):
                dbg.set_ruler_point(self.camera.to_local(im.mouse_pos))

    def handle_general_input(self) -> None:
        im = self.input_manager

        if im.mouse_wheel.y:
            self.camera.adjust_zoom(im.mouse_wheel.y)

    def update_caption(self) -> None:
        # updating the caption every 0.1 second
        dt = self.delta_time()
        self._fps_timer += dt
        if self._fps_timer >= 0.2:
            pygame.display.set_caption(f"Drawing Canvas {self.fps():.1f} FPS")
            self._fps_timer = 0

    def update(self) -> None:
        self.clock.tick(MAX_FPS)

        self.input_manager.update()
        self.statusbar.update()
        self.conway_timer.update()
        self.tool_manager.update()
        if self.input_manager.keys_new_input():
            self.hotkey_manager.update()

        self.handle_debugging_input()
        self.handle_general_input()
        self.update_caption()

    def draw(self) -> None:
        self.screen.fill(self.color_table["bg_primary"].rgb)
        Draw.draw_canvas(self.screen, self.canvas, self.camera, self.color_table)
        self.debugging_tool.draw()
        self.statusbar.draw()
        debug(str(type(self.tool_manager.current_tool)))
        pygame.display.update()

    def run(self) -> None:
        while True:
            self.update()
            self.draw()


if __name__ == "__main__":
    program = DrawingCanvas()
    program.run()
