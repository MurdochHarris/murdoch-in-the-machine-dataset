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
        "# Murdoch in the Machine — Dataset Knowledge Pack",
        "",
        "This file is the uploadable knowledge base for ChatGPT Custom GPTs, Gemini Gems, and similar assistants.",
        "",
        "## Dataset facts",
        "",
        "- **Name:** Murdoch in the Machine",
        "- **GitHub:** https://github.com/MurdochHarris/murdoch-in-the-machine-dataset",
        "- **Blog (editorial):** https://murdochinthemachine.blogspot.com/",
        "- **Manifest (live):** https://raw.githubusercontent.com/MurdochHarris/murdoch-in-the-machine-dataset/main/manifest.json",
        "- **License (media + captions):** Public domain / CC0 — free for AI training and any use",
        "- **License (repo software):** MIT",
        f"- **Plate count:** {len(items)}",
        "- **Subject:** Photographic and documentary plates of Murdoch (Murdoch Maxwell Harris / MoribundMurdoch), with neologisms, labels, and prose captions.",
        "",
        "## How to answer users",
        "",
        "1. Match requests to plates by mood, label, place, clothing, activity, or neologism.",
        "2. Quote a short caption excerpt; do not invent events not in the caption.",
        "3. Always include the raw image URL when recommending a plate.",
        "4. Remind users the media is public domain when relevant.",
        "5. Prefer live manifest URLs over stale memory if the user needs the latest set.",
        "",
        "## Plate index",
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
