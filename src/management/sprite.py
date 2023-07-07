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
        self._visible = True
        self.scene = scene
        self.manager = scene.manager
        self.sprite_manager = scene.sprite_manager
        self.scene.sprite_manager.add(self)

    def update(self) -> None:
        # Mandatory method
        pass

    def draw(self) -> None:
        # Mandatory method
        pass

    def kill(self) -> None:
        self.scene.sprite_manager.remove(self)

    @property
    def visible(self) -> None:
        return self._visible

    @visible.setter
    def visible(self, val: bool) -> None:
        self._visible = val
        (self.sprite_manager.reveal if val else self.sprite_manager.hide)(self)

class SpriteManager:
    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        self.manager = scene.manager
        self.updates: dict[Layers, list[Sprite]] = {layer: [] for layer in Layers}
        self.layers: dict[Layers, list[Sprite]] = {layer: [] for layer in Layers}

    def update(self) -> None:
        for layer in self.updates:
            for sprite in self.updates[layer]:
                sprite.update()

    def draw(self) -> None:
        for layer in self.layers:
            for sprite in self.layers[layer]:
                sprite.draw()

    def add(self, sprite: Sprite) -> None:
        self.updates[sprite._layer].append(sprite)
        if sprite.visible:
            self.reveal(sprite)

    def remove(self, sprite: Sprite) -> None:
        self.updates[sprite._layer].remove(sprite)
        if sprite.visible:
            self.hide(sprite)

    def reveal(self, sprite: Sprite) -> None:
        try:
            self.layers[sprite._layer].append(sprite)
        except ValueError:
            pass

    def hide(self, sprite: Sprite) -> None:
        try:
            self.layers[sprite._layer].remove(sprite)
        except ValueError:
            pass