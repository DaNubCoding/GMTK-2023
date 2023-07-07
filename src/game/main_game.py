import pygame

from src.management.scene import Scene

class MainGame(Scene):
    def setup(self) -> None:
        super().setup()
        # here

    def update(self) -> None:
        # here
        super().update()
        # or here

    def draw(self) -> None:
        self.manager.screen.fill((25, 25, 25))
        pygame.draw.rect(self.manager.screen, (255, 0, 0), (100, 100, 100, 100))
        # here
        super().draw()
        # or here