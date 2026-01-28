from __future__ import annotations

from typing import Iterable

import cv2
import mediapipe as mp

from .landmarks import LM


class PoseEstimator:
    def __init__(
        self,
        *,
        model_complexity: int = 1,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        mp_pose = mp.solutions.pose
        self._pose = mp_pose.Pose(
            model_complexity=model_complexity,
            enable_segmentation=False,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def close(self) -> None:
        self._pose.close()

    def detect_points(
        self, frame_bgr, *, width: int, height: int, lms: Iterable[LM]
    ) -> dict[LM, tuple[int, int]] | None:
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        res = self._pose.process(rgb)
        if not res.pose_landmarks:
            return None

        all_lms = res.pose_landmarks.landmark

        out: dict[LM, tuple[int, int]] = {}
        for lm in lms:
            i = lm.value
            p = all_lms[i]
            x = max(0, min(width - 1, int(p.x * width)))
            y = max(0, min(height - 1, int(p.y * height)))
            out[lm] = (x, y)
        return out
