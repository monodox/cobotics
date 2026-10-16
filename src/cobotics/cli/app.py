"""CLI entry point: builds the system and launches the interactive shell."""

from __future__ import annotations

import typer

from cobotics.ai.providers import build_backend
from cobotics.cli import render
from cobotics.cli.shell import run_shell
from cobotics.config.settings import get_settings
from cobotics.control.planner import MotionPlanner
from cobotics.core.agent import Agent
from cobotics.hardware.simulator import build_simulator
from cobotics.perception.pipeline import PerceptionPipeline
from cobotics.utils.errors import CoboticsError
from cobotics.utils.logging import setup_logging

app = typer.Typer(
    add_completion=False,
    help="cobotics - interactive CLI for a Physical AI Intelligence system.",
)


def _build_agent() -> Agent:
    settings = get_settings()
    setup_logging(settings.log_level)

    if settings.hardware_backend != "simulator":
        raise CoboticsError(
            f"Hardware backend '{settings.hardware_backend}' is not wired up yet. "
            "Use the simulator (COBOTICS_HARDWARE_BACKEND=simulator)."
        )

    registry, _world = build_simulator(
        bounds=settings.world_bounds,
        start_position=settings.start_position,
        move_speed=settings.move_speed,
    )
    perception = PerceptionPipeline(registry)
    planner = MotionPlanner(registry)
    backend = build_backend(settings)

    render.info(f"AI backend: {backend.name}  |  hardware: {settings.hardware_backend}")
    return Agent(backend=backend, perception=perception, planner=planner)


@app.command()
def shell() -> None:
    """Launch the interactive cobotics shell (default)."""
    try:
        agent = _build_agent()
    except CoboticsError as exc:
        render.error(str(exc))
        raise typer.Exit(code=1)
    run_shell(agent)


def main() -> None:
    """Console-script entry point.

    If invoked with no subcommand, default to the interactive shell.
    """
    import sys

    if len(sys.argv) == 1:
        shell()
    else:
        app()


if __name__ == "__main__":
    main()
