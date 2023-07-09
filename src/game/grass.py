from pygame.locals import *
from random import *
from math import *
import pygame

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common.timer import LoopTimer
import src.common.textures as texture
import src.common.audio as audio
from src.common.constants import *
from src.common.utils import *

class Grass(Sprite):
    def __init__(self, scene: Scene, x: int, withered: bool = False) -> None:
        super().__init__(scene, Layers.GRASS)
        self.scene.plants[int(x)] = self
        self.size = texture.grass.size.copy()
        self.pos = VEC(x, -150)
        self.sheet = texture.grass_sprout
        self.frame = 0
        self.ani_timer = LoopTimer(lambda: 0.08)
        self.bright = False
        self.lighten = (randint(0, 15), randint(0, 40), randint(0, 15))
        self.withered = withered
        if self.withered:
            self.sheet = texture.grass
            self.frame = randint(0, self.sheet.len - 1)
            self.ani_timer = LoopTimer(lambda: uniform(0.15, 0.3))

        if not withered:
            self.scene.stats["grass"] += 1
            self.scene.stats["distance"] = max(self.scene.stats["distance"], int(abs(self.pos.x)))

    def update(self) -> None:
        if not (self.scene.camera.pos.x - 1 <= self.pos.x <= self.scene.camera.pos.x + WIDTH + 1): return
        self.pos.y = self.scene.get_y(self.pos.x)

        if self.ani_timer.ended and not self.withered:
            self.frame += 1
            self.frame %= self.sheet.len
            if self.frame == 0:
                self.sheet = texture.grass
                self.ani_timer = LoopTimer(lambda: uniform(0.15, 0.3))

        self.bright = False
        if self.scene.player is self:
            self.bright = True

    def draw(self) -> None:
        if not (self.scene.camera.pos.x - 1 <= self.pos.x <= self.scene.camera.pos.x + WIDTH + 1): return
        image = self.sheet[self.frame].copy()
        if self.withered:
            (surf := pygame.Surface(image.get_size())).fill((140, 0, 0))
            image.blit(surf, (0, 0), special_flags=BLEND_RGB_ADD)
        if self.bright:
            (surf := pygame.Surface(image.get_size())).fill((80, 80, 80))
            image.blit(surf, (0, 0), special_flags=BLEND_RGB_ADD)
        (surf := pygame.Surface(image.get_size())).fill(self.lighten)
        image.blit(surf, (0, 0), special_flags=BLEND_RGB_ADD)
        self.manager.screen.blit(image, self.pos - (self.size.x / 2, self.size.y) - self.scene.camera.pos)

    def spread(self) -> None:
        if self.scene.energy_display.energy <= 0: return
        self.scene.energy_display.energy -= 1
        left = [-x for x in range(6) if self.pos.x - x not in self.scene.plants]
        right = [x for x in range(6) if self.pos.x + x not in self.scene.plants]
        direction = choice([left, right]) if len(left) == len(right) else (left if len(left) > len(right) else right)
        if not direction: return
        Grass(self.scene, self.pos.x + choice(direction))
        audio.grow.play()

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
            self.scene.stats["grass"] += 1
            self.scene.stats["distance"] = max(self.scene.stats["distance"], int(abs(self.scene.player.pos.x)))