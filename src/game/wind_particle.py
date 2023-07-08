from pygame.locals import *
from random import *

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common.constants import *

class WindParticle(Sprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layers.WIND)
        self.pos = VEC(randint(-100, WIDTH + 100), -5)
        self.vel = VEC(0, 0)
        self.image = pygame.Surface((1, 1), SRCALPHA)
        self.image.fill((230, 230, 230, 20))
        self.factor = uniform(0.7, 1.3)

    def update(self) -> None:
        self.vel.y += GRAVITY * self.manager.dt
        self.vel.y *= 0.99
        self.vel.x += self.scene.wind_speed * self.factor * self.manager.dt
        self.pos += self.vel * self.manager.dt

    def draw(self) -> None:
        self.scene.wind.image.blit(self.image, self.pos)