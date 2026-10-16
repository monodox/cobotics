"""Slash-command handlers for the interactive shell."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from cobotics.cli import render
from cobotics.core.agent import Agent
from cobotics.core.intent import Intent
from cobotics.utils.errors import CoboticsError

# A handler returns True to keep the shell running, False to exit.
Handler = Callable[["CommandContext", Intent], bool]


@dataclass
class CommandContext:
    agent: Agent


_HANDLERS: dict[str, Handler] = {}
_HELP: dict[str, str] = {}


def command(name: str, help_text: str):
    def deco(fn: Handler) -> Handler:
        _HANDLERS[name] = fn
        _HELP[name] = help_text
        return fn

    return deco


@command("help", "Show this help")
def _help(ctx: CommandContext, intent: Intent) -> bool:
    rows = {f"/{name}": text for name, text in sorted(_HELP.items())}
    render.info("Available commands:")
    render.result(rows)
    render.info("Anything else is sent to the AI agent as natural language.")
    return True


@command("exit", "Leave the shell")
def _exit(ctx: CommandContext, intent: Intent) -> bool:
    render.info("Goodbye.")
    return False


@command("quit", "Leave the shell")
def _quit(ctx: CommandContext, intent: Intent) -> bool:
    return _exit(ctx, intent)


@command("status", "Show devices and world state")
def _status(ctx: CommandContext, intent: Intent) -> bool:
    rows = []
    for device in ctx.agent.planner.registry.all():
        status = device.status()
        status["kind"] = device.kind.value
        rows.append(status)
    render.device_table(rows)
    return True


@command("sensors", "Read all sensors")
def _sensors(ctx: CommandContext, intent: Intent) -> bool:
    view = ctx.agent.perception.perceive()
    if not view.readings:
        render.warn("No sensors registered.")
        return True
    render.result({name: str(r) for name, r in view.readings.items()})
    return True


@command("move", "Move the robot: /move <x> <y>")
def _move(ctx: CommandContext, intent: Intent) -> bool:
    if len(intent.args) != 2:
        render.error("Usage: /move <x> <y>   e.g. /move 3 4")
        return True
    try:
        x, y = float(intent.args[0]), float(intent.args[1])
    except ValueError:
        render.error("x and y must be numbers.")
        return True
    try:
        result = ctx.agent.planner.move_to(x, y)
        render.result(result)
    except CoboticsError as exc:
        render.error(str(exc))
    return True


@command("grip", "Operate the gripper: /grip open|close")
def _grip(ctx: CommandContext, intent: Intent) -> bool:
    if len(intent.args) != 1 or intent.args[0].lower() not in {"open", "close"}:
        render.error("Usage: /grip open|close")
        return True
    try:
        result = ctx.agent.planner.grip(intent.args[0].lower())
        render.result(result)
    except (CoboticsError, ValueError) as exc:
        render.error(str(exc))
    return True


@command("reset", "Reset conversation and world view")
def _reset(ctx: CommandContext, intent: Intent) -> bool:
    ctx.agent.session.reset()
    from cobotics.ai.prompts import SYSTEM_PROMPT

    ctx.agent.session.add("system", SYSTEM_PROMPT)
    render.info("Session reset.")
    return True


def dispatch(ctx: CommandContext, intent: Intent) -> bool:
    """Run a command intent. Returns False to stop the shell."""
    handler = _HANDLERS.get(intent.command)
    if handler is None:
        render.error(f"Unknown command: /{intent.command}. Try /help.")
        return True
    return handler(ctx, intent)


def known_commands() -> list[str]:
    return sorted(_HANDLERS.keys())
