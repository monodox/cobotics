"""Interactive REPL loop."""

from __future__ import annotations

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory

from cobotics.cli import commands, render
from cobotics.cli.commands import CommandContext
from cobotics.core.agent import Agent
from cobotics.core.intent import IntentKind, parse


def _completer() -> WordCompleter:
    words = [f"/{c}" for c in commands.known_commands()]
    return WordCompleter(words, ignore_case=True, sentence=True)


def run_shell(agent: Agent) -> None:
    """Start the interactive loop. Blocks until the user exits."""
    render.banner()

    ctx = CommandContext(agent=agent)
    session: PromptSession = PromptSession(
        history=InMemoryHistory(),
        auto_suggest=AutoSuggestFromHistory(),
        completer=_completer(),
    )

    running = True
    while running:
        try:
            raw = session.prompt("cobotics> ")
        except (EOFError, KeyboardInterrupt):
            render.info("\nGoodbye.")
            break

        intent = parse(raw)

        if intent.kind is IntentKind.EMPTY:
            continue
        if intent.kind is IntentKind.COMMAND:
            running = commands.dispatch(ctx, intent)
            continue

        # CHAT -> AI agent
        try:
            reply = agent.chat(intent.text)
            render.assistant(reply)
        except Exception as exc:  # keep the shell alive on backend failures
            render.error(f"AI error: {exc}")
