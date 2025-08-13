from __future__ import annotations
from typing import List, Tuple
from PIL import Image

from animator.instruction import Instruction

class Sprite:
    def __init__(self, name: str, image: Image.Image, position=(0, 0), visible=False):
        self.name = name
        self.base_image = image.convert("RGBA")
        self.position = list(position)
        self.opacity = 255
        self.visible = visible  # hidden until first instruction starts
        self.instructions: List[Instruction] = []
        self.natural_size: Tuple[int, int] = self.base_image.size

    def update(self, t: float) -> None:
        any_active = False
        for anim in self.instructions:
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