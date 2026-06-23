# Voice Interface Design Notes

The core package is intentionally dependency-light. Heavy engines such as NeMo,
Piper, pyannote, sounddevice, or local LLM clients are isolated behind optional
extras so the CLI, tests, and plugin development work offline on any platform.

## Runtime pipeline

1. Audio frontend captures PCM chunks from one or more microphones.
2. VAD marks speech and silence boundaries for natural turn-taking.
3. Streaming ASR produces partial and final `TranscriptEvent` objects.
4. Conversation orchestration forwards final text to a local responder or LLM.
5. Streaming TTS emits `AudioChunk` objects and can be stopped for barge-in.
6. Plugins can intercept recognized commands before or after LLM handling.

## Privacy posture

Imports and deterministic demos do not perform network calls. Model downloads,
cloud fallbacks, and remote LLM endpoints must be explicitly configured by the
operator.
