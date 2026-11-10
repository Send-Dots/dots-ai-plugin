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

Each server acts only on the Dots App the user picked when they authorized it.
Never switch environments on your own. If the user hasn't said which
environment to use, ask before any `execute_tool` call. Name the server
(`dots` or `dots-sandbox`) in every preview and approval request.
`search_tools` and `read_doc` return the same results on either server.

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

Every `search_tools` result has a `read_only` flag. Treat any operation whose
`read_only` is not `true` as a write, including user and flow changes, and
follow these steps:

1. For money-moving operations, generate a UUID v4 as the idempotency key
   before the preview. Put it in the right place:
   - If the operation takes a `body`, put `"idempotency_key": "<uuid>"`
     inside the body JSON. The API ignores the top-level `idempotency_key`
     argument for these operations.
   - `dots_payouts_send` and `dots_payout_batches_create` take
     `idempotency_key` as a top-level argument.
2. Run the call with `dry_run: true`. If the operation's schema has no
   `dry_run`, describe the exact call to the user instead.
3. Show the preview to the user, naming the server, and wait for explicit
   approval.
4. Send the same arguments again with `dry_run` removed and `confirm: true`
   added. The server rejects a call that has both. Keep the operation,
   server, recipient, amount, and idempotency key unchanged. If any of them
   change, preview again and get approval again.

The server does not check for an earlier dry run or for approval; these steps
are the only safeguard.

### Missing money movement access

A successful dry run does not mean the user can move money. If the user did
not check **Allow money movement** when they authorized, the confirmed call
fails with an error that mentions `DOTS_BLOCK_MONEY_MOVEMENT` or says "This
MCP grant does not include money movement". Both mean the same thing. Do not
suggest changing environment variables. Tell the user to log out of that
server in Cursor's MCP settings, reconnect, and check **Allow money
movement**. That checkbox requires payout permissions on the App.

### Timeouts and retries

Each operation times out after 120 seconds. A timed-out or cancelled payout
may still have been submitted. Before retrying, check what happened with a
read operation such as `dots_payout_links_list`, `dots_payout_batches_get`, or
`dots_transfers_get` (use `search_tools` for the exact names). If you retry,
reuse the same idempotency key in the same place, so the API returns the
existing payout instead of creating a second one.

If the server replies "The hosted MCP server is busy; retry shortly", nothing
was sent, so it is safe to retry.

## Limits of the hosted server

The hosted server runs users, transfers, transactions, flows, payouts, payout
links, payout batches, and operations commands, plus reads for vendors and
payables. `dots_call` sends only GET and HEAD requests. Apps, roles,
developers, payout agent commands, `dots_request`, and file inputs are not
available. For those, point the user to the local server: `dots --mcp` from
the Dots CLI.

At most 16 operations run at once. Each client IP is limited to 120 requests
per minute, and request bodies are capped at 64 KB, which limits payout batch
size.

Use transfers operations to inspect a transfer and its status. Use
transactions operations to inspect the ledger entries created by transfers and
other money movement.
