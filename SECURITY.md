# Security Policy

## Supported Versions
Only the latest commit on the default branch (`main`) of **murdoch-in-the-machine-dataset** is actively supported.

This repository is mostly static media, a JSON manifest, two small Python scripts, and a zero-dependency HTML gallery. There is no server-side application to patch weekly — but supply-chain and content integrity still matter.

## What Counts as a Security Issue Here
- Malicious or deceptive files in `media/` (e.g. polyglot “images,” oversized bombs, embedded executable content).
- Script changes that exfiltrate data, run unexpected network calls, or write outside the repo root.
- XSS or open-redirect issues in `index.html` if it starts interpreting untrusted fields unsafely.
- Compromised `manifest.json` URLs pointing crawlers at hostile hosts.

Ordinary “this photo is weird” reports and caption typos are **not** security issues — open a normal issue or PR.

## Reporting a Vulnerability
Do not report security vulnerabilities through public GitHub issues. Publicly disclosing a vulnerability gives malicious actors the exact blueprints they need to exploit users before a patch can be developed and distributed. However, maybe eventually we could convert the security vulnerability into a good cybersecurity lesson to share with people.

Please report them directly via email to: [Email Not Set Up Yet — Find a reasonable way to contact MoribundMurdoch, e.g., carrier pigeon or the unique centerline rips ancient Chinese dudes used in their missives.]

We will acknowledge receipt ASAP.

## Safe Defaults for Consumers
- Prefer files served from this repository’s `raw.githubusercontent.com` URLs as listed in `manifest.json`.
- Re-run `python3 manifest.py` after any local media change; do not hand-edit URL hosts unless you know why.
- Treat Blogger CDN links as ephemeral sources; this repo is the durable archive.
