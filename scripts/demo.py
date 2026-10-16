"""Cobotics demo — the key application modules in action.

An interactive menu showcasing the full embodied loop:

    SENSE  -> REASON -> ACT

    SENSE   perception pipeline reads the simulated sensors
    REASON  the agent runtime, powered by an NVIDIA Nemotron model served on
            Nebius Token Factory (offline stub when not configured)
    ACT     the motion planner drives the actuators

Run from the project root:
    python scripts/demo.py              # interactive menu
    python scripts/demo.py --nebius     # reason with NVIDIA Nemotron on Nebius
    python scripts/demo.py 1            # run option 1 directly (non-interactive)

Options:
    1  Walkthrough      SENSE -> REASON -> ACT, one pass, fully labelled
    2  Batch processing simulate many episodes and process sensor data at scale
                        (the same worker runs unchanged as a Nebius Serverless Job)
    3  Reasoning chat   a few natural-language turns through the agent runtime
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

# Allow running without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rich.console import Console  # noqa: E402
from rich.panel import Panel  # noqa: E402
from rich.rule import Rule  # noqa: E402
from rich.table import Table  # noqa: E402

from cobotics.ai.base import Message  # noqa: E402
from cobotics.ai.providers import (  # noqa: E402
    DEFAULT_NEBIUS_MODEL,
    StubBackend,
    build_backend,
)
from cobotics.config.settings import Settings  # noqa: E402
from cobotics.control.planner import MotionPlanner  # noqa: E402
from cobotics.core.agent import Agent  # noqa: E402
from cobotics.hardware.simulator import build_simulator  # noqa: E402
from cobotics.perception.pipeline import PerceptionPipeline  # noqa: E402

console = Console()
ARROW = "->"


# --------------------------------------------------------------------------- #
# Backend selection — prefer NVIDIA Nemotron on Nebius when configured.
# --------------------------------------------------------------------------- #
def make_agent(use_nebius: bool) -> tuple[Agent, str]:
    if use_nebius:
        backend = build_backend(Settings(ai_backend="nebius"))
        label = f"Nebius Token Factory {ARROW} NVIDIA {backend._model}"  # type: ignore[attr-defined]
    else:
        backend = StubBackend()
        label = (
            "offline stub (run with --nebius or COBOTICS_AI_BACKEND=nebius for "
            f"NVIDIA Nemotron: {DEFAULT_NEBIUS_MODEL})"
        )

    registry, _world = build_simulator()
    agent = Agent(
        backend=backend,
        perception=PerceptionPipeline(registry),
        planner=MotionPlanner(registry),
    )
    return agent, label


def header(backend_label: str) -> None:
    console.print(
        Panel.fit(
            "[bold]Cobotics[/bold] - Physical AI Intelligence\n"
            f"[dim]SENSE {ARROW} REASON {ARROW} ACT[/dim]\n\n"
            "Reasoning powered by [bold green]NVIDIA Nemotron[/bold green]\n"
            "served on [bold cyan]Nebius Token Factory[/bold cyan]\n\n"
            f"[dim]backend: {backend_label}[/dim]",
            border_style="cyan",
            title="key application modules",
        )
    )


# --------------------------------------------------------------------------- #
# Option 1 — SENSE -> REASON -> ACT walkthrough
# --------------------------------------------------------------------------- #
def _sense(agent: Agent, label: str) -> None:
    console.print(Rule(f"[bold cyan]SENSE[/bold cyan] - perception pipeline ({label})"))
    for _, reading in agent.perception.perceive().readings.items():
        console.print(f"   {reading}")


def _reason(agent: Agent, prompt: str, backend_label: str) -> None:
    console.print(
        Rule(f"[bold green]REASON[/bold green] - agent runtime [dim]({backend_label})[/dim]")
    )
    console.print(f"   [dim]user[/dim]  > {prompt}")
    console.print(f"   [green]cobotics[/green] > {agent.chat(prompt)}")


def _act(description: str, result: dict) -> None:
    console.print(Rule(f"[bold magenta]ACT[/bold magenta] - motion planner ({description})"))
    for key, value in result.items():
        console.print(f"   [bold]{key}[/bold]: {value}")


def option_walkthrough(agent: Agent, backend_label: str) -> None:
    _sense(agent, "initial state")
    _reason(agent, "What should I check before moving?", backend_label)
    _act("drive to (3, 4)", agent.planner.move_to(3.0, 4.0))
    _act("close gripper", agent.planner.grip("close"))
    _sense(agent, "after acting")
    console.print(
        Panel.fit(
            f"Embodied loop complete: sensed {ARROW} reasoned with NVIDIA Nemotron "
            f"on Nebius Token Factory {ARROW} acted on the actuators.",
            border_style="green",
            title="done",
        )
    )


# --------------------------------------------------------------------------- #
# Option 2 — batch sensor-data processing (runs as a Nebius Serverless Job)
# --------------------------------------------------------------------------- #
def _run_episode(seed: int) -> dict:
    rng = random.Random(seed)
    registry, world = build_simulator(bounds=(10.0, 10.0))
    perception = PerceptionPipeline(registry)
    planner = MotionPlanner(registry)

    steps = rng.randint(2, 6)
    for _ in range(steps):
        planner.move_to(rng.uniform(0, 10), rng.uniform(0, 10))
    planner.grip(rng.choice(["open", "close"]))

    view = perception.perceive()
    return {
        "seed": seed,
        "steps": steps,
        "battery": round(world.battery, 1),
        "position": [round(p, 2) for p in world.position],
        "gripper": "closed" if world.gripper_closed else "open",
        "readings": view.as_dict(),
    }


def option_batch(agent: Agent, backend_label: str, episodes: int = 20) -> None:
    console.print(
        Rule(
            f"[bold cyan]BATCH[/bold cyan] - processing {episodes} episodes "
            "[dim](runs unchanged as a Nebius Serverless Job)[/dim]"
        )
    )
    results = [_run_episode(seed) for seed in range(episodes)]
    batteries = [e["battery"] for e in results]
    stats = {
        "episodes": len(results),
        "avg_battery_remaining": round(sum(batteries) / len(batteries), 2),
        "min_battery_remaining": min(batteries),
        "gripper_closed_count": sum(1 for e in results if e["gripper"] == "closed"),
    }

    table = Table(title="aggregate statistics")
    table.add_column("metric", style="cyan")
    table.add_column("value")
    for key, value in stats.items():
        table.add_row(key, str(value))
    console.print(table)

    # Summarize the batch with NVIDIA Nemotron on Nebius when the backend is real.
    if not isinstance(agent._backend, StubBackend):  # type: ignore[attr-defined]
        console.print(
            Rule("[bold green]REASON[/bold green] - NVIDIA Nemotron batch summary")
        )
        summary = agent._backend.complete(  # type: ignore[attr-defined]
            [
                Message("system", "You summarize robotics batch-processing results."),
                Message("user", f"Summarize these stats in 2-3 sentences:\n{json.dumps(stats)}"),
            ]
        )
        console.print(f"   [green]Nemotron[/green] > {summary}")
    else:
        console.print(
            "[dim]   (run with --nebius to summarize this batch with "
            "NVIDIA Nemotron on Nebius Token Factory)[/dim]"
        )


# --------------------------------------------------------------------------- #
# Option 3 — reasoning chat
# --------------------------------------------------------------------------- #
def option_chat(agent: Agent, backend_label: str) -> None:
    console.print(
        Rule(f"[bold green]REASON[/bold green] - agent runtime [dim]({backend_label})[/dim]")
    )
    for prompt in (
        "hello",
        "how do I move the robot?",
        "what is the battery level?",
    ):
        console.print(f"   [dim]user[/dim]  > {prompt}")
        console.print(f"   [green]cobotics[/green] > {agent.chat(prompt)}\n")


# --------------------------------------------------------------------------- #
# Menu driver
# --------------------------------------------------------------------------- #
OPTIONS = {
    "1": ("Walkthrough   (SENSE -> REASON -> ACT)", option_walkthrough),
    "2": ("Batch processing  (Nebius Serverless Job style)", option_batch),
    "3": ("Reasoning chat    (NVIDIA Nemotron on Nebius)", option_chat),
}


def _print_menu() -> None:
    console.print("\n[bold]Choose a demo:[/bold]")
    for key, (title, _) in OPTIONS.items():
        console.print(f"   [cyan]{key}[/cyan]  {title}")
    console.print("   [cyan]q[/cyan]  quit")


def main() -> None:
    args = [a for a in sys.argv[1:]]
    use_nebius = "--nebius" in args
    preset = next((a for a in args if a in OPTIONS), None)

    agent, backend_label = make_agent(use_nebius)
    header(backend_label)

    # Non-interactive: a numeric arg runs that option once and exits.
    if preset:
        OPTIONS[preset][1](agent, backend_label)
        return

    # Interactive menu loop.
    while True:
        _print_menu()
        try:
            choice = console.input("\n[bold cyan]demo>[/bold cyan] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            console.print("\nBye.")
            return
        if choice in ("q", "quit", "exit"):
            console.print("Bye.")
            return
        if choice in OPTIONS:
            console.print()
            # Fresh agent per run so each demo starts from a clean world.
            agent, backend_label = make_agent(use_nebius)
            OPTIONS[choice][1](agent, backend_label)
        else:
            console.print("[yellow]Pick 1, 2, 3, or q.[/yellow]")


if __name__ == "__main__":
    main()
