# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project

Cobotics is an interactive CLI for a Physical AI Intelligence system — reasoning
over robots, sensors, and actuators, with a built-in simulator so it runs with
no real hardware. Python, `src/` layout, packaged with setuptools.

## Layout

```
src/cobotics/
├── cli/          entry point (app.py), REPL loop (shell.py), commands, rendering
├── core/         agent, intent parsing, session state
├── ai/           LLMBackend interface + providers (stub/nebius/openai/anthropic)
├── hardware/     device/sensor/actuator abstractions + simulator
├── perception/   sensor data -> world state
├── control/      intents -> motion/commands
├── config/       pydantic-settings + defaults.yaml
└── utils/        logging, errors
tests/            pytest suite (offline, no network)
scripts/demo.py   non-interactive walkthrough against the simulator
```

## Conventions

- Python >= 3.9. Use `from __future__ import annotations` and type hints.
- Keep the import/package name **lowercase** `cobotics`. The display name in
  user-facing text and docs is capitalized **Cobotics**.
- Match existing style: docstrings on public classes/functions, `rich`/`typer`
  patterns already in the repo, small focused modules.
- Settings are env-driven with the `COBOTICS_` prefix; API keys use their raw
  env names (`NEBIUS_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).

## Hard rules

- The default AI backend must stay `stub` so the app and tests run **offline**
  with no API key or network. Nebius/OpenAI/Anthropic are opt-in.
- Tests must not make real network calls.
- Never commit real API keys. Use placeholders in `.env.example` only;
  machine-specific secrets go in the git-ignored `.env.local`.

## Setup, test, run

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest -q                     # run the suite
python scripts/demo.py        # offline sanity check
cobotics                      # launch the CLI
```

## Before you finish

- Run `pytest -q` and ensure it passes.
- Keep changes minimal and consistent with surrounding code.
- Update `CHANGELOG.md` under "Unreleased" for user-visible changes.
