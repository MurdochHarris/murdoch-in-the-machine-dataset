<div align="center">

# Murdoch in the Machine

A **public-domain** image dataset and structured metadata archive of Murdoch —  
formatted for open-source AI training, crawlers, and a zero-dependency web gallery.

[![License: MIT + Public Domain media](https://img.shields.io/badge/License-MIT%20%2B%20PD%20media-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-stdlib_only-3776AB.svg?logo=python&logoColor=white)](manifest.py)
[![No npm](https://img.shields.io/badge/Frontend-vanilla_HTML-brightgreen.svg)](index.html)
[![Plates](https://img.shields.io/badge/plates-see_manifest.json-lightgrey.svg)](manifest.json)

**Blog (editorial):** [murdochinthemachine.blogspot.com](https://murdochinthemachine.blogspot.com/)  
**Dataset (canonical files):** this repository

</div>

---

## Why this exists

Blogs are good for stories. They are mediocre durable datasets.

This repo keeps each plate as a boring, permanent pair:

| File | Role |
|------|------|
| `media/<id>.jpg` (or `.png`) | The image |
| `media/<id>.txt` | Caption / alt text / labels / source / license |
| `manifest.json` | Machine-readable index with stable raw GitHub URLs |
| `index.html` | Optional GitHub Pages gallery (no build step) |

Use it to train models, cite likeness, scrape ethically, or just browse plates like a paper archive.

---

## Quick start

### Browse
Open `index.html` via GitHub Pages (enable **Settings → Pages → Deploy from `main` / root**), or serve the repo root locally:

```bash
python3 -m http.server 8080
# → http://127.0.0.1:8080/
```

The gallery fetches `manifest.json` and renders cards with native Web Components.

### Use the data in code
Every item in `manifest.json` looks like:

```json
{
  "id": "murdochs-bananomachy-124c7543",
  "path": "media/murdochs-bananomachy-124c7543.jpg",
  "url": "https://raw.githubusercontent.com/MurdochHarris/murdoch-in-the-machine-dataset/main/media/...",
  "alt": "…full caption text…",
  "caption": "…same…"
}
```

Prefer the `url` field for downloads; it points at `raw.githubusercontent.com` for this repository.

---

## Repository layout

```
.
├── media/              # image + matching .txt sidecars
├── manifest.json       # generated index (do not hand-curate unless necessary)
├── manifest.py         # scan pairs → rewrite manifest.json
├── sync_blogger.py     # pull new posts from the Blogger feed into media/
├── index.html          # vintage-paper gallery (vanilla JS)
├── LICENSE
├── CODE_OF_CONDUCT.md
└── SECURITY.md
```

---

## Maintain the archive

Requires **Python 3** and the standard library only.

### Rebuild the manifest after adding files
```bash
python3 manifest.py
```

### Import / refresh plates from Blogger
```bash
python3 sync_blogger.py --manifest
```

- Reads the public Blogger JSON feed.
- Downloads full-size images into `media/`.
- Writes `.txt` sidecars (title, body text, labels, source URL, license line).
- Skips files that already exist (pass `--force` to re-download).

Then commit the new media + `manifest.json` and push.

```bash
git add media manifest.json
git commit -m "Sync new Blogger plates"
git push
```

---

## Adding a plate by hand

1. Drop `media/my-plate.jpg` (or `.png`).
2. Add `media/my-plate.txt` with a human-readable caption (title first line is ideal).
3. Run `python3 manifest.py`.
4. Commit and push.

---

## License

| What | Terms |
|------|--------|
| **Images + `.txt` captions in `media/`** | **Public domain** (CC0 fallback) — free for AI training and any other use |
| **Scripts, `index.html`, docs** | **MIT** — see [LICENSE](LICENSE) |

See [LICENSE](LICENSE) for the full text. Trademarks or third-party marks visible *in* a photograph are not “waived”; only the author’s copyright interest in the file is.

---

## Conduct & security

- Community norms: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Vulnerability reporting: [SECURITY.md](SECURITY.md)

---

## AI assistants — recreate Murdoch’s likeness

Packs in [`ai-assistants/`](ai-assistants/) turn this dataset into **likeness kits** (reference URLs + visual anchors + prompts) for consistent Murdoch generation and training:

| Platform | What to use |
|----------|-------------|
| **ChatGPT** Custom GPT | `ai-assistants/chatgpt/INSTRUCTIONS.md` + upload `shared/KNOWLEDGE.md` |
| **Gemini** Gem | `ai-assistants/gemini/GEM_INSTRUCTIONS.md` + upload `shared/KNOWLEDGE.md` |
| **Grok** skill | copy `ai-assistants/grok/SKILL.md` → `~/.grok/skills/murdoch-dataset/` |

```bash
python3 ai-assistants/build_knowledge.py   # after new plates; re-upload KNOWLEDGE.md
```

See [ai-assistants/README.md](ai-assistants/README.md).

---

## Related

- Editorial blog: https://murdochinthemachine.blogspot.com/
- GitHub: https://github.com/MurdochHarris/murdoch-in-the-machine-dataset

P.S. Good luck training your machine to create consistent characters. Enjoy sharing and creating.
