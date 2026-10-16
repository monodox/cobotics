"""Parse raw user input into a structured intent.

Slash-prefixed input becomes a COMMAND intent; everything else is CHAT, routed
to the AI agent.
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass, field
from enum import Enum


class IntentKind(str, Enum):
    COMMAND = "command"
    CHAT = "chat"
    EMPTY = "empty"


@dataclass
class Intent:
    kind: IntentKind
    command: str = ""
    args: list[str] = field(default_factory=list)
    text: str = ""


def parse(raw: str) -> Intent:
    stripped = raw.strip()
    if not stripped:
        return Intent(kind=IntentKind.EMPTY)

    if stripped.startswith("/"):
        try:
            parts = shlex.split(stripped[1:])
        except ValueError:
            parts = stripped[1:].split()
        if not parts:
            return Intent(kind=IntentKind.EMPTY)
        return Intent(
            kind=IntentKind.COMMAND,
            command=parts[0].lower(),
            args=parts[1:],
            text=stripped,
        )

    return Intent(kind=IntentKind.CHAT, text=stripped)
