from opensimplex import noise2
from pygame.locals import *
import pygame

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common.constants import *

class Ground(Sprite):
    def __init__(self, scene: Scene, x: int) -> None:
        super().__init__(scene, Layers.GROUND)
        self.scene.grounds[x] = self
        self.pos = VEC(x, noise2(x * 0.04, 0.5) * 14 + 60)
        self.surface = pygame.Surface((1, 50), SRCALPHA)
        self.surface.fill(GROUND_COLOR)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.manager.screen.blit(self.surface, self.pos - self.scene.camera.pos)