from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import cv2

from .process_video import process_video
from .trails import Trail
from .video_overlay import PoseEstimator


@dataclass(frozen=True)
class TraceConfig:
    max_trail: Optional[int] = None
    draw_current_points: bool = True


class WristTraceProcessor:
    def __init__(self, cfg: TraceConfig) -> None:
        self._cfg = cfg
        self._pose = PoseEstimator()
        # self._left = Trail(maxlen=cfg.max_trail)
        self._right = Trail(maxlen=cfg.max_trail)

    def close(self) -> None:
        self._pose.close()

    def on_frame(self, frame_bgr, info) -> None:
        pose = self._pose.detect(frame_bgr, width=info.width, height=info.height)

        # self._left.draw(frame_bgr)
        self._right.draw(frame_bgr)

        if pose is None:
            return

        # self._left.add(pose.left_wrist)
        self._right.add(pose.right_wrist)

        # self._left.draw(frame_bgr)
        self._right.draw(frame_bgr)

        if self._cfg.draw_current_points:
            # cv2.circle(frame_bgr, pose.left_wrist, 6, (0, 255, 0), -1)
            cv2.circle(frame_bgr, pose.right_wrist, 12, (0, 255, 0), -1)


def trace_wrists(
    input_path: str | Path,
    output_path: str | Path,
    *,
    max_trail: int = 0,
    draw_current_points: bool = True,
) -> None:
    cfg = TraceConfig(
        max_trail=None if max_trail == 0 else max_trail,
        draw_current_points=draw_current_points,
    )
    proc = WristTraceProcessor(cfg)
    try:
        process_video(input_path, output_path, proc.on_frame)
    finally:
        proc.close()
