# Copyright 2026 Binary Core LLC
# SPDX-License-Identifier: Apache-2.0

"""Search and list orchestrators for the Sketchfab skill."""

from __future__ import annotations

import asyncio
from typing import Any

import requests
from bowerbot.skills import ToolResult

from bowerbot_skill_sketchfab.utils.api_utils import (
    format_model_list,
    get_json,
)


async def search_my_models(token: str, params: dict[str, Any]) -> ToolResult:
    """Search the authenticated user's own Sketchfab library."""
    query = params["query"]
    max_results = min(params.get("max_results", 10), 24)
    try:
        data = await asyncio.to_thread(
            get_json, "/me/models", token, {"q": query, "count": max_results},
        )
    except (requests.RequestException, RuntimeError) as e:
        return ToolResult(success=False, error=str(e))
    return ToolResult(success=True, data=format_model_list(data))


async def list_my_models(token: str, params: dict[str, Any]) -> ToolResult:
    """List every model in the authenticated user's account."""
    max_results = min(params.get("max_results", 24), 24)
    try:
        data = await asyncio.to_thread(
            get_json, "/me/models", token, {"count": max_results},
        )
    except (requests.RequestException, RuntimeError) as e:
        return ToolResult(success=False, error=str(e))
    return ToolResult(success=True, data=format_model_list(data))
