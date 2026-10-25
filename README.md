# MIN-208: OpenAI — Community Communications Lead Application Package

This repository contains the complete tailored executive application package, strategy brief, and verified 1-page CV for **OpenAI Community Communications Lead** (Product & Research Communications team, in collaboration with Culture & Community Engagement), prepared under the **Mindrock Agent Constitution (AGENTS.md)**.

**Application Status:** Confirmed **SUBMITTED** by Principal Pavel Cherkashin on 2026-10-24 (21:41 PDT) via Ashby (Submission 1 of 5 in the OpenAI portfolio). This repository archives and proves the canonical application package, verified layout, and reproducible build pipeline.

## Quick Links
- **Application Record & Submission Card:** [docs/ONE_TAP_APPLICATION_CARD.md](docs/ONE_TAP_APPLICATION_CARD.md)
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
To install the dependencies for building and verifying both PDF and PNG artifacts:
```bash
pip install -r requirements.txt
```

### 2. Build CV (PDF & 300 DPI HD PNG)
```bash
python build_oai_cv.py
```

### 3. Verify Constraints & Reproducibility

```bash
# 1. Verify exactly 1 page
python3 -c 'from pypdf import PdfReader; pages = len(PdfReader("cv-pavel-cherkashin-oai.pdf").pages); assert pages == 1, f"Expected 1 page, got {pages}"; print("PDF page count: PASS (1 page)")'

# 2. Verify programmatic layout, zero collisions, and page boundary containment
python3 -c 'from build_oai_cv import verify_layout_and_collisions; rep = verify_layout_and_collisions("cv-pavel-cherkashin-oai.pdf"); assert rep["text_overlap_count"] == 0 and rep["out_of_bounds_count"] == 0, f"Collisions: {rep}"; print(f"Layout & collision check: PASS ({rep})")'

# 3. Verify 300 DPI metadata and geometry (2550 x 3300)
python3 -c 'from PIL import Image; im = Image.open("cv-pavel-cherkashin-oai-hd.png"); assert im.size == (2550, 3300), f"Bad size {im.size}"; dpi = round(im.info.get("dpi", (0, 0))[0]); assert dpi == 300, f"Bad dpi {dpi}"; print(f"PNG resolution: PASS ({im.size}, {dpi} DPI)")'

# 4. Verify byte-for-byte reproducible PDF build against committed artifact
python3 build_oai_cv.py /tmp/rebuilt.pdf /tmp/rebuilt.png
cmp cv-pavel-cherkashin-oai.pdf /tmp/rebuilt.pdf && echo "PDF deterministic byte match: PASS"

# 5. Verify pixel-identical PNG equivalence (zero visual or pixel drift)
# Note: PNG compression stream bytes can differ at the zlib Huffman layer (byte 69) across OS/zlib versions (e.g., macOS vs Linux),
# but the decoded pixel raster is 100% deterministic across all platforms.
python3 -c 'import hashlib; from PIL import Image, ImageChops; im1 = Image.open("cv-pavel-cherkashin-oai-hd.png"); im2 = Image.open("/tmp/rebuilt.png"); diff = ImageChops.difference(im1, im2).getbbox(); assert diff is None, f"Visual drift detected: {diff}"; h1 = hashlib.sha256(im1.convert("RGB").tobytes()).hexdigest(); h2 = hashlib.sha256(im2.convert("RGB").tobytes()).hexdigest(); assert h1 == h2 == "c6ecb2b122d38d116e6ca0e7efc53449b9b55f29aca3dac0db37a534d8e91e2e", f"Hash mismatch: {h1} vs {h2}"; print("PNG pixel-identical match: PASS (SHA-256: c6ecb2b1...)")'

# 6. Verify cryptographic manifest integrity
sha256sum -c evidence/MANIFEST.sha256
```

## Paradigm: 6-Month Comms Automation Arc
Built around Pavel Cherkashin's core operator-storyteller philosophy:
> *"Automating communications operations—story sourcing, editorial cadence, distribution reach, and sentiment telemetry—while fiercely preserving human judgment, cultural taste, trust, and authentic community voices. Bringing OpenAI products closer to everyday communities by propelling AI out of tech subcultures into mainstream culture (sports, music, design, food, fandoms) on a disciplined 6-month arc."*
