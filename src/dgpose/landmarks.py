from __future__ import annotations

from enum import Enum


class LM(Enum):
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16


LM_NAME_MAP: dict[str, LM] = {
    "le": LM.LEFT_ELBOW,
    "re": LM.RIGHT_ELBOW,
    "lw": LM.LEFT_WRIST,
    "rw": LM.RIGHT_WRIST,
}
