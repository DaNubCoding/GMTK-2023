from pygame.locals import *
from random import *
from math import *
import pygame

from src.management.scene import Scene
from src.common.timer import LoopTimer
import src.common.textures as texture
from src.common.constants import *

class MainMenu(Scene):
    def setup(self) -> None:
        super().setup()
        self.flash_timer = LoopTimer(lambda: 0.5)
        self.white = False
        self.white_text = MAIN_FONT.render("Press space to start!", False, (255, 255, 255))
        self.black_text = MAIN_FONT.render("Press space to start!", False, (0, 0, 0))

    def update(self) -> None:
        super().update()
        if self.flash_timer.ended:
            self.white = not self.white

        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            self.manager.new_scene("MainGame")

    def draw(self) -> None:
        self.manager.screen.blit(texture.menu, (0, 0))
        super().draw()
        self.manager.screen.blit(self.white_text if self.white else self.black_text, (WIDTH / 2 - self.white_text.get_width() / 2, 75))