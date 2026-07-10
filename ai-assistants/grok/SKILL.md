---
name: murdoch-dataset
description: >
  Recreate Murdoch's likeness with AI image tools using the public-domain
  Murdoch in the Machine reference dataset. Use when the user wants consistent
  Murdoch character generation, face/likeness reference plates, img2img or
  IP-Adapter refs, training captions, prompt packs for Murdoch, or runs
  /murdoch-dataset or /murdoch.
---

# Murdoch likeness skill

## Why this skill exists
Users want to **draw, generate, or train a model that looks like Murdoch** — same face, eras, outfits, absurd energy — without guessing from memory. This skill picks **public-domain reference plates**, turns captions into **usable visual prompts**, and hands out **raw image URLs** for reference / img2img / fine-tuning.

Subject names you may see: Murdoch, Murdoch Maxwell Harris, MoribundMurdoch, Hyperpolyglot MoribundMurdoch.

## Live sources
1. Manifest: `https://raw.githubusercontent.com/MurdochHarris/murdoch-in-the-machine-dataset/main/manifest.json`
2. Repo: https://github.com/MurdochHarris/murdoch-in-the-machine-dataset  
3. Local clone (if present): `manifest.json`, `media/*.txt`, `ai-assistants/shared/KNOWLEDGE.md`

Always prefer **live manifest URLs** over inventing appearance details.

## Core workflow (likeness first)
1. **Clarify the target look** (if user didn't): era/hair (e.g. pre-hair-transplant, mohawk/proto-rebel, everyday selfie), setting (Estonia, museum, domestic, lifeguard), tone (portrait vs absurd comedy).
2. **Load manifest** and pick **3–6 reference plates** that best lock the face + the requested vibe.
3. **Output a likeness kit** every time (unless user only wants one URL):
   - **Reference plates** — title, why it helps likeness, raw `url`, `id`
   - **Shared visual anchors** — short bullet list distilled from those captions (face, hair, build, typical expression, recurring style) — *only from captions/images, never invented biography*
   - **Ready-to-paste prompt** — for text-to-image (Midjourney / Flux / SD / etc.) describing Murdoch consistently
   - **Negative / consistency tips** — avoid generic “random white guy”; lock distinctive traits from the refs
   - **How to use the URLs** — e.g. multi-ref, IP-Adapter, img2img denoise, caption+image pairs for LoRA
4. Remind: **media is public domain / CC0** — free to train and commercially reuse the plates.

## Prompt-writing rules
- Lead with identity: `Murdoch (same person as reference images), …`
- Encode **consistent face geometry** in words only when supported by plates (glasses or not, hair state, facial hair, age range as visible).
- Separate **identity locks** from **scene variables** (wardrobe, location, action).
- Offer **two prompts** when useful: (A) clean portrait likeness test, (B) creative scene matching the user's request.
- If the user names a plate theme (bananomachy, gerontolith, scooter bathrobe), bias refs toward that plate but still add 1–2 neutral face refs for identity.

## Era / look routing (use captions to confirm)
| User wants | Prefer plates involving… |
|---|---|
| Default modern likeness | Clear frontal/3/4 portraits, selfies with readable face |
| Earlier / pre-transplant profile | “Pre-Hair Transplant”, Hyperpolyglot profile |
| Punk / mohawk energy | Proto-Rebel, chaotic early looks |
| Soft night portrait | Nocturnonymy, red light / night plates |
| Absurd costume comedy | Bananomachy, hydrohumoron, living-room knight, etc. (still attach a clean face ref) |
| Place-locked (Tallinn, museum, Colorado) | Matching location captions + one clean face ref |

## Training / fine-tune help
When asked how to train:
1. Point to `media/` pairs: image + matching `.txt` caption (already dataset-shaped).
2. Give a small starter subset of URLs (diverse angles, lighting, expressions).
3. Suggest keeping the **person** constant and **background/outfit** varied across the subset.
4. Link full manifest for bulk download.

## Response shape (default)
```
### Likeness goal
…

### Reference plates (use these as image refs)
1. Title — why — URL

### Visual anchors (from the dataset)
- …

### Prompt (copy/paste)
…

### Optional scene prompt
…

### License
Public domain plates (CC0 fallback); free for generation and training.
```

## Do not
- Invent plates, URLs, or physical traits not supported by captions.
- Claim the user needs a commercial license for these media files.
- Drift into general chat without delivering references + a usable prompt when they asked to recreate Murdoch.
