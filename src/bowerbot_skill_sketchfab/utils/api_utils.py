# Copyright 2026 Binary Core LLC
# SPDX-License-Identifier: Apache-2.0

"""Sketchfab HTTP primitives — auth headers, naming, response shaping."""

from __future__ import annotations

from typing import Any

import httpx

BASE_URL = "https://api.sketchfab.com/v3"


def auth_headers(token: str) -> dict[str, str]:
    """Build the Authorization + User-Agent headers for Sketchfab API calls."""
    return {
        "Authorization": f"Token {token}",
        "User-Agent": "bowerbot-skill-sketchfab/1.0",
    }


def parse_response(resp: httpx.Response, endpoint: str) -> dict[str, Any]:
    """Parse a Sketchfab response, raising a clear error on WAF / empty body."""
    waf_action = resp.headers.get("x-amzn-waf-action")
    if waf_action:
        raise RuntimeError(
            f"Sketchfab WAF blocked the request to {endpoint} "
            f"(action={waf_action!r}). This is IP-based rate limiting from "
            "AWS CloudFront, not an auth or skill problem. Wait a few "
            "minutes and retry, or switch networks."
        )
    if not resp.content:
        raise RuntimeError(
            f"Sketchfab returned an empty body (HTTP {resp.status_code}) "
            f"for {endpoint}. Likely rate limit, outage, or temporary "
            "server-side error. Retry in a moment.",
        )
    try:
        return resp.json()
    except ValueError as e:
        raise RuntimeError(
            f"Sketchfab returned non-JSON (HTTP {resp.status_code}) "
            f"for {endpoint}: {resp.content[:200]!r}",
        ) from e


def safe_file_name(name: str) -> str:
    """Sanitize a string for use as a download file name."""
    return "".join(c for c in name if c.isalnum() or c in "_-").strip()


def format_model_list(api_response: dict[str, Any]) -> list[dict[str, Any]]:
    """Reduce a ``/me/models`` response to the fields the LLM consumes."""
    results: list[dict[str, Any]] = []
    for model in api_response.get("results", []):
        thumbs = model.get("thumbnails", {}).get("images", [])
        thumbnail = thumbs[0].get("url") if thumbs else None
        results.append({
            "uid": model["uid"],
            "name": model["name"],
            "description": model.get("description", ""),
            "url": model.get("viewerUrl", ""),
            "vertex_count": model.get("vertexCount"),
            "face_count": model.get("faceCount"),
            "is_downloadable": model.get("isDownloadable", False),
            "tags": [t.get("name", "") for t in model.get("tags", [])],
            "thumbnail": thumbnail,
        })
    return results
