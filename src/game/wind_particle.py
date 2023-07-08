from pygame.locals import *
from random import *

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common.timer import LoopTimer
from src.common.constants import *
from src.common.utils import *

class WindParticle(Sprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layers.WIND)
        self.pos = VEC(randint(-100, WIDTH + 100), -5)
        self.vel = VEC(0, 0)
        self.factor = uniform(0.7, 1.3)

    def update(self) -> None:
        self.vel.y += GRAVITY * self.manager.dt
        self.vel.y *= 0.1 ** self.manager.dt
        self.vel.x += self.scene.wind_speed * self.factor * self.manager.dt
        self.pos += self.vel * self.manager.dt

    def draw(self) -> None:
        self.scene.wind.image.set_at(inttup(self.pos), (230, 230, 230, 50))