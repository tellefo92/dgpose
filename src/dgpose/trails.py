from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Iterable, Optional

import cv2
import numpy as np

Point = tuple[int, int]


@dataclass
class Trail:
    maxlen: Optional[int] = None
    _pts: Deque[Point] = field(default_factory=deque)

    def add(self, p: Point) -> None:
        if self.maxlen is None:
            self._pts.append(p)
        else:
            if self._pts.maxlen != self.maxlen:
                self._pts = deque(self._pts, maxlen=self.maxlen)
            self._pts.append(p)

    def draw(self, frame_bgr, *, thickness: int = 2, color=(0,255,255)) -> None:
        if len(self._pts) < 2:
            return
        arr = np.array(self._pts, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(frame_bgr, [arr], False, color, thickness)
