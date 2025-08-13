from __future__ import annotations
from typing import Callable, List, Tuple
import numpy as np
from PIL import Image
import imageio.v3 as iio


def render_frames(
    width: int,
    height: int,
    duration: float,
    fps: int,
    draw_frame_fn: Callable[[Image.Image, float], None],
    bg_color: Tuple[int, int, int],
) -> List[np.ndarray]:
    frames: List[np.ndarray] = []
    t = 0.0
    dt = 1.0 / float(fps)

    while t <= duration + 1e-9:
        # RGBA canvas for compositing
        canvas = Image.new("RGBA", (width, height), (*bg_color, 255))
        draw_frame_fn(canvas, t)
        # Convert to RGB ndarray for imageio
        rgb = canvas.convert("RGB")
        frames.append(np.asarray(rgb))
        t += dt

    return frames


def export_animation(
    width: int,
    height: int,
    duration: float,
    fps: int,
    draw_frame_fn: Callable[[Image.Image, float], None],
    output_path: str,
    bg_color: Tuple[int, int, int] = (255, 255, 255),
) -> None:
    frames = render_frames(width, height, duration, fps, draw_frame_fn, bg_color)
    iio.imwrite(output_path, frames, fps=fps)