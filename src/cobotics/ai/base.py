"""LLM backend interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Message:
    role: str   # "system" | "user" | "assistant"
    content: str


class LLMBackend(ABC):
    """Minimal interface every AI backend must implement."""

    @abstractmethod
    def complete(self, messages: list[Message]) -> str:
        """Return the assistant's reply for the given message history."""

    @property
    def name(self) -> str:
        return self.__class__.__name__
