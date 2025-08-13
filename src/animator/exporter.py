from __future__ import annotations
from typing import Dict, List, Tuple
import numpy as np
from PIL import Image
import imageio.v3 as iio
from animator.sprite import Sprite

def render_frames(
    width: int,
    height: int,
    duration: float,
    fps: int,
    sprites: Dict[str, Sprite],
    bg_color: Tuple[int, int, int],
) -> List[np.ndarray]:
    frames: List[np.ndarray] = []
    t = 0.0
    dt = 1.0 / float(fps)

    while t <= duration + 1e-9:
        canvas = Image.new("RGBA", (width, height), (*bg_color, 255))
        for name in sorted(sprites.keys()):
            sp = sprites[name]
            sp.update(t)
            sp.draw(canvas)
        rgb = canvas.convert("RGB")
        frames.append(np.asarray(rgb))
        t += dt

    return frames

def export_animation(
    width: int,
    height: int,
    duration: float,
    fps: int,
    sprites: Dict[str, Sprite],
    output_path: str,
    bg_color: Tuple[int, int, int] = (255, 255, 255),
) -> None:
    frames = render_frames(width, height, duration, fps, sprites, bg_color)
    iio.imwrite(output_path, frames, fps=fps)