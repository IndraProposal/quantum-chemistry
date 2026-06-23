"""Full-duplex conversation orchestration."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass

from voice_interface.asr.base import StreamingASR, TranscriptEvent
from voice_interface.tts.base import AudioChunk, StreamingTTS


@dataclass(frozen=True, slots=True)
class ConversationTurn:
    user_text: str
    assistant_text: str
    speaker: str | None = None


class ConversationLoop:
    """Coordinates STT → responder/LLM → TTS with barge-in support."""

    def __init__(
        self,
        asr: StreamingASR,
        tts: StreamingTTS,
        responder: Callable[[str], str] | None = None,
    ) -> None:
        self.asr = asr
        self.tts = tts
        self.responder = responder or (lambda text: f"I heard: {text}")
        self.turns: list[ConversationTurn] = []
        self._speaking = False

    def handle_audio(self, pcm_chunks: Iterable[bytes]) -> list[ConversationTurn]:
        self.asr.start()
        completed: list[ConversationTurn] = []
        for chunk in pcm_chunks:
            event = self.asr.transcribe_chunk(chunk)
            if event is None:
                continue
            if self._speaking and event.text.strip():
                self.tts.stop()
                self._speaking = False
            if event.is_final and event.text.strip():
                completed.append(self._answer(event))
        final = self.asr.finish()
        if final and final.text.strip():
            completed.append(self._answer(final))
        return completed

    def _answer(self, event: TranscriptEvent) -> ConversationTurn:
        assistant_text = self.responder(event.text)
        self._speaking = True
        for audio in self.tts.synthesize_stream(assistant_text):
            self._consume_audio(audio)
            if audio.is_final:
                break
        self._speaking = False
        turn = ConversationTurn(user_text=event.text, assistant_text=assistant_text, speaker=event.speaker)
        self.turns.append(turn)
        return turn

    def _consume_audio(self, audio: AudioChunk) -> None:
        # Real audio playback is implemented by CLI/daemon frontends so this
        # core loop remains easy to test and embed.
        return None
