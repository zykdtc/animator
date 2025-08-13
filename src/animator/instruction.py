from __future__ import annotations
from collections.abc import Callable
from typing import Tuple

class Instruction:
    """Base time-bounded instruction.
    Subclasses may override apply(t) for event-like behavior (Entry/Exit).
    """
    def __init__(self, start: float, duration: float, update_fn: Callable[[float], None] | None = None):
        self.start = float(start)
        self.duration = float(duration)
        self.update_fn = update_fn

    def is_applying(self, t: float) -> bool:
        return self.start <= t <= (self.start + self.duration)

    def apply(self, t: float) -> None:
        if self.update_fn is None:
            return
        if not self.is_applying(t):
            return
        u = (t - self.start) / self.duration if self.duration > 0 else 1.0
        u = 0.0 if u < 0 else (1.0 if u > 1.0 else u)
        self.update_fn(u)

# ── Concrete instructions ────────────────────────────────────────────────────

class EntryInst(Instruction):
    """Make the sprite appear on canvas at a given time and position.
    Stays on canvas until an ExitInst hides it.
    """
    def __init__(self, sprite, time: float, position: Tuple[float, float]):
        super().__init__(start=time, duration=0.0, update_fn=None)
        self.sprite = sprite
        self.position = (float(position[0]), float(position[1]))

    def apply(self, t: float) -> None:  # event-style: trigger at time
        if t >= self.start:
            sp = self.sprite
            sp.on_canvas = True
            sp.visible = True
            sp.position[0], sp.position[1] = self.position

class ExitInst(Instruction):
    """Remove the sprite from the canvas at a given time."""
    def __init__(self, sprite, time: float):
        super().__init__(start=time, duration=0.0, update_fn=None)
        self.sprite = sprite

    def apply(self, t: float) -> None:  # event-style
        if t >= self.start:
            sp = self.sprite
            sp.on_canvas = False
            sp.visible = False

class MoveInst(Instruction):
    def __init__(self, sprite, start: float, duration: float, p0: Tuple[float, float], p1: Tuple[float, float]):
        def update(u: float, sp=sprite, a=p0, b=p1):
            if not getattr(sp, "on_canvas", True):
                return
            sp.position[0] = a[0] + (b[0] - a[0]) * u
            sp.position[1] = a[1] + (b[1] - a[1]) * u
        super().__init__(start, duration, update)

class FadeInst(Instruction):
    def __init__(self, sprite, start: float, duration: float, a0: int, a1: int):
        a0 = int(a0); a1 = int(a1)
        def update(u: float, sp=sprite, _a0=a0, _a1=a1):
            if not getattr(sp, "on_canvas", True):
                return
            sp.opacity = int(round(_a0 + (_a1 - _a0) * u))
        super().__init__(start, duration, update)