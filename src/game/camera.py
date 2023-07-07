from src.management.scene import Scene
from src.common.constants import *
from src.common.utils import *

class Camera:
    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        self.manager = scene.manager
        self.player = scene.player
        self.true_pos = self.player.pos.copy()

    def update(self) -> None:
        self.player = self.scene.player
        tick_offset = self.player.pos - self.true_pos - VEC(SIZE) // 2 - (0, 20)
        self.true_pos += tick_offset * 2 * self.manager.dt
        self.pos = intvec(self.true_pos)