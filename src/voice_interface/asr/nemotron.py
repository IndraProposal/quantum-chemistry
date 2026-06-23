"""Adapter for NVIDIA Nemotron streaming ASR.

The module keeps heavyweight NeMo dependencies optional. In production, install
`voice-interface[nemotron]` and use :class:`NemotronStreamingASR`; tests can use
:class:`ScriptedASR` from this module without model files or network access.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable

from voice_interface.asr.base import TranscriptEvent
from voice_interface.config import ASRConfig


class NemotronStreamingASR:
    """Lazy wrapper around a cache-aware Nemotron streaming recognizer."""

    def __init__(self, config: ASRConfig | None = None) -> None:
        self.config = config or ASRConfig()
        self._engine = None
        self._started = False

    def start(self) -> None:
        """Initialize optional NeMo components only when the stream starts."""

        if self._started:
            return
        try:
            import nemo.collections.asr as nemo_asr  # type: ignore[import-not-found]
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "Nemotron ASR requires optional NVIDIA NeMo dependencies. "
                "Install with `pip install voice-interface[nemotron]` and "
                "download the model explicitly for offline use."
            ) from exc
        self._engine = nemo_asr.models.ASRModel.from_pretrained(self.config.model)
        self._started = True

    def transcribe_chunk(self, pcm16: bytes) -> TranscriptEvent | None:
        if not pcm16:
            return None
        if self._engine is None:  # pragma: no cover - backend-specific
            raise RuntimeError("ASR stream has not been started")
        # NeMo streaming APIs vary by release; keep the boundary isolated here.
        result = self._engine.transcribe([pcm16], batch_size=1)  # type: ignore[attr-defined]
        text = result[0] if result else ""
        return TranscriptEvent(text=text, is_final=False, language=self.config.language)

    def finish(self) -> TranscriptEvent | None:
        return None


class ScriptedASR:
    """Deterministic ASR for tests, demos, and plugin development."""

    def __init__(self, events: Iterable[str | TranscriptEvent]) -> None:
        self.events = deque(
            event if isinstance(event, TranscriptEvent) else TranscriptEvent(text=event, is_final=True)
            for event in events
        )

    def start(self) -> None:
        return None

    def transcribe_chunk(self, pcm16: bytes) -> TranscriptEvent | None:
        if not pcm16 or not self.events:
            return None
        return self.events.popleft()

    def finish(self) -> TranscriptEvent | None:
        if self.events:
            event = self.events.popleft()
            return TranscriptEvent(text=event.text, is_final=True, speaker=event.speaker, language=event.language)
        return None
