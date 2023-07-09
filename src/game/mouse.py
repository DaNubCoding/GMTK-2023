from pygame.locals import *
from random import *
from math import *
import pygame

from src.game.death_particle import DeathParticle
from src.management.sprite import Sprite, Layers
from src.common.timer import LoopTimer, Timer
from src.game.dandelion import Dandelion
from src.management.scene import Scene
import src.common.textures as texture
from src.common.constants import *
from src.common.utils import *

class Mouse(Sprite):
    def __init__(self, scene: Scene, x: int) -> None:
        super().__init__(scene, Layers.ANIMALS)
        self.scene.mice_count += 1
        self.size = VEC(texture.mouse.get_size())
        self.pos = VEC(x, self.scene.get_y(x))
        self.vel = VEC(0, 0)
        self.direction = 20 if self.pos.x < self.scene.camera.pos.x else -20
        self.start_move_timer = LoopTimer(lambda: uniform(1, 5))
        self.move_timer = Timer(lambda: uniform(0.4, 1))
        self.image = texture.mouse.copy()
        self.dead = False
        self.death_timer = Timer(lambda: 1.5)
        self.health = 2
        self.in_grass = False
        self.knockback = False
        self.immune_timer = Timer(lambda: 0.2)
        self.immune = False
        self.collided = None
        self.flashing = False
        self.flash_count = 0
        self.flash_timer = LoopTimer(lambda: 0.2)
        self.white = False
        self.dandify = False

    def update(self) -> None:
        if not (self.scene.camera.pos.x - 60 <= self.pos.x <= self.scene.camera.pos.x + WIDTH + 60): self.kill()

        if self.dead:
            self.disintegrate()
            return

        if self.start_move_timer.ended:
            self.move_timer.start()
            self.direction = uniform(-20, -15) if randint(0, 1) else uniform(15, 20)
        if not self.move_timer.ended:
            self.pos.x += self.direction * self.manager.dt
        if self.knockback:
            self.vel.x -= sign(self.vel.x) * 350 * self.manager.dt
            self.vel.y += GRAVITY * self.manager.dt
            self.pos += self.vel * self.manager.dt
            if self.pos.y > self.scene.get_y(self.pos.x):
                self.knockback = False
        else:
            self.pos.y = self.scene.get_y(self.pos.x)

        for x in range(int(-self.size.x // 2) - 2, int(self.size.x // 2) + 2):
            if int(self.pos.x + x) in self.scene.plants and not self.scene.plants[int(self.pos.x + x)].withered and self.pos.y < self.scene.get_y(self.pos.x) + 6 and not isinstance(self.scene.plants[int(self.pos.x + x)], Dandelion):
                if randint(0, 1):
                    self.move_timer.stop()
                self.direction = abs(self.direction) * -sign(x)

        if self.flashing and self.flash_timer.ended:
            self.flash_count += 1
            self.white = not self.white
            if self.flash_count > 6:
                self.flashing = False
                self.white = False

        if self.immune:
            if self.immune_timer.ended:
                self.immune = False
            return
        for x in range(int(-self.size.x // 2) + 1, int(self.size.x // 2) + 1):
            if int(self.pos.x + x) in self.scene.plants and not self.scene.plants[int(self.pos.x + x)].withered and not isinstance(self.scene.plants[int(self.pos.x + x)], Dandelion):
                self.damage(x)
                if self.health == 0:
                    self.dead = True
                    self.death_timer.start()
                    self.collided = self.scene.plants[int(self.pos.x + x)]

        for bush in self.scene.bushes:
            if not bush.detached: continue
            if self.pos.x - 16 <= bush.pos.x <= self.pos.x + 16:
                self.damage(bush.pos.x - self.pos.x)
                if self.health == 0:
                    self.dead = True
                    self.death_timer.start()
                    self.scene.energy_display.energy += 10

        for seed in self.scene.dandelion_seeds:
            if pygame.Rect(seed.pos, seed.size).colliderect(pygame.Rect(self.pos - (self.size.x / 2, self.size.y) + (2, 2), self.size - (4, 4))):
                self.damage(seed.pos.x - self.pos.x)
                if self.health == 0:
                    self.dead = True
                    self.death_timer.start()
                    self.scene.energy_display.energy += 5
                    self.dandify = True

    def damage(self, x: int) -> None:
        self.knockback = True
        self.flashing = True
        self.vel.x = -sign(x) * 90
        self.vel.y = -20
        self.immune_timer.start()
        self.immune = True
        self.health -= 1
        self.direction = -sign(x) * abs(self.direction)

    def draw(self) -> None:
        if not (self.scene.camera.pos.x - 10 <= self.pos.x <= self.scene.camera.pos.x + WIDTH + 10): return
        image = pygame.transform.flip(self.image, self.direction < 0, False)
        if self.white:
            (surf := pygame.Surface(image.get_size())).fill((255, 255, 255))
            image.blit(surf, (0, 0), special_flags=BLEND_RGB_ADD)
        self.manager.screen.blit(image, self.pos - (self.size.x / 2, self.size.y) - self.scene.camera.pos)

    def disintegrate(self) -> None:
        for _ in range(ceil(self.death_timer.progress * 8)):
            pos = (randint(0, self.image.get_width() - 1), randint(0, self.image.get_height() - 1))
            color = self.image.get_at(pos)
            self.image.set_at(pos, (0, 0, 0, 0))
            if color != (0, 0, 0, 0):
                DeathParticle(self.scene, self.pos + pos - (self.size.x / 2, self.size.y), color)
        if self.death_timer.ended:
            self.kill()
            self.scene.mice_count -= 1
            if self.collided and abs(self.scene.player.pos.x - self.collided.pos.x) < self.image.get_width() // 2:
                self.scene.energy_display.energy += 10
            if self.dandify:
                if int(self.pos.x) in self.scene.plants:
                    self.scene.plants[int(self.pos.x)].kill()
                self.scene.plants[int(self.pos.x)] = Dandelion(self.scene, int(self.pos.x))
            self.scene.stats["mouse"] += 1