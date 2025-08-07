import pygame


class Sprite:
    def __init__(self, name, image, position=(0, 0)):
        self.name = name
        self.image = image
        self.position = list(position)
        self.animations = []

    def move_to(self, target_pos, start_time, duration, easing_func):
        self.animations.append((start_time, duration, self.position.copy(), target_pos, easing_func))

    def update(self, current_time):
        for (start, duration, from_pos, to_pos, easing) in self.animations:
            t = (current_time - start) / duration
            if 0 <= t <= 1:
                self.position[0] = from_pos[0] + (to_pos[0] - from_pos[0]) * easing(t)
                self.position[1] = from_pos[1] + (to_pos[1] - from_pos[1]) * easing(t)

    def draw(self, surface):
        surface.blit(self.image, self.position)
