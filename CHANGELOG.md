# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nebius Token Factory AI backend that calls an NVIDIA Nemotron model through
  the OpenAI-compatible inference API (`COBOTICS_AI_BACKEND=nebius`).
- `[nebius]` optional dependency extra.
- GitHub Actions CI running the test suite on Python 3.9–3.13.
- MIT `LICENSE`.
- Project docs: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md`, `ROADMAP.md`, `SECURITY.md`.
- `.env.local` support (git-ignored) for machine-specific secrets.

### Changed
- README documents the Nebius/Nemotron backend and the project repository URL.
- User-facing display name capitalized as "Cobotics" (package/import name
  remains lowercase `cobotics`).

## [0.1.0] - 2026-10-16

### Added
- Initial release: interactive CLI for a Physical AI Intelligence system.
- Hybrid command interface (slash-commands + natural language).
- Hardware abstraction layer with a built-in simulator (position, battery,
  range sensors; drive and gripper actuators).
- Pluggable AI backends: offline `stub` (default), OpenAI, Anthropic.
- Perception pipeline and motion planner.
- Config via `pydantic-settings` + `defaults.yaml`.
- pytest test suite and `scripts/demo.py`.
