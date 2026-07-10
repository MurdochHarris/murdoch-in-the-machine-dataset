#!/usr/bin/env python3
"""Scan image/.txt pairs and write manifest.json for the Murdoch dataset."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "manifest.json"
IMAGE_EXTS = {".jpg", ".jpeg", ".png"}

# Fallback when git remote is unavailable
DEFAULT_OWNER = "MurdochHarris"
DEFAULT_REPO = "murdoch-in-the-machine-dataset"
DEFAULT_BRANCH = "main"


def git_remote_parts() -> tuple[str, str] | None:
    try:
        url = subprocess.check_output(
            ["git", "-C", str(ROOT), "remote", "get-url", "origin"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

    # git@github.com:owner/repo.git  or  https://github.com/owner/repo.git
    m = re.search(r"github\.com[:/]([^/]+)/([^/.]+)", url)
    if not m:
        return None
    return m.group(1), m.group(2)


def git_branch() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "--abbrev-ref", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip() or DEFAULT_BRANCH
    except (subprocess.CalledProcessError, FileNotFoundError):
        return DEFAULT_BRANCH


def raw_base() -> str:
    parts = git_remote_parts()
    owner, repo = parts if parts else (DEFAULT_OWNER, DEFAULT_REPO)
    branch = git_branch()
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}"


def iter_images(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part.startswith(".") for part in path.parts):
            continue
        if path.suffix.lower() not in IMAGE_EXTS:
            continue
        yield path


def load_caption(image: Path) -> str:
    txt = image.with_suffix(".txt")
    if not txt.is_file():
        return ""
    return txt.read_text(encoding="utf-8", errors="replace").strip()


def build_manifest() -> dict:
    base = raw_base()
    items = []

    for image in iter_images(ROOT):
        if image.name == "manifest.json":
            continue
        rel = image.relative_to(ROOT).as_posix()
        caption = load_caption(image)
        items.append(
            {
                "id": image.stem,
                "path": rel,
                "url": f"{base}/{rel}",
                "alt": caption,
                "caption": caption,
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(items),
        "base_url": base,
        "items": items,
    }


def main() -> int:
    data = build_manifest()
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.name} ({data['count']} items) → {data['base_url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
