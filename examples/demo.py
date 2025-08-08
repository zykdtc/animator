import pygame
import os
from animator.sprite import Sprite
from animator.parser import load_instructions
from animator.exporter import export_animation

def main():
    # Load assets
    pygame.init()
    pygame.display.set_mode((1, 1), flags=pygame.HIDDEN)  # or headless

    hero_img = pygame.image.load("examples/assets/hero.png").convert_alpha()
    sprites = {
        "hero": Sprite("hero", hero_img)
    }

    # Load and assign animations
    load_instructions("examples/animation.json", sprites)

    # Draw function per frame
    def draw_frame(surface: pygame.Surface, time: float):
        for sprite in sprites.values():
            sprite.update(time)
            sprite.draw(surface)

    export_animation(
        width=640,
        height=480,
        duration=5.0,
        fps=30,
        draw_frame_fn=draw_frame,
        output_path="output.mp4"
    )

if __name__ == "__main__":
    main()
