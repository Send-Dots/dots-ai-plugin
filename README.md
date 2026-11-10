# Dots plugin for Cursor

Connects Cursor to the hosted [Dots](https://usedots.com) MCP server, so the agent can search the Dots docs and API and run operations on your Dots App.

## What it adds

- **MCP servers**
  - `dots-sandbox`: `https://mcp.dots.dev/sandbox/mcp`
  - `dots`: `https://mcp.dots.dev/mcp` (production)
- **Skill** `dots`: how to use `search_tools`, `read_doc`, and `execute_tool`, and how to preview payouts before you send them.
- **Rule** `dots-money-movement`: dry run, approval, and idempotency rules for money-moving calls.

## Sign in

The first time Cursor connects to a server, it opens the Dots dashboard. Pick the App the agent can act on. The agent gets your dashboard permissions on that App and can't switch Apps or environments.

Money movement is off unless you check **Allow money movement** when you authorize. Access expires after 30 days. To revoke it sooner, open the App's developer tools in dashboard settings and click **Revoke** under **Connected MCP clients**. Apps on the Core plan don't have developer tools, so their access lasts until it expires.

If you only need one environment, disable the other server in Cursor's MCP settings.

## Docs only

To read the docs without signing in, use `https://mcp.dots.dev/docs`. It offers only `search_tools` and `read_doc`.

## More

See the [Dots CLI docs](https://docs.usedots.com/dots-cli) for the full tool reference and the local `dots --mcp` server.
