# Voice Interface

A lightweight, local-first Python library and CLI foundation for room-scale
human-computer voice interaction. The project is designed around streaming STT,
streaming TTS, VAD-driven turn taking, interruption handling, and a plugin layer
for voice-triggered tools while keeping cloud calls opt-in only.

## Goals

- **Offline by default:** no network calls during import or normal operation.
- **Low latency:** chunk-oriented ASR/TTS boundaries suitable for 80-300 ms loops.
- **Full duplex:** pause/stop speech output when new human speech arrives.
- **Extensible:** swap ASR, VAD, TTS, LLM, diarization, and GUI frontends.
- **Room-ready:** provide primitives for multi-mic and multi-speaker evolution.

## Install

```bash
python -m pip install -e .
```

Optional local backends can be installed as needed:

```bash
python -m pip install -e '.[audio,piper,nemotron,diarization,llm]'
```

Model downloads are intentionally explicit so deployments can prepare an offline
model cache. The default ASR target is `nvidia/nemotron-3.5-asr-streaming-0.6b`;
the default TTS target is Piper.

## CLI

Run an offline deterministic smoke demo without model downloads:

```bash
voice-interface demo --say "Hey computer, summarize the room notes."
```

Check optional backend guidance:

```bash
voice-interface doctor
```

## Python API

```python
from voice_interface.asr.nemotron import ScriptedASR
from voice_interface.conversation.loop import ConversationLoop
from voice_interface.tts.piper import PiperTTS

loop = ConversationLoop(ScriptedASR(["Hello computer."]), PiperTTS())
turns = loop.handle_audio([b"\1\0" * 800])
print(turns[0].assistant_text)
```

## Architecture

- `voice_interface.asr` contains the optional Nemotron adapter plus test/demo ASR.
- `voice_interface.audio` contains local VAD primitives.
- `voice_interface.tts` contains a Piper adapter with an offline fallback tone.
- `voice_interface.conversation` coordinates STT → responder/LLM → TTS.
- `voice_interface.plugins` registers local voice commands/actions.
- `voice_interface.gui` is reserved for lightweight Streamlit/Tauri frontends.

## Roadmap

1. Core Nemotron cache-aware streaming adapter and real microphone input.
2. Streaming Piper/StyleTTS output with robust barge-in playback controls.
3. Local diarization and speaker clustering for multi-human rooms.
4. Ollama/llama.cpp integration, persistent memory, GUI status display, and docs.

## Legacy prototype

The existing `limitless_drive` preservation index remains available through the
`limitless-index` console script while this repository evolves toward the local
voice-interface library.
