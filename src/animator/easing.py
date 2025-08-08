from typing import Callable


def linear(t):
    return t

class AnimationInstruction:
    def __init__(
        self,
        start: float,
        duration: float,
        update_fn: Callable[[float], None]
    ):
        self.start = start
        self.duration = duration
        self.update_fn = update_fn

    def apply(self, current_time: float):
        t = (current_time - self.start) / self.duration
        if 0.0 <= t <= 1.0:
            self.update_fn(t)


def make_move_fn(sprite, start_pos, end_pos):
    def fn(t: float):
        sprite.position[0] = start_pos[0] + (end_pos[0] - start_pos[0]) * t
        sprite.position[1] = start_pos[1] + (end_pos[1] - start_pos[1]) * t
    return fn

def make_fade_fn(sprite, start_opacity, end_opacity):
    def fn(t: float):
        sprite.opacity = int(start_opacity + (end_opacity - start_opacity) * t)
    return fn