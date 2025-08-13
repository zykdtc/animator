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
        # Presence control: sprites are not on canvas until an EntryInst fires
        self.on_canvas = False
        self.visible = visible  # UI hint; drawing is gated by on_canvas
        self.instructions: List[Instruction] = []
        self.natural_size: Tuple[int, int] = self.base_image.size
    
    def update(self, t: float) -> None:
        for inst in self.instructions:
            inst.apply(t)

    def draw(self, canvas: Image.Image) -> None:
        if not self.on_canvas:
            return
        if self.opacity >= 255:
            img = self.base_image
        else:
            img = self.base_image.copy()
            a = img.split()[-1]
            a = a.point(lambda px: int(px * (self.opacity / 255.0)))
            img.putalpha(a)
        x, y = int(self.position[0]), int(self.position[1])
        canvas.alpha_composite(img, dest=(x, y))
