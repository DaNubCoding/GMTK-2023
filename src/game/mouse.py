from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
import src.common.textures as texture
from src.common.constants import *

class Mouse(Sprite):
    def __init__(self, scene: Scene, x: int) -> None:
        super().__init__(scene, Layers.ANIMALS)
        self.size = VEC(texture.mouse.get_size())
        self.pos = VEC(x, self.scene.get_y(x))

    def update(self) -> None:
        self.pos.y = self.scene.get_y(self.pos.x)

    def draw(self) -> None:
        self.manager.screen.blit(texture.mouse, self.pos - (self.size.x / 2, self.size.y) - self.scene.camera.pos)