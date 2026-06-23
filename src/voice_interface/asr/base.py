"""ASR interfaces and lightweight transcript types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class TranscriptEvent:
    text: str
    is_final: bool
    speaker: str | None = None
    language: str | None = None
    start_ms: int | None = None
    end_ms: int | None = None


class StreamingASR(Protocol):
    def start(self) -> None: ...

    def transcribe_chunk(self, pcm16: bytes) -> TranscriptEvent | None: ...

    def finish(self) -> TranscriptEvent | None: ...
