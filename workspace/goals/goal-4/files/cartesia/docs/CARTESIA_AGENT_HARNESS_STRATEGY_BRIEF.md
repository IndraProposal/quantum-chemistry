# Strategic Brief: Building Low-Latency Agent Harness Infrastructure at Cartesia

**Candidate:** Pavel Cherkashin (`pavel@mindrock.capital`)  
**Role Target:** Software Engineer, Agent Harness (Managed Agents Platform), Cartesia  
**Posting:** [https://jobs.ashbyhq.com/cartesia/16cd6cd7-454b-4e44-9a04-6a4677a3e920](https://jobs.ashbyhq.com/cartesia/16cd6cd7-454b-4e44-9a04-6a4677a3e920)  
**Linear Ticket:** MIN-213  
**Context:** Cartesia Managed Agents runtime platform  

---

## 1. Executive Summary & Thesis
Cartesia has unlocked breakthrough efficiency and fidelity in voice AI through foundational State Space Models (SSMs). Bringing these models to developers and end users requires an unshakeable runtime foundation: the **Managed Agents platform**.

Voice agents face latency budgets orders of magnitude stricter than text chatbots. In conversational voice, delays above 300–400ms break conversational flow, cause awkward turn interruptions, and destroy user immersion.

The Agent Harness engineer must solve four coupled systems bottlenecks:
1. **Real-time Audio Transport:** Streaming audio bidirectional chunks over WebSockets, WebRTC, and telephony bridges without packet drops, jitter, or buffer bloat.
2. **Conversational Latency Tracing:** Eliminating latency overhead at every handoff across the pipeline: Speech-to-Text (STT) transcription &rarr; LLM token streaming &rarr; Text-to-Speech (TTS) audio synthesis.
3. **Resilient Agent Lifecycle & Cold Starts:** Sub-100ms agent worker container provisioning, intelligent session reuse, and graceful load shedding during peak concurrency.
4. **Automated Eval Suites & LLM Judges:** Continuous regression testing verifying not only semantic intent and safety, but timing metrics (TTFT, turn-taking latency, barge-in response).

---

## 2. Technical Alignment: Fleet Architecture to Voice Agent Harness

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Client / Telephony Edge                           │
│                 (WebRTC Audio Stream / SIP Gateway / WebSockets)             │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Real-time Audio Stream
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Cartesia Managed Agents Harness (Platform Engine)                           │
│ ┌───────────────────────────┐ ┌───────────────────────────┐ ┌─────────────┐ │
│ │ Audio Streaming Transport │ │ Concurrency & Slot Router │ │ Telemetry   │ │
│ │ (Jitter Buffer, Barge-in) │ │ (WIP Limits, Cold-Start)  │ │ (Latency/Tr)│ │
│ └─────────────┬─────────────┘ └─────────────┬─────────────┘ └─────────────┘ │
└───────────────┼─────────────────────────────┼───────────────────────────────┘
                │ Audio Frames                │ Text Prompts
                ▼                             ▼
┌─────────────────────────────┐ ┌─────────────────────────────┐ ┌─────────────┐
│ Cartesia Real-Time STT      │ │ Streaming LLM Engine        │ │ Cartesia    │
│ (Streaming Voice Detection) │ │ (Token-by-Token Streaming)  │ │ Sonic TTS   │
└─────────────────────────────┘ └─────────────────────────────┘ └─────────────┘
```

### Pillar A: Sub-300ms Conversational Latency Optimization
- **Streaming Handshakes:** Instead of waiting for a complete user utterance before initiating LLM inference, pipeline early streaming tokens from STT into the LLM as soon as voice activity detection (VAD) confirms speech intent.
- **Pipelined TTS Synthesis:** Stream initial LLM tokens directly into Cartesia's Sonic TTS engine in sub-sentence chunks (e.g. 3–5 words), generating the first audio packet before the LLM finishes generating the full sentence.
- **Barge-In (Interruption) Truncation:** Immediate audio stream cancellation and LLM generation abort when incoming user voice is detected, clearing downlink audio buffers instantly.

### Pillar B: Daemon Harness & Slot Management
- Applying learnings from `fleetd`: slot isolation (preventing thread contention across active conversations), deterministic task queues, and zero-leak state machines for long-running voice sessions.
- Graceful degradation: during traffic surges, maintain latency SLAs for active calls while queuing or smoothly shedding new requests.

### Pillar C: Rigorous Eval Harness & Regression Detection
- Continuous evaluation running automated voice dialog scenarios against simulated user personas.
- Multi-dimensional scoring:
  - Latency SLA: p50, p95, p99 Time-To-First-Audio (TTFA).
  - Voice Naturalness & Interruptibility: Barge-in responsiveness within 150ms.
  - LLM-as-Judge Semantic Accuracy: Ensuring tool calls and conversation goals succeed.

---

## 3. Candidate Alignment & Ramp Commitment
- **Direct Strengths:** High systems fluency, production agent harnesses, automated eval pipelines, deep familiarity with coding agents, clear architectural documentation.
- **Ramp Commitment:** Fast, first-principles assimilation of WebRTC/SIP/RTP nuances and Pipecat/LiveKit architectures.
- **Presence:** In-person collaborative presence at Cartesia's San Francisco office.
