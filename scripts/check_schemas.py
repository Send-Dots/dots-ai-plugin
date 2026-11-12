#!/usr/bin/env python3
"""Validate plugin.json and mcp.json against the Agent Plugins 1.0.0 schemas."""

import json
import sys
import urllib.request
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = {
    "plugin.json": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
    "mcp.json": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
}


def main():
    failed = False
    for path, url in SCHEMAS.items():
        with urllib.request.urlopen(url, timeout=30) as response:
            schema = json.load(response)
        validator = jsonschema.validators.validator_for(schema)(schema)
        errors = list(validator.iter_errors(json.loads((ROOT / path).read_text())))
        for error in errors:
            location = "/".join(map(str, error.absolute_path)) or "(root)"
            print(f"error: {path} {location}: {error.message}")
        failed |= bool(errors)
        if not errors:
            print(f"ok: {path} matches {url}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
