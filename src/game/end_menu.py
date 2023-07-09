from pygame.locals import *
from random import *
from math import *
import pygame

from src.game.end_text import StatText, LongStatText
from src.management.scene import Scene
from src.common.timer import LoopTimer
from src.common.constants import *

class EndMenu(Scene):
    def setup(self) -> None:
        super().setup()
        self.blur_amount = 1
        self.blur_timer = LoopTimer(lambda: 0.08)
        self.background = pygame.transform.gaussian_blur(self.previous_scene.screenshot, 1)
        self.stats = self.previous_scene.stats

        for i, stat in enumerate(self.stats):
            StatText(self, i, stat, self.stats[stat])
        score = int(self.stats["distance"] * 1 + self.stats["grass"] * 0.5 + (30 if self.stats["bush"] else 0) + self.stats["bush"] * 2 + (60 if self.stats["dandelion"] else 0) + self.stats["dandelion"] * 3 + self.stats["beetle"] * 0.2 + (40 if self.stats["mouse"] else 0) + self.stats["mouse"] * 0.5 + (80 if self.stats["bird"] else 0) + self.stats["bird"] * 4)
        self.final = LongStatText(self, 5 + i * 10 + 15, "Final score", score)

        self.text_surf = MAIN_FONT.render("Press space to restart", False, (0, 0, 0), None, 39)

    def update(self) -> None:
        super().update()

        if self.final.complete:
            keys = pygame.key.get_pressed()
            if keys[K_SPACE]:
                self.manager.new_scene("MainGame")

    def draw(self) -> None:
        if self.blur_timer.ended and self.blur_amount < 7:
            self.background = pygame.transform.gaussian_blur(self.background, 1)
            self.blur_amount += 1
        self.manager.screen.blit(self.background, (0, 0))
        super().draw()

        if self.final.complete:
            self.manager.screen.blit(self.text_surf, (83, 39))