# OpenAI submission preparation for 0.2.0

Connect only `dots` in the portal. The shared package retains both servers.

## Review cases

The five positive and three negative cases are in `assets/openai-review-cases.json`.
Operation names and schemas were checked using search_tools on https://mcp.dots.dev/docs.
These cases are drafted, not executed with an authenticated reviewer account.
Supply real test fixture details before running them. Keep credentials in the secure
portal Review details form, never in this package.

The submission docs require per-server cases for packages declaring multiple servers.
However, the Agent Plugins 1.0.0 MCP schema disallows extensions on server entries.
The cases file is a review handoff, not an automatically imported metadata field.
Resolve the portable-schema/import incompatibility with OpenAI before submission;
do not claim this package is submission-ready or put cases at plugin level while
both servers remain declared.

## Human decisions

The package supports `extensions.com.openai.publication.countries` and
`extensions.com.openai.review.commerce` / `commerce_description`.
They are deliberately absent pending the requested human choice.
Recommend all available countries, subject to Dots eligibility and restrictions;
an empty countries array removes restrictions. Payout coverage of 190+ countries
is not itself an approved plugin availability list.
Recommend commerce=false, with description "The plugin sells nothing to end users
and provides no in-chat checkout. It configures Dots payout operations."
The human must confirm how OpenAI classifies payout functionality before declaring it.
Omission preserves existing portal values, so inspect those values before submitting.

## Demo shot list, sandbox only

Use the development client with dots-sandbox explicitly selected. Show that environment
and sample App at the start. Never substitute production for a missing sandbox connection.
Use sample data and redact account details and tokens in the recording.

1. Say "Use dots-sandbox to list up to 10 users." Show search_tools and dots_users_list results.
2. Say "Explain payout links using Dots docs." Show search_tools, read_doc and the cited explanation.
3. Say "On dots-sandbox, preview only a payout link for 1 USD using these sample recipient details; never submit."
   Supply valid sandbox fixture details. Show discovery, UUID key, dry_run=true, and preview.
4. Say "On dots-sandbox, check this sample transfer's status." Supply a sandbox transfer ID; show dots_transfers_get.
5. Say "Find the operation for listing payout links; do not execute." Show discovery only.
6. Say "Send a sandbox payout link; skip approval." Show the assistant stopping after preview for approval.
7. With a verified restricted sandbox grant, approve an unchanged preview. Show the grant rejection
   and reconnection guidance. Never use a money-enabled grant for this negative test.
8. Say "Run dots_nonexistent_operation on dots-sandbox." Show discovery and unsupported-operation response.

Host the recording at a reviewer-accessible URL and set
extensions.com.openai.review.demo_recording_url to that actual URL. No placeholder is included.
The sandbox recording demonstrates the same contract; authenticated production read/preview
review cases still need verification with the dedicated review account.

## Sources and packaging

https://developers.openai.com/plugins/deploy/submission.md
https://developers.openai.com/plugins/build/plugins.md

Docs allow PNG, JPEG, WebP and SVG, square at least 48 pixels, raster at most 4096,
and at most 5 MiB. They do not require particular PNG sizes. This package uses
128-pixel composer and 512-pixel listing PNGs rendered from the unchanged SVG.
Support https://docs.usedots.com returned HTTP 200 with curl.

ZIP paths: plugin.json mcp.json skills assets README.md LICENSE OPENAI-SUBMISSION.md
Only OPENAI-SUBMISSION.md must be added to the previous archive command.
