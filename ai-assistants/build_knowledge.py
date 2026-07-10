#!/usr/bin/env python3
"""Regenerate ai-assistants/shared knowledge files from manifest.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED = Path(__file__).resolve().parent / "shared"
MANIFEST = ROOT / "manifest.json"


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    items = data.get("items") or []
    SHARED.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Murdoch in the Machine — Likeness Knowledge Pack",
        "",
        "Uploadable knowledge for ChatGPT, Gemini, Grok, and similar assistants.",
        "**Primary use:** help users recreate Murdoch’s likeness (consistent character generation and training).",
        "",
        "## Dataset facts",
        "",
        "- **Name:** Murdoch in the Machine",
        "- **Subject names:** Murdoch, Murdoch Maxwell Harris, MoribundMurdoch, Hyperpolyglot MoribundMurdoch",
        "- **GitHub:** https://github.com/MurdochHarris/murdoch-in-the-machine-dataset",
        "- **Blog (editorial):** https://murdochinthemachine.blogspot.com/",
        "- **Manifest (live):** https://raw.githubusercontent.com/MurdochHarris/murdoch-in-the-machine-dataset/main/manifest.json",
        "- **License (media + captions):** Public domain / CC0 — free for AI training, fine-tunes, and commercial likeness use of these files",
        "- **License (repo software):** MIT",
        f"- **Plate count:** {len(items)}",
        "- **Format:** each plate is an image plus a caption (title, description, labels, source URL)",
        "",
        "## How to help with likeness",
        "",
        "1. Treat this as a **character reference sheet set**, not only a photo gallery.",
        "2. For generation requests: pick face-readable plates + vibe matches; return raw **image_url**s.",
        "3. Distill **visual anchors** only from captions (hair era, expression, wardrobe, place).",
        "4. Write **copy-paste prompts** that lock identity first, then scene.",
        "5. For training: recommend diverse image+caption pairs and the public-domain license.",
        "6. Do not invent plates, URLs, or appearance details missing from captions.",
        "7. Prefer live manifest URLs when knowledge may be stale.",
        "",
        "## Plate index (references)",
        "",
    ]

    for i, item in enumerate(items, 1):
        caption = (item.get("caption") or item.get("alt") or "").strip()
        title = caption.split("\n", 1)[0].strip() if caption else item.get("id", "Untitled")
        lines += [
            f"### {i}. {title}",
            "",
            f"- **id:** `{item.get('id', '')}`",
            f"- **path:** `{item.get('path', '')}`",
            f"- **image_url:** {item.get('url', '')}",
            "",
            "**Caption:**",
            "",
            caption if caption else "_(no caption)_",
            "",
            "---",
            "",
        ]

    (SHARED / "KNOWLEDGE.md").write_text("\n".join(lines), encoding="utf-8")

    slim = [
        "# Murdoch plate quick index",
        "",
        "id | title | image_url",
        "---|---|---",
    ]
    for item in items:
        caption = (item.get("caption") or item.get("alt") or "").strip()
        title = (
            caption.split("\n", 1)[0].strip().replace("|", "/")
            if caption
            else item.get("id", "")
        )
        slim.append(f"`{item.get('id', '')}` | {title} | {item.get('url', '')}")
    (SHARED / "INDEX.md").write_text("\n".join(slim) + "\n", encoding="utf-8")

    (SHARED / "manifest.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"Wrote {SHARED}/KNOWLEDGE.md, INDEX.md, manifest.json ({len(items)} plates)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
