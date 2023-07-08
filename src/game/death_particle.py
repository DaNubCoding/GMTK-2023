from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common.timer import Timer
from src.common.constants import *
from src.common.utils import *

class DeathParticle(Sprite):
    def __init__(self, scene: Scene, pos: tuple[int, int], color: tuple[int, int, int]) -> None:
        super().__init__(scene, Layers.ANIMALS)
        self.color = color
        self.pos = VEC(pos)
        self.vel = VEC(0, 0)
        self.kill_timer = Timer(lambda: 1)
        self.kill_timer.start()

    def update(self) -> None:
        self.vel.y += GRAVITY * self.manager.dt
        self.pos += self.vel * self.manager.dt
        if self.pos.y > (y := self.scene.get_y(self.pos.x) - 1):
            self.pos.y = y
        if self.kill_timer.ended:
            self.kill()

    def draw(self) -> None:
        self.manager.screen.set_at(inttup(self.pos - self.scene.camera.pos), self.color)