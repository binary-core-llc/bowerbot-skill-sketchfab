<div align="center">

# bowerbot-skill-sketchfab

**Sketchfab provider skill for [BowerBot](https://github.com/binary-core-llc/bowerbot).**

Searches and downloads 3D models from the user's authenticated Sketchfab account in USDZ format.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.12+-blue)](https://www.python.org/)
[![Built by Binary Core LLC](https://img.shields.io/badge/Built%20by-Binary%20Core%20LLC-black)](https://binarycore.us)

</div>

---

## What it does

This skill connects BowerBot to the authenticated user's **own** Sketchfab model library, not the public marketplace. It exposes three LLM-callable tools:

| Tool | Description |
|------|-------------|
| `search_my_models` | Search your uploaded models by keyword |
| `list_my_models` | List every model in your account |
| `download_model` | Download a model in USDZ format into BowerBot's library cache |

Downloaded models land under `<assets_dir>/cache/sketchfab/` and are immediately searchable through BowerBot's `search_assets` / `list_assets` tools.

## Install

```bash
pip install bowerbot-skill-sketchfab
```

BowerBot discovers the skill automatically via Python entry points (`bowerbot.skills`). No code changes required in BowerBot.

## Configure

Add a `sketchfab` block to `~/.bowerbot/config.json`:

```json
{
  "skills": {
    "sketchfab": {
      "enabled": true,
      "config": { "token": "your-sketchfab-api-token" }
    }
  }
}
```

Get a token at https://sketchfab.com/settings/password.

## Usage

Once installed and configured, the skill is just available to BowerBot. Talk to the agent normally:

```
You: search my Sketchfab for a round bistro table
BowerBot: Found "Round Bistro Table" (uid: abc123). Want me to download it?

You: yes please
BowerBot: Downloaded to assets/cache/sketchfab/Round_Bistro_Table.usdz

You: place it at the center of the room
BowerBot: Placed at /Scene/Furniture/Round_Bistro_Table_01 (5.0, 0.0, 4.0)
```

## Architecture

This skill follows BowerBot's required FastAPI-style internal layout:

```
src/bowerbot_skill_sketchfab/
  skill.py          # Skill subclass. Tool registration + execute() dispatch only.
  SKILL.md          # Natural-language instructions injected into the LLM prompt.
  schemas/          # Pydantic models for Sketchfab API payloads
  services/         # One orchestrator per tool (search, download)
  tools/            # Tool definitions surfaced to the LLM
  utils/            # Pure-function primitives (HTTP, naming, response shaping)
```

The skill is **hyper-isolated**: it imports only from `bowerbot.skills` (the public SDK) and its own submodules. No reach into `bowerbot.utils`, `bowerbot.services`, or any other core internal.

## Development

Clone the BowerBot core and this skill side by side, then install both editable:

```bash
git clone https://github.com/binary-core-llc/bowerbot.git
git clone https://github.com/binary-core-llc/bowerbot-skill-sketchfab.git
cd bowerbot-skill-sketchfab
uv pip install -e ../bowerbot
uv pip install -e .[dev]
uv run pytest
```

## License

Apache 2.0. See [LICENSE](LICENSE).

---

Built with 🐦 by [Binary Core LLC](https://binarycore.us)
