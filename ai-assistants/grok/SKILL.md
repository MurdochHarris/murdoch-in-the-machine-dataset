---
name: murdoch-dataset
description: >
  Browse and cite the public-domain Murdoch in the Machine image dataset.
  Use when the user asks for Murdoch reference images, likeness plates,
  dataset captions, labels, raw GitHub image URLs, AI-training assets,
  or runs /murdoch-dataset or /murdoch.
---

# Murdoch in the Machine — Dataset skill

## Mission
Help the user find Murdoch plates (public-domain images + captions) for reference, training, or citation. Prefer live data over stale memory.

## Live sources (fetch these)
1. **Manifest (preferred):**  
   `https://raw.githubusercontent.com/MurdochHarris/murdoch-in-the-machine-dataset/main/manifest.json`
2. **Repo:** https://github.com/MurdochHarris/murdoch-in-the-machine-dataset  
3. **Blog:** https://murdochinthemachine.blogspot.com/

If network is unavailable and this skill sits beside a clone of the repo, read local `manifest.json` and `media/*.txt` instead.

Local knowledge pack (if present in the same project):  
`ai-assistants/shared/KNOWLEDGE.md` and `ai-assistants/shared/INDEX.md`.

## Workflow
1. Load the manifest JSON (`items[]` with `id`, `path`, `url`, `alt`/`caption`).
2. Filter by user query against caption text, id, path, labels inside caption.
3. Rank simple keyword hits; if empty, broaden (synonyms, place names, clothing).
4. Reply with **2–5** best plates unless the user wants one or all.
5. For each plate output:
   - **Title** — first line of caption
   - **Why** — one short sentence
   - **URL** — `url` field (raw.githubusercontent.com)
   - **id** — for scripting
6. Mention license when relevant: media/captions are **public domain / CC0**; code is **MIT**.

## Commands users may say
- `/murdoch-dataset banana` — search
- `/murdoch random` — one random plate
- “plates for consistent character training”
- “Estonia selfies with URLs”

## Rules
- Do not invent plates or URLs.
- Do not claim copyright over the media.
- Prefer raw GitHub URLs over Blogger CDN links.
- After local media changes in a clone, suggest: `python3 manifest.py` and `python3 ai-assistants/build_knowledge.py`.
