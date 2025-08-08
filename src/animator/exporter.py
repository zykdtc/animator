import pygame
import imageio.v3 as iio
import numpy as np
from typing import Callable

def init_headless(width: int, height: int) -> pygame.Surface:
    pygame.display.init()
    pygame.display.set_mode((1, 1), flags=pygame.HIDDEN)
    screen = pygame.Surface((width, height))
    return screen

def render_frames(
    width: int,
    height: int,
    duration: float,
    fps: int,
    draw_frame_fn: Callable[[pygame.Surface, float], None]
) -> list[np.ndarray]:
    pygame.init()
    screen = init_headless(width, height)
    frame_time = 1.0 / fps
    time = 0.0
    frames = []

    while time <= duration:
        screen.fill((255, 255, 255))
        draw_frame_fn(screen, time)
        frame = pygame.surfarray.array3d(screen).swapaxes(0, 1)
        frames.append(frame)
        print(f"time: {time}")
        time += frame_time

    pygame.quit()
    return frames

def export_animation(
    width: int,
    height: int,
    duration: float,
    fps: int,
    draw_frame_fn: Callable[[pygame.Surface, float], None],
    output_path: str
):
    frames = render_frames(width, height, duration, fps, draw_frame_fn)
    iio.imwrite(output_path, frames, fps=fps)
