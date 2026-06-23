"""Command-line entry points for local voice-interface demos."""

from __future__ import annotations

import argparse

from voice_interface.asr.nemotron import ScriptedASR
from voice_interface.conversation.loop import ConversationLoop
from voice_interface.tts.piper import PiperTTS


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a local voice-interface demo or daemon.")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="Run an offline scripted full-duplex smoke demo")
    demo.add_argument("--say", default="Hello computer.", help="Scripted utterance to feed into the loop")
    sub.add_parser("doctor", help="Print optional backend installation guidance")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "doctor":
        print("Core package is installed. Optional extras: [nemotron], [piper], [audio], [diarization], [llm].")
        return 0
    loop = ConversationLoop(ScriptedASR([args.say]), PiperTTS())
    turns = loop.handle_audio([b"\1\0" * 800])
    for turn in turns:
        print(f"user: {turn.user_text}")
        print(f"assistant: {turn.assistant_text}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
