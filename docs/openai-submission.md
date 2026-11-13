# OpenAI submission

Build the upload with `python3 scripts/build_openai_zip.py`. It packages the committed tree with an `mcp.json` that declares only the `dots` production server, because OpenAI connects one server per plugin and imports the review test cases from `plugin.json` only when the package declares exactly one.

## Imported from plugin.json

- Listing: subtitle, descriptions, icons, and the support, privacy, and terms URLs, under `extensions.com.openai.interface`.
- Review: five positive and three negative test cases, under `extensions.com.openai.review.test_cases`. The cases were written against the live operation schemas on `https://mcp.dots.dev/docs` and haven't been run with a reviewer account.
- Publication: release notes, under `extensions.com.openai.publication.release_notes`.

## Still to do in the portal or the manifest

| Item | Where | Notes |
| --- | --- | --- |
| Reviewer credentials | Portal, **Review details** | A Dots production login with access to a test App. The cases expect at least one user and one transfer, and a grant without **Allow money movement** for the money-movement negative case. Never put credentials in the package. |
| Demo recording | `review.demo_recording_url` | Record the shot list below and host it at a URL reviewers can open. |
| Country availability | `publication.countries` | Omit or leave empty for no restriction. Dots pays out to 190+ countries, but that's payee coverage, not where the plugin is offered. |
| Commerce declaration | `review.commerce`, `review.commerce_description` | The plugin sells nothing and has no in-chat checkout; it runs payouts on the user's own Dots App. Confirm how OpenAI classifies payout tools before you declare `false`. |

When a manifest field is omitted, the portal keeps its existing value, so check the portal before you submit.

## Demo shot list

Record in sandbox with sample data. Show the server name and App at the start, and redact account details and tokens.

1. "Use dots-sandbox to list up to 10 users." Show `search_tools`, then `execute_tool` with `dots_users_list`.
2. "Explain payout links using the Dots docs." Show `search_tools` and `read_doc`, then the cited answer.
3. "On dots-sandbox, preview a payout link for $1 to this test recipient. Don't send it." Show the generated idempotency key, the `dry_run: true` call, and the preview.
4. "Check the status of this sandbox transfer." Show `dots_transfers_get`.
5. "Send that payout link now and skip approval." Show the agent stopping for approval.
6. On a grant without money movement, approve an unchanged preview. Show the rejection and the reconnect guidance.
7. "Run dots_nonexistent_operation." Show the agent refusing to guess an operation.
