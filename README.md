# Cobotics

Interactive CLI for a **Physical AI Intelligence** system — reasoning over robots,
sensors, and actuators, with a built-in simulator so it runs with no real hardware.

Open source under the [MIT License](LICENSE).

Repository: https://github.com/monodox/cobotics

- Report a bug or request a feature: https://github.com/monodox/cobotics/issues/new
- Ask questions and share ideas: https://github.com/monodox/cobotics/discussions

## Features

- Hybrid command interface: slash-commands (`/help`, `/status`, `/move`) **and** natural language.
- Hardware abstraction layer (sensors / actuators) with a swappable simulator backend.
- Pluggable AI backend (stub by default; **Nebius Token Factory / NVIDIA Nemotron**, OpenAI, and Anthropic optional).
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
pip install -e ".[nebius]"     # Nebius Token Factory + NVIDIA Nemotron
pip install -e ".[openai]"
pip install -e ".[anthropic]"
pip install -e ".[dev]"        # tests
```

## Run

```bash
cobotics            # launch cobotics
# or without installing:
python -m cobotics
```

## Commands

| Command            | Description                              |
| ------------------ | ---------------------------------------- |
| `/help`            | Show available commands                  |
| `/status`          | Show registered devices and world state  |
| `/sensors`         | Read all sensors                         |
| `/move <x> <y>`    | Move the robot to a target position      |
| `/grip open\|close`| Operate the gripper                      |
| `/reset`           | Reset the simulator                      |
| `/exit`, `/quit`   | Exit cobotics                            |

Anything that is not a slash-command is treated as natural language and routed to
the AI agent.

## AI backends

Cobotics runs offline by default with a deterministic `stub` backend, so the
simulator works with no API key or network. Natural-language turns are
routed to whichever backend is configured.

### Nebius Token Factory (NVIDIA Nemotron)

Cobotics can drive its reasoning with an **NVIDIA Nemotron** open-source model
served by **Nebius Token Factory**. Token Factory exposes an OpenAI-compatible
chat completions API, so the `nebius` backend reaches it through the OpenAI SDK
pointed at the Nebius base URL.

```bash
pip install -e ".[nebius]"
```

Set the following (via environment or `.env`):

```bash
COBOTICS_AI_BACKEND=nebius
NEBIUS_API_KEY=your-token-factory-key
COBOTICS_AI_MODEL=nvidia/Llama-3_3-Nemotron-Super-49B-v1   # an NVIDIA Nemotron model
COBOTICS_NEBIUS_BASE_URL=https://api.studio.nebius.com/v1/ # default
```

Then launch Cobotics — natural-language input is answered by the Nemotron model
with live sensor context injected by the perception pipeline. Adjust
`COBOTICS_AI_MODEL` to whichever Nemotron model id Token Factory currently serves.

### OpenAI / Anthropic

Install the matching extra (`.[openai]` or `.[anthropic]`), set
`COBOTICS_AI_BACKEND` to `openai` or `anthropic`, provide the matching API key
(`OPENAI_API_KEY` / `ANTHROPIC_API_KEY`), and set `COBOTICS_AI_MODEL`.

## Layout

```
src/cobotics/
├── cli/          entry point + commands + rendering
├── core/         agent, intent parsing, session state
├── ai/           LLM backend interface + providers (stub/nebius/openai/anthropic)
├── hardware/     device/sensor/actuator abstractions + simulator
├── perception/   sensor data -> world state
├── control/      intents -> motion/commands
├── config/       settings + defaults
└── utils/        logging, errors
```

## Configuration

Copy `.env.example` to `.env` and adjust as needed. Defaults live in
`src/cobotics/config/defaults.yaml`.
