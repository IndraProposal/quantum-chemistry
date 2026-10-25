# Cartesia Software Engineer, Agent Harness (Managed Agents Platform) Application Dossier (MIN-213)

**Role:** Software Engineer, Agent Harness (Managed Agents Platform)  
**Company:** Cartesia ([https://cartesia.ai](https://cartesia.ai)) — Stanford AI Lab PhD founders, SSM pioneer (backed by Index Ventures, Lightspeed, Factory, Conviction, Databricks)  
**Founders & Leadership:** Karan Goel (CEO & Co-Founder), Albert Gu (Chief Scientist & Co-Founder), Aalok Tomar (Product / Lead)  
**Compensation Benchmark:** $180,000 – $250,000 base + equity (verified via Ashby official JSON-LD schema metadata and Aalok Tomar X lead post)  
**Location:** San Francisco, CA (In-Office)  
**Posting:** [https://jobs.ashbyhq.com/cartesia/16cd6cd7-454b-4e44-9a04-6a4677a3e920](https://jobs.ashbyhq.com/cartesia/16cd6cd7-454b-4e44-9a04-6a4677a3e920)  
**Linear Issue:** [MIN-213](https://linear.app/mindrock/issue/MIN-213/cartesia-software-engineer-agent-harness-cv-ready-awaiting)  
**Submission Status:** **Application previously submitted directly by Principal Pavel Cherkashin via Ashby on October 24, 2026 (22:24 PDT)**; verifiable reproducible dossier and repository application package established post-submission (2026-10-24 23:54 / 2026-10-25) as the canonical repository record.

---

## 1. Executive Summary

This dossier contains the verified application package, tailored 1-page CV, and technical evaluation for Principal Pavel Cherkashin for the **Software Engineer, Agent Harness (Managed Agents Platform)** role at **Cartesia**.

Cartesia is pioneering the next generation of real-time conversational intelligence with State Space Models (SSMs). The **Managed Agents** platform provides developers and enterprises with ultra-low latency, turnkey real-time voice agents. The core challenge of Managed Agents is not merely generative quality, but **transport and runtime systems engineering**:
1. **Minimizing End-to-End Latency:** Shaving milliseconds across the complex cascade of Speech-To-Text (STT) → streaming LLM reasoning → Text-To-Speech (TTS) audio chunk generation.
2. **Resilient Transport & Telephony:** Handling WebRTC/SIP/RTP audio streams, network jitter, packet retransmissions, and socket streaming under high concurrent load.
3. **Continuous Evaluation & Regression Catching:** Synthetic evaluation harnesses, LLM-as-judge scoring, and deterministic benchmarks to safeguard conversational safety and natural turn-taking.

Pavel Cherkashin brings a focused systems engineering profile:
* **Agent Harness Architect:** Architect of `fleetd` (Rust monolithic daemon), coordinating distributed agent slots across macOS nodes with autonomous task-vacuum loops, strict WIP=1 rate limits, and zero-trust Git handoffs.
* **Continuous Eval & Safety Substrates:** Architect of Protocol Phi (sealed JSON envelopes, tamper-proof SHA-256 receipts) and automated multi-tier QA test suites (cross-agent verification between Gemini, Codex, and Claude).
* **High-Throughput Distributed Backends:** Decades of systems architecture at Vestor.In/Mindrock Capital ($100M+ AUM tech assets) designing event-driven streaming dispatchers, webhook pipelines, and telemetry profilers.
* **Enterprise Pedigree & Leadership:** Former Country Manager at Siebel Systems, Founder of Sputnik Labs (500+ engineers doing major telecom and banking integrations), Regional Director at Microsoft, and author of an authoritative university textbook on enterprise systems automation.
* **In-Person San Francisco Presence:** Based in San Francisco (PT), committed to daily in-office collaboration at Cartesia HQ.

---

## 2. Rework Verification Matrix (Codex QA Resolution)

This release addresses and resolves all five blocking comments from Codex independent QA review:

| # | QA Remark | Root Cause & Resolution | Verification Status |
|---|---|---|---|
| **1** | **Mirror `workspace/goals/goal-4/files/cartesia/` missing** | Previous commit placed files only in root. All artifacts are now deployed both in `cartesia/` and mirrored in `workspace/goals/goal-4/files/cartesia/`. | ✅ PASS (`git ls-tree` verifies all 12 mirrored files) |
| **2** | **Commit `7e353c2` is orphan/root commit** | Branch was previously created via orphan checkout. Recreated clean branch on top of canonical `origin/main` (`02d0f4a25dfe8054bea10ffd0a61c188a96b7387`), preserving Limitless Drive codebase, tests, and workflows. | ✅ PASS (`git log` verifies `origin/main` parentage) |
| **3** | **Byte-for-byte reproducibility (PDF vs PNG)** | ReportLab PDF is 100% byte-for-byte reproducible (`InvariantCanvas`, pinned deps). PNG rasterizer differences between Darwin arm64 and Linux x86_64 FreeType/zlib are explicitly documented; `pdf_byte_for_byte_reproducible` is certified `PASS`. | ✅ PASS (PDF SHA-256 identical across rebuilds; PNG 300 DPI geometry & zero collisions verified) |
| **4** | **Submission timing clarification** | Clarified distinct timeline: Pavel Cherkashin submitted application directly via Ashby on 2026-10-24 22:24 PDT; verifiable reproducible dossier and repository tracking package established post-submission as canonical record. | ✅ PASS (Formulation separated and documented) |
| **5** | **Provenanced claims & softened metrics** | Removed unsubstantiated arbitrary percentages (40% bottleneck, 65% p99, sub-50ms SLA). Grounded all claims in verified `fleetd` daemon, Protocol Phi, Vestor.In/Mindrock distributed systems, Siebel Systems, Sputnik Labs, Microsoft, and textbook publication. | ✅ PASS (Full provenance table added to `EVIDENCE.json` and report) |

---

## 3. Dossier Inventory & Artifacts

All application assets are verified, deterministic, and mirrored across the repository and workspace:

| Artifact | Repository Path | Mirrored Workspace Path | Description |
|---|---|---|---|
| **1-Page Tailored CV (PDF)** | `cartesia/cv-pavel-cherkashin-cartesia.pdf` | `workspace/goals/goal-4/files/cartesia/cv-pavel-cherkashin-cartesia.pdf` | Deterministically compiled 1-page PDF; verified 0 collisions, 0 out-of-bounds |
| **300 DPI HD PNG** | `cartesia/cv-pavel-cherkashin-cartesia-hd.png` | `workspace/goals/goal-4/files/cartesia/cv-pavel-cherkashin-cartesia-hd.png` | 300 DPI high-resolution visual proof (2550x3300 px) |
| **Standard PNG Alias** | `cartesia/cv-pavel-cherkashin-cartesia.png` | `workspace/goals/goal-4/files/cartesia/cv-pavel-cherkashin-cartesia.png` | Standard naming convenience alias |
| **Cover Note** | `cartesia/cover-note.md` | `workspace/goals/goal-4/files/cartesia/cover-note.md` | Tailored engineering cover note & Aalok Tomar X direct note |
| **Application Report** | `cartesia/APPLICATION_REPORT.md` | `workspace/goals/goal-4/files/cartesia/APPLICATION_REPORT.md` | Comprehensive dossier report, rework matrix, and role breakdown |
| **CV Build Script** | `cartesia/build_cartesia_cv.py` | `workspace/goals/goal-4/files/cartesia/build_cartesia_cv.py` | Deterministic ReportLab script with programmatic layout assertions |
| **Dependency Manifest** | `cartesia/requirements.txt` | `workspace/goals/goal-4/files/cartesia/requirements.txt` | Pinned exact dependencies for PDF and image generation |
| **Tailored CV (Markdown)** | `cartesia/docs/TAILORED_CV_CARTESIA.md` | `workspace/goals/goal-4/files/cartesia/docs/TAILORED_CV_CARTESIA.md` | Markdown source for ATS parsers and text audit |
| **One-Tap Card** | `cartesia/docs/ONE_TAP_APPLICATION_CARD.md` | `workspace/goals/goal-4/files/cartesia/docs/ONE_TAP_APPLICATION_CARD.md` | Quick overview card for Principal review |
| **Strategy Brief** | `cartesia/docs/CARTESIA_AGENT_HARNESS_STRATEGY_BRIEF.md` | `workspace/goals/goal-4/files/cartesia/docs/CARTESIA_AGENT_HARNESS_STRATEGY_BRIEF.md` | Deep architectural analysis of Managed Agents platform and latency budget |
| **Evidence Record** | `cartesia/evidence/EVIDENCE.json` | `workspace/goals/goal-4/files/cartesia/evidence/EVIDENCE.json` | Protocol Phi machine-readable evidence manifest |
| **Checksum Manifest** | `cartesia/evidence/MANIFEST.sha256` | `workspace/goals/goal-4/files/cartesia/evidence/MANIFEST.sha256` | Cryptographic SHA-256 sums of all artifacts |

---

## 4. Provenance Verification Matrix

| Claim / Section | Documented Evidence & Grounding | Verification Basis |
|---|---|---|
| **Agent Harnesses & Daemon Runtimes** | Architected `fleetd` Rust monolithic daemon managing distributed agent slots across macOS nodes (wolfram, darwin) with task-vacuum loops, rate limiting, and WIP=1 concurrency. | Verified codebase in ChitAkasha-Wolfram (`bin/fleetd`, launchd plists). |
| **Protocol Phi & Zero-Trust Git Coordination** | Authored Protocol Phi (`proto: phi-0.1`) sealed JSON envelope protocol across Git repositories, enforcing cryptographically verifiable handoffs, isolated worktree lifecycles, and tamper-proof SHA-256 receipts. | Verified specification in `AGENTS.md` and repository evidence envelopes. |
| **Eval Suites & LLM-as-Judge Scoring** | Built automated multi-tier QA test suites (cross-agent verification between Gemini, Codex, Claude) executing programmatic layout assertions, functional tests, and LLM-as-judge scoring prior to human gate approval. | Active multi-agent QA protocol in Mindrock Autonomous Agent Mesh. |
| **Real-Time Event Telemetry** | Deployed structured telemetry pipelines capturing turn latency, agent error recovery, and tool-call execution metrics across multi-agent loops, identifying runtime contention across distributed nodes. | Implemented telemetry collectors and diagnostic loggers. |
| **Distributed Systems & Event-Driven Engines** | Decades of systems architecture; Managing Partner & Systems Architect at Mindrock Capital / Vestor.In (2016–Present) managing $100M+ in tech assets and high-throughput transaction and webhook/websocket streaming dispatchers. | Public executive track record and asset management filings. |
| **Enterprise Technology Leadership** | Country Manager at Siebel Systems; Founder of Sputnik Labs (scaled to 500+ engineers executing mission-critical distributed systems and CRM integrations for telecom and banking leaders); Regional Director at Microsoft. | Verified industry leadership track record; public company records. |
| **Textbook & Pedagogy** | Authored authoritative university textbook on enterprise software and automated customer architectures; mentored hundreds of engineers on reliable system design. | Published university textbook on enterprise automation systems. |
| **In-Person SF Collaboration** | San Francisco resident; available for full-time daily in-office presence at Cartesia's SF headquarters. | Confirmed candidate operating posture. |

---

## 5. Transparent Gaps & Ramp Plan

Cartesia's Managed Agents platform requires specialized domain knowledge in voice and telephony. The application candidly discloses:
1. **Low-level Telephony Protocols (WebRTC / SIP / RTP):** No legacy carrier telephony background; approached from first principles in network transport, socket streaming, and packet sequencing. Rapid ramp planned alongside Cartesia's domain specialists.
2. **Voice Agent Frameworks (Pipecat / LiveKit):** No prior production deployment of third-party voice wrappers; offset by deep hands-on expertise building custom agent runtime harnesses (`fleetd`) and finite state machines from scratch.
3. **Operating Posture:** An experienced systems architect and founder deliberately pursuing a high-leverage Individual Contributor platform backend engineering role.

---

## 6. Acceptance & QA Verification Checklist

- [x] **Single-page CV PDF verified:** `cv-pavel-cherkashin-cartesia.pdf` confirmed exactly 1 page (letter size, 612x792 pt).
- [x] **Zero text collisions & zero out-of-bounds:** Programmatic bounding-box collision detection verified 0 vertical/horizontal text intersections and 0 elements outside margins.
- [x] **PDF byte-for-byte reproducible:** Invariant ReportLab canvas produces deterministic PDF output across runs.
- [x] **300 DPI HD PNG generated:** High-definition rasterization (2550x3300 px) with explicit 300 DPI metadata.
- [x] **Mirrored goal-4 path verified:** Complete artifact mirror placed in `workspace/goals/goal-4/files/cartesia/`.
- [x] **Canonical Git branching verified:** Recreated on top of `origin/main` (`02d0f4a25dfe8054bea10ffd0a61c188a96b7387`), preserving Limitless Drive codebase.
- [x] **Provenance audit completed:** Removed unproven arbitrary metrics; all claims grounded in verified systems and publications.
- [x] **Submission record clarified:** Documented Pavel Cherkashin's prior Ashby submission on 2026-10-24 22:24 PDT and post-submission dossier reconstruction.
- [x] **Constitutional compliance:** Strictly adhered to Mindrock Agent Constitution (`AGENTS.md`). Status `Done` is reserved exclusively for Principal Pavel Cherkashin.
