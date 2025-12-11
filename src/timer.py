import time
from static import *


class Timer:
    def __init__(
        self, callback: Callable, time_sec: int = 1, one_trigger: bool = True
    ) -> None:
        self.start_time: int | None = None
        self.callback = callback
        self.time = time_sec
        self.one_trigger = one_trigger

    @property
    def is_running(self) -> bool:
        return self.start_time != None

    def start(self) -> None:
        self.start_time = time.time()

    def stop(self) -> None:
        self.start_time = None

    def update(self) -> None:
        if not self.start_time:
            return

        current_time = time.time()

        if current_time - self.start_time >= self.time:
            self.callback()
            self.start_time = None if self.one_trigger else current_time
