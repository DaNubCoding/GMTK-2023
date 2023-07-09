from pygame.locals import *
from random import *
from math import *
import pygame

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common.timer import LoopTimer
import src.common.textures as texture
from src.common.constants import *
from src.common.utils import *

class Dandelion(Sprite):
    def __init__(self, scene: Scene, x: int, withered: bool = False) -> None:
        super().__init__(scene, Layers.GRASS)
        self.scene.plants[int(x)] = self
        self.size = VEC(texture.dandelion.get_size())
        self.pos = VEC(x, -200)
        self.sheet = texture.dandelion
        self.bright = False
        self.lighten = (randint(0, 15), randint(0, 40), randint(0, 15))
        self.withered = withered

    def update(self) -> None:
        if not (self.scene.camera.pos.x - 1 <= self.pos.x <= self.scene.camera.pos.x + WIDTH + 1): return
        self.pos.y = self.scene.get_y(self.pos.x)

        self.bright = False
        if self.scene.player is self:
            self.bright = True

    def draw(self) -> None:
        if not (self.scene.camera.pos.x - 1 <= self.pos.x <= self.scene.camera.pos.x + WIDTH + 1): return
        image = texture.dandelion.copy()
        if self.withered:
            (surf := pygame.Surface(image.get_size())).fill((140, 0, 0))
            image.blit(surf, (0, 0), special_flags=BLEND_RGB_ADD)
        if self.bright:
            (surf := pygame.Surface(image.get_size())).fill((80, 80, 80))
            image.blit(surf, (0, 0), special_flags=BLEND_RGB_ADD)
        self.manager.screen.blit(image, self.pos - (self.size.x / 2, self.size.y) - self.scene.camera.pos)

    def spread(self) -> None:
        if self.scene.energy_display.energy <= 0: return
        self.scene.energy_display.energy -= 1
        for _ in range(3):
            DandelionSeed(self.scene, self.pos - (1, self.size.y - 2) + (randint(-2, 2), randint(-2, 2)))

    def move(self, direction: int) -> None:
        skip = abs(direction)
        x = self.pos.x
        for _ in range(skip):
            x += sign(direction)
            while x not in self.scene.plants:
                x += sign(direction)
                if abs(x - self.pos.x) > 8:
                    return
        self.scene.player = self.scene.plants[int(x)]
        if self.scene.player.withered:
            self.scene.player.withered = False
            self.scene.energy_display.energy -= 1

class DandelionSeed(Sprite):
    def __init__(self, scene: Scene, pos: tuple[int, int]) -> None:
        super().__init__(scene, Layers.GRASS)
        self.scene.dandelion_seeds.append(self)
        self.size = VEC(texture.dandelion_seed.get_size())
        self.pos = VEC(pos)
        self.vel = VEC(0, 0)
        self.lift = uniform(20, 160)
        self.lift_timer = LoopTimer(lambda: uniform(0.3, 0.7))

    def update(self) -> None:
        self.vel.y += GRAVITY * self.manager.dt
        self.vel.x += self.scene.wind_speed * self.manager.dt
        self.vel.y -= self.lift * self.manager.dt
        self.vel *= 0.03 ** self.manager.dt
        self.pos += self.vel * self.manager.dt

        if self.lift_timer.ended:
            self.lift = uniform(20, 160)

        if self.pos.y + 3 >= self.scene.get_y(self.pos.x):
            self.kill()

        if not (self.scene.camera.pos.x - 50 < self.pos.x < self.scene.camera.pos.x + WIDTH + 50):
            self.kill()

    def draw(self) -> None:
        self.manager.screen.blit(texture.dandelion_seed, self.pos - self.size // 2 - self.scene.camera.pos)

    def kill(self) -> None:
        self.scene.dandelion_seeds.remove(self)
        super().kill()