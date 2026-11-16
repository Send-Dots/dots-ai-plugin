#!/usr/bin/env python3
"""Check the skill and rule against the live Dots MCP server.

The server ships from the dots repo, so its tool names and argument shapes can
change without a change here. This calls the unauthenticated docs endpoint,
which serves the same search_tools and read_doc results and operation schemas
as the authenticated servers, and fails when something the skill relies on is
gone.
"""

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = os.environ.get("DOTS_MCP_DOCS_URL", "https://mcp.dots.dev/docs")
INSTRUCTION_FILES = ["skills/dots/SKILL.md", "rules/dots-money-movement.mdc"]

# The skill's dry run, confirm, and idempotency steps depend on these inputs.
MONEY_MOVING = [
    "dots_payouts_send",
    "dots_payout_batches_create",
    "dots_payout_links_create",
    "dots_transfers_create",
]
SAFETY_INPUTS = ["dry_run", "confirm", "idempotency_key"]

OPERATION_FIELDS = ["kind", "name", "description", "read_only", "input_schema", "guide", "command"]
DOC_FIELDS = ["kind", "path", "title", "section", "url"]


def rpc(method, params):
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(),
        headers={"content-type": "application/json", "accept": "application/json, text/event-stream"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode()
    # Streamable HTTP may answer with plain JSON or a single SSE event.
    payload = next(
        (line[5:] for line in body.splitlines() if line.startswith("data:")),
        body,
    )
    message = json.loads(payload)
    if "error" in message:
        raise RuntimeError(f"{method}: {message['error']}")
    return message["result"]


def call_tool(name, arguments):
    result = rpc("tools/call", {"name": name, "arguments": arguments})
    if result.get("isError"):
        raise RuntimeError(f"{name} failed: {result.get('content')}")
    return result


def find_operation(name):
    results = call_tool("search_tools", {"query": name, "limit": 10})["structuredContent"]["results"]
    return next((r for r in results if r.get("kind") == "operation" and r.get("name") == name), None)


def main():
    errors = []

    referenced = set()
    for path in INSTRUCTION_FILES:
        referenced |= set(re.findall(r"\bdots_[a-z_]+\b", (ROOT / path).read_text()))
    # OpenAI review cases must use real operations. Negative cases name
    # unsupported or made-up operations on purpose, so only positives count.
    review = json.loads((ROOT / "plugin.json").read_text())
    positive = (
        review.get("extensions", {}).get("com.openai", {}).get("review", {})
        .get("test_cases", {}).get("positive", [])
    )
    referenced |= set(re.findall(r"\bdots_[a-z_]+\b", json.dumps(positive)))
    for name in sorted(referenced | set(MONEY_MOVING)):
        operation = find_operation(name)
        if operation is None:
            errors.append(f"operation `{name}` is not in search_tools results")
            continue
        missing = [field for field in OPERATION_FIELDS if field not in operation]
        if missing:
            errors.append(f"`{name}` result lacks {missing}")
        if name in MONEY_MOVING:
            properties = operation.get("input_schema", {}).get("properties", {})
            absent = [field for field in SAFETY_INPUTS if field not in properties]
            if absent:
                errors.append(f"money-moving `{name}` no longer accepts {absent}")
            # Operations without a `body` input build the request themselves and
            # always put the key in it; for the rest, the skill relies on the
            # server copying the top-level key into the body.
            elif "body" in properties and "request body" not in properties[
                "idempotency_key"
            ].get("description", ""):
                errors.append(
                    f"`{name}` idempotency_key no longer says it is stored in the request body; "
                    "re-check the skill's key placement"
                )
            if operation.get("read_only") is not False:
                errors.append(f"money-moving `{name}` has read_only={operation.get('read_only')!r}")

    docs = call_tool("search_tools", {"query": "what is a payout link", "limit": 10})
    doc = next((r for r in docs["structuredContent"]["results"] if r.get("kind") == "doc"), None)
    if doc is None:
        errors.append("search_tools returned no doc results for a question")
    else:
        missing = [field for field in DOC_FIELDS if field not in doc]
        if missing:
            errors.append(f"doc result lacks {missing}")
        page = call_tool("read_doc", {"path": doc["path"]})["content"][0]["text"]
        if not page.strip():
            errors.append(f"read_doc returned an empty page for {doc['path']}")

    for error in errors:
        print(f"error: {error}")
    if errors:
        sys.exit(1)
    print(f"ok: {len(referenced | set(MONEY_MOVING))} operations and docs results match {ENDPOINT}")


if __name__ == "__main__":
    main()
