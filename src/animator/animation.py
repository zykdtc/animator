from __future__ import annotations
from typing import Dict, Optional, Tuple

from animator.parser import load_scene
from animator.exporter import export_animation

class Animation:
    """
    Public interface:

        import animator.animation
        assets = "examples/sample/assets"
        inst = "examples/sample/animation.json"
        anim = animator.animation.Animation(assets, inst, canvas_size=(640, 480), fps=30)
        anim.export("examples/sample/output.mp4")
    """

    def __init__(
        self,
        assets_dir: str,
        instructions_path: str,
        canvas_size: Tuple[int, int] = (640, 480),
        fps: int = 30,
        bg_color: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        self.assets_dir = assets_dir
        self.instructions_path = instructions_path
        self.width, self.height = canvas_size
        self.fps = fps
        self.bg_color = bg_color

        # Build sprites + animations from instructions
        self.sprites, self.scene_duration = load_scene(
            self.instructions_path, self.assets_dir
        )

    def _draw_frame(self, image, t: float) -> None:
        # image is a PIL.Image in RGBA mode; clear to bg
        r, g, b = self.bg_color
        image.paste((r, g, b, 255), (0, 0, self.width, self.height))
        # Update then draw (deterministic order by name)
        for name in sorted(self.sprites.keys()):
            sp = self.sprites[name]
            sp.update(t)
            sp.draw(image)

    def export(self, output_path: str, duration: Optional[float] = None) -> None:
        try:
            import imageio_ffmpeg  # noqa: F401 (optional, for MP4)
        except Exception:
            pass
        final_duration = float(duration) if duration is not None else float(self.scene_duration)
        export_animation(
            width=self.width,
            height=self.height,
            duration=final_duration,
            fps=self.fps,
            draw_frame_fn=self._draw_frame,
            output_path=output_path,
            bg_color=self.bg_color,
        )

    def summary(self) -> str:
        lines = [
            f"Canvas: {self.width}x{self.height} @ {self.fps} FPS",
            f"Sprites: {len(self.sprites)}",
            f"Duration: {self.scene_duration:.3f}s",
        ]
        for name, sp in sorted(self.sprites.items()):
            w, h = sp.natural_size
            lines.append(f" - {name}: size={w}x{h}, pos={tuple(sp.position)}")
        return "\n".join(lines)