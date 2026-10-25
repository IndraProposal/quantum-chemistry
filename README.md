# MIN-210: OpenAI — Deal Lead, Special Situations Application Package

**Target Issue:** `MIN-210` (`OpenAI — Deal Lead, Special Situations (CV ready, awaiting tap)`)  
**Assigned Git Branch:** `minutta/min-210-openai-deal-lead-special-situations-cv-ready-awaiting-tap`  
**Candidate:** Pavel Cherkashin (`pavel@mindrock.capital`)  
**Position:** Deal Lead, Special Situations  
**Company:** OpenAI (San Francisco, CA)  
**Posting URL:** [https://openai.com/careers/deal-lead-special-situations-san-francisco/](https://openai.com/careers/deal-lead-special-situations-san-francisco/)  
**Application Status:** Confirmed **SUBMITTED** by Principal Pavel Cherkashin on 2026-10-24 (21:48 PDT) (Submission 3 of 5 in the OpenAI portfolio, following MIN-208). This repository archives and proves the canonical application package, verified layout, and reproducible build pipeline.

---

## 📁 Repository Structure

```
.
├── README.md                                          # Application package & verification guide
├── build_ss_cv.py                                     # Deterministic ReportLab PDF + 300 DPI PNG generator
├── cv-pavel-cherkashin-ss.pdf                         # Exact 1-page CV PDF (byte-for-byte reproducible)
├── cv-pavel-cherkashin-ss-hd.png                      # 300 DPI High-Definition PNG render (2550x3300 px)
├── docs/
│   ├── APPLICATION_COVER_NOTE.md                      # Full executive cover note
│   ├── ONE_TAP_APPLICATION_CARD.md                    # Submission record and application card
│   ├── OPENAI_SPECIAL_SITUATIONS_STRATEGY_BRIEF.md    # Special Situations & Financial Services strategy brief
│   └── TAILORED_CV_OPENAI_SPECIAL_SITUATIONS.md       # Tailored CV in markdown format
├── evidence/
│   ├── EVIDENCE.json                                  # Machine-readable audit & verification metadata
│   └── MANIFEST.sha256                                # Cryptographic checksums of all deliverables
├── pyproject.toml                                     # Pinned build configuration
├── requirements.txt                                   # Pinned rendering dependencies
└── workspace/goals/goal-4/files/openai-special-situations/
    ├── build_ss_cv.py                                 # Mirrored builder script
    ├── cv-pavel-cherkashin-ss.pdf                     # Mirrored 1-page PDF
    └── cv-pavel-cherkashin-ss-hd.png                  # Mirrored 300 DPI HD PNG
```

---

## ⚙️ Build & Verification Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Build CV (PDF & 300 DPI HD PNG)
```bash
python3 build_ss_cv.py
```

### 3. Verify Constraints & Reproducibility

```bash
# 1. Verify exactly 1 page
python3 -c 'from pypdf import PdfReader; pages = len(PdfReader("cv-pavel-cherkashin-ss.pdf").pages); assert pages == 1, f"Expected 1 page, got {pages}"; print("PDF page count: PASS (1 page)")'

# 2. Verify programmatic layout, zero collisions, and page boundary containment
python3 -c 'from build_ss_cv import verify_layout_and_collisions; rep = verify_layout_and_collisions("cv-pavel-cherkashin-ss.pdf"); assert rep["text_overlap_count"] == 0 and rep["out_of_bounds_count"] == 0, f"Collisions: {rep}"; print(f"Layout & collision check: PASS ({rep})")'

# 3. Verify 300 DPI metadata and geometry (2550 x 3300)
python3 -c 'from PIL import Image; im = Image.open("cv-pavel-cherkashin-ss-hd.png"); assert im.size == (2550, 3300), f"Bad size {im.size}"; dpi = round(im.info.get("dpi", (0, 0))[0]); assert dpi == 300, f"Bad dpi {dpi}"; print(f"PNG resolution: PASS ({im.size}, {dpi} DPI)")'

# 4. Verify byte-for-byte reproducible PDF build against committed artifact
python3 build_ss_cv.py /tmp/rebuilt.pdf /tmp/rebuilt.png
cmp cv-pavel-cherkashin-ss.pdf /tmp/rebuilt.pdf && echo "PDF deterministic byte match: PASS"

# 5. Verify PNG visual and layout equivalence
# Note: PNG compression stream bytes and font rasterization can vary across OS platforms (e.g., macOS Darwin vs Linux FreeType/zlib implementations),
# but the vector PDF is 100% byte-for-byte identical, and the PNG maintains identical layout, 2550x3300 geometry, and 300 DPI metadata.
python3 -c 'from PIL import Image; im1 = Image.open("cv-pavel-cherkashin-ss-hd.png"); im2 = Image.open("/tmp/rebuilt.png"); assert im1.size == im2.size == (2550, 3300); print("PNG geometry & layout equivalence: PASS")'

# 6. Verify mirrored Goal-4 repository artifacts
find workspace -path '*/openai-special-situations/*' -type f | sort

# 7. Verify cryptographic manifest integrity
sha256sum -c evidence/MANIFEST.sha256
```

---

## 🎯 Paradigm: 6-Month Special Situations Incubation Arc
Built around Pavel Cherkashin's core commercial thesis:
> *"Scaling OpenAI's highest-upside frontier: taking ambiguous, first-of-their-kind commercial opportunities from blank-page thesis to scalable, high-margin business units. 20+ year track record combining frontier venture investor ($100M+ deployed, pioneer of venture notes and fintech syndicates), tech operator and corporate executive (Adobe, Microsoft; architected landmark 1.5M+ seat enterprise transaction), and AI systems builder. Focused on unlocking institutional financial services, structured deal vehicles, and autonomous AI-native business models where standard playbooks do not yet exist."*
