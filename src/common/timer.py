from typing import Callable
import time

class Timer:
    def __init__(self, func: Callable) -> None:
        self.func = func
        self._start = time.time()
        self.period = func()
        self.started = False

    def start(self) -> None:
        self.started = True
        self._start = time.time()
        self.period = self.func()

    def stop(self) -> None:
        self.period = 0

    @property
    def progress(self) -> float:
        return (time.time() - self._start) / self.period

    @property
    def ended(self) -> bool:
        if not self.started: return False
        if time.time() - self._start < self.period: return False
        return True

class LoopTimer:
    def __init__(self, func: Callable) -> None:
        self.func = func
        self.start = time.time()
        self.period = func()

    @property
    def ended(self) -> bool:
        if time.time() - self.start < self.period:
            return False

        self.start = time.time()
        self.period = self.func()
        return True