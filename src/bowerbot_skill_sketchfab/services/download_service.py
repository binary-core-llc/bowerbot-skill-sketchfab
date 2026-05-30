# Copyright 2026 Binary Core LLC
# SPDX-License-Identifier: Apache-2.0

"""Download orchestrator for the Sketchfab skill."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from bowerbot.skills import SkillContext, ToolResult

from bowerbot_skill_sketchfab.utils.api_utils import (
    get_bytes,
    get_json,
    safe_file_name,
)

logger = logging.getLogger(__name__)


async def download_model(
    token: str, params: dict[str, Any], ctx: SkillContext,
) -> ToolResult:
    """Download a model in USDZ format into the skill's cache_dir."""
    if ctx.cache_dir is None:
        return ToolResult(
            success=False,
            error="Sketchfab skill has no cache_dir; library_dir not configured.",
        )

    uid = params["uid"]
    name = params["name"]
    safe_name = safe_file_name(name) or uid

    download_info = await asyncio.to_thread(
        get_json, f"/models/{uid}/download", token,
    )

    usdz = download_info.get("usdz") or {}
    if not usdz.get("url"):
        return ToolResult(
            success=False,
            error=(
                f"Model '{name}' ({uid}) has no USDZ format available. "
                "Only USD assets are supported."
            ),
        )

    download_url = usdz["url"]
    file_size = usdz.get("size", 0)
    logger.info("Downloading USDZ (%s bytes) for %s", file_size, name)

    final_path = ctx.cache_dir / f"{safe_name}.usdz"
    final_path.write_bytes(await asyncio.to_thread(get_bytes, download_url))

    logger.info("Downloaded %s to %s", name, final_path)
    return ToolResult(
        success=True,
        data={
            "file_path": str(final_path),
            "format": "usdz",
            "size_bytes": file_size,
            "name": name,
            "uid": uid,
            "message": f"Downloaded {name} (USDZ) to {final_path}",
        },
    )
