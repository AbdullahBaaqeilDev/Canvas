from app_context import AppContext


class UIManager:
    def __init__(self, ctx: AppContext | None = None) -> None:
        self.ctx = ctx

    def update(self) -> None:
        pass
