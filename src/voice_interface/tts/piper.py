"""Local Piper TTS integration with a deterministic fallback."""

from __future__ import annotations

import math
import struct
from collections.abc import Iterator

from voice_interface.config import TTSConfig
from voice_interface.tts.base import AudioChunk


class PiperTTS:
    def __init__(self, config: TTSConfig | None = None) -> None:
        self.config = config or TTSConfig()
        self._stopped = False

    def synthesize_stream(self, text: str) -> Iterator[AudioChunk]:
        """Yield local audio chunks.

        If Piper bindings are unavailable, emit a short quiet tone so the rest
        of the full-duplex pipeline remains testable offline.
        """

        self._stopped = False
        try:
            from piper.voice import PiperVoice  # type: ignore[import-not-found]
        except ImportError:
            yield from self._fallback_tone(text)
            return
        voice = PiperVoice.load(self.config.voice)  # pragma: no cover - optional
        for chunk in voice.synthesize_stream_raw(text):  # pragma: no cover
            if self._stopped:
                break
            yield AudioChunk(pcm16=chunk, sample_rate=self.config.sample_rate)
        yield AudioChunk(pcm16=b"", sample_rate=self.config.sample_rate, is_final=True)

    def _fallback_tone(self, text: str) -> Iterator[AudioChunk]:
        duration = min(0.8, max(0.08, len(text) / 120.0))
        total = int(self.config.sample_rate * duration)
        frame_count = max(1, int(self.config.sample_rate * self.config.stream_chunk_ms / 1000))
        for offset in range(0, total, frame_count):
            if self._stopped:
                break
            samples = []
            for index in range(offset, min(offset + frame_count, total)):
                samples.append(int(1200 * math.sin(2 * math.pi * 220 * index / self.config.sample_rate)))
            yield AudioChunk(pcm16=struct.pack("<" + "h" * len(samples), *samples), sample_rate=self.config.sample_rate)
        yield AudioChunk(pcm16=b"", sample_rate=self.config.sample_rate, is_final=True)

    def stop(self) -> None:
        self._stopped = True
