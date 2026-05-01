# Copyright 2026 Binary Core LLC
# SPDX-License-Identifier: Apache-2.0

"""Verify the skill conforms to the BowerBot Skill contract.

These tests do not hit the Sketchfab API; they exercise the contract
itself: tool registration, entry-point discovery, validate_config
behavior, and dispatch routing.
"""

from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

import pytest

from bowerbot.skills import (
    Skill,
    SkillCategory,
    SkillConfigError,
    SkillContext,
    Tool,
)

from bowerbot_skill_sketchfab import SketchfabSkill


def _make_ctx(tmp: Path) -> SkillContext:
    """Build a minimal SkillContext for offline tests."""
    cache_dir = tmp / "cache" / "sketchfab"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return SkillContext(library_dir=tmp, cache_dir=cache_dir)


def test_skill_subclasses_skill_contract():
    """SketchfabSkill is a concrete Skill with the expected metadata."""
    skill = SketchfabSkill(token="dummy")
    assert isinstance(skill, Skill)
    assert skill.name == "sketchfab"
    assert skill.category == SkillCategory.ASSET_PROVIDER
    assert skill.cache_subdir == "cache/sketchfab"


def test_get_tools_returns_three_tools():
    """The skill exposes exactly the three Sketchfab tools."""
    skill = SketchfabSkill(token="dummy")
    tools = skill.get_tools()
    assert all(isinstance(t, Tool) for t in tools)
    assert {t.name for t in tools} == {
        "search_my_models", "list_my_models", "download_model",
    }


def test_validate_config_raises_when_token_missing():
    """validate_config raises SkillConfigError when no token is set."""
    skill = SketchfabSkill(token="")
    with pytest.raises(SkillConfigError) as exc_info:
        skill.validate_config()
    assert "token" in str(exc_info.value).lower()


def test_validate_config_passes_with_token():
    """validate_config returns silently when a token is configured."""
    skill = SketchfabSkill(token="abc123")
    skill.validate_config()


def test_execute_unknown_tool_returns_error():
    """An unknown tool name returns a clear ToolResult error."""
    skill = SketchfabSkill(token="abc123")
    with tempfile.TemporaryDirectory() as tmp:
        ctx = _make_ctx(Path(tmp))
        result = asyncio.run(skill.execute("does_not_exist", {}, ctx))
    assert not result.success
    assert "Unknown tool" in result.error


def test_entry_point_is_discoverable_via_importlib_metadata():
    """The skill registers under bowerbot.skills entry-point group.

    Proves an installed skill (editable or wheel) is discoverable by
    BowerBot's SkillRegistry without any in-tree code.
    """
    from importlib.metadata import entry_points

    eps = entry_points(group="bowerbot.skills")
    sketchfab_eps = [ep for ep in eps if ep.name == "sketchfab"]
    assert len(sketchfab_eps) == 1, (
        "Expected exactly one 'sketchfab' entry point under 'bowerbot.skills'. "
        f"Found: {[ep.value for ep in sketchfab_eps]}"
    )
    skill_cls = sketchfab_eps[0].load()
    assert skill_cls is SketchfabSkill
