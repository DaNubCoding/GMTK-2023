from pygame.locals import *
import pygame

from src.management.scene import Scene
from src.game.grass import Grass
from src.game.ground import Ground
from src.game.camera import Camera
from src.common.constants import *

class MainGame(Scene):
    def setup(self) -> None:
        super().setup()
        self.grasses = {}

        self.player = Grass(self, 64)
        self.camera = Camera(self)

        self.grounds = {}
        for x in range(WIDTH + 1):
            Ground(self, x)

    def update(self) -> None:
        self.camera.update()
        super().update()
        if KEYDOWN in self.manager.events:
            if self.manager.events[KEYDOWN].key == K_SPACE:
                self.player.spread()
            elif self.manager.events[KEYDOWN].key == K_LEFT:
                self.player.move(-1)
            elif self.manager.events[KEYDOWN].key == K_RIGHT:
                self.player.move(1)

    def draw(self) -> None:
        self.manager.screen.fill(SKY_COLOR)
        # here
        super().draw()
        # or here