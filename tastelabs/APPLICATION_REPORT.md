# Application Dossier & Evaluation Report: Taste Labs — AI Engineer, RL & Evals

**Linear Ticket:** [MIN-235](https://linear.app/mindrock/issue/MIN-235/taste-labs-ai-engineer-rl-and-evals-ashby-sf-on-site)  
**Run ID:** `run-7378dd1efc00`  
**Builder Slot:** `agy@wolfram`  
**Target Entity:** Taste Labs ([tastelabs.com](https://tastelabs.com))  
**Founder & Hiring Post:** Thais Castello Branco ([@thaiscbranco_](https://x.com/thaiscbranco_))  
**Role:** AI Engineer, RL & Evals (Technical Staff)  
**Location:** San Francisco, CA (SF On-Site, Full-Time)  
**Compensation:** $175,000 – $275,000 base + equity (up to $300,000 exceptional). JD verified live 2026-10-26.  
**Target Intake Route:** Ashby Application Form (`tastelabs.com/careers`)  
**Application Fields:** Resume PDF + LinkedIn Profile + 2 Free-Text Questions (Interest & Fit) + U.S. Work Authorization. *(No cover-letter field)*  
**Operational Status:** `DELIVERED` (Staged and verified locally; NOT sent autonomously. Tap-gated for Principal Pavel Cherkashin).  

---

## 1. Company, Product & Evaluation Context

### A. About Taste Labs
Taste Labs is a San Francisco-based AI research and infrastructure startup founded in late 2025 by Thais Castello Branco, backed by an $18.5M seed round co-led by Amplify Partners and CRV. The company's mission is to **end "AI slop"** and build the foundational data, evaluation, and infrastructure layer that gives AI models and agent runtimes genuine "taste."

### B. The Subjective Domain Problem & The Taste Layer
While frontier AI models excel in verifiable, objective domains (such as competitive mathematics, code compilation, and chess) where automated compilers and unit tests provide crisp ground truth, they struggle severely in subjective domains like visual design, editorial style, layout balance, brand tone, and aesthetic harmony.
Without granular measurement, generative models collapse to the mean—producing bland, mediocre, synthetic content ("AI slop"). Taste Labs approaches this not as an intractable model limitation, but as a **measurement and evaluation problem**. By decomposing qualitative aesthetics into structured, codifiable grading rubrics and held-out verifier environments, Taste Labs makes taste tractable for reinforcement learning.

### C. Ecosystem Role
Taste Labs operates across two vital vectors:
1. **Frontier AI Labs:** Supplying specialized post-training data, grading rubrics, and RL evaluation environments so foundational models learn aesthetic boundaries.
2. **Agent-Layer Companies:** Providing runtime context layers, prompt scaffolding, and taste verification tools so application-layer agents generate distinctive, on-brand outputs.

---

## 2. Candidate Positioning & Strategic Fit

### A. The Core Seat
Pavel Cherkashin targets the **AI Engineer, RL & Evals** seat, focusing on:
1. **Task Design for Taste:** Structuring ambiguous, subjective design and creative challenges into granular, multi-stage evaluation tasks.
2. **Grading Methods & Rubrics:** Decomposing qualitative aesthetic judgment into deterministic, reproducible rubrics, programmatic layout assertion engines, and multi-model LLM-as-judge scoring.
3. **Agent Harnesses & Context Layers:** Architecting high-concurrency agent runtimes (`fleetd` in Rust), dynamic context injection, token budgeting, and Model Context Protocol (MCP) tool integrations.
4. **Deterministic Backend Verification:** Building zero-trust verification pipelines, isolated execution worktrees, tamper-evident cryptographic manifests, and automated regression test harnesses.

### B. Transparent Technical Gaps (Honest Alignment)
* **Declared Growth Edge: Large-Scale Distributed RL Cluster Infra:** Low-level distributed RL infrastructure (multi-node GPU cluster topologies, Megatron-LM/DeepSpeed training loops, NCCL collective communications, and custom CUDA/Triton kernels) are a growth edge, not historical depth.
* **Strategic Complementarity:** By taking total ownership of evals rigor, task design for taste, grading rubrics, agent context layers, and deterministic backend verification, the candidate enables core RL infra researchers to focus 100% of their energy on training loops and cluster optimization.

---

## 3. Application Artifacts & Verification Table

All artifacts have been compiled, programmatically verified, and synchronized across both the canonical git repository and the Goal-4 workspace mirrors:

| Artifact Name | Canonical Repo Path | Workspace Mirror Path | Technical Verification & Specification |
|---|---|---|---|
| **1-Page CV (PDF)** | `tastelabs/cv-pavel-cherkashin-tastelabs.pdf` | `workspace/goals/goal-4/files/tastelabs/cv-pavel-cherkashin-tastelabs.pdf` | Programmatically verified: 1 page Letter (`612x792 pt`), 0 text collisions, 0 out-of-bounds elements, Unicode NotoSans font suite with full Cyrillic support, deterministic ReportLab build (`rl_config.invariant=1`). Verified SHA-256: `3284a3da879d8b472c8387c282395cc7b5f8359f74a1e31e84807e45a44396d2`. |
| **High-Res PNG (300 DPI)** | `tastelabs/cv-pavel-cherkashin-tastelabs-hd.png` | `workspace/goals/goal-4/files/tastelabs/cv-pavel-cherkashin-tastelabs-hd.png` | `2550x3300 px`, explicit 300 DPI metadata (`(299.9994, 299.9994)`). Full Cyrillic typography rendered without tofu. Ready for direct attachment or preview. |
| **Standard PNG Alias** | `tastelabs/cv-pavel-cherkashin-tastelabs.png` | `workspace/goals/goal-4/files/tastelabs/cv-pavel-cherkashin-tastelabs.png` | Direct alias of high-resolution card for universal platform preview. |
| **CV Builder Script** | `tastelabs/build_tastelabs_cv.py` | `workspace/goals/goal-4/files/tastelabs/build_tastelabs_cv.py` | Python 3 script with embedded Unicode fonts, InvariantCanvas, programmatic collision engine, glyph verification, and automatic dual-tree mirror synchronization. |
| **Ashby Form Answers** | `tastelabs/ashby-answers.md` | `workspace/goals/goal-4/files/tastelabs/ashby-answers.md` | Complete free-text answers for Question 1 (Interest / Ending AI Slop) and Question 2 (Fit / Strengths & Honest Gaps). |
| **One-Tap Application Card** | `tastelabs/ONE_TAP_APPLICATION_CARD.md` | `workspace/goals/goal-4/files/tastelabs/ONE_TAP_APPLICATION_CARD.md` | Executive 1-tap summary card with verified role details and copy-paste prompts. |
| **Claim Ledger** | `tastelabs/evidence/CLAIM_LEDGER.md` | `workspace/goals/goal-4/files/tastelabs/evidence/CLAIM_LEDGER.md` | Comprehensive mapping of all CV claims to verified primary sources (MSU degree, Siebel Systems, Sputnik Labs, INTUIT textbook ISBN) with exact public catalog and archive links. |
| **Machine Evidence** | `tastelabs/evidence/EVIDENCE.json` | `workspace/goals/goal-4/files/tastelabs/evidence/EVIDENCE.json` | Machine-readable manifest tracking ticket, git branch, acceptance assertions, compensation details, limitations, and `DELIVERED` status. |
| **SHA-256 Manifest** | `tastelabs/evidence/MANIFEST.sha256` | `workspace/goals/goal-4/files/tastelabs/evidence/MANIFEST.sha256` | Tamper-evident checksums of all tracked canonical source files, font files, lockfile, and reproducible PDF. |
| **Transitive Lockfile** | `tastelabs/requirements.lock` | `workspace/goals/goal-4/files/tastelabs/requirements.lock` | Pinned lockfile enforcing Python runtime (Python >= 3.12, < 3.14) and platform constraints. |
| **Direct Dependencies** | `tastelabs/requirements.txt` | `workspace/goals/goal-4/files/tastelabs/requirements.txt` | Direct pinned dependencies (`reportlab==5.1.0`, `pymupdf==2.0`, `pypdf==6.21.2`, `pillow==12.3.0`). |
| **Verification Suite** | `tastelabs/test_cv_harness.py` | `workspace/goals/goal-4/files/tastelabs/test_cv_harness.py` | 8-stage automated verification suite testing runtime, imports, layout, glyph integrity & anti-tofu, digest, PNG specs, manifest, and dual-tree parity. |

---

## 4. Verification Check Details & Determinism Scope

1. **Single-Page Constraint:** Programmatic inspection via PyMuPDF and pypdf confirms `page_count == 1`.
2. **Zero Layout Collisions:** Bounding-box intersection scan confirms `text_overlap_count == 0` across all 14 distinct text blocks.
3. **Zero Out-of-Bounds Text:** Every element is strictly contained within printable dimensions (`out_of_bounds_count == 0`).
4. **Deterministic PDF Scope:** Recompiling with `build_tastelabs_cv.py` produces the identical SHA-256 digest (`3284a3da879d8b472c8387c282395cc7b5f8359f74a1e31e84807e45a44396d2`) under CPython 3.12 on macOS Darwin arm64.
5. **Unicode Glyph Integrity & Anti-Tofu Verification:** Complete Unicode coverage via embedded NotoSans fonts. Cyrillic title *(Стратегия управления взаимоотношениями с клиентами (CRM))* renders flawlessly with zero missing glyphs, 0 replacement characters (`\ufffd`), and 0 tofu blocks.
6. **Image Geometry & DPI Metadata:** Pillow inspection confirms geometry `(2550, 3300)` px and 300 DPI metadata `(299.9994, 299.9994)`.
7. **Dual-Tree Mirror Parity:** `diff -rq tastelabs workspace/goals/goal-4/files/tastelabs` yields zero discrepancies across all files and fonts.
7. **Factual Grounding & Claim Ledger:** All biographical claims strictly map to confirmed primary sources with public links:
   - Undergraduate Degree: MSU 1995 B.S. in Computer Science in Global Ecology (`msu.ru`); IIASA research fellowship (`iiasa.ac.at`).
   - Published Textbook: INTUIT / BINOM, Moscow, 2007, 384 pp., ISBN 978-5-94774-643-3, cataloged in Russian State Library (RSL ID `01003185368`).
   - Enterprise Leadership: Sputnik Labs (CNews M&A archive: acquired by Technoserv in 2008), Siebel Systems (Country Manager, Russia & CIS), Microsoft Russia.
8. **Transitive Dependency Pinning:** Full `requirements.lock` generated and validated across clean virtual environments.

---

## 5. Operational Status & Governance Boundaries

* **Tap-Gate Active:** In accordance with Sections 4 and 5 of the Mindrock Agent Constitution (`AGENTS.md`), autonomous agents do not initiate unauthorized outbound communication. Staged package is delivered locally and awaits Principal Pavel Cherkashin's manual 1-tap review and transmission via Ashby.
* **Current Operational Status:** `DELIVERED` (Ready for submission).
* **Linear Status:** In accordance with constitutional rules, builder agent `agy` does not mark Linear issue MIN-235 `Done`. The ticket is transitioned to `In Review` with label `Role: QA-Needed`, and handed off to `@codex` for independent verification.
