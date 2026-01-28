from __future__ import annotations

from typing import Tuple
from dataclasses import dataclass

Color = Tuple[int, int, int]

@dataclass(frozen=True)
class ColorScheme:
    point: Color
    trail: Color
    line: Color | None = None

DEFAULT_COLORS: dict[str, ColorScheme] = {
    "left_wrist": ColorScheme(point=(0, 255, 0), trail=(0, 200, 0)),
    "right_wrist": ColorScheme(point=(255, 0, 0), trail=(200, 0, 0)),
    "left_elbow": ColorScheme(point=(0, 255, 255), trail=(0, 200, 200)),
    "right_elbow": ColorScheme(point=(255, 255, 0), trail=(200, 200, 0)),
}
