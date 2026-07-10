# AI assistant packs — recreate Murdoch’s likeness

These files turn the dataset into **likeness kits** for ChatGPT, Gemini, and Grok: reference plates, visual anchors, and prompts so people can generate or train a **consistent Murdoch**, not just browse a gallery.

```
ai-assistants/
├── README.md
├── build_knowledge.py
├── shared/
│   ├── KNOWLEDGE.md      ← upload this (plates + captions + URLs)
│   ├── INDEX.md
│   └── manifest.json
├── chatgpt/
│   ├── INSTRUCTIONS.md
│   └── CONVERSATION_STARTERS.md
├── gemini/
│   └── GEM_INSTRUCTIONS.md
└── grok/
    └── SKILL.md
```

After new plates:

```bash
python3 ai-assistants/build_knowledge.py
```

Re-upload `shared/KNOWLEDGE.md` on ChatGPT/Gemini when it changes.

---

## What a good answer looks like

Assistants should return a **likeness kit**:

1. **Reference plates** — raw GitHub image URLs (face locks + vibe matches)  
2. **Visual anchors** — what to keep constant across gens  
3. **Prompts** — identity test + optional scene  
4. **Training note** — public domain; use `media/` image+`.txt` pairs or the URLs  

Live catalog:  
https://raw.githubusercontent.com/MurdochHarris/murdoch-in-the-machine-dataset/main/manifest.json

---

## ChatGPT (Custom GPT)

1. **Create a GPT** → Configure  
2. **Name:** Murdoch Likeness / Murdoch in the Machine  
3. **Description:** Public-domain Murdoch reference plates + prompts for consistent AI likeness and character training.  
4. **Instructions:** paste [`chatgpt/INSTRUCTIONS.md`](chatgpt/INSTRUCTIONS.md)  
5. **Conversation starters:** [`chatgpt/CONVERSATION_STARTERS.md`](chatgpt/CONVERSATION_STARTERS.md)  
6. **Knowledge:** upload `shared/KNOWLEDGE.md` (optional: `shared/manifest.json`)  
7. Enable **Browsing** if you want live manifest refresh  

---

## Gemini (Gem)

1. New Gem  
2. **Instructions:** paste [`gemini/GEM_INSTRUCTIONS.md`](gemini/GEM_INSTRUCTIONS.md)  
3. **Files:** upload `shared/KNOWLEDGE.md`  

---

## Grok (Skill)

```bash
mkdir -p ~/.grok/skills/murdoch-dataset
cp ai-assistants/grok/SKILL.md ~/.grok/skills/murdoch-dataset/SKILL.md
```

Trigger: `/murdoch-dataset`, `/murdoch`, or “generate Murdoch consistently / likeness refs”.

The skill fetches the **live** `manifest.json` so it stays current after you push new plates.

---

## Tip for image tools

| Workflow | How to use this pack |
|----------|----------------------|
| Text-to-image | Paste identity prompt; attach 1–4 reference URLs if the tool allows |
| Img2img / IP-Adapter | Use face-lock plate URLs as references; keep identity weight high |
| LoRA / fine-tune | Download diverse `media/*` pairs or URLs from the likeness kit |
