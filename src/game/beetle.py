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

class Beetle(Sprite):
    def __init__(self, scene: Scene, x: int) -> None:
        super().__init__(scene, Layers.ANIMALS)
        self.size = VEC(texture.beetle.get_size())
        self.pos = VEC(x, 110)
        self.direction = 20 if self.pos.x < self.scene.camera.pos.x else -20
        self.start_move_timer = LoopTimer(lambda: uniform(1, 5))
        self.move_timer = Timer(lambda: uniform(0.4, 1))
        self.image = texture.beetle.copy()
        self.dead = False
        self.death_timer = Timer(lambda: 1)
        self.digging = True
        self.collided = None
        self.dandify = False
        self.sound_timer = LoopTimer(lambda: 1.5)

    def update(self) -> None:
        if not (self.scene.camera.pos.x - 60 <= self.pos.x <= self.scene.camera.pos.x + WIDTH + 60): self.kill()

        if self.dead:
            self.disintegrate()
            return

        if self.pos.y > self.scene.get_y(self.pos.x) + 2:
            self.pos.y -= 6 * self.manager.dt
        else:
            self.pos.y = self.scene.get_y(self.pos.x)
            self.digging = False

        if self.start_move_timer.ended and not self.digging:
            self.move_timer.start()
            self.direction = uniform(-20, -15) if randint(0, 1) else uniform(15, 20)
        if not self.move_timer.ended and not self.digging:
            self.pos.x += self.direction * self.manager.dt
            if self.sound_timer.ended:
                choice(audio.footsteps).play()

        for x in range(int(-self.size.x // 2) - 2, int(self.size.x // 2) + 2):
            if int(self.pos.x + x) in self.scene.plants and not self.scene.plants[int(self.pos.x + x)].withered and not isinstance(self.scene.plants[int(self.pos.x + x)], Dandelion):
                if randint(0, 1):
                    self.move_timer.stop()
                self.direction = abs(self.direction) * -sign(x)

        if self.digging: return
        for x in range(int(-self.size.x // 2) + 1, int(self.size.x // 2) + 1):
            if int(self.pos.x + x) in self.scene.plants and not self.scene.plants[int(self.pos.x + x)].withered and not isinstance(self.scene.plants[int(self.pos.x + x)], Dandelion):
                self.dead = True
                self.death_timer.start()
                self.collided = self.scene.plants[int(self.pos.x + x)]
                audio.hurt.play()
                audio.disintegrate.play()

        for bush in self.scene.bushes:
            if not bush.detached: continue
            if self.pos.x - 8 <= bush.pos.x <= self.pos.x + 8:
                self.dead = True
                self.death_timer.start()
                self.scene.energy_display.energy += 2
                audio.hurt.play()
                audio.disintegrate.play()

        for seed in self.scene.dandelion_seeds:
            if pygame.Rect(seed.pos, seed.size).colliderect(pygame.Rect(self.pos - (self.size.x / 2, self.size.y), self.size)):
                self.dead = True
                self.death_timer.start()
                self.dandify = True
                audio.hurt.play()
                audio.disintegrate.play()

    def draw(self) -> None:
        if not (self.scene.camera.pos.x - 5 <= self.pos.x <= self.scene.camera.pos.x + WIDTH + 5): return
        image = self.image.copy()
        if self.digging:
            image = pygame.transform.rotate(image, 90)
        image = pygame.transform.flip(image, self.direction < 0, False)
        self.manager.screen.blit(image, self.pos - (self.size.x / 2, self.size.y) - self.scene.camera.pos)

    def disintegrate(self) -> None:
        for _ in range(ceil(self.death_timer.progress)):
            pos = (randint(0, self.image.get_width() - 1), randint(0, self.image.get_height() - 1))
            color = self.image.get_at(pos)
            self.image.set_at(pos, (0, 0, 0, 0))
            if color != (0, 0, 0, 0):
                DeathParticle(self.scene, self.pos + pos - (self.size.x / 2, self.size.y), color)
        if self.death_timer.ended:
            self.kill()
            if self.collided and abs(self.scene.player.pos.x - self.collided.pos.x) <= 5:
                self.scene.energy_display.energy += 2
            if self.dandify:
                if int(self.pos.x) in self.scene.plants:
                    self.scene.plants[int(self.pos.x)].kill()
                self.scene.plants[int(self.pos.x)] = Dandelion(self.scene, int(self.pos.x))
            self.scene.stats["beetle"] += 1