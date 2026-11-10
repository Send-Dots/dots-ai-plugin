---
name: dots
description: Use the Dots MCP server to answer questions about the Dots API and docs, and to run Dots operations such as listing users, checking transfers, and sending payouts. Use when the user mentions Dots, payouts, payout links, flows, or transfers.
---

# Dots

The plugin adds two MCP servers. Both expose the same three tools.

| Server | Environment |
| --- | --- |
| `dots-sandbox` | Sandbox (`https://mcp.dots.dev/sandbox/mcp`) |
| `dots` | Production (`https://mcp.dots.dev/mcp`) |

Never switch environments on your own. Each server acts only on the Dots App the
user picked when they authorized it.

## Tools

1. `search_tools`: search operations and docs by keyword, for example
   `send payout`, `list users`, or `what is a payout link`. Results include
   each operation's name and input schema. `limit` defaults to 10, max 100.
2. `read_doc`: read a docs page as markdown, for example
   `guides/payout-links` or
   `api-reference/payout-links/create-payout-link`.
3. `execute_tool`: run an operation by name with arguments that match its
   schema:

   ```json
   { "name": "dots_users_list", "arguments": { "query": ["limit=10"] } }
   ```

Always call `search_tools` to find the operation name and schema before
calling `execute_tool`. Do not guess operation names.

To answer questions about integrating Dots into the user's code, use
`search_tools` and `read_doc` and cite the docs page you used.

## Writes and payouts

1. Run every money-moving operation with `dry_run: true` first.
2. Show the preview to the user and wait for explicit approval.
3. Only then repeat the call with `confirm: true`.
4. Always pass an `idempotency_key` on payouts.

The server does not check for an earlier dry run or for approval. If the user
did not check **Allow money movement** when they authorized, money-moving
calls fail. Tell the user to reauthorize; do not try to work around it.

Each operation times out after 120 seconds. A timed-out or cancelled payout
may still have been submitted. Check its status before retrying, and reuse the
same `idempotency_key`.

## Limits of the hosted server

The hosted server runs users, transfers, transactions, flows, payouts, payout
links, payout batches, and operations commands, plus reads for vendors and
payables. `dots_call` sends only GET and HEAD requests. Apps, roles,
developers, `dots_request`, and file inputs are not available. For those,
point the user to the local server: `dots --mcp` from the Dots CLI.

Treat any question about transactions as a transfers query.
