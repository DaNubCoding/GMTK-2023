from pygame.locals import *
import pytweening as tween
import pygame

from src.management.sprite import Sprite, Layers
from src.common.timer import LoopTimer, Timer
from src.management.scene import Scene
from src.common.constants import *

class StatText(Sprite):
    def __init__(self, scene: Scene, index: int, name: str, value: int) -> None:
        super().__init__(scene, Layers.GUI)
        self.pos = VEC(5, 5 + index * 10)
        self.text = f"{name}: {value}"
        self.text_surf = MAIN_FONT.render(self.text, False, (0, 0, 0))
        self.size = VEC(75, self.text_surf.get_height())
        self.progress = 0
        self.linear_progress = 0
        self.delay_timer = Timer(lambda: index * 0.2)
        self.delay_timer.start()

    def update(self) -> None:
        if not self.delay_timer.ended: return
        self.linear_progress += 0.8 * self.manager.dt
        if self.linear_progress > 1:
            self.linear_progress = 1
            return
        self.progress = tween.easeOutExpo(self.linear_progress)

    def draw(self) -> None:
        if not self.delay_timer.ended: return
        (surf := pygame.Surface(VEC(self.size.x * self.progress, self.size.y), SRCALPHA)).fill((255, 255, 255, 40))
        self.manager.screen.blit(surf, self.pos)
        pygame.draw.rect(self.manager.screen, (0, 0, 0), (self.pos, (self.size.x * self.progress, self.size.y)), 1)
        if self.progress > 0.75:
            self.manager.screen.blit(self.text_surf, self.pos + (2, 0))

class LongStatText(Sprite):
    def __init__(self, scene: Scene, y: int, name: str, value: int) -> None:
        super().__init__(scene, Layers.GUI)
        self.pos = VEC(5, y)
        self.text = f"{name}: {value}"
        self.text_surf = MAIN_FONT.render(self.text, False, (0, 0, 0))
        self.size = VEC(118, self.text_surf.get_height())
        self.flash_timer = LoopTimer(lambda: 0.5)
        self.white = False
        self.delay_timer = Timer(lambda: 1.8)
        self.delay_timer.start()
        self.complete = False

    def update(self) -> None:
        if not self.delay_timer.ended: return
        self.complete = True
        if self.flash_timer.ended:
            self.white = not self.white

    def draw(self) -> None:
        if not self.delay_timer.ended: return
        (surf := pygame.Surface(self.size, SRCALPHA)).fill((255, 255, 255, 40))
        self.manager.screen.blit(surf, self.pos)
        pygame.draw.rect(self.manager.screen, (self.white * 255,) * 3, (self.pos, self.size), 1)
        self.manager.screen.blit(self.text_surf, self.pos + (2, 0))