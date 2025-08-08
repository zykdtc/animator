from animator.exporter import export_animation
import pygame

def draw_circle(screen: pygame.Surface, t: float):
    x = int(100 + 200 * t)  # move right over time
    y = 240
    pygame.draw.circle(screen, (0, 128, 255), (x, y), 30)

if __name__ == "__main__":
    export_animation(
        width=640,
        height=480,
        duration=2.0,
        fps=30,
        draw_frame_fn=draw_circle,
        output_path="output.gif"  # or "output.mp4"
    )
