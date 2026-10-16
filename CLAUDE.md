# CLAUDE.md

This project's agent guidance lives in [AGENTS.md](AGENTS.md). Please read it
before making changes.

Quick reminders:

- Import/package name is lowercase `cobotics`; the display name is `Cobotics`.
- The default AI backend is `stub` and must keep working **offline** (no key,
  no network). Nebius Token Factory (NVIDIA Nemotron), OpenAI, and Anthropic are
  opt-in.
- Tests must not make network calls. Run `pytest -q` before finishing.
