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
import src.common.audio as audio
from src.common.utils import *

class Bird(Sprite):
    def __init__(self, scene: Scene, x: int) -> None:
        super().__init__(scene, Layers.ANIMALS)
        self.scene.bird_count += 1
        self.size = texture.bird.size.copy()
        self.pos = VEC(x, -30)
        self.vel = VEC(0, 0)
        self.target = self.pos + (randint(-10, 10), randint(40, 60))
        self.frame = 0
        self.ani_timer = LoopTimer(lambda: 0.05)
        self.dead = False
        self.death_timer = Timer(lambda: 1.5)
        self.health = 3
        self.immune_timer = Timer(lambda: 0.2)
        self.immune = False
        self.collided = None
        self.flashing = False
        self.flash_count = 0
        self.flash_timer = LoopTimer(lambda: 0.2)
        self.white = False
        self.dandify = False
        self.sound_timer = LoopTimer(lambda: uniform(1, 4))

    def update(self) -> None:
        if not (self.scene.camera.pos.x - 60 <= self.pos.x <= self.scene.camera.pos.x + WIDTH + 60): self.kill()

        if self.dead:
            self.disintegrate()
            return

        if self.sound_timer.ended:
            choice(audio.chirp).play()

        if self.ani_timer.ended:
            self.frame += 1
            self.frame %= texture.bird.len

        if self.pos.distance_to(self.target) <= 2:
            self.target = self.pos + (randint(-40, -15) if randint(0, 1) else randint(15, 40), randint(-5, 8))
        self.vel = (self.target - self.pos and (self.target - self.pos).normalize()) * 25
        self.pos += self.vel * self.manager.dt

        if self.flashing and self.flash_timer.ended:
            self.flash_count += 1
            self.white = not self.white
            if self.flash_count > 6:
                self.flashing = False
                self.white = False

        self.rect = pygame.Rect(self.pos - (self.size.x / 2, self.size.y) + (0, 2), self.size - (0, 4))

        if self.target.x > self.scene.camera.pos.x + WIDTH:
            self.target.x -= 20
        elif self.target.x < self.scene.camera.pos.x:
            self.target.x += 20
        if self.target.y < 0:
            self.target.y += 10

        if self.immune:
            if self.immune_timer.ended:
                self.immune = False
            return
        for x in range(int(-self.size.x // 2) + 1, int(self.size.x // 2) + 1):
            if int(self.pos.x + x) in self.scene.plants and not self.scene.plants[int(self.pos.x + x)].withered and not isinstance(self.scene.plants[int(self.pos.x + x)], Dandelion):
                plant = self.scene.plants[int(self.pos.x + x)]
                if plant.pos.y - 6 > self.rect.bottom: continue
                self.damage()
                if self.health == 0:
                    audio.disintegrate.play()
                    self.dead = True
                    self.death_timer.start()
                    self.collided = self.scene.plants[int(self.pos.x + x)]
                break

        for bush in self.scene.bushes:
            if not bush.detached: continue
            if self.rect.colliderect(pygame.Rect(bush.pos.x - bush.size.x / 2, bush.pos.y - bush.size.y, bush.size.x, bush.size.y)):
                self.damage()
                if self.health == 0:
                    audio.disintegrate.play()
                    self.dead = True
                    self.death_timer.start()
                    self.scene.energy_display.energy += 10
                break

        for seed in self.scene.dandelion_seeds:
            if self.rect.colliderect(pygame.Rect(seed.pos, seed.size)):
                self.damage()
                if self.health == 0:
                    audio.disintegrate.play()
                    self.dead = True
                    self.death_timer.start()
                    self.scene.energy_display.energy += 5
                    self.dandify = True
                break

    def damage(self) -> None:
        audio.hurt.play()
        self.knockback = True
        self.flashing = True
        self.immune_timer.start()
        self.immune = True
        self.health -= 1
        self.target = self.pos - (self.target - self.pos) - (0, 20)

    def draw(self) -> None:
        if not (self.scene.camera.pos.x - 10 <= self.pos.x <= self.scene.camera.pos.x + WIDTH + 10): return
        image = pygame.transform.flip(texture.bird[self.frame], self.vel.x < 0, False)
        if self.white:
            (surf := pygame.Surface(image.get_size())).fill((255, 255, 255))
            image.blit(surf, (0, 0), special_flags=BLEND_RGB_ADD)
        self.manager.screen.blit(image, self.pos - (self.size.x / 2, self.size.y) - self.scene.camera.pos)

    def disintegrate(self) -> None:
        for _ in range(ceil(self.death_timer.progress * 8)):
            image = texture.bird[self.frame].copy()
            pos = (randint(0, texture.bird.size.x - 1), randint(0, texture.bird.size.y - 1))
            color = image.get_at(pos)
            image.set_at(pos, (0, 0, 0, 0))
            if color != (0, 0, 0, 0):
                DeathParticle(self.scene, self.pos + pos - (self.size.x / 2, self.size.y), color)
        if self.death_timer.ended:
            self.kill()
            self.scene.mice_count -= 1
            if self.collided and abs(self.scene.player.pos.x - self.collided.pos.x) < texture.bird.size.x // 2:
                self.scene.energy_display.energy += 10
            if self.dandify:
                if int(self.pos.x) in self.scene.plants:
                    self.scene.plants[int(self.pos.x)].kill()
                self.scene.plants[int(self.pos.x)] = Dandelion(self.scene, int(self.pos.x))
            self.scene.stats["bird"] += 1