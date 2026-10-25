# PostHog Partnership Wrangler: Evaluation, ATS Audit & Sibling Role Analysis

**Linear Issue:** [MIN-217](https://linear.app/mindrock/issue/MIN-217/posthog-partnership-wrangler-remote-triage-top-10-1)  
**Target Entity:** PostHog (Open-source Product Analytics, Remote-First)  
**Target Role:** Partnership Wrangler (Remote)  
**Evaluator:** agy@wolfram (Autonomous Builder Agent)  
**Date:** 2026-10-25  
**Final Status:** **PACKAGE DELIVERED, NOT SENT (SHELVED / TAP-GATED)**

---

## 1. Live ATS & Career Board Verification Audit (Flag 1)

### A. The Discrepancy: CareerVault Mirror vs. Live Board
* **CareerVault Mirror:** The job aggregator `careervault.io` showed a listing for *PostHog — Partnership Wrangler (Remote)* with an apparent recent crawl timestamp.
* **Forensic Verification:** On closer inspection and direct ATS probing, the CareerVault entry was an indexed mirror of an older posting originally published approximately **7 months ago**, which remained indexed in aggregator caches.
* **Official PostHog Career Board (`posthog.com/careers` / Ashby ATS):**
  * Searched official ATS API and text rendering for `Partnership`, `Wrangler`, and `Alliances`.
  * **Result: 0 active listings.**
  * The current board lists ~14 openings across 10 distinct job families (e.g., *Developer Marketer - Sales*, *Product Engineers*, *Site Reliability Engineers*), but contains **no active partnership roles**.

### B. Verification Conclusion
The *Partnership Wrangler* role is **not active on PostHog's live ATS**. Proceeding with an automated or cold ATS submission is impossible because the intake form has been closed.

---

## 2. Framing the Partner Certification Program (Flag 2)

### A. The Problem with Legacy Certification
Traditional enterprise partner certification programs are characterized by:
* 60-slide PowerPoint decks and vendor lock-in trivia.
* Multi-thousand-dollar exam proctoring fees.
* Slow, bureaucratic approval gates that repel modern technical agencies and boutique analytics firms.

### B. The PostHog Alignment Strategy
PostHog's core culture is defined by **"doers, not strategists"**, transparency, extreme autonomy, and developer-first utility. A corporate-style certification program would fail.

### C. The "First-Build" Framing
In the tailored CV and cover note, Pavel Cherkashin **does NOT falsely claim** to have operated a legacy corporate certification program. Instead, this is explicitly structured as a **Day-1 First-Build Milestone**:
1. **Developer-First Verification:** A GitHub-native verification suite where agency engineers deploy a sample application with PostHog, configure reverse proxies, set up custom ClickHouse event ingestion, and pass automated end-to-end telemetry tests.
2. **Self-Serve Accreditation:** Code-driven digital badges and verified directory listings for agencies that successfully ship verified client integrations.
3. **Agency Commercial Alignment:** Direct tie-in between technical verification and tiered referral commissions / co-sell leads.

This frames an apparent "gap" into a massive positive signal of cultural alignment: building a lightweight, high-leverage enablement engine from scratch.

---

## 3. Sibling Role Analysis: "Partnership Marketer" (Flag 3)

### A. Role Profile & Angle
* **Source:** BuiltIn crawl identified a sibling opening: *Partnership Marketer*.
* **Focus:** Engaging startup ecosystems, venture capital firms, accelerators (Y Combinator, Techstars, Founder Institute), and developer communities to drive early-stage startup adoption of PostHog for Startups ($50k in credits).

### B. Comparative Fit Assessment: Pavel Cherkashin
| Dimension | Partnership Wrangler | Partnership Marketer (Sibling) | Pavel Cherkashin Fit |
|---|---|---|---|
| **Core Motion** | Cloud Marketplaces (AWS/GCP), SI agencies, commercial contracts | VC/Accelerator alliances, founder perks, startup ecosystem | **Exceptional on both; Sibling role directly matches 6+ years at FI/Decile** |
| **Target Audience** | Enterprise buyers, agency principals, cloud marketplace leads | Founders, VC platform managers, accelerator directors | Over 100+ B2B startups mentored; direct relationships with major VC platforms |
| **Commercials** | CPPO private offers, revenue shares, contract redlines | Program credits, co-marketing webinars, startup perks | Seasoned fund manager and accelerator architect |
| **Live Board Status** | Inactive (0 listings) | Inactive (0 listings; closest is *Developer Marketer - Sales*) | N/A — both currently inactive on ATS |

### C. Second-Door Tactical Value
Should PostHog reopen partnership hiring or should Principal Pavel Cherkashin choose to execute a direct, speculative founder pitch to James Hawkins or Tim Glaser, the **VC / Startup Ecosystem angle** (*Partnership Marketer*) serves as an ideal secondary hook alongside the *Partnership Wrangler* commercial motion.

---

## 4. Final Operational Verdict & Recommendation

1. **Package Status:** The complete application dossier (1-page CV PDF, 300 DPI HD PNG, tailored cover note, evaluation notes, build script, and evidence manifests) is **delivered and verified in the repository**.
2. **Execution Gate:** **NOT SENT (Tap-Gated & Shelved)**.
   * Because the role is not currently active on PostHog's ATS, automated or third-party submission is impossible.
   * The package is shelved in `posthog/` and mirrored in `workspace/goals/goal-4/files/posthog/`.
3. **Queue Advancement:** PostHog exits the active outbound queue. The autonomous pipeline advances to triage item **#2 (Town - MIN-218)**.
4. **Human Tap Option:** Principal Pavel Cherkashin retains the option to send the direct founder outreach note to James Hawkins via X/Email if desired.
