# Timely — meeting programme MCP server for Claude, Cursor and any MCP client

**Timely builds a meeting programme — a fixed number of meetings, or everything inside a calendar
period — keeps every revision, and renders the approved version to a PDF through Doksi. A person
approves; an AI cannot. It runs as a hosted MCP server over HTTPS.**

| | |
|---|---|
| Endpoint | `https://timely.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open |
| Registry | `pro.publifye/timely` ([server.json](server.json); not yet published to the registry) |
| Product site | <https://timely.publifye.com> |
| Capability tools | **8** ([full schemas](tools.json)) |

## Connect

```jsonc
{ "mcpServers": { "timely": { "type": "http", "url": "https://timely.publifye.com/mcp" } } }
```

Claude Code: `claude mcp add --transport http timely https://timely.publifye.com/mcp`, then `/mcp`
to sign in. The discovery chain is the same as for the other servers:
**[../../docs/connect.md](../../docs/connect.md)**.

## An AI cannot publish a programme

`draft_approve` exists, is documented, and **refuses every MCP caller**. It returns:

> human approval required: open the account preview and approve there; MCP cannot publish

That is the whole design, not a limitation waiting to be lifted. An assistant may create a
programme, edit it, restyle it and render a preview — everything up to the point where a document
becomes the one a congregation or a committee will actually read. Publishing needs a person looking
at the rendered preview and confirming it. The tool is present rather than absent so an agent
discovers the boundary by reading the surface, instead of by guessing why nothing was published.

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

Every tool is documented with its exact description, annotations and input schema — 8 in all,
generated from the service's own registry, never written by hand.

| Area | The question it answers | Tools |
|---|---|---|
| **[Read a programme](tools/read.md)** | What is published, what is drafted, and what changed? | 3 |
| **[Build and render](tools/build.md)** | Create, edit, restyle, preview — and where approval stops. | 5 |

Machine-readable: **[tools.json](tools.json)** carries all 8 with full JSON Schema, plus every
excluded bucket listed by name so the count is auditable. `admin_timely_list` is staff-only and is
excluded from the customer surface.

## What it does not do

- **It does not publish.** See above. This is the point of the product, not a gap in it.
- **It is not a calendar or a booking system.** Timely produces the programme document; it does not
  invite anyone, hold availability or send reminders.
- **It does not render its own PDFs.** That is Doksi's job, and the artifact is content-addressed so
  the approved preview and the published document are provably the same bytes.

## Plans

Plans and prices can change; **the current ones are always on <https://timely.publifye.com>**, and
where this page and the site differ, the site is right.
