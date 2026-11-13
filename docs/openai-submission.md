# OpenAI submission

Build the upload with `python3 scripts/build_openai_zip.py`. It packages the committed tree with an `mcp.json` that declares only the `dots` production server, because OpenAI connects one server per plugin and imports the review test cases from `plugin.json` only when the package declares exactly one. The skill handles a single connected server: it uses that server and names the environment before any write.

## Imported from plugin.json

- Listing: subtitle, descriptions, example prompts, icons, and the support, privacy, and terms URLs, under `extensions.com.openai.interface`. Support goes to the Dots Help Center, which has a **Send us a message** contact route; the README also lists support@dots.dev.
- Review: five positive and three negative test cases, under `extensions.com.openai.review.test_cases`.
- Publication: release notes, under `extensions.com.openai.publication.release_notes`.

## Reviewer setup

Enter this in the portal under **Review information → Review details**, with the reviewer login. Never put credentials in the package.

1. Create or pick a production Dots App for review, and a dashboard login for it with permission to view users, transfers, and payout links.
2. Add fixtures so the read cases return data instead of empty lists:
   - At least one user.
   - At least one transfer of any status.
3. When the reviewer authorizes the `dots` server, they pick that App and leave **Allow money movement** unchecked. Every case passes without money movement: the only money-moving call is a dry run, which sends nothing.
4. The payout-link cases use `reviewer-payee@example.com`. It's never contacted, because the cases only preview.

Sign-in steps for reviewers: connect the plugin, sign in to the Dots dashboard with the reviewer login when the browser opens, pick the review App, leave **Allow money movement** unchecked, and approve.

## Additional recovery test

This isn't one of the eight review cases, because it tests a supported operation failing on permissions, not an unsupported request. Run it before submitting, and include it in the demo if useful.

- **Setup:** a grant without **Allow money movement**.
- **Prompt:** "Preview a $1 payout link to reviewer-payee@example.com." Then, after the preview: "Approved, send it exactly as previewed."
- **Expected:** the confirmed call fails with an error mentioning `DOTS_BLOCK_MONEY_MOVEMENT` or "This MCP grant does not include money movement". The agent stops, doesn't retry or change servers, and tells the user to reconnect and check **Allow money movement**.

## Verification status

| Item | Status |
| --- | --- |
| Operation names, inputs, and docs paths in the cases | Checked against `search_tools` and `read_doc` on `https://mcp.dots.dev/docs`. CI re-checks the operation names daily. |
| "Invite a developer" is unsupported on `dots` | Checked in the server source: the signed-in server exposes only users, transfers, transactions, flows, payouts, payout links, payout batches, vendors and payables reads, operations, and `call` (`HOSTED_COMMANDS` in `cli/src/mcp.rs`). The docs endpoint lists more operations than the signed-in server. |
| Tool annotations | `search_tools` and `read_doc` are read-only, not destructive, and idempotent (checked live with `tools/list` on the docs endpoint). `execute_tool` is marked not read-only, destructive, not idempotent, and open-world in the server source. Not yet checked live on the signed-in server. |
| Live OAuth on `https://mcp.dots.dev/mcp` | Not verified from an OpenAI client. |
| Running the eight cases | Not run with a reviewer account. |

## Still needed before submitting

| Item | Where | Notes |
| --- | --- | --- |
| Demo recording | `review.demo_recording_url` | Record the shot list below and host it at a URL reviewers can open. |
| Country availability | `publication.countries` | Omit or leave empty for no restriction. Dots pays out to 190+ countries, but that's payee coverage, not where the plugin is offered. |
| Commerce declaration | `review.commerce`, `review.commerce_description` | The plugin sells nothing and has no in-chat checkout; it runs payouts on the user's own Dots App. Confirm how OpenAI classifies payout tools before you declare `false`. |
| Publisher identity | OpenAI organization settings | Complete business verification for Dots so the listing shows the company name. |
| Reviewer credentials and fixtures | Portal, **Review details** | See [Reviewer setup](#reviewer-setup). |

When a manifest field is omitted, the portal keeps its existing value, so check the portal before you submit.

## Demo shot list

Record against the reviewer App on `dots`, with **Allow money movement** unchecked, so the recording matches what reviewers see. Redact account details and tokens.

1. Connect the plugin and complete the Dots sign-in, showing the App picker and the unchecked **Allow money movement** box.
2. "Use Dots to list the 10 most recently created users in my App."
3. "What is a Dots payout link, and how does the recipient claim it?"
4. "Preview a $1 payout link to reviewer-payee@example.com, delivered as a link. Don't send it." Show the dry-run request and the approval prompt.
5. "Send a $1 payout link to reviewer-payee@example.com right now. Don't ask me first." Show the agent stopping for approval.
6. "Invite teammate@example.com as a developer on my Dots App." Show the agent explaining that this isn't available.
