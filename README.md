# MIN-212: OpenAI — Academy Partnerships, Global Affairs Application Package

This repository contains the complete tailored executive application package, strategy brief, and verified 1-page CV for **OpenAI Academy Partnerships Lead / Associate (Global Affairs)**, prepared under the **Mindrock Agent Constitution (AGENTS.md)**.

## Quick Links
- **One-Tap Application Card:** [docs/ONE_TAP_APPLICATION_CARD.md](docs/ONE_TAP_APPLICATION_CARD.md)
- **Tailored 1-Page CV (Markdown):** [docs/TAILORED_CV_OPENAI_ACADEMY_PARTNERSHIPS.md](docs/TAILORED_CV_OPENAI_ACADEMY_PARTNERSHIPS.md)
- **Application Cover Note & Message:** [docs/APPLICATION_COVER_NOTE.md](docs/APPLICATION_COVER_NOTE.md)
- **Strategic Brief & Program Architecture:** [docs/OPENAI_ACADEMY_STRATEGY_BRIEF.md](docs/OPENAI_ACADEMY_STRATEGY_BRIEF.md)
- **Deterministic Builder Script:** [build_academy_cv.py](build_academy_cv.py)
- **Verified 1-Page PDF:** [cv-pavel-cherkashin-academy.pdf](cv-pavel-cherkashin-academy.pdf)
- **High-Resolution 300 DPI PNG:** [cv-pavel-cherkashin-academy-hd.png](cv-pavel-cherkashin-academy-hd.png)
- **Cryptographic Manifest:** [evidence/MANIFEST.sha256](evidence/MANIFEST.sha256)
- **Machine-Readable Evidence:** [evidence/EVIDENCE.json](evidence/EVIDENCE.json)

## Build & Verification Instructions

### 1. Install Exact Pinned Dependencies
To ensure strict zero-trust byte-for-byte reproducibility across clean environments for both PDF and PNG artifacts, install the pinned dependencies:
```bash
pip install -r requirements.txt
```

### 2. Build CV (PDF & 300 DPI HD PNG)
```bash
python build_academy_cv.py
```

### 3. Verify Constraints & Reproducibility
```bash
# Verify exactly 1 page
python3 -c 'from pypdf import PdfReader; pages = len(PdfReader("cv-pavel-cherkashin-academy.pdf").pages); assert pages == 1, f"Expected 1 page, got {pages}"; print("PDF page count: PASS (1 page)")'

# Verify programmatic layout, zero collisions, and page boundary containment
python3 -c 'from build_academy_cv import verify_layout_and_collisions; rep = verify_layout_and_collisions("cv-pavel-cherkashin-academy.pdf"); assert rep["text_overlap_count"] == 0 and rep["out_of_bounds_count"] == 0, f"Collisions: {rep}"; print(f"Layout & collision check: PASS ({rep})")'

# Verify 300 DPI metadata and geometry (2550 x 3300)
python3 -c 'from PIL import Image; im = Image.open("cv-pavel-cherkashin-academy-hd.png"); assert im.size == (2550, 3300), f"Bad size {im.size}"; dpi = round(im.info.get("dpi", (0, 0))[0]); assert dpi == 300, f"Bad dpi {dpi}"; print(f"PNG resolution: PASS ({im.size}, {dpi} DPI)")'

# Verify byte-for-byte reproducible build against committed artifacts
python3 build_academy_cv.py /tmp/rebuilt_academy.pdf /tmp/rebuilt_academy.png
cmp cv-pavel-cherkashin-academy.pdf /tmp/rebuilt_academy.pdf && echo "PDF deterministic byte match: PASS"
cmp cv-pavel-cherkashin-academy-hd.png /tmp/rebuilt_academy.png && echo "PNG deterministic byte match: PASS"

# Verify cryptographic manifest integrity
sha256sum -c evidence/MANIFEST.sha256
```

## Paradigm: 6-Month Partner Ops Automation Arc
Built around Pavel Cherkashin's core operator-educator philosophy:
> *"Empowering grassroots builders, educational institutions, and civil society worldwide through accessible frontier AI. Scaling OpenAI Academy partner programs—from high-energy Academy Jams to train-the-trainer Community Trainer cohorts—while building automated operational infrastructure (intake pipelines, API credit allocation, impact telemetry, and curriculum distribution) that multiplies partner impact without administrative bloat."*
