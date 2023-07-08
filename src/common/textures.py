import pygame

from .constants import *

pygame.display.set_mode((1, 1), pygame.NOFRAME)

def load_image(file):
    return pygame.image.load(f"res/textures/{file}").convert_alpha()

class SpriteSheet(list):
    def __init__(self, path: str, width: int) -> None:
        self.image = load_image(path)
        for i in range(self.image.get_width() // width):
            self.append(self.image.subsurface((i * width, 0, width, self.image.get_height())))
        self.size = VEC(width, self.image.get_height())
        self.len = len(self)

grass = SpriteSheet("grass.png", 3)
energy = load_image("energy.png")
mouse = load_image("mouse.png")
bush = load_image("bush.png")
beetle = load_image("beetle.png")

pygame.display.quit()