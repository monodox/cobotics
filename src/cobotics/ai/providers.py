"""Concrete AI backends: stub (offline), OpenAI, Anthropic."""

from __future__ import annotations

from cobotics.ai.base import LLMBackend, Message
from cobotics.config.settings import Settings
from cobotics.utils.errors import AIBackendError


class StubBackend(LLMBackend):
    """Offline backend. Deterministic, no network, no API key.

    Good enough to drive the shell and demo the flow end-to-end.
    """

    def complete(self, messages: list[Message]) -> str:
        last_user = next(
            (m.content for m in reversed(messages) if m.role == "user"), ""
        )
        text = last_user.lower().strip()

        if not text:
            return "I'm listening. Tell me what to do, or type /help."
        if any(k in text for k in ("hello", "hi", "hey")):
            return "Hello. I'm cobotics. Ask me to move, grip, or read sensors."
        if "battery" in text:
            return "Use /status or /sensors to see the live battery level."
        if any(k in text for k in ("move", "go", "drive")):
            return "To move, use `/move <x> <y>` — e.g. `/move 3 4`."
        if "grip" in text or "grab" in text:
            return "Use `/grip open` or `/grip close` to operate the gripper."
        if "help" in text:
            return "Type /help for commands, or just describe a task."
        return (
            "[stub AI] I understood: "
            f"'{last_user}'. Configure a real backend "
            "(COBOTICS_AI_BACKEND=openai|anthropic) for full reasoning."
        )


class OpenAIBackend(LLMBackend):
    def __init__(self, settings: Settings) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - optional dep
            raise AIBackendError(
                "openai package not installed. Run: pip install -e '.[openai]'"
            ) from exc
        if not settings.openai_api_key:
            raise AIBackendError("OPENAI_API_KEY is not set.")
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._model = settings.ai_model

    def complete(self, messages: list[Message]) -> str:  # pragma: no cover - network
        resp = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
        )
        return resp.choices[0].message.content or ""


class AnthropicBackend(LLMBackend):
    def __init__(self, settings: Settings) -> None:
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover - optional dep
            raise AIBackendError(
                "anthropic package not installed. Run: pip install -e '.[anthropic]'"
            ) from exc
        if not settings.anthropic_api_key:
            raise AIBackendError("ANTHROPIC_API_KEY is not set.")
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self._model = settings.ai_model

    def complete(self, messages: list[Message]) -> str:  # pragma: no cover - network
        system = "\n".join(m.content for m in messages if m.role == "system")
        convo = [
            {"role": m.role, "content": m.content}
            for m in messages
            if m.role != "system"
        ]
        resp = self._client.messages.create(
            model=self._model,
            system=system or None,
            messages=convo,
            max_tokens=1024,
        )
        return "".join(block.text for block in resp.content if block.type == "text")


def build_backend(settings: Settings) -> LLMBackend:
    """Factory: pick a backend from settings."""
    backend = settings.ai_backend.lower()
    if backend == "stub":
        return StubBackend()
    if backend == "openai":
        return OpenAIBackend(settings)
    if backend == "anthropic":
        return AnthropicBackend(settings)
    raise AIBackendError(f"Unknown AI backend: {settings.ai_backend!r}")
