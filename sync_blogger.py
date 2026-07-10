#!/usr/bin/env python3
"""Pull Murdoch posts from Blogger into media/ image + .txt pairs.

Uses only the standard library. Re-run anytime; skips unchanged files.
Then run manifest.py (or pass --manifest) to refresh manifest.json.

  python3 sync_blogger.py
  python3 sync_blogger.py --manifest
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent
MEDIA = ROOT / "media"
FEED_URL = (
    "https://www.blogger.com/feeds/3241175302474432802/posts/default"
    "?alt=json&max-results=500"
)
USER_AGENT = "murdoch-in-the-machine-dataset/1.0 (+https://github.com/MurdochHarris/murdoch-in-the-machine-dataset)"


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in ("script", "style"):
            self._skip = True
        elif tag == "br":
            self._parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self._skip = False
        elif tag in ("p", "div", "li", "h1", "h2", "h3", "tr"):
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self._parts.append(data)

    def text(self) -> str:
        t = "".join(self._parts)
        t = re.sub(r"[ \t\f\v]+", " ", t)
        t = re.sub(r" *\n *", "\n", t)
        t = re.sub(r"\n{3,}", "\n\n", t)
        return t.strip()


def html_to_text(raw: str) -> str:
    p = TextExtractor()
    try:
        p.feed(raw)
        p.close()
    except Exception:
        return re.sub(r"<[^>]+>", " ", raw).strip()
    return p.text()


def slugify(title: str, post_id: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"[-\s]+", "-", s).strip("-")
    s = s[:80] or "post"
    # short stable suffix from Blogger post id
    digest = hashlib.sha1(post_id.encode()).hexdigest()[:8]
    return f"{s}-{digest}"


def fullsize_url(url: str) -> str:
    """Ask Blogger for the largest available render of a hosted image."""
    u = url.strip()
    # /img/b/.../s720/file.jpg  →  /s0/file.jpg
    u = re.sub(r"/s\d+-c/", "/s0/", u)
    u = re.sub(r"/s\d+/", "/s0/", u)
    # /img/a/TOKEN=s72-c  →  =s0
    u = re.sub(r"=s\d+(-c)?$", "=s0", u)
    return u


def extract_image_urls(html: str) -> list[str]:
    hrefs = re.findall(
        r'href=["\'](https://blogger\.googleusercontent\.com/[^"\']+)["\']',
        html,
        flags=re.I,
    )
    srcs = re.findall(
        r'src=["\'](https://blogger\.googleusercontent\.com/[^"\']+)["\']',
        html,
        flags=re.I,
    )
    seen: set[str] = set()
    out: list[str] = []
    for u in hrefs + srcs:
        if "blogblog.com" in u or "/widgets/" in u:
            continue
        fu = fullsize_url(u)
        if fu not in seen:
            seen.add(fu)
            out.append(fu)
    return out


def guess_ext(url: str, content_type: str | None) -> str:
    path = unquote(urlparse(url).path)
    m = re.search(r"\.(jpe?g|png|gif|webp)$", path, re.I)
    if m:
        return "." + m.group(1).lower().replace("jpeg", "jpg")
    if content_type:
        ct = content_type.split(";")[0].strip().lower()
        return {
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/webp": ".webp",
        }.get(ct, ".jpg")
    return ".jpg"


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
        ctype = resp.headers.get("Content-Type")
    if not dest.suffix:
        dest = dest.with_suffix(guess_ext(url, ctype))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return  # type: ignore[return-value]


def download_to(url: str, dest_no_ext: Path) -> Path:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
        ctype = resp.headers.get("Content-Type")
    dest = dest_no_ext.with_suffix(guess_ext(url, ctype))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest


def post_link(entry: dict) -> str:
    for link in entry.get("link", []):
        if link.get("rel") == "alternate" and link.get("type", "").startswith("text/html"):
            return link.get("href", "")
    return ""


def post_id(entry: dict) -> str:
    raw = entry.get("id", {}).get("$t", "")
    # tag:blogger.com,1999:blog-...post-388811326735345660
    m = re.search(r"post-(\d+)", raw)
    return m.group(1) if m else raw


def write_sidecar(path: Path, *, title: str, body: str, labels: list[str], source: str, published: str) -> None:
    lines = [
        title.strip(),
        "",
    ]
    if body:
        lines.append(body)
        lines.append("")
    if labels:
        lines.append("Labels: " + ", ".join(labels))
    if published:
        lines.append(f"Published: {published}")
    if source:
        lines.append(f"Source: {source}")
    lines.append("License: Public domain (Murdoch in the Machine dataset)")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def sync(*, force: bool = False) -> int:
    print(f"Fetching feed…")
    feed = fetch_json(FEED_URL)["feed"]
    entries = feed.get("entry") or []
    print(f"Found {len(entries)} posts")
    MEDIA.mkdir(parents=True, exist_ok=True)

    saved = 0
    skipped = 0
    failed = 0

    for entry in entries:
        title = (entry.get("title") or {}).get("$t", "Untitled").strip()
        pid = post_id(entry)
        slug = slugify(title, pid)
        content_html = (entry.get("content") or entry.get("summary") or {}).get("$t", "")
        body = html_to_text(content_html)
        labels = [
            c["term"]
            for c in entry.get("category", [])
            if c.get("term") and not str(c.get("scheme", "")).endswith("#kind")
        ]
        # drop atom scheme noise
        labels = [l for l in labels if "schemas.google" not in l]
        source = post_link(entry)
        published = (entry.get("published") or {}).get("$t", "")

        urls = extract_image_urls(content_html)
        if not urls:
            thumb = (entry.get("media$thumbnail") or {}).get("url")
            if thumb:
                urls = [fullsize_url(thumb)]
        if not urls:
            print(f"  skip (no image): {title}")
            skipped += 1
            continue

        for i, url in enumerate(urls):
            name = slug if len(urls) == 1 else f"{slug}-{i + 1}"
            # existing file with any image ext?
            existing = next(
                (p for p in MEDIA.glob(name + ".*") if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"}),
                None,
            )
            txt_path = MEDIA / f"{name}.txt"

            if existing and txt_path.is_file() and not force:
                print(f"  keep: {existing.name}")
                skipped += 1
                continue

            try:
                dest = download_to(url, MEDIA / name)
                write_sidecar(
                    dest.with_suffix(".txt"),
                    title=title,
                    body=body,
                    labels=labels,
                    source=source,
                    published=published,
                )
                print(f"  + {dest.name} ({dest.stat().st_size // 1024} KB)")
                saved += 1
                time.sleep(0.25)  # be polite to Blogger CDN
            except urllib.error.HTTPError as e:
                print(f"  ! HTTP {e.code} for {title}: {url[:80]}…")
                failed += 1
            except Exception as e:
                print(f"  ! {title}: {e}")
                failed += 1

    print(f"Done. saved={saved} skipped={skipped} failed={failed}")
    return 0 if failed == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="re-download even if files exist")
    ap.add_argument("--manifest", action="store_true", help="run manifest.py after sync")
    args = ap.parse_args()

    code = sync(force=args.force)
    if args.manifest:
        subprocess.check_call([sys.executable, str(ROOT / "manifest.py")], cwd=str(ROOT))
    return code


if __name__ == "__main__":
    sys.exit(main())
