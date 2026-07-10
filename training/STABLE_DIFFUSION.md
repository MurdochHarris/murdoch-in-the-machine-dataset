# Stable Diffusion & friends — Murdoch likeness

This dataset is already shaped for SD-style training: every plate is an **image + matching `.txt` caption** under `media/`.

**Goal:** teach a model (usually a **LoRA**) to recreate **Murdoch** so you can prompt him into new scenes.

| License | Media + captions are **public domain / CC0** — fine for training and commercial gens from your model. |
|---------|--------------------------------------------------------------------------------------------------------|

Live files: https://github.com/MurdochHarris/murdoch-in-the-machine-dataset  

---

## Paths (pick one)

| Path | Effort | Best when |
|------|--------|-----------|
| **A. Reference only** (no training) | Minutes | Img2img, IP-Adapter, “reference image” UIs |
| **B. LoRA / DreamBooth** | ~30–90 min on a GPU | You want `murdoch` in the prompt forever |
| **C. Full fine-tune** | Heavy | Usually overkill for ~22 plates — prefer LoRA |

For most people: **B (LoRA)** or **A** while testing.

---

## A. No training — use plates as references

1. Open any plate from the repo or raw URL, e.g.  
   `https://raw.githubusercontent.com/MurdochHarris/murdoch-in-the-machine-dataset/main/media/<file>.jpg`
2. In your UI:
   - **Img2img** — load plate, denoise **0.35–0.55**, prompt the new scene + “same person”.
   - **IP-Adapter / FaceID / PuLID** — use 1–4 face-readable plates as refs.
   - **ComfyUI** — IP-Adapter Advanced or FaceID node chain with those images.
3. For costume/absurd scenes, still attach **one clean face plate** so identity doesn’t drift.

**Face-friendly starters** (check current `manifest.json` for exact paths): clear selfies and portraits (e.g. nocturnonymy, pre-hair-transplant profile, proto-rebel, Tallinn selfies). Costume plates (bananomachy, hydrohumoron, etc.) are great for *style/vibe*, weaker alone for face lock.

---

## B. Train a LoRA (recommended)

### 1. Get the images

```bash
git clone https://github.com/MurdochHarris/murdoch-in-the-machine-dataset.git
cd murdoch-in-the-machine-dataset
```

Or download only `media/` from GitHub.

### 2. Export a trainer-ready folder

```bash
python3 training/export_sd_dataset.py
# → training/sd-dataset/   (images + .txt captions, trigger word applied)
```

Useful flags:

```bash
# Classic DreamBooth-style token
python3 training/export_sd_dataset.py --trigger "ohwx murdoch"

# Short captions (first line of each .txt only) — often trains cleaner
python3 training/export_sd_dataset.py --short

# Both
python3 training/export_sd_dataset.py --trigger "murdoch" --short --out ~/datasets/murdoch
```

Default trigger: **`murdoch`**.  
Each caption becomes something like:

```text
murdoch, Proto-Rebel Murdoch
```

or, without `--short`, the full caption with the trigger prefixed.

### 3. Folder layout trainers expect

```text
training/sd-dataset/
  some-plate.jpg
  some-plate.txt
  other-plate.png
  other-plate.txt
  ...
```

That is the usual **image + same-name caption** layout for:

