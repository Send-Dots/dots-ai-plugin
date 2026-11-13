#!/usr/bin/env python3
"""Build the ZIP to upload to the OpenAI plugin portal.

OpenAI connects one MCP server per plugin, and it imports the review test
cases in plugin.json only when the package declares exactly one server. The
repo's mcp.json declares production and sandbox for the other clients, so the
ZIP's copy keeps only production. Everything else is taken from the
committed tree, so uncommitted edits never ship.

Usage: python3 scripts/build_openai_zip.py [OUTPUT]
"""

import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER = "dots"
PATHS = ["plugin.json", "mcp.json", "skills", "assets", "README.md", "LICENSE"]


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True).stdout


def main():
    version = json.loads(git("show", "HEAD:plugin.json"))["version"]
    output = Path(sys.argv[1] if len(sys.argv) > 1 else f"dots-openai-{version}.zip").resolve()

    files = git("ls-tree", "-r", "--name-only", "HEAD", "--", *PATHS).decode().splitlines()
    mcp = json.loads(git("show", "HEAD:mcp.json"))
    if SERVER not in mcp["mcpServers"]:
        sys.exit(f"mcp.json has no `{SERVER}` server")
    mcp["mcpServers"] = {SERVER: mcp["mcpServers"][SERVER]}

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in files:
            data = (json.dumps(mcp, indent=2) + "\n").encode() if name == "mcp.json" else git("show", f"HEAD:{name}")
            archive.writestr(name, data)

    print(output)
    for name in files:
        print(f"  {name}")


if __name__ == "__main__":
    main()
