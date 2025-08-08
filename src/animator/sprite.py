import pygame
from animator.easing import AnimationInstruction


class Sprite:
    def __init__(self, name: str, image: pygame.Surface, position=(0, 0)):
        self.name = name
        self.image = image
        self.position = list(position)
        self.opacity = 255
        self.animations: list[AnimationInstruction] = []

    def update(self, time: float):
        for anim in self.animations:
            anim.apply(time)

    def draw(self, surface: pygame.Surface):
        temp = self.image.copy()
        temp.set_alpha(self.opacity)
        surface.blit(temp, self.position)
