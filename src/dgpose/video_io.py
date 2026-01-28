from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import cv2


@dataclass(frozen=True)
class VideoInfo:
    path: Path
    fps: float
    width: int
    height: int
    frame_count: int


class VideoOpenError(RuntimeError):
    pass


class VideoWriterOpenError(RuntimeError):
    pass


def open_video(path: str | path) -> tuple[cv2.VideoCapture, VideoInfo]:
    p = Path(path)
    cap = cv2.VideoCapture(str(p))
    if not cap.isOpened():
        raise VideoOpenError("Failed to open video: {p}")

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    if fps <= 0:
        fps = 30.0

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)

    info = VideoInfo(
        path=p, fps=fps, width=width, height=height, frame_count=frame_count
    )
    return cap, info


def iter_frames(cap: cv2.VideoCapture) -> Iterator[tuple[int, "cv2.Mat"]]:
    i = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        yield i, frame
        i += 1


def open_writer(
    out_path: str | Path,
    *,
    fps: float,
    width: int,
    height: int,
    codec: str = "mp4v",
) -> cv2.VideoWriter:
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*codec)
    writer = cv2.VideoWriter(str(p), fourcc, fps, (width, height))
    if not writer.isOpened():
        raise VideoWriterOpenError(
            f"Failed to open VideoWriter: {p} (codec={codec}). "
            "Try codec='XVID' and an .avi output."
        )
    return writer
