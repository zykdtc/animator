from __future__ import annotations
import pygame
import imageio.v3 as iio
import numpy as np
from typing import Callable, List


def _init_headless(width: int, height: int) -> pygame.Surface:
    pygame.display.init()
    pygame.display.set_mode((1, 1), flags=pygame.HIDDEN)
    screen = pygame.Surface((width, height))
    return screen


def render_frames(
    width: int,
    height: int,
    duration: float,
    fps: int,
    draw_frame_fn: Callable[[pygame.Surface, float], None],
) -> List[np.ndarray]:
    pygame.init()
    screen = _init_headless(width, height)

    frames: List[np.ndarray] = []
    t = 0.0
    dt = 1.0 / float(fps)

    # Use <= so last frame at exactly duration is captured
    while t <= duration + 1e-9:
        screen.fill((255, 255, 255))
        draw_frame_fn(screen, t)
        frame = pygame.surfarray.array3d(screen).swapaxes(0, 1)
        frames.append(frame)
        t += dt

    pygame.quit()
    return frames


def export_animation(
    width: int,
    height: int,
    duration: float,
    fps: int,
    draw_frame_fn: Callable[[pygame.Surface, float], None],
    output_path: str,
) -> None:
    frames = render_frames(width, height, duration, fps, draw_frame_fn)
    iio.imwrite(output_path, frames, fps=fps)