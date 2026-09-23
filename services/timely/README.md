# Timely — meeting programme MCP server for Claude, Cursor and any MCP client

**Timely builds a meeting programme — a fixed number of meetings, or everything inside a calendar
period — keeps every revision, and renders the approved version to a PDF through Doksi. An assistant may
publish only the exact revision and PDF the user has just confirmed. It runs as a hosted MCP server
over HTTPS.**

| | |
|---|---|
| Endpoint | `https://timely.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open |
| Registry | [`pro.publifye/timely`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) ([server.json](server.json)) |
| Product site | <https://timely.publifye.com> |
| Capability tools | **31** ([full schemas](tools.json)) |
| Surface described | generated from source `354ee8b`; the same tool surface is live in production as version 0.1.198 (`9ce28e3`, released 2026-09-23) |

## Connect

```jsonc
{ "mcpServers": { "timely": { "type": "http", "url": "https://timely.publifye.com/mcp" } } }
```

Claude Code: `claude mcp add --transport http timely https://timely.publifye.com/mcp`, then `/mcp`
to sign in. The discovery chain is the same as for the other servers:
**[../../docs/connect.md](../../docs/connect.md)**.

## Publishing needs the user's explicit yes, for the exact revision and PDF

An assistant **can** publish a programme with `draft_approve`; no browser step or signed
confirmation page is involved. What it cannot do is publish on its own initiative. The tool's own
description tells the assistant to show the user the exact revision, the PDF download link and the
public address, to flag open assumptions, and to **ask** — a general request to edit is not consent.
The server then enforces the part it can check:

- `user_confirmed` must be `true`; otherwise the call is refused with *"ask the user explicitly
  before publishing; user_confirmed must be true only after their affirmative answer"*;
- `revision`, `content_hash` and `pdf_hash` must name the exact preview that was shown; if the
  programme or its PDF has changed since, the approval does not match and nothing is published;
- the stored PDF is published as it is, without re-rendering, so what was approved is what goes out.

`user_confirmed` is the assistant's statement that the user said yes; the server records it in the
programme's audit trail (`mcp_user_confirmed_publication`) but cannot see the conversation. The
hashes are what make a yes apply to one revision and one PDF only.

## Edits are atomic against a hash

`timely_edit` applies explicit operations against a `base_hash`. If the programme moved since the
agent last read it, the edit is refused rather than merged — so two assistants, or an assistant and
a person, cannot silently overwrite one another. Every commit becomes an immutable revision, and
`timely_history` returns those revisions with their changes and the PDF each one produced.

## It renders through Doksi

`timely_render` sends the current draft to **[Doksi](../doksi)** and retains the exact preview PDF
that was produced — the same artifact a person then approves. The two servers are separate products
and can be used separately; Timely simply does not re-implement document rendering.

## What the tools do

Every tool is documented with its exact description, annotations and input schema — 31 in all,
generated from the service's own registry, never written by hand.

| Area | The question it answers | Tools |
|---|---|---|
| **[Read a programme](tools/read.md)** | What is published, what is drafted, and what changed? | 6 |
| **[Build and render](tools/build.md)** | Create, edit, restyle, preview — and where approval stops. | 7 |
| **[Websites and widgets](tools/websites.md)** | Where may the programme appear, and how does it look there? | 3 |
| **[Organisation and homepage](tools/organisation.md)** | What does the shared organisation page say, and how does it become a homepage? | 8 |
| **[Export, import and the bin](tools/lifecycle.md)** | How is a programme backed up, restored, or taken down? | 7 |

Machine-readable: **[tools.json](tools.json)** carries all 31 with full JSON Schema, plus every
excluded bucket listed by name so the count is auditable. Fourteen staff-only `admin_*` tools, ten
log and operations tools, and the `operator_guide`/`instance_status` pair are excluded from the
customer surface.

## Nothing is deleted in one step

`timely_delete` moves a programme — or the organisation page — to a bin: it leaves every public
address at once and can be brought back with `timely_restore` until the purge date that
`timely_trash_list` shows. `timely_export` returns a lossless, schema-versioned JSON backup with a
SHA-256 over its exact bytes, and `timely_import` only ever creates a new programme from a file that
validates against `timely_export_schema` — it never overwrites an existing one.

## What it does not do

- **It does not publish on its own.** Publishing takes the user's explicit yes for one revision
  and its PDF; see above.
- **It is not a calendar or a booking system.** Timely produces the programme document; it does not
  invite anyone, hold availability or send reminders.
- **It does not render its own PDFs.** That is Doksi's job, and the artifact is content-addressed so
  the approved preview and the published document are provably the same bytes.

## Plans

Plans and prices can change; **the current ones are always on <https://timely.publifye.com>**, and
where this page and the site differ, the site is right.
