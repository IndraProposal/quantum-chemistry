"""Simple local voice action plugin registry."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VoiceCommand:
    name: str
    phrase: str
    handler: Callable[[str], str]


class PluginRegistry:
    def __init__(self) -> None:
        self._commands: list[VoiceCommand] = []

    def register(self, command: VoiceCommand) -> None:
        self._commands.append(command)

    def dispatch(self, text: str) -> str | None:
        normalized = text.casefold()
        for command in self._commands:
            if command.phrase.casefold() in normalized:
                return command.handler(text)
        return None
