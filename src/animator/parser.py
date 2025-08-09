from __future__ import annotations
import json
import os
from typing import Dict, Tuple, Any
import pygame

from animator.sprite import Sprite, AnimationInstruction

# Optional: simple linear easing; can be extended via animator.easing
_def_ease = lambda x: x


def _compute_duration(animations: list[dict]) -> float:
    end = 0.0
    for a in animations:
        end = max(end, float(a["start"]) + float(a["duration"]))
    return end


def load_scene(instructions_path: str, assets_dir: str) -> Tuple[Dict[str, Sprite], float]:
    """
    Build sprites (with images) and attach animations from a JSON scene file.

    JSON schema (example):
    {
      "sprites": [
        {"name": "hero1", "image": "hero.png", "initial_position": [0,100]},
        {"name": "hero2", "image": "hero.png", "initial_position": [0,200]}
      ],
      "animations": [
        {"type":"move","target":"hero1","from":[0,100],"to":[300,100],"start":0.0,"duration":2.0},
        {"type":"fade","target":"hero2","from":0,"to":255,"start":1.0,"duration":1.0}
      ]
    }
    """
    with open(instructions_path, "r") as f:
        data: Dict[str, Any] = json.load(f)

    sprites: Dict[str, Sprite] = {}
    image_cache: Dict[str, pygame.Surface] = {}

    # Create Sprite instances (dedupe images by filename)
    for spec in data.get("sprites", []):
        name = spec["name"]
        img_name = spec["image"]
        pos = tuple(spec.get("initial_position", (0, 0)))

        if img_name not in image_cache:
            img_path = os.path.join(assets_dir, img_name)
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"Asset not found: {img_path}")
            image_cache[img_name] = pygame.image.load(img_path).convert_alpha()

        sprites[name] = Sprite(name, image_cache[img_name], pos, visible=False)

    # Attach animations to their targets
    for a in data.get("animations", []):
        tname = a["target"]
        if tname not in sprites:
            raise KeyError(f"Target sprite '{tname}' not declared in 'sprites'.")
        sp = sprites[tname]
        start = float(a["start"])
        dur = float(a["duration"])
        atype = a["type"]

        if atype == "move":
            p0 = tuple(a["from"]) ; p1 = tuple(a["to"])
            def move_fn(u: float, sp=sp, p0=p0, p1=p1):
                sp.position[0] = p0[0] + (p1[0] - p0[0]) * u
                sp.position[1] = p0[1] + (p1[1] - p0[1]) * u
            sp.animations.append(AnimationInstruction(start, dur, move_fn))

        elif atype == "fade":
            a0 = int(a["from"]) ; a1 = int(a["to"])
            def fade_fn(u: float, sp=sp, a0=a0, a1=a1):
                sp.opacity = int(round(a0 + (a1 - a0) * u))
            sp.animations.append(AnimationInstruction(start, dur, fade_fn))

        else:
            raise ValueError(f"Unknown animation type: {atype}")

    total_duration = _compute_duration(data.get("animations", []))
    return sprites, total_duration