from pygame.locals import *

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common.timer import LoopTimer
import src.common.textures as texture
from src.common.constants import *
from src.common.utils import *

class Bush(Sprite):
    def __init__(self, scene: Scene, x: int) -> None:
        super().__init__(scene, Layers.PLANTS)
        self.scene.plants[int(x)] = self
        self.size = VEC(texture.bush.get_size())
        self.pos = VEC(x, -200)
        self.vel = VEC(0, 0)
        self.bright = False
        self.detached = False
        self.detach_timer = LoopTimer(lambda: 0.5)

    def update(self) -> None:
        self.bright = False
        if self.scene.player is self:
            self.bright = True

        if self.detached:
            self.vel.x += self.scene.wind_speed * self.manager.dt
            if not self.scene.gust:
                self.vel.x *= 0.85
            self.vel.x *= 0.98
            self.pos += self.vel * self.manager.dt
            if self.detach_timer.ended:
                self.scene.energy_display.energy -= 1

        self.pos.y = self.scene.get_y(self.pos.x)

    def draw(self) -> None:
        image = texture.bush.copy()
        if self.bright:
            (surf := pygame.Surface(image.get_size())).fill((60, 60, 60))
            image.blit(surf, (0, 0), special_flags=BLEND_RGB_ADD)
        self.manager.screen.blit(image, self.pos - (self.size.x / 2, self.size.y) - self.scene.camera.pos)

    def spread(self) -> None:
        self.detached = not self.detached

    def move(self, direction: int) -> None:
        skip = abs(direction)
        x = self.pos.x
        for _ in range(skip):
            x += sign(direction)
            while x not in self.scene.plants:
                x += sign(direction)
                if abs(x - self.pos.x) > 20:
                    return
        self.scene.player = self.scene.plants[int(x)]