from __future__ import annotations

from pathlib import Path

from .overlay import OverlayConfig, OverlayProcessor
from .process_video import process_video


def run_overlay(
    input_path: str | Path, output_path: str | Path, cfg: OverlayConfig
) -> None:
    proc = OverlayProcessor(cfg)
    try:
        process_video(input_path, output_path, proc.on_frame)
    finally:
        proc.close()
