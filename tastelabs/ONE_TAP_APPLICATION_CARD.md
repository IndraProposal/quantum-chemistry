# ONE-TAP APPLICATION CARD: Taste Labs (AI Engineer, RL & Evals)

**Linear Issue:** [MIN-235](https://linear.app/mindrock/issue/MIN-235/taste-labs-ai-engineer-rl-and-evals-ashby-sf-on-site)  
**Run ID:** `run-f2d5284e8462`  
**Candidate:** Pavel Cherkashin (`pavel@mindrock.capital`)  
**Target Organization:** Taste Labs ([https://tastelabs.com](https://tastelabs.com))  
**Hiring Context & Founder:** Thais Castello Branco ([@thaiscbranco_](https://x.com/thaiscbranco_))  
**Role Scope:** AI Engineer, RL & Evals (Technical Staff) — Full-Time, In-Office San Francisco, CA  
**Compensation:** $175,000 – $275,000 base + equity (up to $300,000 for exceptional profiles). JD verified live 2026-10-26.  
**Application Channel:** Ashby Application Form (`tastelabs.com/careers`)  
**Form Inputs Required:** Resume PDF + LinkedIn URL + 2 Free-Text Prompts (Interest + Fit) + U.S. Work Auth. *(No standalone cover-letter field)*  
**Operational Status:** `READY_FOR_TAP_REVIEW` (Delivered locally; NOT sent autonomously. Tap-gated for Principal Pavel Cherkashin).  

---

## ⚡ Executive Mission & Thesis

- **The Problem:** AI models excel at objective, verifiable domains (math, code, chess) with ground-truth unit tests, but catastrophically fail in subjective, creative, and qualitative domains (design, tone, brand voice, aesthetic harmony). Without granular evals, models collapse to the mean—generating generic **"AI slop."**
- **Taste Labs' Thesis:** Taste is not an intractable mystery; it is a measurement and decomposition problem. By decomposing creative assets into testable rubrics, grading methods, and RL environments, models can systematically learn and adhere to taste.
- **Ecosystem Role:** Taste Labs supplies specialized post-training data, rubrics, and RL evals to **frontier AI labs**, while equipping **agent-layer companies** with runtime context and taste verifiers.

---

## 🎯 Candidate Fit & Honest Gaps

### High Conviction Strengths
- **Evals Harness Architecture & Rubrics:** Architect of Protocol Phi (Φ-0.1), multi-model LLM-as-judge scoring, Bradley-Terry Elo estimation, and deterministic layout assertion engines (0 collisions, 0 out-of-bounds, 1 page invariant).
- **Autonomous Agent Harnesses & Context Layers:** Architect of `fleetd` (high-concurrency Rust daemon managing multi-agent execution, WIP=1 slot scheduling, and MCP server integrations), stateful agent isolation, and token budgeting.
- **Enterprise Scale & Startup DNA:** Founded Sputnik Labs, scaling it from zero to 500+ employees (acquired by Technoserv in 2008); built large-scale customer interaction rubrics and predictive scoring pipelines.
- **Technical Pedagogy & Author:** Authored 384-page published university textbook on CRM and enterprise automation systems (*CRM Strategy*, INTUIT/BINOM, ISBN 978-5-94774-643-3, Russian State Library).

### Transparent Gaps & Ramp Posture
- **Declared Growth Edge: Scalable RL Cluster Infra & Training Loops:** Low-level distributed RL infrastructure (multi-node GPU cluster topologies, Megatron-LM/DeepSpeed training loops, NCCL collective communications, and custom CUDA/Triton kernels) are a growth edge, not historical depth.
- **Strategic Complementarity:** By taking total ownership of evals rigor, task design for taste, grading rubrics, agent context layers, and deterministic backend verification, the candidate enables core RL infra researchers to focus 100% of their energy on training loops and cluster optimization.

---

## 🗂️ Staged Artifacts & Verification Table

| Artifact Name | Local File Path | Workspace Mirror Path | Specification & Verification Details |
|---|---|---|---|
| **1-Page CV (PDF)** | `tastelabs/cv-pavel-cherkashin-tastelabs.pdf` | `workspace/goals/goal-4/files/tastelabs/cv-pavel-cherkashin-tastelabs.pdf` | Programmatically verified: 1 page Letter (`612x792 pt`), 0 collisions, 0 out-of-bounds elements. SHA-256: `1908e0e5a8a8cc0adba89baa31db39758f83a1a994e1b13793e9bdc2b9a64aea`. |
| **High-Res PNG (300 DPI)** | `tastelabs/cv-pavel-cherkashin-tastelabs-hd.png` | `workspace/goals/goal-4/files/tastelabs/cv-pavel-cherkashin-tastelabs-hd.png` | `2550x3300 px`, explicit 300 DPI metadata `(299.9994, 299.9994)`. Ready for direct upload/preview. |
| **Standard PNG Alias** | `tastelabs/cv-pavel-cherkashin-tastelabs.png` | `workspace/goals/goal-4/files/tastelabs/cv-pavel-cherkashin-tastelabs.png` | Direct alias for universal image viewers. |
| **CV Builder Script** | `tastelabs/build_tastelabs_cv.py` | `workspace/goals/goal-4/files/tastelabs/build_tastelabs_cv.py` | Python 3 script with InvariantCanvas, programmatic collision engine, and automatic dual-tree mirror synchronization. |
| **Ashby Form Answers** | `tastelabs/ashby-answers.md` | `workspace/goals/goal-4/files/tastelabs/ashby-answers.md` | Complete free-text answers for Question 1 (Interest / Ending AI Slop) and Question 2 (Fit / Strengths & Honest Gaps). |
| **Application Report** | `tastelabs/APPLICATION_REPORT.md` | `workspace/goals/goal-4/files/tastelabs/APPLICATION_REPORT.md` | Full application dossier and evaluation methodology report. |
| **Claim Ledger** | `tastelabs/evidence/CLAIM_LEDGER.md` | `workspace/goals/goal-4/files/tastelabs/evidence/CLAIM_LEDGER.md` | Comprehensive mapping of all CV claims to verified primary sources (MSU degree, Siebel Systems, Sputnik Labs, INTUIT textbook ISBN). |
| **Machine Evidence** | `tastelabs/evidence/EVIDENCE.json` | `workspace/goals/goal-4/files/tastelabs/evidence/EVIDENCE.json` | Machine-readable manifest tracking ticket, git branch, acceptance assertions, compensation details, limitations, and `DELIVERED` status. |
| **SHA-256 Manifest** | `tastelabs/evidence/MANIFEST.sha256` | `workspace/goals/goal-4/files/tastelabs/evidence/MANIFEST.sha256` | Tamper-evident checksums of all tracked canonical source files, lockfile, and reproducible PDF. |
| **Transitive Lockfile** | `tastelabs/requirements.lock` | `workspace/goals/goal-4/files/tastelabs/requirements.lock` | Pinned lockfile enforcing Python runtime (Python >= 3.12, < 3.14) and platform constraints. |
| **Direct Dependencies** | `tastelabs/requirements.txt` | `workspace/goals/goal-4/files/tastelabs/requirements.txt` | Direct pinned dependencies (`reportlab==5.1.0`, `pymupdf==2.0`, `pypdf==6.21.2`, `pillow==12.3.0`). |
| **Verification Suite** | `tastelabs/test_cv_harness.py` | `workspace/goals/goal-4/files/tastelabs/test_cv_harness.py` | 7-stage automated verification suite testing runtime, imports, layout, digest, PNG specs, manifest, and dual-tree parity. |

---

## 📋 Direct Copy-Paste for Ashby Form

### Question 1: What excites you about Taste Labs and our mission to end "AI slop" and crack subjective domains?
*(Copy text block from `tastelabs/ashby-answers.md` Section 1)*

### Question 2: Why are you a strong fit for the AI Engineer, RL & Evals role, and what are your technical strengths and growth edges?
*(Copy text block from `tastelabs/ashby-answers.md` Section 2)*

### Resume File:
`~/workspace/goals/goal-4/files/tastelabs/cv-pavel-cherkashin-tastelabs.pdf`
