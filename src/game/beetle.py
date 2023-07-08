from random import *
from math import *
import pygame

from src.management.sprite import Sprite, Layers
from src.common.timer import LoopTimer, Timer
from src.game.death_particle import DeathParticle
from src.management.scene import Scene
import src.common.textures as texture
from src.common.constants import *

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
        self.death_timer = Timer(lambda: 1.5)
        self.digging = True

    def update(self) -> None:
        if self.dead:
            self.disintegrate()
            return

        if self.pos.y > self.scene.get_y(self.pos.x):
            self.pos.y -= 6 * self.manager.dt
        else:
            self.pos.y = self.scene.get_y(self.pos.x)
            self.digging = False

        if self.start_move_timer.ended and not self.digging:
            self.move_timer.start()
            self.direction = uniform(-20, -15) if randint(0, 1) else uniform(15, 20)
        if not self.move_timer.ended and not self.digging:
            self.pos.x += self.direction * self.manager.dt

        if self.digging: return
        for x in range(int(-self.size.x // 2) + 1, int(self.size.x // 2)):
            if int(self.pos.x + x) in self.scene.plants:
                self.dead = True
                self.death_timer.start()
                self.collided = self.scene.plants[int(self.pos.x + x)]

    def draw(self) -> None:
        image = pygame.transform.flip(self.image, self.direction < 0, False)
        if self.digging:
            image = pygame.transform.rotate(image, -90)
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
            if abs(self.scene.player.pos.x - self.collided.pos.x) < self.image.get_width() // 2:
                self.scene.energy_display.energy += 10