from voice_interface.audio.vad import EnergyVAD
from voice_interface.asr.nemotron import ScriptedASR
from voice_interface.cli import main
from voice_interface.conversation.loop import ConversationLoop
from voice_interface.plugins.registry import PluginRegistry, VoiceCommand
from voice_interface.tts.piper import PiperTTS


def test_scripted_conversation_loop_returns_spoken_turn():
    loop = ConversationLoop(ScriptedASR(["Open the lab notes."]), PiperTTS(), responder=lambda text: f"Action: {text}")

    turns = loop.handle_audio([b"\1\0" * 400])

    assert len(turns) == 1
    assert turns[0].user_text == "Open the lab notes."
    assert turns[0].assistant_text == "Action: Open the lab notes."


def test_energy_vad_detects_silence_and_speech():
    vad = EnergyVAD()

    assert not vad.analyze(b"\0\0" * 160).is_speech
    assert vad.analyze((10000).to_bytes(2, "little", signed=True) * 160).is_speech


def test_plugin_registry_dispatches_matching_voice_command():
    registry = PluginRegistry()
    registry.register(VoiceCommand("lights", "turn on lights", lambda text: f"matched {text}"))

    assert registry.dispatch("Please turn on lights in the room") == "matched Please turn on lights in the room"
    assert registry.dispatch("what time is it") is None


def test_cli_demo_outputs_transcript(capsys):
    assert main(["demo", "--say", "Testing local voice."]) == 0

    output = capsys.readouterr().out
    assert "user: Testing local voice." in output
    assert "assistant: I heard: Testing local voice." in output
