# OpenAI — Global Head of Education GTM (MIN-211)

**Application Package & Deterministic Verification Repository**

- **Role:** Global Head of Education GTM
- **Company:** OpenAI (San Francisco, CA)
- **Posting URL:** [https://openai.com/careers/global-head-of-education-gtm-san-francisco/](https://openai.com/careers/global-head-of-education-gtm-san-francisco/)
- **Linear Issue:** `MIN-211` (`OpenAI — Global Head of Education GTM (CV ready, awaiting tap)`)
- **Assigned Git Branch:** `minutta/min-211-openai-global-head-of-education-gtm-cv-ready-awaiting-tap`
- **Base Commit:** `02d0f4a25dfe8054bea10ffd0a61c188a96b7387` (`origin/main`)
- **Candidate:** Pavel Cherkashin (`pavel@mindrock.capital`)
- **Key Positioning Angle:** Operator + Investor + Teacher; Education GTM system & team; Adobe 1.5M+ licenses landmark deal blueprint.
- **Application Status:** Confirmed **SUBMITTED** by Principal Pavel Cherkashin on 2026-10-24 (22:01 PDT). Submission 4 of 5 in the OpenAI strategic set.

---

## 📁 Package Structure

```
.
├── README.md                                     # This document
├── build_edgtm_cv.py                             # Deterministic ReportLab PDF + 300 DPI PNG generator
├── cv-pavel-cherkashin-edgtm.pdf                 # Exact 1-page CV PDF (byte-for-byte verified)
├── cv-pavel-cherkashin-edgtm-hd.png              # 300 DPI High-Definition PNG render (2550x3300 px)
├── docs/
│   ├── APPLICATION_COVER_NOTE.md                 # Full cover letter and outreach copy (Adobe deal focus)
│   ├── ONE_TAP_APPLICATION_CARD.md               # Summary action card for Principal Pavel Cherkashin
│   ├── OPENAI_EDUCATION_GTM_STRATEGY_BRIEF.md    # In-depth Education GTM strategy and roadmap
│   └── TAILORED_CV_OPENAI_EDUCATION_GTM.md       # Markdown version of the tailored CV
├── evidence/
│   ├── EVIDENCE.json                             # Machine-readable verification & audit metadata
│   └── MANIFEST.sha256                           # Cryptographic checksums of all deliverables
├── pyproject.toml                                # Project metadata and pinned dependencies
└── requirements.txt                              # Exact pinned render dependencies
```

---

## ⚙️ Building & Verification Instructions

### 1. Pinned Dependencies
To reproduce the PDF and PNG builds across clean environments:
```bash
pip install -r requirements.txt
```
Pinned versions: `reportlab==5.1.0`, `PyMuPDF==2.0`, `pypdf==6.21.2`, `Pillow==12.3.0`.

### 2. Generate PDF and PNG
```bash
python3 build_edgtm_cv.py /tmp/min211-rebuilt.pdf /tmp/min211-rebuilt.png
```

### 3. Verification Suite

#### A. PDF Page Count & Layout Constraints
```bash
python3 -c 'from pypdf import PdfReader; pages = len(PdfReader("cv-pavel-cherkashin-edgtm.pdf").pages); assert pages == 1, f"Expected 1 page, got {pages}"; print("PDF page count: PASS (1 page)")'
python3 -c 'from build_edgtm_cv import verify_layout_and_collisions; rep = verify_layout_and_collisions("cv-pavel-cherkashin-edgtm.pdf"); assert rep["text_overlap_count"] == 0 and rep["out_of_bounds_count"] == 0, f"Collisions: {rep}"; print(f"Layout & collision check: PASS ({rep})")'
```

#### B. Byte-for-Byte Deterministic PDF Match
```bash
cmp cv-pavel-cherkashin-edgtm.pdf /tmp/min211-rebuilt.pdf && echo "PDF deterministic byte match: PASS"
```
PDF SHA-256: `cd6f20f9c45a59acd6b2451647f272bc2ca8a92d9e151f4d5014fd2064c65131`.

#### C. High-Definition 300 DPI PNG Resolution & Geometry
```bash
python3 -c 'from PIL import Image; im = Image.open("cv-pavel-cherkashin-edgtm-hd.png"); assert im.size == (2550, 3300), f"Bad size {im.size}"; dpi = round(im.info.get("dpi", (0, 0))[0]); assert dpi == 300, f"Bad dpi {dpi}"; print(f"PNG resolution: PASS ({im.size}, {dpi} DPI)")'
```

#### D. Pixel-Identical PNG Verification (Zero Visual or Raster Drift)
*Note on PNG compression across platforms:* PNG compression stream bytes can differ at the zlib Huffman layer across operating systems (Darwin libz generates file SHA-256 `d1371faaa55fec281ec83e8e4cf74b0fc2eeb55645653feec78be6d8fdf1b9e5`; Linux zlib generates `517a31244e82df422998393e1b711bc3289dc62a2faeb25ff282367dca467c64`). However, decoded pixel rasters are 100% deterministic across all platforms.
```bash
python3 -c 'import hashlib; from PIL import Image, ImageChops; im1 = Image.open("cv-pavel-cherkashin-edgtm-hd.png"); im2 = Image.open("/tmp/min211-rebuilt.png"); diff = ImageChops.difference(im1, im2).getbbox(); assert diff is None, f"Visual drift detected: {diff}"; h1 = hashlib.sha256(im1.convert("RGB").tobytes()).hexdigest(); h2 = hashlib.sha256(im2.convert("RGB").tobytes()).hexdigest(); assert h1 == h2 == "75381c93cc8f2ebdef15f4575411aaea5d53e13e7b9bb4b73fec943af8201a1d", f"Hash mismatch: {h1} vs {h2}"; print("PNG pixel-identical match: PASS (RGB pixel SHA-256: 75381c93...)")'
```

#### E. Common Git History (Merge Base with `main` / `work`)
```bash
git merge-base origin/main HEAD
# Returns: 02d0f4a25dfe8054bea10ffd0a61c188a96b7387
```

#### F. Repository Location & Goal-4 Path Verification
From repository root:
```bash
test -d workspace/goals/goal-4/files/openai-education-gtm && echo "Goal-4 package directory: PASS"
```

#### G. Cryptographic Manifest Verification
```bash
sha256sum --check evidence/MANIFEST.sha256
```
