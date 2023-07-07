from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.management.scene import Scene

from abc import ABC as AbstractClass
from enum import Enum, auto

class Layers(Enum):
    DEFAULT = auto()

class Sprite(AbstractClass):
    def __init__(self, scene: Scene, layer: int | Layers) -> None:
        self._layer = Layers(layer)
        self.scene = scene
        self.manager = scene.manager
        self.scene.sprite_manager.add(self)

    def update(self) -> None:
        # Mandatory method
        pass

    def draw(self) -> None:
        # Mandatory method
        pass

    def kill(self) -> None:
        self.scene.sprite_manager.remove(self)

class SpriteManager:
    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        self.manager = scene.manager
        self.layers: dict[Layers, list[Sprite]] = {layer: [] for layer in Layers}

    def update(self) -> None:
        for layer in self.layers:
            for sprite in self.layers[layer]:
                sprite.update()

    def draw(self) -> None:
        for layer in self.layers:
            for sprite in self.layers[layer]:
                sprite.draw()

    def add(self, sprite: Sprite) -> None:
        self.layers[sprite._layer].append(sprite)

    def remove(self, sprite: Sprite) -> None:
        self.layers[sprite._layer].remove(sprite)