from pygame.locals import *

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
import src.common.textures as texture
from src.common.constants import *
from src.common.utils import *

class Bush(Sprite):
    def __init__(self, scene: Scene, x: int) -> None:
        super().__init__(scene, Layers.PLANTS)
        self.scene.plants[int(x)] = self
        self.size = VEC(texture.bush.get_size())
        self.pos = VEC(x, -200)
        self.bright = False

    def update(self) -> None:
        self.pos.y = self.scene.get_y(self.pos.x)

        self.bright = False
        if self.scene.player is self:
            self.bright = True

    def draw(self) -> None:
        image = texture.bush.copy()
        if self.bright:
            (surf := pygame.Surface(image.get_size())).fill((60, 60, 60))
            image.blit(surf, (0, 0), special_flags=BLEND_RGB_ADD)
        self.manager.screen.blit(image, self.pos - (self.size.x / 2, self.size.y) - self.scene.camera.pos)

    def spread(self) -> None:
        pass

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