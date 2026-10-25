# MIN-208: OpenAI — Community Communications Lead Application Package

This repository contains the complete tailored executive application package, strategy brief, and verified 1-page CV for **OpenAI Community Communications Lead** (Product & Research Communications team, in collaboration with Culture & Community Engagement), prepared under the **Mindrock Agent Constitution (AGENTS.md)**.

## Quick Links
- **One-Tap Application Card:** [docs/ONE_TAP_APPLICATION_CARD.md](docs/ONE_TAP_APPLICATION_CARD.md)
- **Tailored 1-Page CV (Markdown):** [docs/TAILORED_CV_OPENAI_COMMUNITY_COMMS.md](docs/TAILORED_CV_OPENAI_COMMUNITY_COMMS.md)
- **Ashby Application Cover Note:** [docs/ASHBY_APPLICATION_NOTE.md](docs/ASHBY_APPLICATION_NOTE.md)
- **Strategic Brief & Narrative Positioning:** [docs/OPENAI_COMMUNITY_COMMS_STRATEGY_BRIEF.md](docs/OPENAI_COMMUNITY_COMMS_STRATEGY_BRIEF.md)
- **Builder Script:** [build_oai_cv.py](build_oai_cv.py)
- **Verified 1-Page PDF:** [cv-pavel-cherkashin-oai.pdf](cv-pavel-cherkashin-oai.pdf)
- **High-Resolution 300 DPI PNG:** [cv-pavel-cherkashin-oai-hd.png](cv-pavel-cherkashin-oai-hd.png)
- **Cryptographic Manifest:** [evidence/MANIFEST.sha256](evidence/MANIFEST.sha256)
- **Machine-Readable Evidence:** [evidence/EVIDENCE.json](evidence/EVIDENCE.json)

## Build & Verification Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Build CV (PDF & 300 DPI HD PNG)
```bash
python build_oai_cv.py
```

### 3. Verify Constraints & Reproducibility
```bash
# Verify exactly 1 page
python3 -c 'from pypdf import PdfReader; pages = len(PdfReader("cv-pavel-cherkashin-oai.pdf").pages); assert pages == 1, f"Expected 1 page, got {pages}"; print("PDF page count: PASS (1 page)")'

# Verify programmatic layout, zero collisions, and page boundary containment
python3 -c 'from build_oai_cv import verify_layout_and_collisions; rep = verify_layout_and_collisions("cv-pavel-cherkashin-oai.pdf"); assert rep["text_overlap_count"] == 0 and rep["out_of_bounds_count"] == 0, f"Collisions: {rep}"; print(f"Layout & collision check: PASS ({rep})")'

# Verify 300 DPI metadata and geometry (2550 x 3300)
python3 -c 'from PIL import Image; im = Image.open("cv-pavel-cherkashin-oai-hd.png"); assert im.size == (2550, 3300), f"Bad size {im.size}"; dpi = round(im.info.get("dpi", (0, 0))[0]); assert dpi == 300, f"Bad dpi {dpi}"; print(f"PNG resolution: PASS ({im.size}, {dpi} DPI)")'

# Verify byte-for-byte reproducible build
python3 build_oai_cv.py /tmp/rebuilt.pdf /tmp/rebuilt.png
cmp cv-pavel-cherkashin-oai.pdf /tmp/rebuilt.pdf && echo "PDF deterministic byte match: PASS"
cmp cv-pavel-cherkashin-oai-hd.png /tmp/rebuilt.png && echo "PNG deterministic byte match: PASS"

# Verify cryptographic manifest integrity
sha256sum -c evidence/MANIFEST.sha256
```

## Paradigm: 6-Month Comms Automation Arc
Built around Pavel Cherkashin's core operator-storyteller philosophy:
> *"Automating communications operations—story sourcing, editorial cadence, distribution reach, and sentiment telemetry—while fiercely preserving human judgment, cultural taste, trust, and authentic community voices. Bringing OpenAI products closer to everyday communities by propelling AI out of tech subcultures into mainstream culture (sports, music, design, food, fandoms) on a disciplined 6-month arc."*
