# Security Policy

## Supported versions

Cobotics is pre-1.0 and under active development. Security fixes are applied to
the latest `main` and the most recent release.

| Version | Supported |
| ------- | --------- |
| 0.1.x   | ✅        |
| < 0.1   | ❌        |

## Reporting a vulnerability

Please report security issues **privately** rather than opening a public issue.

- Preferred: use GitHub's private vulnerability reporting on
  https://github.com/monodox/cobotics (Security → Report a vulnerability).
- Include a description, steps to reproduce, affected version/commit, and any
  proof-of-concept.

We aim to acknowledge reports within a few days and will keep you updated on a
fix. Please give us reasonable time to address the issue before any public
disclosure.

## Handling secrets

- Never commit real API keys. `.env.example` holds placeholders only;
  machine-specific secrets belong in the git-ignored `.env.local`.
- API keys (`NEBIUS_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) are read
  from the environment and are never logged or echoed by the application.
- If you believe a key was committed, rotate it immediately and open a private
  report so history can be scrubbed.
