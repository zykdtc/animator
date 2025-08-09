from __future__ import annotations
import pygame
from typing import Callable, List, Tuple

class AnimationInstruction:
    def __init__(self, start: float, duration: float, update_fn: Callable[[float], None]):
        self.start = float(start)
        self.duration = float(duration)
        self.update_fn = update_fn

    def applies(self, t: float) -> bool:
        return self.start <= t <= (self.start + self.duration)

    def apply(self, t: float) -> None:
        if not self.applies(t):
            return
        # Normalize to [0,1]
        u = (t - self.start) / self.duration if self.duration > 0 else 1.0
        u = max(0.0, min(1.0, u))
        self.update_fn(u)

class Sprite:
    def __init__(self, name: str, image: pygame.Surface, position=(0, 0), visible=False):
        self.name = name
        self.image = image
        self.position = list(position)
        self.opacity = 255
        self.visible = visible  # default hidden until first instruction starts
        self.animations: List[AnimationInstruction] = []
        self.natural_size: Tuple[int, int] = image.get_size()  # 👈 asset size info

    def update(self, t: float) -> None:
        # Be invisible unless at least one animation has started
        any_active = False
        for anim in self.animations:
            if t >= anim.start:
                any_active = True
            anim.apply(t)
        self.visible = self.visible or any_active

    def draw(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        temp = self.image.copy()
        temp.set_alpha(self.opacity)
        surface.blit(temp, self.position)