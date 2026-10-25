# Application Dossier & Evaluation Report: Hillclimb AI — Employee #5 (Evals & Environments for RSI)

**Linear Ticket:** [MIN-222](https://linear.app/mindrock/issue/MIN-222/hillclimb-ai-employee-5-evals-environments-for-rsi-x-hiring-thread)  
**Run ID:** `run-53d100ae2faa` (Reworked from `run-c4cef5195da8`)  
**Builder Slot:** `agy@wolfram`  
**Target Entity:** Hillclimb AI ([@hillclimbai](https://x.com/hillclimbai))  
**Founders:** Jun Park ([@jparkjmc](https://x.com/jparkjmc)) & Ibrakhim Ustelbay  
**Hiring Context:** X hiring thread (2026-10-25)  
**Role:** Employee #5 — Evals & Environments for RSI (Candidate Seat: Evals Research & Technical Systems Writing)  
**Location:** San Francisco, CA (In-Person SF)  
**Compensation:** $200,000 base salary + 2.0% equity + comprehensive benefits (negotiable based on lab/data experience)  
**Target Channel:** X Direct Message to Jun Park ([@jparkjmc](https://x.com/jparkjmc))  
**Contact Note:** `research@hillclimb.com` is verified as DeepRSI site research inquiry contact, not a confirmed candidate hiring intake route.  
**Dispatch Status:** `SENT` (Tap-Gate successfully passed & executed. Principal Pavel Cherkashin personally reviewed and transmitted the application via X DM to @jparkjmc on 2026-10-25 at ~06:39 PDT. Staged artifacts transmitted as delivered; currently awaiting reply).

---

## 1. Company, Product & Benchmark Context

### A. About Hillclimb AI
Hillclimb AI is an applied frontier AI research lab founded by Jun Park and Ibrakhim Ustelbay, backed by prominent researchers and investors including Jeff Dean and Paul Graham. The lab focuses on **Recursive Self-Improvement (RSI)**—building specialized reinforcement learning environments and proprietary research datasets to train AI models that can autonomously discover, optimize, and evaluate novel machine learning pipelines.

### B. DeepRSI Benchmark Context
Hillclimb recently launched **DeepRSI**, an empirical evaluation benchmark designed to test frontier autonomous agents on open-ended, long-horizon machine learning engineering:
* **48-Hour Open-Ended Horizon:** Instead of short code-completion or unit-test puzzles, agent harnesses operate across a continuous 48-hour window on real research tasks without internet access.
* **15 Real-World Research ML Tasks:** Encompasses deep learning training recipes, GPU kernel optimization (Triton/CUDA), estimator accuracy, hyperparameter exploration, and novel algorithm synthesis.
* **Held-Out Private Verifiers:** Evaluates agent submissions against private held-out test datasets to prevent synthetic benchmark memorization and reward hacking.
* **Bradley-Terry Elo Evaluation:** Pairs candidate model checkpoints and baseline architectures in comparative head-to-head match-ups to establish a continuous, dynamic Elo rating.

### C. The Core Problem Hillclimb Solves
The frontier bottleneck in RSI is not simply model weights; it is **evals and environments**—specifically turning messy, high-dimensional proprietary research runs into rigorous, reproducible benchmarks that frontier models cannot cheat.

---

## 2. Candidate Positioning: The Evals + Writing Seat

### A. The Core Seat
Pavel Cherkashin deliberately targets Employee #5 as the **Evals Research and Technical Systems Writing Lead**:
1. **Evaluation Harness Architecture:** Designing deterministic, multi-tier evaluation suites with programmatic boundary assertions, automated cross-model validation gates, and private held-out test harnesses.
2. **Turning Research Data into Standardized Benchmarks:** Ingesting raw experimental outputs, failed training runs, and agent telemetry into clean, reproducible benchmark tasks.
3. **High-Signal Technical Writing:** Authoring comprehensive benchmark methodologies, anti-gaming disclosures, public documentation, and research notes (leveraging published textbook authorship and systems documentation background).

### B. Transparent Technical Gaps (Honest Alignment)
* **Declared Gap 1: RL Simulation Environments:** Low-level reinforcement learning environment mechanics, physics simulators, and complex game/wrapper engines are **NOT** the candidate's core depth. Hillclimb's DeepMind alumni and quant researchers provide world-class depth in this area.
* **Declared Gap 2: Large-Scale Training Infra:** Distributed multi-node GPU cluster topologies, Megatron/DeepSpeed distributed training loops, and low-level kernel compilation infra are **NOT** claimed.
* **Strategic Fit:** By taking total ownership of evals rigor, held-out verifier integrity, failure-mode taxonomies, and technical writing, the candidate enables the core RL and infra researchers to focus 100% of their energy on training loops and model hillclimbing.

---

## 3. Application Artifacts & Verification Table

All artifacts have been compiled, programmatically verified, and synchronized across both the canonical git repository and the Goal-4 workspace mirror:

| Artifact Name | Canonical Repo Path | Workspace Mirror Path | Technical Verification & Specification |
|---|---|---|---|
| **1-Page CV (PDF)** | `hillclimb/cv-pavel-cherkashin-hillclimb.pdf` | `workspace/goals/goal-4/files/hillclimb/cv-pavel-cherkashin-hillclimb.pdf` | Programmatically verified: 1 page Letter (`612x792 pt`), 0 text collisions, 0 out-of-bounds elements, deterministic ReportLab build (`rl_config.invariant=1`). Verified digest: `bcbe206...`. |
| **High-Res PNG (300 DPI)** | `hillclimb/cv-pavel-cherkashin-hillclimb-hd.png` | `workspace/goals/goal-4/files/hillclimb/cv-pavel-cherkashin-hillclimb-hd.png` | `2550x3300 px`, explicit 300 DPI metadata (`(299.9994, 299.9994)`). Ready for direct attachment in X DM. Note: visual geometry & DPI metadata are verified; byte-level hash determinism is explicitly not asserted for PNG rasterization. |
| **Standard PNG Alias** | `hillclimb/cv-pavel-cherkashin-hillclimb.png` | `workspace/goals/goal-4/files/hillclimb/cv-pavel-cherkashin-hillclimb.png` | Direct alias of high-resolution card for universal platform preview. |
| **CV Builder Script** | `hillclimb/build_hillclimb_cv.py` | `workspace/goals/goal-4/files/hillclimb/build_hillclimb_cv.py` | Python 3 script with InvariantCanvas, programmatic collision engine, and automatic dual-tree mirror synchronization. |
| **X DM Record** | `hillclimb/dm-draft.md` | `workspace/goals/goal-4/files/hillclimb/dm-draft.md` | High-signal outreach record transmitted to Jun Park (@jparkjmc) highlighting DeepRSI context, declared gaps, and evals+writing seat. |
| **X DM Record (Alias)** | `hillclimb/x-dm-draft.md` | `workspace/goals/goal-4/files/hillclimb/x-dm-draft.md` | Identical alias of outreach record (`cmp` verified). |
| **Claim Ledger** | `hillclimb/evidence/CLAIM_LEDGER.md` | `workspace/goals/goal-4/files/hillclimb/evidence/CLAIM_LEDGER.md` | Comprehensive mapping of all CV claims to verified primary sources (MSU degree, Siebel Systems, Sputnik Labs, INTUIT textbook ISBN) with exact public catalog and archive links. Headcount claim purged. |
| **Machine Evidence** | `hillclimb/evidence/EVIDENCE.json` | `workspace/goals/goal-4/files/hillclimb/evidence/EVIDENCE.json` | Machine-readable manifest tracking ticket, git branch, acceptance assertions, compensation details, limitations, and `SENT` status. |
| **SHA-256 Manifest** | `hillclimb/evidence/MANIFEST.sha256` | `workspace/goals/goal-4/files/hillclimb/evidence/MANIFEST.sha256` | Tamper-evident checksums of all tracked canonical source files, lockfile, and reproducible PDF. |
| **Transitive Lockfile** | `hillclimb/requirements.lock` | `workspace/goals/goal-4/files/hillclimb/requirements.lock` | Full transitive lockfile pinning all 16 direct and transitive dependencies with explicit Python runtime (Python >= 3.10, <= 3.13) and platform constraints. |
| **Direct Dependencies** | `hillclimb/requirements.txt` | `workspace/goals/goal-4/files/hillclimb/requirements.txt` | Direct pinned dependencies (`reportlab==5.1.0`, `pymupdf==2.0`, `pypdf==6.21.2`, `pillow==12.3.0`). |

---

## 4. Verification Check Details & Determinism Scope

1. **Single-Page Constraint:** Programmatic inspection via PyMuPDF and pypdf confirms `page_count == 1`.
2. **Zero Layout Collisions:** Bounding-box intersection scan confirms `text_overlap_count == 0` across all 17 distinct text blocks.
3. **Zero Out-of-Bounds Text:** Every element is strictly contained within printable dimensions (`out_of_bounds_count == 0`).
4. **Deterministic PDF Scope:** Recompiling with `build_hillclimb_cv.py` produces the identical SHA-256 digest (`bcbe206...`) under Python 3.10–3.13 on POSIX/macOS/Linux matching ReportLab configurations. Across heterogeneous platforms, ReportLab layout dimensions, page count, and bounding box containment remain strictly invariant.
5. **Image Geometry & DPI Metadata vs. Rasterizer Non-Determinism:** Pillow inspection confirms geometry `(2550, 3300)` and 300 DPI metadata. Note that PNG rasterization is subject to OS-level font rasterizer anti-aliasing and Deflate compression variations; byte-level hash determinism for PNG is explicitly **NOT asserted** (`NOT_ASSERTED`).
6. **Dual-Tree Mirror Parity:** `diff -rq hillclimb workspace/goals/goal-4/files/hillclimb` yields zero discrepancies.
7. **Factual Grounding & Claim Ledger:** All biographical claims strictly map to confirmed primary sources with public links:
   - Undergraduate Degree: MSU 1995 B.S. in Computer Science in Global Ecology (`msu.ru`); IIASA research fellowship (`iiasa.ac.at`).
   - Published Textbook: INTUIT / BINOM, Moscow, 2007, 384 pp., ISBN 978-5-94774-643-3, cataloged in Russian State Library (RSL ID `01003185368`) and National Electronic Library (NEL).
   - Enterprise Leadership: Sputnik Labs (CNews M&A archive: acquired by Technoserv in 2008), Siebel Systems (Country Manager, Russia & CIS), Microsoft Russia.
   - Headcount Audit: Unverified headcount metric ("110+") purged from CV and ledger.
8. **Transitive Dependency Pinning:** Full `requirements.lock` generated and validated across clean virtual environments.

---

## 5. Operational Status & Governance Boundaries

* **Historical Tap-Gate Completed:** In accordance with Sections 4 and 5 of the Mindrock Agent Constitution (`AGENTS.md`), autonomous agents did not initiate unauthorized outbound communication. Principal Pavel Cherkashin conducted manual 1-tap review and transmitted the outreach package via X DM to @jparkjmc on 2026-10-25 at ~06:39 PDT.
* **Current Operational Status:** `SENT` (Awaiting response from Jun Park / Hillclimb AI).
* **Linear Status:** In accordance with constitutional rules, builder agent `agy` does not mark Linear issue MIN-222 `Done`. The ticket is transitioned to `In Review` with label `Role: QA-Needed`, and handed off to `@codex` for independent verification.
