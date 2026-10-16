# cobotics

Interactive CLI for a **Physical AI Intelligence** system — reasoning over robots,
sensors, and actuators, with a built-in simulator so it runs with no real hardware.

## Features

- Interactive hybrid shell: slash-commands (`/help`, `/status`, `/move`) **and** natural language.
- Hardware abstraction layer (sensors / actuators) with a swappable simulator backend.
- Pluggable AI backend (stub by default; OpenAI/Anthropic optional).
- Config- and env-driven via `pydantic-settings`.

## Install

```bash
# from the project root
python -m venv .venv
.venv\Scripts\activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .
```

Optional AI backends:

```bash
pip install -e ".[openai]"
pip install -e ".[anthropic]"
pip install -e ".[dev]"        # tests
```

## Run

```bash
cobotics            # launch the interactive shell
# or without installing:
python -m cobotics
```

## Shell commands

| Command            | Description                              |
| ------------------ | ---------------------------------------- |
| `/help`            | Show available commands                  |
| `/status`          | Show registered devices and world state  |
| `/sensors`         | Read all sensors                         |
| `/move <x> <y>`    | Move the robot to a target position      |
| `/grip open\|close`| Operate the gripper                      |
| `/reset`           | Reset the simulator                      |
| `/exit`, `/quit`   | Leave the shell                          |

Anything that is not a slash-command is treated as natural language and routed to
the AI agent.

## Layout

```
src/cobotics/
├── cli/          interactive shell + commands + rendering
├── core/         agent, intent parsing, session state
├── ai/           LLM backend interface + providers (stub/openai/anthropic)
├── hardware/     device/sensor/actuator abstractions + simulator
├── perception/   sensor data -> world state
├── control/      intents -> motion/commands
├── config/       settings + defaults
└── utils/        logging, errors
```

## Configuration

Copy `.env.example` to `.env` and adjust as needed. Defaults live in
`src/cobotics/config/defaults.yaml`.
