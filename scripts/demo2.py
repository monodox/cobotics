"""Demo 2 — Patrol / waypoint mission (standalone).

Scenario: the robot visits a sequence of waypoints, sensing at each one. Before
every leg it reasons (NVIDIA Nemotron on Nebius Token Factory) and checks whether
the battery is sufficient to continue — sense-reason-act in a loop.

    python scripts/demo2.py            # typing animation on
    python scripts/demo2.py --nebius   # reason with NVIDIA Nemotron on Nebius
    python scripts/demo2.py --fast     # disable the typing animation
"""

from __future__ import annotations

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

WAYPOINTS = [(2.0, 2.0), (8.0, 1.0), (9.0, 9.0), (1.0, 7.0)]
LOW_BATTERY = 95.0


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
            title="demo 2 - patrol mission",
        )
    )
    _sleep(SECTION_PAUSE)


def sense(agent: Agent, label: str) -> None:
    section(f"[bold cyan]SENSE[/bold cyan] - perception pipeline ({label})")
    for _, reading in agent.perception.perceive().readings.items():
        typeln(f"   {reading}")


def reason(agent: Agent, prompt: str, label: str) -> None:
    section(f"[bold green]REASON[/bold green] - agent runtime [dim]({label})[/dim]")
    typeln(f"   [dim]user[/dim]  > {prompt}")
    typeln(f"   [green]cobotics[/green] > {agent.chat(prompt)}")


def run(agent: Agent, label: str) -> None:
    sense(agent, "mission start")
    reason(agent, f"Patrol these waypoints in order: {WAYPOINTS}. What should I watch?", label)

    for i, wp in enumerate(WAYPOINTS, start=1):
        battery = agent.perception.perceive().get("battery")
        section(
            f"[bold yellow]LEG {i}/{len(WAYPOINTS)}[/bold yellow] - "
            f"waypoint {wp} [dim](battery {battery}%)[/dim]"
        )
        if battery is not None and battery < LOW_BATTERY:
            typeln(f"   [red]battery {battery}% below {LOW_BATTERY}% - aborting patrol[/red]")
            break
        result = agent.planner.move_to(*wp)
        typeln(f"   arrived {result['to']}  (drove {result['distance']} m)")
        reading = agent.perception.perceive().readings.get("range")
        if reading:
            typeln(f"   sensed {reading}")
    else:
        console.print(
            Panel.fit(
                f"Patrol complete: visited all {len(WAYPOINTS)} waypoints.",
                border_style="green",
                title="mission done",
            )
        )
        return

    console.print(
        Panel.fit(
            "Patrol ended early on a low-battery check.",
            border_style="yellow",
            title="mission halted",
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
