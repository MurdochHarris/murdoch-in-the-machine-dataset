#!/usr/bin/env python3
"""Export media/ image+.txt pairs into a Stable Diffusion trainer folder.

Examples:
  python3 training/export_sd_dataset.py
  python3 training/export_sd_dataset.py --trigger "ohwx murdoch" --short
  python3 training/export_sd_dataset.py --src media --out ~/datasets/murdoch
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def pairs(src: Path) -> list[tuple[Path, Path | None]]:
    found: list[tuple[Path, Path | None]] = []
    for img in sorted(src.rglob("*")):
        if not img.is_file() or img.suffix.lower() not in IMAGE_EXTS:
            continue
        if any(p.startswith(".") for p in img.parts):
            continue
        txt = img.with_suffix(".txt")
        found.append((img, txt if txt.is_file() else None))
    return found


def format_caption(raw: str, *, trigger: str, short: bool) -> str:
    text = (raw or "").strip()
    if short and text:
        text = text.split("\n", 1)[0].strip()
    text = " ".join(text.split())
    trigger = trigger.strip()
    if not trigger:
        return text
    if not text:
        return trigger
    # avoid double-prefix if re-exported
    low = text.lower()
    if low.startswith(trigger.lower() + ",") or low.startswith(trigger.lower() + " "):
        return text
    return f"{trigger}, {text}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--src",
        type=Path,
        default=ROOT / "media",
        help="folder of image+.txt pairs (default: ./media)",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=ROOT / "training" / "sd-dataset",
        help="output dataset folder (default: ./training/sd-dataset)",
    )
    ap.add_argument(
        "--trigger",
        default="murdoch",
        help='trigger token prefixed to captions (default: "murdoch"; empty to skip)',
    )
    ap.add_argument(
        "--short",
        action="store_true",
        help="use only the first line of each caption (often better for face LoRAs)",
    )
    ap.add_argument(
        "--symlink",
        action="store_true",
        help="symlink images instead of copying (saves disk; trainers must follow links)",
    )
    args = ap.parse_args()

    src = args.src.expanduser().resolve()
    out = args.out.expanduser().resolve()
    if not src.is_dir():
        print(f"Source not found: {src}", file=sys.stderr)
        return 1

    items = pairs(src)
    if not items:
        print(f"No images under {src}", file=sys.stderr)
        return 1

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    n = 0
    for img, txt in items:
        dest_img = out / img.name
        if dest_img.exists():
            # rare name collision from nested trees
            dest_img = out / f"{img.stem}_{n}{img.suffix}"
        if args.symlink:
            dest_img.symlink_to(img)
        else:
            shutil.copy2(img, dest_img)

        raw = txt.read_text(encoding="utf-8", errors="replace") if txt else img.stem
        caption = format_caption(raw, trigger=args.trigger, short=args.short)
        dest_img.with_suffix(".txt").write_text(caption + "\n", encoding="utf-8")
        n += 1
        print(f"  {dest_img.name}")

    print(f"\nExported {n} pairs → {out}")
    print(f"Trigger: {args.trigger!r}  short={args.short}")
    print("Point your LoRA trainer at this folder.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
