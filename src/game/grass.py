from pygame.locals import *
from random import *
from math import *
import pygame

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common.timer import LoopTimer
import src.common.textures as texture
from src.common.constants import *

class Grass(Sprite):
    def __init__(self, scene: Scene, x: int) -> None:
        super().__init__(scene, Layers.PLANTS)
        self.scene.grasses[x] = self
        self.size = texture.grass.size.copy()
        self.pos = VEC(x, 0)
        self.frame = 0
        self.ani_timer = LoopTimer(lambda: uniform(0.15, 0.3))
        self.bright = False
        self.lighten = (randint(0, 15), randint(0, 40), randint(0, 15))

    def update(self) -> None:
        self.pos.y = self.scene.grounds[floor(self.pos.x - 0.5)].pos.y

        if self.ani_timer.ended:
            self.frame += 1
            self.frame %= texture.grass.len

        self.bright = False
        if self.scene.player is self:
            self.bright = True

    def draw(self) -> None:
        image = texture.grass[self.frame].copy()
        if self.bright:
            (surf := pygame.Surface(image.get_size())).fill((80, 80, 80))
            image.blit(surf, (0, 0), special_flags=BLEND_RGB_ADD)
        (surf := pygame.Surface(image.get_size())).fill(self.lighten)
        image.blit(surf, (0, 0), special_flags=BLEND_RGB_ADD)
        self.manager.screen.blit(image, self.pos - (self.size.x / 2, self.size.y) - self.scene.camera.pos)

    def spread(self) -> None:
        choices = [x for x in range(-5, 6) if self.pos.x + x not in self.scene.grasses]
        if not choices: return
        Grass(self.scene, self.pos.x + choice(choices))

    def move(self, direction: int) -> None:
        x = self.pos.x + direction
        while x not in self.scene.grasses:
            x += direction
            if not (0 <= x < WIDTH):
                return
        self.scene.player = self.scene.grasses[x]