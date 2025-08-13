from __future__ import annotations
from typing import Callable, List, Tuple
from PIL import Image

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
        u = (t - self.start) / self.duration if self.duration > 0 else 1.0
        u = 0.0 if u < 0 else (1.0 if u > 1.0 else u)
        self.update_fn(u)

class Sprite:
    def __init__(self, name: str, image: Image.Image, position=(0, 0), visible=False):
        self.name = name
        self.base_image = image.convert("RGBA")
        self.position = list(position)
        self.opacity = 255
        self.visible = visible  # hidden until first instruction starts
        self.animations: List[AnimationInstruction] = []
        self.natural_size: Tuple[int, int] = self.base_image.size

    def update(self, t: float) -> None:
        any_active = False
        for anim in self.animations:
            if t >= anim.start:
                any_active = True
            anim.apply(t)
        self.visible = self.visible or any_active

    def draw(self, canvas: Image.Image) -> None:
        if not self.visible:
            return
        # Apply opacity on a copy to avoid mutating base
        if self.opacity >= 255:
            img = self.base_image
        else:
            img = self.base_image.copy()
            a = img.split()[-1]
            # scale existing alpha by self.opacity
            a = a.point(lambda px: int(px * (self.opacity / 255.0)))
            img.putalpha(a)
        x, y = int(self.position[0]), int(self.position[1])
        canvas.alpha_composite(img, dest=(x, y))