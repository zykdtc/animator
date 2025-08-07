import numpy
import pygame
from animator.sprite import Sprite
from animator.easing import linear
import imageio.v3 as iio

class Animation:
    def __init__(self, screen: pygame.Surface, instructions, sprites: dict[str, Sprite], export_path: str | None = None):
        self.screen = screen
        self.instructions = instructions
        self.sprites = sprites
        self.clock = pygame.time.Clock()
        self.time = 0.0
        self.frames: list[numpy.ndarray] = []
        self.export_path = export_path

    def run(self):
        running = True
        frame_count = 0

        while running:
            dt = self.clock.tick(60) / 1000.0  # 60 FPS
            self.time += dt
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for sprite in self.sprites.values():
                sprite.update(self.time)
                sprite.draw(self.screen)

            # Capture frame
            if self.export_path:
                frame = pygame.surfarray.array3d(self.screen).swapaxes(0, 1)
                self.frames.append(frame)

            pygame.display.flip()
            frame_count += 1

            if self.time > 3.0:  # Stop after 3 seconds (or use instruction-driven duration)
                running = False

        if self.export_path:
            if self.export_path.endswith('.mp4'):
                iio.imwrite(
                    "output.mp4",
                    self.frames,
                    codec="libx264",  # common H.264 codec
                    fps=60
                )
            elif self.export_path.endswith('.gif'):
                iio.imwrite(
                    "output.gif",
                    self.frames,
                    fps=60
                )