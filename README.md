# Dots plugin

Connects your AI agent to the hosted [Dots](https://usedots.com) MCP server, so the agent can search the Dots docs and API and run operations on your Dots App. It works in Cursor, Claude (Claude Code, claude.ai, and Cowork), OpenAI Codex and ChatGPT, and Grok Build.

## What it adds

- **MCP servers**
  - `dots`: `https://mcp.dots.dev/mcp` (production)
  - `dots-sandbox`: `https://mcp.dots.dev/sandbox/mcp` (not in the OpenAI listing, which connects one server per plugin and uses production)
- **Skill** `dots`: how to use `search_tools`, `read_doc`, and `execute_tool`, and how to preview payouts before you send them.
- **Rule** `dots-money-movement` (Cursor only): dry run, approval, and idempotency rules for money-moving calls. The skill carries the same rules for other clients.

## Sign in

The first time your client connects to a server, it opens the Dots dashboard. Pick the App the agent can act on. The agent gets your dashboard permissions on that App and can't switch Apps or environments.

Money movement is off unless you check **Allow money movement** when you authorize. Access expires after 30 days. To revoke it sooner, open the App's developer tools in dashboard settings and click **Revoke** under **Connected MCP clients**. Apps on the Core plan don't have developer tools, so their access lasts until it expires.

If you only need one environment, disable the other server in your client's MCP settings.

## Docs only

To read the docs without signing in, use `https://mcp.dots.dev/docs`. It offers only `search_tools` and `read_doc`.

## Data and network access

The plugin contains only configuration and instructions. It runs no local code and has no hooks.

- It connects only to `https://mcp.dots.dev`, which Dots operates.
- Authentication is OAuth 2.1 through the Dots dashboard. The plugin stores no credentials; your MCP client holds the access token.
- Operations act on the Dots App you authorize, through the Dots API. Requests and results include data from that App, such as user names, emails, phone numbers, and payout amounts.
- `search_tools` and `read_doc` read docs bundled with the server and don't call the Dots API.

## Package layout

One repository serves every client. Each client reads its own manifest:

| Client | Manifest | MCP config |
| --- | --- | --- |
| Cursor | `.cursor-plugin/plugin.json` | `mcp.json` |
| Claude, Grok Build | `.claude-plugin/plugin.json` | `.mcp.json` |
| OpenAI Codex and ChatGPT | `plugin.json` ([Agent Plugins](https://agent-plugins.org)) | `mcp.json` |

All clients share `skills/dots/SKILL.md`. When you change a server URL, update both `mcp.json` and `.mcp.json`. When you release, raise `version` in all three manifests. To build the OpenAI upload, run `python3 scripts/build_openai_zip.py`; see [docs/openai-submission.md](docs/openai-submission.md).

## Checks

CI runs these on every pull request and daily, and you can run them locally:

- `python3 scripts/check_manifests.py`: the three manifests share `name`, `version`, `repository`, and `license`, and both MCP configs list the same servers.
- `python3 scripts/check_schemas.py`: `plugin.json` and `mcp.json` match the Agent Plugins schemas. Requires `jsonschema`.
- `claude plugin validate --strict .`: Claude's manifest, MCP config, and directory checks.
- `python3 scripts/check_server_contract.py`: every operation the skill and rule name still exists on `https://mcp.dots.dev/docs`, and money-moving operations still accept `dry_run`, `confirm`, and `idempotency_key`.

## Support

Email support@dots.dev or message us from the [Dots Help Center](https://support.usedots.com/en/).

## More

See the [Dots CLI docs](https://docs.usedots.com/dots-cli) for the full tool reference and the local `dots --mcp` server.
