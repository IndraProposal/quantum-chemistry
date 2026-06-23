"""Voice activity detection helpers."""

from __future__ import annotations

import math
import struct
from dataclasses import dataclass

from voice_interface.config import VADConfig


@dataclass(slots=True)
class VADEvent:
    is_speech: bool
    rms: float


class EnergyVAD:
    """Dependency-free VAD suitable as a conservative default/fallback."""

    def __init__(self, config: VADConfig | None = None) -> None:
        self.config = config or VADConfig()

    def analyze(self, pcm16: bytes) -> VADEvent:
        if len(pcm16) < 2:
            return VADEvent(is_speech=False, rms=0.0)
        sample_count = len(pcm16) // 2
        samples = struct.unpack("<" + "h" * sample_count, pcm16[: sample_count * 2])
        rms = math.sqrt(sum(sample * sample for sample in samples) / sample_count) / 32768.0
        return VADEvent(is_speech=rms >= self.config.speech_threshold, rms=rms)
