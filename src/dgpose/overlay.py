from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import cv2

from .colors import ColorScheme, DEFAULT_COLORS
from .landmarks import LM
from .pose_estimator import PoseEstimator
from .trails import Trail


@dataclass(frozen=True)
class OverlayConfig:
    show_points: set[LM] = field(default_factory=set)
    trail_points: set[LM] = field(default_factory=set)
    lines: set[tuple[LM, LM]] = field(default_factory=set)
    max_trail: Optional[int] = None

    point_radius: int = 6
    line_thickness: int = 3
    trail_thickness: int = 2

    colors: dict[LM, ColorScheme] = field(default_factory=dict)


class OverlayProcessor:
    def __init__(self, cfg: OverlayConfig) -> None:
        self._cfg = cfg
        self._pose = PoseEstimator()
        self._trails: dict[LM, Trail] = {
            lm: Trail(maxlen=cfg.max_trail) for lm in cfg.trail_points
        }

        self._needed: set[LM] = set()
        self._needed |= cfg.show_points
        self._needed |= cfg.trail_points
        for a, b in cfg.lines:
            self._needed.add(a)
            self._needed.add(b)

        self._colors: dict[LM, ColorScheme] = {}

        for lm in self._needed:
            key = lm.name.lower()
            self._colors[lm] = cfg.colors.get(
                lm,
                DEFAULT_COLORS.get(key, ColorScheme((0,255,0),(0,255,0)))
            )

    def close(self) -> None:
        self._pose.close()

    def on_frame(self, frame_bgr, info) -> None:
        # Always draw existing trails
        for lm, t in self._trails.items():
            t.draw(frame_bgr, thickness=self._cfg.trail_thickness, color=self._colors[lm].trail)

        if not self._needed:
            return

        # Detect only the points we need this frame
        pts = self._pose.detect_points(
            frame_bgr, width=info.width, height=info.height, lms=self._needed
        )
        if pts is None:
            return

        # Update trails with the current frame's lm positions
        for lm, trail in self._trails.items():
            p = pts.get(lm)
            if p:
                trail.add(p)
        
        # Redraw trails so the newest segment appears immediately
        for lm, t in self._trails.items():
            t.draw(
                frame_bgr,
                thickness=self._cfg.trail_thickness,
                color=self._colors[lm].trail,
            )

        # Draw current-frame lines
        for a, b in self._cfg.lines:
            pa = pts.get(a)
            pb = pts.get(b)
            if pa and pb:
                color = self._colors[a].line or (255, 255, 255)
                cv2.line(frame_bgr, pa, pb, color, self._cfg.line_thickness)
        
        # Draw current-frame points
        for lm in self._cfg.show_points:
            p = pts.get(lm)
            if p:
                cv2.circle(
                    frame_bgr,
                    p,
                    self._cfg.point_radius,
                    self._colors[lm].point,
                    -1
                )
