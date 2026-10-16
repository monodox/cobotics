"""Demo 3 — Batch policy evaluation at scale (standalone).

Scenario: run many randomized episodes through the simulator, score each one,
and summarize the batch. Designed to run as a Nebius Serverless Job for offline
evaluation; with --nebius it summarizes the results using NVIDIA Nemotron.

    python scripts/demo3.py                 # typing animation on
    python scripts/demo3.py --nebius        # Nemotron summary of the batch
    python scripts/demo3.py --fast          # disable the typing animation
    python scripts/demo3.py --episodes 100  # choose how many episodes to score
"""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

# Allow running without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rich.console import Console  # noqa: E402
from rich.panel import Panel  # noqa: E402
from rich.rule import Rule  # noqa: E402
from rich.table import Table  # noqa: E402

from cobotics.ai.base import Message  # noqa: E402
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
            title="demo 3 - batch policy evaluation",
        )
    )
    _sleep(SECTION_PAUSE)


def run_episode(seed: int) -> dict:
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
        "gripper": "closed" if world.gripper_closed else "open",
        "readings": view.as_dict(),
    }


def _score(episode: dict) -> float:
    return round(episode["battery"] - episode["steps"] * 2.0, 1)


def run(agent: Agent, label: str, episodes: int) -> None:
    section(
        f"[bold cyan]EVAL[/bold cyan] - scoring {episodes} episodes "
        "[dim](runs unchanged as a Nebius Serverless Job)[/dim]"
    )
    results = [run_episode(seed) for seed in range(episodes)]
    scores = [_score(e) for e in results]
    ranked = sorted(zip(scores, results), key=lambda t: t[0], reverse=True)

    stats = {
        "episodes": episodes,
        "best_score": max(scores),
        "worst_score": min(scores),
        "avg_score": round(sum(scores) / len(scores), 2),
    }

    table = Table(title="top 3 episodes by policy score")
    table.add_column("rank", style="cyan")
    table.add_column("score")
    table.add_column("steps")
    table.add_column("battery")
    for rank, (score, ep) in enumerate(ranked[:3], start=1):
        table.add_row(str(rank), str(score), str(ep["steps"]), str(ep["battery"]))
        _sleep(LINE_PAUSE)
    console.print(table)
    _sleep(SECTION_PAUSE)

    for key, value in stats.items():
        typeln(f"   [bold]{key}[/bold]: {value}")

    if not isinstance(agent._backend, StubBackend):  # type: ignore[attr-defined]
        section("[bold green]REASON[/bold green] - NVIDIA Nemotron evaluation summary")
        summary = agent._backend.complete(  # type: ignore[attr-defined]
            [
                Message("system", "You summarize robot policy-evaluation results."),
                Message("user", f"Summarize this evaluation in 2-3 sentences:\n{json.dumps(stats)}"),
            ]
        )
        typeln(f"   [green]Nemotron[/green] > {summary}")
    else:
        console.print(
            Panel.fit(
                "Evaluated the policy across the batch. Run with --nebius to add an "
                "NVIDIA Nemotron summary of the results.",
                border_style="green",
                title="evaluation done",
            )
        )


def main() -> None:
    global ANIMATE
    args = sys.argv[1:]
    if "--fast" in args or not sys.stdout.isatty():
        ANIMATE = False
    use_nebius = "--nebius" in args

    episodes = 30
    if "--episodes" in args:
        try:
            episodes = int(args[args.index("--episodes") + 1])
        except (IndexError, ValueError):
            pass

    agent, label = make_agent(use_nebius)
    header(label)
    run(agent, label, episodes)


if __name__ == "__main__":
    main()
