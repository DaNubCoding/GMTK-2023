from random import *
from math import *
import pygame

from src.management.sprite import Sprite, Layers
from src.common.timer import LoopTimer, Timer
from src.game.death_particle import Particle
from src.management.scene import Scene
import src.common.textures as texture
from src.common.constants import *

class Mouse(Sprite):
    def __init__(self, scene: Scene, x: int) -> None:
        super().__init__(scene, Layers.ANIMALS)
        self.size = VEC(texture.mouse.get_size())
        self.pos = VEC(x, self.scene.get_y(x))
        self.direction = 0
        self.start_move_timer = LoopTimer(lambda: uniform(1, 5))
        self.start_move_timer.start += 2
        self.move_timer = Timer(lambda: uniform(0.4, 1))
        self.image = texture.mouse
        self.dead = False
        self.death_timer = Timer(lambda: 1.5)

    def update(self) -> None:
        if self.dead:
            self.disintegrate()
            return

        self.pos.y = self.scene.get_y(self.pos.x)

        if self.start_move_timer.ended:
            self.move_timer.start()
            self.direction = uniform(-20, -15) if randint(0, 1) else uniform(15, 20)
        if not self.move_timer.ended:
            self.pos.x += self.direction * self.manager.dt

        for x in range(int(-self.size.x // 2), int(self.size.x // 2)):
            if int(self.pos.x + x) in self.scene.grasses:
                self.dead = True
                self.death_timer.start()

    def draw(self) -> None:
        image = pygame.transform.flip(self.image, self.direction < 0, False)
        self.manager.screen.blit(image, self.pos - (self.size.x / 2, self.size.y) - self.scene.camera.pos)

    def disintegrate(self) -> None:
        for _ in range(ceil(self.death_timer.progress * 8)):
            pos = (randint(0, self.image.get_width() - 1), randint(0, self.image.get_height() - 1))
            color = self.image.get_at(pos)
            self.image.set_at(pos, (0, 0, 0, 0))
            if color != (0, 0, 0, 0):
                Particle(self.scene, self.pos + pos - (self.size.x / 2, self.size.y), color)
        if self.death_timer.ended:
            self.kill()