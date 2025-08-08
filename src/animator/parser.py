import json
from typing import Any, Callable
from animator.sprite import Sprite
from animator.easing import AnimationInstruction, make_move_fn, make_fade_fn

def load_instructions(path: str, sprites: dict[str, Sprite]):
    with open(path, "r") as f:
        instructions: list[dict[str, Any]] = json.load(f)

    for instr in instructions:
        target = instr["target"]
        sprite = sprites[target]

        if instr["type"] == "move":
            start_pos = instr["from"]
            end_pos = instr["to"]
            start = instr["start"]
            duration = instr["duration"]

            sprite.animations.append(
                AnimationInstruction(start, duration, make_move_fn(sprite, start_pos, end_pos))
            )

        elif instr["type"] == "fade":
            start_opacity = instr["from"]
            end_opacity = instr["to"]
            start = instr["start"]
            duration = instr["duration"]

            sprite.animations.append(
                AnimationInstruction(start, duration, make_fade_fn(sprite, start_opacity, end_opacity))
            )
