from typing import Callable
import time

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