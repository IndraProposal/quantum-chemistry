"""TTS interfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class AudioChunk:
    pcm16: bytes
    sample_rate: int
    is_final: bool = False


class StreamingTTS(Protocol):
    def synthesize_stream(self, text: str): ...

    def stop(self) -> None: ...
