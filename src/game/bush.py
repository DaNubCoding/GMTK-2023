from pygame.locals import *
from random import *
from math import *

from src.management.sprite import Sprite, Layers
from src.management.scene import Scene
from src.common.timer import LoopTimer
import src.common.textures as texture
from src.common.constants import *
import src.common.audio as audio
from src.common.utils import *

class Bush(Sprite):
    def __init__(self, scene: Scene, x: int, withered: bool = False) -> None:
        super().__init__(scene, Layers.BUSH)
        self.scene.plants[int(x)] = self
        self.scene.bushes.append(self)
        self.size = VEC(texture.bush.get_size())
        self.pos = VEC(x, -200)
        self.fixed_x = x
        self.vel = VEC(0, 0)
        self.bright = False
        self.detached = False
        self.detach_timer = LoopTimer(lambda: 1.2)
        self.rot = 0
        self.withered = withered
        self.replaced_plant = None
        self.sound_timer = LoopTimer(lambda: 1)

        if not withered:
            self.scene.stats["bush"] += 1
            self.scene.stats["distance"] = max(self.scene.stats["distance"], int(abs(self.pos.x)))

    def update(self) -> None:
        self.bright = False
        if self.scene.player is self:
            self.bright = True

        if self.detached:
            self.vel.x += self.scene.wind_speed * self.manager.dt
            if not self.scene.gust:
                self.vel.x *= 0.015 ** self.manager.dt
            self.vel.x *= 0.1 ** self.manager.dt
            self.pos += self.vel * self.manager.dt
            if self.detach_timer.ended:
                self.scene.energy_display.energy -= 1

            if self.sound_timer.ended:
                choice(audio.rustle).play()

        self.pos.y = self.scene.get_y(self.pos.x)

    def draw(self) -> None:
        if not (self.scene.camera.pos.x - 10 <= self.pos.x <= self.scene.camera.pos.x + WIDTH + 10): return
        image = texture.bush.copy()
        if self.withered:
            (surf := pygame.Surface(image.get_size())).fill((140, 0, 0))
            image.blit(surf, (0, 0), special_flags=BLEND_RGB_ADD)
        if self.bright:
            (surf := pygame.Surface(image.get_size())).fill((60, 60, 60))
            image.blit(surf, (0, 0), special_flags=BLEND_RGB_ADD)
        if self.detached:
            self.rot += -degrees(self.vel.x * self.manager.dt / (texture.bush.get_width() // 2))
            image = pygame.transform.rotate(image, self.rot)
        self.manager.screen.blit(image, self.pos - (image.get_width() / 2, image.get_height() / 2 + self.size.y / 2) - self.scene.camera.pos)

    def spread(self) -> None:
        self.detached = not self.detached
        self.withered = self.detached
        if not self.detached:
            del self.scene.plants[self.fixed_x]
            self.fixed_x = int(self.pos.x)
            if self.fixed_x in self.scene.plants:
                self.scene.plants[self.fixed_x].kill()
            self.scene.plants[self.fixed_x] = self
            self.scene.stats["distance"] = max(self.scene.stats["distance"], int(abs(self.pos.x)))

    def move(self, direction: int) -> None:
        if self.detached: return
        skip = abs(direction)
        x = int(self.pos.x)
        for _ in range(skip):
            x += sign(direction)
            while x not in self.scene.plants:
                x += sign(direction)
                if abs(x - self.pos.x) > 20:
                    return
        self.scene.player = self.scene.plants[x]
        if self.scene.player.withered:
            self.scene.player.withered = False
            self.scene.energy_display.energy -= 1
            self.scene.stats["bush"] += 1
            self.scene.stats["distance"] = max(self.scene.stats["distance"], int(abs(self.scene.player.pos.x)))