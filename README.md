# MIN-207: Copperlane (Veronica Garg / Athan Zhang / Brianna Lin) Application Package

This repository contains the complete tailored executive application package, strategy brief, and verified 1-page CV for **Copperlane** (YC W26), prepared under the **Mindrock Agent Constitution (AGENTS.md)**.

## Quick Links
- **One-Tap Application Card:** [docs/ONE_TAP_APPLICATION_CARD.md](docs/ONE_TAP_APPLICATION_CARD.md)
- **Tailored 1-Page CV (Markdown):** [docs/TAILORED_CV_COPPERLANE.md](docs/TAILORED_CV_COPPERLANE.md)
- **Direct Outreach Copy (X DM & Email):** [docs/DM_OUTREACH_VERONICA_GARG.md](docs/DM_OUTREACH_VERONICA_GARG.md)
- **Strategic Company Brief:** [docs/COPPERLANE_STRATEGY_BRIEF.md](docs/COPPERLANE_STRATEGY_BRIEF.md)
- **Builder Script:** [build_copper_cv.py](build_copper_cv.py)
- **Atomic Evidence Refresh Script:** [refresh_evidence.py](refresh_evidence.py)
- **Verified 1-Page PDF:** [cv-pavel-cherkashin-copper.pdf](cv-pavel-cherkashin-copper.pdf)
- **High-Resolution 300 DPI PNG:** [cv-pavel-cherkashin-copper-hd.png](cv-pavel-cherkashin-copper-hd.png)
- **Cryptographic Manifest:** [evidence/MANIFEST.sha256](evidence/MANIFEST.sha256)
- **Machine-Readable Evidence:** [evidence/EVIDENCE.json](evidence/EVIDENCE.json)

## Verification & Clean-Room Workflows

### Dual-Artifact Reproducibility Model
This package follows a transparent dual-artifact model honoring the cross-platform realities of document generation and rasterization:
1. **Deterministic 1-Page PDF (`cv-pavel-cherkashin-copper.pdf`):**  
   Compiled from Python/ReportLab source code (`build_copper_cv.py`) with invariant timestamps (`rl_config.invariant=1`, `SOURCE_DATE_EPOCH=946684800`). Rebuilding from source generates the exact same bit-for-bit SHA-256 hash (`f1531ebe9bd4237a1a0141f637120a74e6d36a1b1f06e37aff72225be13e7363`) across all platforms (Darwin arm64, Linux x86_64).
2. **Canonical Platform-Rendered HD PNG (`cv-pavel-cherkashin-copper-hd.png`):**  
   The committed 300 DPI high-definition PNG (2550×3300, ~848 KB, SHA-256 `a2b29932f4a775fb79b5d856235cbf4a25f9eb879c69bd771dd4051f75667416`) is the canonical visual deliverable. Cross-platform PDF-to-bitmap rasterizers (PyMuPDF / FreeType / font anti-aliasing backends) exhibit minor subpixel hinting variations across operating systems (e.g. Darwin vs Linux FreeType producing ~848 KB vs ~868 KB). Therefore, binary byte-for-byte identity across heterogeneous OS environments is not claimed for rendered PNGs "from source".  
   Instead, `build_copper_cv.py` validates that the canonical PNG strictly conforms to geometry (`2550×3300`) and metadata (`300 DPI`) constraints and preserves it, preventing working-tree churn across heterogeneous builder and QA nodes.

### Workflow A: Zero-Touch Verification (Pre-Built Deliverables)
In a fresh repository clone, verify the committed package against the cryptographic manifest:
```bash
sha256sum -c evidence/MANIFEST.sha256
```

### Workflow B: Deterministic Rebuild & Preservation Cycle
To rebuild the PDF from source, validate the canonical PNG, and verify working tree cleanliness:

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Deterministic Build (`build`)
Recompiles the PDF deterministically from source and validates/preserves the canonical HD PNG deliverable:
```bash
python build_copper_cv.py
```
*(Note: `build_copper_cv.py` automatically runs atomic evidence refresh upon completion; working tree remains clean).*

#### 3. Verification (`verify`)
```bash
# Verify exactly 1 page
python -c 'from pypdf import PdfReader; pages = len(PdfReader("cv-pavel-cherkashin-copper.pdf").pages); assert pages == 1, f"Expected 1 page, got {pages}"; print("PDF page count: PASS (1 page)")'

# Verify 300 DPI metadata and geometry (2550 x 3300)
python -c 'from PIL import Image; im = Image.open("cv-pavel-cherkashin-copper-hd.png"); assert im.size == (2550, 3300), f"Bad size {im.size}"; dpi = round(im.info.get("dpi", (0, 0))[0]); assert dpi == 300, f"Bad dpi {dpi}"; print(f"PNG resolution: PASS ({im.size}, {dpi} DPI)")'

# Verify cryptographic manifest integrity (12/12 files OK)
sha256sum -c evidence/MANIFEST.sha256
```

### Workflow C: Host Native PNG Re-rendering (`--force` or absent PNG)
To verify that the builder script can independently render a fresh HD PNG from the compiled PDF:
```bash
python build_copper_cv.py --force
```
The host rasterizer generates a new 300 DPI PNG (`2550×3300`). Note that running `refresh_evidence.py` after a force re-render will update `evidence/MANIFEST.sha256` and `evidence/EVIDENCE.json` to reflect the host's specific rasterizer byte stream and file size.

## Paradigm: 6-Month Automation Arc
Built around Pavel Cherkashin's core philosophy:
> *"I don’t come to warm a chair. I build autonomous operational infrastructure, eliminate friction, and automate myself out of repetitive execution within 6 months—leaving behind self-driving verification systems, codified playbooks, and high-uptime underwriting pipelines."*
