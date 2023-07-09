from pygame.locals import *
from random import *
from math import *
import pygame

from src.management.sprite import Sprite, Layers
from src.game.wind_particle import WindParticle
from src.common.timer import LoopTimer, Timer
from src.management.scene import Scene
import src.common.textures as texture
from src.game.ground import Ground
from src.game.camera import Camera
from src.game.beetle import Beetle
from src.common.constants import *
from src.game.mouse import Mouse
from src.game.grass import Grass
import src.common.audio as audio
from src.game.bird import Bird

class MainGame(Scene):
    def setup(self) -> None:
        super().setup()
        
        self.stats = {
            "distance": 0,
            "grass": 0,
            "bush": 0,
            "dandelion": 0,
            "beetle": 0,
            "mouse": 0,
            "bird": 0,
        }

        self.plants = {}
        self.grounds = {}
        for x in range(-WIDTH // 2, WIDTH // 2 + 1):
            Ground(self, x)
        self.player = Grass(self, 0)
        self.camera = Camera(self)
        self.energy_display = EnergyDisplay(self)
        self.mice_timer = LoopTimer(lambda: uniform(6, 10))
        self.mice_count = 0
        self.beetle_timer = LoopTimer(lambda: uniform(4, 7))
        self.wind_speed = choice([-50, 50])
        self.wind_speed_timer = LoopTimer(lambda: uniform(4, 12))
        self.wind = Wind(self)
        self.wind_particle_timer = LoopTimer(lambda: 0.2)
        self.wind_gust_start_timer = LoopTimer(lambda: uniform(6, 8))
        self.wind_gust_timer = Timer(lambda: uniform(3, 5))
        self.wind_gust_timer.start()
        self.gust = False
        self.bushes = []
        self.dandelion_seeds = []
        self.bird_timer = LoopTimer(lambda: uniform(4, 7))
        self.bird_count = 0

        pygame.mixer.pause()
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        audio.wind.play(-1)

    def update(self) -> None:
        self.camera.update()
        super().update()

        keys = pygame.key.get_pressed()
        if KEYDOWN in self.manager.events:
            if self.manager.events[KEYDOWN].key == K_SPACE:
                self.player.spread()
            elif self.manager.events[KEYDOWN].key == K_LEFT:
                self.player.move(-5 if keys[K_LCTRL] else -1)
            elif self.manager.events[KEYDOWN].key == K_RIGHT:
                self.player.move(5 if keys[K_LCTRL] else 1)

        for x in range(WIDTH + 50):
            if self.camera.pos.x - 25 + x not in self.grounds:
                Ground(self, self.camera.pos.x - 25 + x)

        if abs(self.camera.pos.x + WIDTH // 2) > 64 and self.mice_timer.ended and self.mice_count < 2:
            Mouse(self, self.camera.pos.x + choice([-12, WIDTH + 12]))

        if self.beetle_timer.ended:
            Beetle(self, self.camera.pos.x + randint(16, WIDTH - 16))

        if abs(self.camera.pos.x + WIDTH // 2) > 240 and self.bird_timer.ended and self.bird_count < 2:
            Bird(self, self.camera.pos.x + randint(16, WIDTH - 16))

        if self.wind_particle_timer.ended:
            WindParticle(self)
            if self.wind_gust_start_timer.ended:
                self.wind_gust_timer.start()
                self.gust = True
            if not self.wind_gust_timer.ended:
                for _ in range(5):
                    WindParticle(self)
            else:
                self.gust = False

        if self.wind_speed_timer.ended:
            self.wind_speed = choice([-50, 50])

    def draw(self) -> None:
        self.manager.screen.blit(texture.sky, (0, 0))
        # here
        super().draw()
        # or here

    def get_y(self, x: int) -> float:
        try:
            return self.grounds[floor(x - 0.5)].pos.y
        except KeyError:
            return -10

class EnergyDisplay(Sprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layers.GUI)
        self.energy = 10
        self.energy_timer = LoopTimer(lambda: 10)

    def update(self) -> None:
        if self.energy_timer.ended:
            self.energy -= 1
        if self.energy < 0:
            self.energy = 0
            self.scene.screenshot = self.manager.screen.copy()
            self.manager.new_scene("EndMenu")

    def draw(self) -> None:
        self.manager.screen.blit(texture.energy, (3, 2))
        text = ENERGY_FONT.render(f"{self.energy}", False, (0, 0, 0))
        self.manager.screen.blit(text, (24, 0))

class Wind(Sprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layers.WIND)
        self.image = pygame.Surface(SIZE, SRCALPHA)
        self.trans_surf = pygame.Surface(SIZE, SRCALPHA)
        self.trans_surf.fill((0, 0, 0, 12))
        self.fill_timer = LoopTimer(lambda: 0.2)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        if self.fill_timer.ended:
            self.image.blit(self.trans_surf, (0, 0), special_flags=BLEND_RGBA_SUB)
        self.manager.screen.blit(self.image, (0, 0))