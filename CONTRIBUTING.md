# Contributing to bowerbot-skill-sketchfab

Thanks for your interest in contributing!

## Getting Started

Clone the BowerBot core and this skill side by side, then install both editable:

```bash
git clone https://github.com/binary-core-llc/bowerbot.git
git clone https://github.com/binary-core-llc/bowerbot-skill-sketchfab.git
cd bowerbot-skill-sketchfab
uv pip install -e ../bowerbot
uv pip install -e .[dev]
uv run pytest
```

## How to Submit Changes

### 1. Create a branch

Branch names must follow `type/short-description`. This is enforced by CI.

```
feat/collection-search
fix/download-redirect
docs/update-readme
chore/ci-bump
```

Valid types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.

### 2. Open a PR

The PR title must use conventional format. Release Please reads it for versioning and changelogs.

```
feat: add collection search
fix: handle expired tokens gracefully
docs: clarify install instructions
```

All PRs are squash-merged. The PR title becomes the commit on `main`.

## Project Structure

This skill follows the FastAPI-style internal layout BowerBot requires of every skill. See [BowerBot's CONTRIBUTING.md](https://github.com/binary-core-llc/bowerbot/blob/main/CONTRIBUTING.md#writing-a-skill) for the contract.

```
src/bowerbot_skill_sketchfab/
  skill.py          # Skill subclass. Tool registration + execute() dispatch only.
  SKILL.md          # Natural-language instructions injected into the LLM prompt
  schemas/          # Pydantic models for Sketchfab API payloads
  services/         # One orchestrator per tool (search, download)
  tools/            # Tool definitions surfaced to the LLM
  utils/            # Pure-function primitives
```

The skill is hyper-isolated: it imports only from `bowerbot.skills` and its own submodules.

## Code Style

- Python 3.12+
- Type hints on all public functions
- `ruff check src/ tests/` before committing
- `pytest` before opening a PR

## License

By contributing, you agree your contributions are licensed under Apache 2.0.
