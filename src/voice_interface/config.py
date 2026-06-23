"""Configuration models for the local voice interface."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class ASRConfig:
    """Streaming ASR configuration.

    The defaults match a low-latency local setup. Model downloads are explicit
    and handled by optional backend packages, never by importing this library.
    """

    backend: str = "nemotron"
    model: str = "nvidia/nemotron-3.5-asr-streaming-0.6b"
    chunk_ms: int = 160
    language: str = "auto"
    device: str = "auto"
    cache_aware: bool = True


@dataclass(slots=True)
class VADConfig:
    backend: str = "energy"
    sample_rate: int = 16_000
    frame_ms: int = 30
    speech_threshold: float = 0.015
    silence_ms: int = 450


@dataclass(slots=True)
class TTSConfig:
    backend: str = "piper"
    voice: str = "en_US-lessac-medium"
    speaker: str | None = None
    sample_rate: int = 22_050
    stream_chunk_ms: int = 80


@dataclass(slots=True)
class LLMConfig:
    backend: str = "echo"
    model: str | None = None
    endpoint: str = "http://localhost:11434/api/generate"
    system_prompt: str = "You are a concise, helpful local room assistant."


@dataclass(slots=True)
class RoomConfig:
    input_device: str | int | None = None
    output_device: str | int | None = None
    microphone_channels: int = 1
    wake_word: str | None = None
    allow_network: bool = False


@dataclass(slots=True)
class VoiceInterfaceConfig:
    asr: ASRConfig = field(default_factory=ASRConfig)
    vad: VADConfig = field(default_factory=VADConfig)
    tts: TTSConfig = field(default_factory=TTSConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    room: RoomConfig = field(default_factory=RoomConfig)
    session_path: Path = Path(".voice-interface/session.jsonl")
