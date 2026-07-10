# AI assistant packs — Murdoch in the Machine

Files in this folder are ready to paste or upload into **ChatGPT**, **Gemini**, and **Grok**.  
They describe the public-domain Murdoch dataset so an assistant can recommend plates, quote captions, and return stable image URLs.

```
ai-assistants/
├── README.md                 ← you are here
├── shared/
│   ├── KNOWLEDGE.md          ← full plate index + captions (primary upload)
│   ├── INDEX.md              ← short table of id / title / URL
│   └── manifest.json         ← machine copy of the repo manifest
├── chatgpt/
│   ├── INSTRUCTIONS.md       ← Custom GPT system instructions
│   └── CONVERSATION_STARTERS.md
├── gemini/
│   └── GEM_INSTRUCTIONS.md   ← Gemini Gem instructions
└── grok/
    └── SKILL.md              ← Grok Build / agent skill
```

**Source of truth remains the GitHub repo.** After you add plates (`sync_blogger.py` / new media), regenerate knowledge:

```bash
python3 ai-assistants/build_knowledge.py
```

Then re-upload `shared/KNOWLEDGE.md` (and `manifest.json` if you use it) on each platform.

---

## ChatGPT (Custom GPT)

1. Open [ChatGPT](https://chatgpt.com) → **Explore GPTs** → **Create** (or **My GPTs** → **Create a GPT**).
2. **Configure** tab:
   - **Name:** `Murdoch in the Machine`
   - **Description:** Public-domain Murdoch image dataset assistant — captions, labels, raw image URLs for training and reference.
   - **Instructions:** paste entire contents of [`chatgpt/INSTRUCTIONS.md`](chatgpt/INSTRUCTIONS.md).
   - **Conversation starters:** copy lines from [`chatgpt/CONVERSATION_STARTERS.md`](chatgpt/CONVERSATION_STARTERS.md).
   - **Knowledge:** upload:
     - `shared/KNOWLEDGE.md` (required)
     - `shared/manifest.json` (optional, helpful)
   - **Capabilities:** enable **Browsing** if available so the GPT can refresh from GitHub raw URLs when knowledge is stale.
3. Create → save as only you / anyone with link / public (your choice).

No paid API key is required for a basic knowledge GPT. Actions/OpenAPI are optional later.

---

## Gemini (Gem)

1. Open [Gemini](https://gemini.google.com) → **Gem manager** / **Explore Gems** → **New Gem** (wording varies by account).
2. **Name:** `Murdoch in the Machine`
3. **Instructions:** paste [`gemini/GEM_INSTRUCTIONS.md`](gemini/GEM_INSTRUCTIONS.md).
4. **Knowledge / files:** upload `shared/KNOWLEDGE.md` (and optionally `shared/manifest.json`).
5. Save the Gem and start a chat with it.

If your Gemini client only allows one knowledge file, use `KNOWLEDGE.md` alone.

---

## Grok (Skill)

### Option A — Grok Build / local agent skill

Copy the skill into your user skills directory:

```bash
mkdir -p ~/.grok/skills/murdoch-dataset
cp ai-assistants/grok/SKILL.md ~/.grok/skills/murdoch-dataset/SKILL.md
```

Or keep a project skill:

```bash
mkdir -p .grok/skills/murdoch-dataset
cp ai-assistants/grok/SKILL.md .grok/skills/murdoch-dataset/SKILL.md
```

Then run `/murdoch-dataset` or ask in natural language for Murdoch reference plates.

### Option B — Paste as custom instructions

If you only have a chat UI with “custom instructions,” paste the body of `grok/SKILL.md` (below the frontmatter) into that box and attach/link `shared/KNOWLEDGE.md` if the product allows files.

---

## What users should get back

A good answer always includes:

1. Plate title  
2. Short caption / why it matches  
3. Raw image URL (`raw.githubusercontent.com/...`)  
4. License note when relevant (public domain media)

Live manifest (always current after you push):

https://raw.githubusercontent.com/MurdochHarris/murdoch-in-the-machine-dataset/main/manifest.json
