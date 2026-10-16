"""Rich-based rendering helpers for the shell."""

from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def banner() -> None:
    console.print(
        Panel.fit(
            "[bold cyan]cobotics[/bold cyan]  "
            "[dim]Physical AI Intelligence shell[/dim]\n"
            "Type [bold]/help[/bold] for commands, or just talk. "
            "[bold]/exit[/bold] to quit.",
            border_style="cyan",
        )
    )


def info(msg: str) -> None:
    console.print(f"[cyan]{msg}[/cyan]")


def warn(msg: str) -> None:
    console.print(f"[yellow]{msg}[/yellow]")


def error(msg: str) -> None:
    console.print(f"[red]{msg}[/red]")


def assistant(msg: str) -> None:
    console.print(f"[green]cobotics[/green] › {msg}")


def result(data: dict[str, Any]) -> None:
    table = Table(show_header=False, box=None, padding=(0, 1))
    for key, value in data.items():
        table.add_row(f"[bold]{key}[/bold]", str(value))
    console.print(table)


def device_table(rows: list[dict[str, Any]]) -> None:
    if not rows:
        warn("No devices registered.")
        return
    table = Table(title="Devices")
    table.add_column("name", style="cyan")
    table.add_column("kind")
    table.add_column("state")
    for row in rows:
        state = {k: v for k, v in row.items() if k not in ("name", "kind")}
        table.add_row(row.get("name", "?"), row.get("kind", "?"), str(state))
    console.print(table)
