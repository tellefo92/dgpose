import argparse

from dgpose.landmarks import LM_NAME_MAP, LM
from dgpose.overlay import OverlayConfig
from dgpose.run import run_overlay

def _parse_lm_list(s: str) -> set(LM):
    if not s:
        return set()
    out: set[LM] = set()
    for part in s.split(","):
        key = part.strip().lower()
        if not key:
            continue
        out.add(LM_NAME_MAP[key])
    return out

def _parse_lines(s: str) -> set[tuple[LM, LM]]:
    if not s:
        return set()
    out: set[tuple[LM, LM]] = set()
    for part in s.split(","):
        part = part.strip().lower()
        if not part:
            continue
        a, b = part.split("-", 1)
        out.add((LM_NAME_MAP[a.strip()], LM_NAME_MAP[b.strip()]))
    return out

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("output")
    
    p.add_argument("--points", default="lw", help="Comma list: lw,rw,le,re")
    p.add_argument("--trails", default="lw", help="Comma list: which landmarks should leave a trail")
    p.add_argument("--lines", default="", help="Comma list of pairs: le-lw,re-rw")

    p.add_argument("--max-trail", type=int, default=0, help="0 = unlimited, else last N points per trail")
    
    args = p.parse_args()

    cfg = OverlayConfig(
        show_points=_parse_lm_list(args.points),
        trail_points=_parse_lm_list(args.trails),
        lines=_parse_lines(args.lines),
        max_trail=None if args.max_trail == 0 else args.max_trail,
    )

    run_overlay(args.input, args.output, cfg)

if __name__ == "__main__":
    main()
