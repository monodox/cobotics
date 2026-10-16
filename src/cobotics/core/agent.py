"""The agent ties AI reasoning, perception, and control together."""

from __future__ import annotations

from cobotics.ai.base import LLMBackend, Message
from cobotics.ai.prompts import SYSTEM_PROMPT, world_context
from cobotics.control.planner import MotionPlanner
from cobotics.core.session import Session
from cobotics.perception.pipeline import PerceptionPipeline
from cobotics.utils.logging import get_logger

log = get_logger("agent")


class Agent:
    """Routes chat to the LLM (with live world context) and exposes actions."""

    def __init__(
        self,
        backend: LLMBackend,
        perception: PerceptionPipeline,
        planner: MotionPlanner,
        session: Session | None = None,
    ) -> None:
        self._backend = backend
        self._perception = perception
        self._planner = planner
        self.session = session or Session()
        self.session.add("system", SYSTEM_PROMPT)

    @property
    def perception(self) -> PerceptionPipeline:
        return self._perception

    @property
    def planner(self) -> MotionPlanner:
        return self._planner

    def chat(self, text: str) -> str:
        """Handle a natural-language turn, injecting current world state."""
        view = self._perception.perceive()
        context = world_context(view.as_dict())

        self.session.add("user", text)

        messages: list[Message] = self.session.messages()
        # splice a fresh context message right before the latest user turn
        messages = messages[:-1] + [Message("system", context), messages[-1]]

        log.debug("querying backend %s", self._backend.name)
        reply = self._backend.complete(messages)
        self.session.add("assistant", reply)
        return reply
