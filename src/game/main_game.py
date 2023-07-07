from pygame.locals import *
from math import *
import pygame

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
import src.common.textures as texture
from src.game.ground import Ground
from src.game.camera import Camera
from src.common.constants import *
from src.game.mouse import Mouse
from src.game.grass import Grass

class MainGame(Scene):
    def setup(self) -> None:
        super().setup()
        self.grasses = {}

        self.grounds = {}
        for x in range(WIDTH + 1):
            Ground(self, x)

        self.player = Grass(self, 64)
        self.camera = Camera(self)
        self.energy_display = EnergyDisplay(self)
        Mouse(self, 40)

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

    def get_y(self, x: int) -> None:
        return self.grounds[floor(x - 0.5)].pos.y

class EnergyDisplay(Sprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layers.GUI)
        self.energy = 10

    def draw(self) -> None:
        self.manager.screen.blit(texture.energy, (3, 2))
        text = ENERGY_FONT.render(f"{self.energy}", False, (0, 0, 0))
        self.manager.screen.blit(text, (24, 0))