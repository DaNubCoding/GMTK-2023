from opensimplex import noise2, random_seed
from pygame.locals import *
from random import *
import pygame

from src.management.sprite import Sprite, Layers
from src.game.dandelion import Dandelion
from src.management.scene import Scene
from src.common.constants import *
from src.game.grass import Grass
from src.game.bush import Bush

random_seed()

class Ground(Sprite):
    def __init__(self, scene: Scene, x: int) -> None:
        super().__init__(scene, Layers.GROUND)
        self.scene.grounds[int(x)] = self
        self.pos = VEC(x, noise2(x * 0.04, 0.5) * 14 + 60)
        self.surface = pygame.Surface((1, 50), SRCALPHA)
        self.surface.fill(GROUND_COLOR)
        for _ in range(15):
            pos = (0, randint(0, self.surface.get_height() - 1))
            n = randint(-7, 15)
            self.surface.set_at(pos, tuple(map(lambda x: min(x + n + randint(-3, 3), 255), self.surface.get_at(pos))))
        (surf := pygame.Surface((1, randint(1, 3)))).fill((7, 7, 7))
        self.surface.blit(surf, (0, 0), special_flags=BLEND_RGB_SUB)
        (surf := pygame.Surface((1, randint(5, 9)))).fill((6, 6, 6))
        self.surface.blit(surf, (0, 0), special_flags=BLEND_RGB_SUB)
        (surf := pygame.Surface((1, randint(11, 15)))).fill((5, 5, 5))
        self.surface.blit(surf, (0, 0), special_flags=BLEND_RGB_SUB)

        if abs(x) > 200 and randint(0, 20) == 0:
            Dandelion(self.scene, x, True)
        elif abs(x) > 128 and randint(0, 50) == 0:
            Bush(self.scene, x, True)
        elif abs(x) > 30 and randint(0, 50) == 0:
            Grass(self.scene, x, True)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        if not (self.scene.camera.pos.x <= self.pos.x <= self.scene.camera.pos.x + WIDTH): return
        self.manager.screen.blit(self.surface, self.pos - self.scene.camera.pos)