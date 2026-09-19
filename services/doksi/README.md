# Doksi — document and PDF MCP server for Claude, Cursor and any MCP client

**Doksi turns a structured document into a professional PDF: personal and official letters, notices,
agreements, ceremonial covenants, checklists, meeting agendas and schedules — and collects signatures
by individual link or QR code. It runs as a hosted MCP server over HTTPS.**

| | |
|---|---|
| Endpoint | `https://doksi.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open |
| Registry | `pro.publifye/doksi` ([server.json](server.json); not yet published to the registry) |
| Product site | <https://doksi.publifye.com> |
| Capability tools | **22** ([full schemas](tools.json)) |

## Connect

```jsonc
{ "mcpServers": { "doksi": { "type": "http", "url": "https://doksi.publifye.com/mcp" } } }
```

Claude Code: `claude mcp add --transport http doksi https://doksi.publifye.com/mcp`, then `/mcp` to
sign in. The discovery chain is the same as for the other servers:
**[../../docs/connect.md](../../docs/connect.md)**.

## Ask what a kind requires before writing it

Most document tools accept a blob and fail at render. Doksi is built the other way round, and four of
its twenty-two tools exist only so an agent can find out what is expected **before** it composes
anything: `kind_list` names the document kinds, `purpose_list` the purposes, `block_types` the blocks
a body may contain, and `doc_requirements` states what one specific kind demands.

That ordering is deliberate. An agent that can ask what a kind requires produces far fewer refusals
than one that learns by being refused, and the difference shows up as fewer wasted calls rather than
as better error messages.

`doc_validate` then checks a composed document without rendering it, so a draft can be corrected
while it is still cheap.

## Signatures are a request, not a field

Seven tools cover signing, and the shape is a **request** with its own lifecycle rather than a
boolean on a document: create it, describe it, fetch it, replace it, revoke it, render it, and mail
it. A signer receives an individual link or a QR code; a revoked link stops working; rotating a link
does not invalidate the document it points at.

## What the tools do

Every tool is documented with its exact description, annotations and input schema — 22 in all,
generated from the service's own registry, never written by hand.

| Area | The question it answers | Tools |
|---|---|---|
| **[Catalogue](tools/catalogue.md)** | What kinds exist, and what does this one require? | 4 |
| **[Compose and validate](tools/documents.md)** | Is this document well formed, and what does it render to? | 3 |
| **[Issue, share and deliver](tools/delivery.md)** | How does someone else get at it, and how do I take it back? | 6 |
| **[Signatures](tools/signatures.md)** | Who still has to sign, and by which link? | 7 |
| **[Assets](tools/assets.md)** | How do I get a logo or a mark into a document? | 2 |

Machine-readable: **[tools.json](tools.json)** carries all 22 with full JSON Schema, plus every
excluded bucket listed by name so the count is auditable.

## What it does not do

- **Not a word processor.** Doksi renders structured documents of known kinds. It is not a place to
  lay out arbitrary pages.
- **Not a legal service.** An agreement or covenant rendered here is a document, not advice, and a
  signature collected here is not a statement about its legal effect in any jurisdiction.
- **No silent coercion.** A document that does not meet its kind's requirements is refused by
  `doc_validate` rather than rendered with the gaps filled in.

## Plans

A free tier includes a small daily allowance. Plans and prices can change; **the current ones are
always on <https://doksi.publifye.com>**, and where this page and the site differ, the site is right.
