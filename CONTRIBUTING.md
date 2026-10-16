# Contributing to Cobotics

Thanks for your interest in contributing. Cobotics is open source under the
[MIT License](LICENSE), and contributions of all kinds are welcome — bug
reports, docs, features, and hardware drivers.

## Getting started

```bash
git clone https://github.com/monodox/cobotics.git
cd cobotics
python -m venv .venv
.venv\Scripts\activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest -q
```

## Development workflow

1. Fork the repo and create a branch from `main`:
   `git checkout -b feature/short-description`.
2. Make your change. Keep it focused and consistent with the existing style
   (type hints, `from __future__ import annotations`, docstrings, `rich`/`typer`
   patterns).
3. Add or update tests under `tests/`. Tests must run offline — no network calls.
4. Run the suite: `pytest -q`. Make sure it passes.
5. Update `CHANGELOG.md` under the "Unreleased" heading if your change is
   user-visible.
6. Commit with a clear message and open a pull request against `main`.

## Conventions

- The import/package name is lowercase `cobotics`; the display name in docs and
  user-facing text is `Cobotics`.
- The default AI backend is `stub` and must keep working with no API key or
  network. New backends go behind the `LLMBackend` interface in
  `src/cobotics/ai/` and register in `build_backend`.
- New hardware support implements the abstractions in
  `src/cobotics/hardware/base.py` and mirrors the simulator so the rest of the
  system is unaffected.
- Never commit secrets. Use `.env.example` for placeholders; real keys go in the
  git-ignored `.env.local`.

## Reporting bugs and asking questions

- Bugs and feature requests:
  [open an issue](https://github.com/monodox/cobotics/issues/new) with steps to
  reproduce, expected vs. actual behavior, your OS, and Python version. A
  minimal snippet or failing test helps a lot.
- Questions, ideas, and general discussion:
  [start a discussion](https://github.com/monodox/cobotics/discussions).

## Code of conduct

By participating you agree to abide by our
[Code of Conduct](CODE_OF_CONDUCT.md).
