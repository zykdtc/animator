import pygame
import os
from animator.animation import Animation
from animator.sprite import Sprite
from animator.parser import load_instructions
from animator.easing import linear

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    image_path = os.path.join(os.path.dirname(__file__), "../assets/sprite.png")
    sprite_img = pygame.image.load(image_path).convert_alpha()

    sprite = Sprite("hero", sprite_img, (50, 50))
    sprite.move_to((300, 200), start_time=0, duration=2.0, easing_func=linear)

    sprites = {"hero": sprite}
    instructions = []  # For now, just use hardcoded move above

    animation = Animation(screen, instructions, sprites, export_path="output.mp4")
    animation.run()


if __name__ == "__main__":
    main()
