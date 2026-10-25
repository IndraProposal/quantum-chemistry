# OpenAI — Deal Lead, Special Situations (MIN-210)

**Application Package & Deterministic Verification Repository**

- **Role:** Deal Lead, Special Situations
- **Company:** OpenAI (San Francisco, CA)
- **Posting URL:** [https://openai.com/careers/deal-lead-special-situations-san-francisco/](https://openai.com/careers/deal-lead-special-situations-san-francisco/)
- **Linear Issue:** `MIN-210` (`OpenAI — Deal Lead, Special Situations (CV ready, awaiting tap)`)
- **Assigned Git Branch:** `minutta/min-210-openai-deal-lead-special-situations-cv-ready-awaiting-tap`
- **Candidate:** Pavel Cherkashin (`pavel@mindrock.capital`)
- **Key Positioning Angle:** New businesses from thesis to launch; financial services first (venture notes, fintech angels); operator + investor.

---

## 📁 Repository Structure

```
.
├── README.md                                     # This document
├── build_ss_cv.py                                # Deterministic ReportLab PDF + 300 DPI PNG generator
├── cv-pavel-cherkashin-ss.pdf                    # Exact 1-page CV PDF (verified byte-for-byte)
├── cv-pavel-cherkashin-ss-hd.png                 # 300 DPI High-Definition PNG render (2550x3300 px)
├── docs/
│   ├── APPLICATION_COVER_NOTE.md                 # Full executive cover note
│   ├── ONE_TAP_APPLICATION_CARD.md               # Summary action card for Principal Pavel Cherkashin
│   ├── OPENAI_SPECIAL_SITUATIONS_STRATEGY_BRIEF.md # In-depth Special Situations & Financial Services strategy
│   └── TAILORED_CV_OPENAI_SPECIAL_SITUATIONS.md  # Markdown version of the tailored CV
├── evidence/
│   ├── EVIDENCE.json                             # Machine-readable verification & audit metadata
│   └── MANIFEST.sha256                           # Cryptographic checksums of all deliverables
├── pyproject.toml                                # Project metadata and pinned dependencies
└── requirements.txt                              # Exact pinned render dependencies
```

---

## ⚙️ Building & Verifying

To reproduce the exact byte-for-byte PDF and 300 DPI PNG:

```bash
python3 build_ss_cv.py
```

Verification includes:
1. Exact 1-page PDF constraint (`page_count == 1`).
2. Programmatic PyMuPDF text block boundary checks (`out_of_bounds == 0`).
3. Pairwise bounding box collision detection (`collisions == 0`).
4. High-definition 300 DPI PNG export (2550 x 3300 px).
