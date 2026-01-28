from __future__ import annotations

from pathlib import Path

import cv2

from .video_io import iter_frames, open_video, open_writer


def process_video(
    input_path: str | Path,
    output_path: str | Path,
    frame_fn,
) -> None:
    cap, info = open_video(input_path)
    writer = open_writer(
        output_path, fps=info.fps, width=info.width, height=info.height
    )

    try:
        for _i, frame in iter_frames(cap):
            frame_fn(frame, info)
            writer.write(frame)
    finally:
        cap.release()
        writer.release()