- [kohya_ss](https://github.com/bmaltais/kohya_ss) / sd-scripts  
- OneTrainer  
- SimpleTuner  
- Derrian’s Easy Training scripts  
- Many Colab “LoRA trainer” notebooks  

### 4. Base model

Pick what you actually generate with:

| You use | Base (examples) |
|---------|------------------|
| SD 1.5 ecosystem | `runwayml/stable-diffusion-v1-5` or a realistic 1.5 checkpoint |
| SDXL | `stabilityai/stable-diffusion-xl-base-1.0` or a realistic SDXL fine-tune |
| Pony / Illustrious / etc. | That model’s base — train the LoRA **on the same family** you sample with |
| Flux | Flux LoRA trainer (different scripts; same **image+txt** folder still works as the dataset) |

### 5. Starting hyperparameters (~22 images)

These are **starting points**, not law. Adjust if faces collapse or overfit.

| Setting | SD 1.5 LoRA | SDXL LoRA |
|---------|-------------|-----------|
| Resolution | 512 (or 768 if VRAM allows) | 1024 |
| Repeats per image | 10–20 | 5–15 |
| Epochs | 10–20 | 8–15 |
| Unet LR | ~1e-4 | ~1e-4 |
| Text encoder LR | 0 or ~5e-5 | often 0 or low |
| Network dim / alpha | 16–32 / 16–32 | 16–32 / 16–32 |
| Batch size | 1–2 | 1 |
| N-repeats folder name (kohya) | e.g. `15_murdoch` | same idea |

**Kohya-style tip:** put images in a folder named like `15_murdoch` (repeats_class) *or* set repeats in the GUI; captions already contain the trigger.

**Overfit signs:** only reproduces training backgrounds, can’t change clothes/place.  
**Underfit signs:** face never locks. Fix: more repeats, more face-heavy subset, slightly longer train, or add 5–10 extra close crops later.

### 6. Caption tips for better likeness

- Keep the **trigger** (`murdoch` / `ohwx murdoch`) on every file.  
- Prefer **short** captions for pure face LoRAs (`--short`).  
- Use **full** captions if you also want the model to learn labeled concepts (bananomachy, gerontolith, etc.).  
- You can hand-edit any `.txt` in `training/sd-dataset/` before training.  
- Optional: duplicate the best frontal faces with an extra caption line for emphasis (don’t spam 50 copies of one photo).

### 7. Use the LoRA when generating

1. Drop the `.safetensors` into your UI’s LoRA folder  
   (`models/Lora`, Forge/A1111, or ComfyUI `models/loras`).
2. Prompt pattern:

```text
photo of murdoch person, [scene], [lighting], [camera]
```

With a unique token:

```text
photo of ohwx murdoch, sitting in a cafe, natural window light
```

3. LoRA weight: start **0.6–0.85**; raise if identity is weak, lower if style is locked to training poses.  
4. For hard scenes: generate with LoRA + **one reference plate** (IP-Adapter) together.

---

## C. DreamBooth vs LoRA

| | LoRA | DreamBooth (full) |
|--|------|-------------------|
| File size | Small (MBs) | Large |
| Risk of frying base model | Low | Higher |
| Good for 20–40 images | **Yes** | Possible but heavier |
| Sharing | Easy to publish on Civitai | Clumsier |

Prefer **LoRA** unless you already know you want a DreamBooth checkpoint.

---

## D. Automatic1111 / Forge / ComfyUI (after you have a LoRA)

### A1111 / Forge
1. `models/Lora/<name>.safetensors`
2. Prompt: `<lora:name:0.75> murdoch, ...`
3. Or use the LoRA menu to insert the tag.

### ComfyUI
1. `Load LoRA` node on the model (and optionally CLIP).  
2. Strength ~0.7.  
3. Prompt contains your trigger word.  
4. Optional: add IP-Adapter with a plate from `media/` for stubborn scenes.

### Offline “dataset only” install
If a trainer asks for a **dataset path**, point it at:

```text
/path/to/murdoch-in-the-machine-dataset/training/sd-dataset
```

after running `export_sd_dataset.py`.

---

## E. Download without cloning git

From the manifest (all raw URLs):

```bash
python3 - <<'PY'
import json, urllib.request
from pathlib import Path
url = "https://raw.githubusercontent.com/MurdochHarris/murdoch-in-the-machine-dataset/main/manifest.json"
data = json.load(urllib.request.urlopen(url))
out = Path("murdoch-media"); out.mkdir(exist_ok=True)
for it in data["items"]:
    img = it["url"]
    name = Path(it["path"]).name
    print("get", name)
    urllib.request.urlretrieve(img, out / name)
    # captions: same path with .txt on raw github
    cap = img.rsplit(".", 1)[0] + ".txt"
    try:
        urllib.request.urlretrieve(cap, out / (Path(name).stem + ".txt"))
    except Exception as e:
        print("  no caption", e)
print("done", out)
PY
```

Then:

```bash
python3 training/export_sd_dataset.py --src murdoch-media --out training/sd-dataset
```

(`export_sd_dataset.py` accepts `--src` for any folder of image+txt pairs.)

---

## F. Civitai / sharing

If you publish a Murdoch LoRA:

1. Credit the dataset:  
   https://github.com/MurdochHarris/murdoch-in-the-machine-dataset  
2. Note media is **public domain**; your LoRA file can use whatever license you choose for the weights.  
3. Sample prompts + trigger word in the model card.  
4. Don’t claim the photos are copyrighted by you.

---

## G. Checklist

- [ ] Clone or download `media/`  
- [ ] `python3 training/export_sd_dataset.py --trigger murdoch --short`  
- [ ] Train LoRA on **same base family** you sample with  
- [ ] Generate: `murdoch, portrait, soft light` as a likeness test  
- [ ] If face drifts: lower scene complexity, raise LoRA weight, add IP-Adapter ref  
- [ ] If overfit: lower epochs/repeats, shorten captions, more varied prompts  

---

## Related

- Dataset root README: [`../README.md`](../README.md)  
- Chat/agent likeness kits: [`../ai-assistants/`](../ai-assistants/)  
- Rebuild web manifest: `python3 manifest.py`  
