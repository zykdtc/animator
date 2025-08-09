from __future__ import annotations
import os
import pygame
from typing import Dict, Optional, Tuple

from animator.parser import load_scene
from animator.exporter import export_animation

class Animation:
    """
    Public interface:

        import animator.animation
        sample_assets = "examples/sample/assets"
        sample_instructions = "examples/sample/animation.json"
        anim = animator.animation.Animation(sample_assets, sample_instructions,
                                            canvas_size=(640, 480), fps=30)
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

        # Initialize pygame in hidden mode so we can convert images w/ alpha.
        pygame.init()
        pygame.display.set_mode((1, 1), flags=pygame.HIDDEN)

        # Build sprites + animations from instructions (images deduped internally)
        self.sprites, self.scene_duration = load_scene(
            self.instructions_path, self.assets_dir
        )

    def _draw_frame(self, surface: pygame.Surface, t: float) -> None:
        surface.fill(self.bg_color)
        # Update then draw (deterministic order by name)
        for name in sorted(self.sprites.keys()):
            sp = self.sprites[name]
            sp.update(t)
            sp.draw(surface)

    def export(self, output_path: str, duration: Optional[float] = None) -> None:
        """Render frames headlessly and write to GIF/MP4 based on extension."""
        try:
            # If MP4, ensure ffmpeg plugin is importable (zsh users: quote extras).
            import imageio_ffmpeg  # noqa: F401
        except Exception:
            # Not fatal for GIF/PNG sequences; MP4 writer will fail without it.
            pass

        final_duration = (
            float(duration) if duration is not None else float(self.scene_duration)
        )

        export_animation(
            width=self.width,
            height=self.height,
            duration=final_duration,
            fps=self.fps,
            draw_frame_fn=self._draw_frame,
            output_path=output_path,
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