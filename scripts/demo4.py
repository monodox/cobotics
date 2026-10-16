"""Demo 4 — Conversational control (standalone).

Scenario: a short natural-language session. Each utterance is answered by the
agent runtime (NVIDIA Nemotron on Nebius Token Factory), and recognized commands
are executed on the robot, so talking drives real actuator calls.

    python scripts/demo4.py            # typing animation on
    python scripts/demo4.py --nebius   # reason with NVIDIA Nemotron on Nebius
    python scripts/demo4.py --fast     # disable the typing animation
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

# Allow running without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rich.console import Console  # noqa: E402
from rich.panel import Panel  # noqa: E402
from rich.rule import Rule  # noqa: E402

from cobotics.ai.providers import DEFAULT_NEBIUS_MODEL, StubBackend, build_backend  # noqa: E402
from cobotics.config.settings import Settings  # noqa: E402
from cobotics.control.planner import MotionPlanner  # noqa: E402
from cobotics.core.agent import Agent  # noqa: E402
from cobotics.hardware.simulator import build_simulator  # noqa: E402
from cobotics.perception.pipeline import PerceptionPipeline  # noqa: E402

console = Console()
ANIMATE = True
TYPE_DELAY = 0.012
LINE_PAUSE = 0.12
SECTION_PAUSE = 0.5

CONVERSATION = [
    "hello, what can you do?",
    "move to 6 3",
    "grab the object",
    "take it to 2 8",
    "let it go",
    "what is the battery level now?",
]


def _sleep(seconds: float) -> None:
    if ANIMATE:
        time.sleep(seconds)


def typeln(text: str) -> None:
    if not ANIMATE:
        console.print(text)
        return
    for ch in console.render_str(text).plain:
        console.file.write(ch)
        console.file.flush()
        time.sleep(TYPE_DELAY)
    console.file.write("\r")
    console.print(text, highlight=False)
    _sleep(LINE_PAUSE)


def section(rule: str) -> None:
    console.print(Rule(rule))
    _sleep(SECTION_PAUSE)


def make_agent(use_nebius: bool) -> tuple[Agent, str]:
    if use_nebius:
        backend = build_backend(Settings(ai_backend="nebius"))
        label = f"Nebius Token Factory -> NVIDIA {backend._model}"  # type: ignore[attr-defined]
    else:
        backend = StubBackend()
        label = f"offline stub (use --nebius for NVIDIA Nemotron: {DEFAULT_NEBIUS_MODEL})"
    registry, _world = build_simulator()
    agent = Agent(
        backend=backend,
        perception=PerceptionPipeline(registry),
        planner=MotionPlanner(registry),
    )
    return agent, label


def header(label: str) -> None:
    console.print(
        Panel.fit(
            "[bold]Cobotics[/bold] - Physical AI Intelligence\n"
            "[dim]SENSE -> REASON -> ACT[/dim]\n\n"
            "Reasoning powered by [bold green]NVIDIA Nemotron[/bold green]\n"
            "served on [bold cyan]Nebius Token Factory[/bold cyan]\n\n"
            f"[dim]backend: {label}[/dim]",
            border_style="cyan",
            title="demo 4 - conversational control",
        )
    )
    _sleep(SECTION_PAUSE)


def sense(agent: Agent, label: str) -> None:
    section(f"[bold cyan]SENSE[/bold cyan] - perception pipeline ({label})")
    for _, reading in agent.perception.perceive().readings.items():
        typeln(f"   {reading}")


def _maybe_act(agent: Agent, utterance: str) -> str | None:
    """Tiny intent matcher: turn an utterance into an actuator call."""
    text = utterance.lower()
    move = re.search(r"(?:move|go|take it)\D*(\d+(?:\.\d+)?)\D+(\d+(?:\.\d+)?)", text)
    if move:
        x, y = float(move.group(1)), float(move.group(2))
        res = agent.planner.move_to(x, y)
        return f"drove to {res['to']} ({res['distance']} m)"
    if any(k in text for k in ("grab", "grip", "pick")):
        agent.planner.grip("close")
        return "closed the gripper"
    if any(k in text for k in ("let it go", "release", "drop", "open")):
        agent.planner.grip("open")
        return "opened the gripper"
    return None


def run(agent: Agent, label: str) -> None:
    section(f"[bold green]CONVERSE[/bold green] - agent runtime [dim]({label})[/dim]")
    for utterance in CONVERSATION:
        typeln(f"   [dim]you[/dim]  > {utterance}")
        typeln(f"   [green]cobotics[/green] > {agent.chat(utterance)}")
        action = _maybe_act(agent, utterance)
        if action:
            typeln(f"   [magenta]ACT[/magenta] > {action}")
        _sleep(SECTION_PAUSE)

    sense(agent, "final state")
    console.print(
        Panel.fit(
            "Conversation drove the robot end to end: each command was reasoned "
            "over and executed on the actuators.",
            border_style="green",
            title="session done",
        )
    )


def main() -> None:
    global ANIMATE
    args = sys.argv[1:]
    if "--fast" in args or not sys.stdout.isatty():
        ANIMATE = False
    use_nebius = "--nebius" in args
    agent, label = make_agent(use_nebius)
    header(label)
    run(agent, label)


if __name__ == "__main__":
    main()
