#!/usr/bin/env python3
"""Check that the per-client manifests and MCP configs agree with each other.

Each client reads its own copy, so a release that updates one and misses
another ships different versions or server URLs to different clients.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MANIFESTS = [
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
]
SHARED_FIELDS = ["name", "version", "repository", "license"]

# Each MCP config spells the HTTP transport its own way.
MCP_CONFIGS = {
    "mcp.json": "streamable-http",
    ".mcp.json": "http",
}


def load(path):
    try:
        return json.loads((ROOT / path).read_text())
    except (OSError, json.JSONDecodeError) as error:
        sys.exit(f"{path}: {error}")


def main():
    errors = []

    manifests = {path: load(path) for path in MANIFESTS}
    for field in SHARED_FIELDS:
        values = {path: data.get(field) for path, data in manifests.items()}
        if len(set(map(json.dumps, values.values()))) > 1:
            listing = ", ".join(f"{path}={value!r}" for path, value in values.items())
            errors.append(f"`{field}` differs across manifests: {listing}")

    servers = {}
    for path, transport in MCP_CONFIGS.items():
        entries = load(path).get("mcpServers", {})
        for name, entry in entries.items():
            if entry.get("type") != transport:
                errors.append(
                    f"{path}: server `{name}` has type {entry.get('type')!r}, expected {transport!r}"
                )
            if not str(entry.get("url", "")).startswith("https://"):
                errors.append(f"{path}: server `{name}` url must be https")
        servers[path] = {name: entry.get("url") for name, entry in entries.items()}
    first, *rest = MCP_CONFIGS
    for path in rest:
        if servers[path] != servers[first]:
            errors.append(
                f"{path} servers {servers[path]} differ from {first} servers {servers[first]}"
            )

    for error in errors:
        print(f"error: {error}")
    if errors:
        sys.exit(1)
    print(f"ok: {len(MANIFESTS)} manifests and {len(MCP_CONFIGS)} MCP configs agree")


if __name__ == "__main__":
    main()
