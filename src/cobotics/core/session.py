"""Conversation + runtime state for a shell session."""

from __future__ import annotations

from dataclasses import dataclass, field

from cobotics.ai.base import Message


@dataclass
class Session:
    """Holds the rolling conversation history."""

    history: list[Message] = field(default_factory=list)
    max_turns: int = 40

    def add(self, role: str, content: str) -> None:
        self.history.append(Message(role=role, content=content))
        # keep only the most recent turns (plus any leading system message)
        if len(self.history) > self.max_turns:
            head = self.history[:1] if self.history[0].role == "system" else []
            self.history = head + self.history[-self.max_turns :]

    def messages(self) -> list[Message]:
        return list(self.history)

    def reset(self) -> None:
        self.history.clear()
