from __future__ import annotations
import json, os
from typing import Dict, Tuple, Any
from PIL import Image

from animator.sprite import Sprite
from animator.instruction import MoveInst, FadeInst, Instruction


def _compute_duration(instructions: list[dict]) -> float:
    end = 0.0
    for a in instructions:
        end = max(end, float(a["start"]) + float(a["duration"]))
    return end


def load_scene(instructions_path: str, assets_dir: str) -> Tuple[Dict[str, Sprite], float]:
    """
    Build sprites (with PIL images) and attach instructions from a JSON scene file.

    JSON schema (example):
    {
      "sprites": [
        {"name": "hero1", "image": "hero.png", "initial_position": [0,100]},
        {"name": "hero2", "image": "hero.png", "initial_position": [0,200]}
      ],
      "instructions": [
        {"type":"move","target":"hero1","from":[0,100],"to":[300,100],"start":0.0,"duration":2.0},
        {"type":"fade","target":"hero2","from":0,"to":255,"start":1.0,"duration":1.0}
      ]
    }
    """
    with open(instructions_path, "r") as f:
        data: Dict[str, Any] = json.load(f)

    sprites: Dict[str, Sprite] = {}
    image_cache: Dict[str, Image.Image] = {}

    for spec in data.get("sprites", []):
        name = spec["name"]
        img_name = spec["image"]
        pos = tuple(spec.get("initial_position", (0, 0)))

        if img_name not in image_cache:
            img_path = os.path.join(assets_dir, img_name)
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"Asset not found: {img_path}")
            image_cache[img_name] = Image.open(img_path).convert("RGBA")

        sprites[name] = Sprite(name, image_cache[img_name], pos, visible=False)

    for a in data.get("instructions", []):
        tname = a["target"]
        if tname not in sprites:
            raise KeyError(f"Target sprite '{tname}' not declared in 'sprites'.")
        sp = sprites[tname]
        start = float(a["start"]) ; dur = float(a["duration"]) ; atype = a["type"]

        if atype == "move":
            p0 = tuple(a["from"]) ; p1 = tuple(a["to"])
            sp.instructions.append(MoveInst(sp, start, dur, p0, p1))

        elif atype == "fade":
            a0 = int(a["from"]) ; a1 = int(a["to"])
            sp.instructions.append(FadeInst(sp, start, dur, a0, a1))

        else:
            raise ValueError(f"Unknown animation type: {atype}")

    total_duration = _compute_duration(data.get("instructions", []))
    return sprites, total_duration