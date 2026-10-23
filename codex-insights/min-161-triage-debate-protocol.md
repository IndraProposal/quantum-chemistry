# Backstage Triage Debates: Machine-Parsable Epistemic Consensus (MIN-161)

## TL;DR

Multi-agent incident triage fails when it produces noisy conversational chat that fragments context across channels and bombards the human principal. Protocol v0 («Гиббериш v0») isolates diagnostic dialogue to the Linear incident ticket thread, strictly confines agents to read-only inspection, enforces a uniform 6-field schema (ТЕЗИС / ФАКТЫ / ИНТЕРПРЕТАЦИЯ / УВЕРЕННОСТЬ / ПРОВЕРИТЬ / РЕШЕНИЕ), and bubbles up exactly 3 events to Principal Pavel Cherkashin (`DEBATE_OPENED`, `CONSENSUS_REACHED`, `DEADLOCK_ESCALATION`).

## The insight

Agents diagnosing an infrastructure or build failure often have asymmetric views: e.g., `ChatGPT` triaging CI logs from mailer webhooks, `gemini@darwin` monitoring host status and mirrors, `agy@wolfram` inspecting build outputs. If agents argue in natural prose, every turn triggers notifications and alarm fatigue. 

By enforcing the «Gibberish v0» schema:
1. Every argument is constrained to empirical facts, explicit causal links, and calibrated confidence levels (`high`, `medium`, `low`).
2. An autonomous Merger (default: `Muse` / Dean) collapses multi-agent arguments into a single canonical Consensus comment.
3. Dissent is not hidden: if agents diverge in confidence or proposed resolutions, an explicit `DISSENT` block is generated, and the ticket escalates directly to Pavel's «My Issues» for a 1-click decision tap.
4. Active mutations (reruns, branch force pushes, secret edits) are strictly barred during debate, maintaining a $0-budget zero-thrashing guarantee.

## Confidence

High. Directly validated against the MIN-150 pilot (GitLab pipeline #2974623550 with 0 jobs), where `ChatGPT ↔ Muse` correctly identified empty DAG noise vs real failure, avoiding an unnecessary and harmful CI retry.

## What it would take to act on it

1. Deploy the `GibberishMessage` parser and validator into `fleetd` and `Muse` intake poller.
2. Formalize Section 9 in `AGENTS.md` (Mindrock Network Constitution).
3. Connect `gemini@darwin` as a background log-watch agent on Darwin for proactive triage.
