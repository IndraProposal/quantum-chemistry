# MIN-207: Copperlane (Veronica Garg / Athan Zhang / Brianna Lin) Application Package

This repository contains the complete tailored executive application package, strategy brief, and verified 1-page CV for **Copperlane** (YC W26), prepared under the **Mindrock Agent Constitution (AGENTS.md)**.

## Quick Links
- **One-Tap Application Card:** [docs/ONE_TAP_APPLICATION_CARD.md](docs/ONE_TAP_APPLICATION_CARD.md)
- **Tailored 1-Page CV (Markdown):** [docs/TAILORED_CV_COPPERLANE.md](docs/TAILORED_CV_COPPERLANE.md)
- **Direct Outreach Copy (X DM & Email):** [docs/DM_OUTREACH_VERONICA_GARG.md](docs/DM_OUTREACH_VERONICA_GARG.md)
- **Strategic Company Brief:** [docs/COPPERLANE_STRATEGY_BRIEF.md](docs/COPPERLANE_STRATEGY_BRIEF.md)
- **Builder Script:** [build_copper_cv.py](build_copper_cv.py)
- **Verified 1-Page PDF:** [cv-pavel-cherkashin-copper.pdf](cv-pavel-cherkashin-copper.pdf)
- **High-Resolution 300 DPI PNG:** [cv-pavel-cherkashin-copper-hd.png](cv-pavel-cherkashin-copper-hd.png)
- **Cryptographic Manifest:** [evidence/MANIFEST.sha256](evidence/MANIFEST.sha256)
- **Machine-Readable Evidence:** [evidence/EVIDENCE.json](evidence/EVIDENCE.json)

## Build & Verification Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Build CV (PDF & 300 DPI HD PNG)
```bash
python build_copper_cv.py
```

### 3. Verify Constraints
```bash
# Verify exactly 1 page
python -c 'from pypdf import PdfReader; pages = len(PdfReader("cv-pavel-cherkashin-copper.pdf").pages); assert pages == 1, f"Expected 1 page, got {pages}"; print("PDF page count: PASS (1 page)")'

# Verify 300 DPI metadata and geometry (2550 x 3300)
python -c 'from PIL import Image; im = Image.open("cv-pavel-cherkashin-copper-hd.png"); assert im.size == (2550, 3300), f"Bad size {im.size}"; dpi = round(im.info.get("dpi", (0, 0))[0]); assert dpi == 300, f"Bad dpi {dpi}"; print(f"PNG resolution: PASS ({im.size}, {dpi} DPI)")'

# Verify cryptographic manifest integrity
sha256sum -c evidence/MANIFEST.sha256
```

## Paradigm: 6-Month Automation Arc
Built around Pavel Cherkashin's core philosophy:
> *"I don’t come to warm a chair. I build autonomous operational infrastructure, eliminate friction, and automate myself out of repetitive execution within 6 months—leaving behind self-driving verification systems, codified playbooks, and high-uptime underwriting pipelines."*
