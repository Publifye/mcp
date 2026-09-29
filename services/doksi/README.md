# Doksi — document and PDF MCP server for Claude, Cursor and any MCP client

**Doksi turns a structured document into a professional PDF: personal and official letters, notices,
agreements, ceremonial covenants, checklists, meeting agendas and schedules — and collects signatures
by individual link or QR code. It runs as a hosted MCP server over HTTPS.**

| | |
|---|---|
| Endpoint | `https://doksi.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open |
| Registry | [`pro.publifye/doksi`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) ([server.json](server.json)) |
| Product site | <https://doksi.publifye.com> |
| What it solves | <https://publifye.com/doksi> |
| Capability tools | **30** ([full schemas](tools.json)) |

## Connect

```jsonc
{ "mcpServers": { "doksi": { "type": "http", "url": "https://doksi.publifye.com/mcp" } } }
```

Claude Code: `claude mcp add --transport http doksi https://doksi.publifye.com/mcp`, then `/mcp` to
sign in. The discovery chain is the same as for the other servers:
**[../../docs/connect.md](../../docs/connect.md)**.

## Ask what a kind requires before writing it

Most document tools accept a blob and fail at render. Doksi is built the other way round, and four of
its thirty tools exist only so an agent can find out what is expected **before** it composes
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
does not invalidate the document it points at. A signing request can be made over a document you
have already kept, by its `id`, and can be given an expiry.

## What you have kept

An issued document is kept on your account. `doc_list` lists what you have kept, newest first, and
`doc_rename` gives one a private name that is never printed on it or shown to anyone else.
`doc_delete` stops its link, every temporary share link and every open signing request over it at
once, and moves it to the trash; `doc_trash` lists what can still be restored and `doc_restore`
brings it back within 7 days, with a new link. After that it is purged, and the purge is announced
in advance.

Besides a plan or the daily allowance, a document can be paid for with a purchased credit:
`doc_credit_balance` shows what is left and when each pack expires, and `doc_compose_credit`
compiles one PDF against one credit. A refused document is never charged. `doc_access_status` says
before you compose whether a covenant will come out print-ready or as a watermarked preview.

## Marriage covenants: marriage.publifye.com

**<https://marriage.publifye.com>** is Doksi's website for marriage covenants. A couple, or their
pastor or officiant, tells their own AI assistant what the covenant should say: both names, the date
and place, each person's vow, a Bible verse and the witnesses. They choose one of twelve designs and
get back a typeset one-page PDF in A4, or A3 for framing, to sign and hang on the wall.

- **Twelve designs.** Seven painted in watercolour (Champagne Butterfly, Something Blue, Blush
  Petunias, Bridal Lilies, Garden Roses, Blue Iris, Ivory Magnolia), four drawn (Together in Bloom, Butterfly Garden, Hearts Entwined, Olive &
  Promise), and Star & Blossom, with a Star of David, made for a Jewish marriage.
- **The couple's own words.** Each person writes their own vow. The 1662 Book of Common Prayer vows
  are there as an example of wording. The Bible verse is Ecclesiastes 4:12 unless the couple chooses
  one to three others, or none.
- **English and Norwegian.** Sign in ink, or by a personal signing link or QR code.
- **A keepsake, not a certificate.** Every covenant says at its foot that it is not a civil marriage
  certificate. A marriage is registered the way the couple's country requires.
- **Private.** A finished covenant is emailed only to the account that asked for it, and its link
  is never listed or indexed.

There is no separate server to connect. The site uses the Doksi server above: the assistant calls
`doc_requirements` with `kind: covenant` to learn the fields, then `doc_compose` with
`content.occasion: marriage`. Designing, checking the wording and a full preview marked PREVIEW are free with
a Publifye account. The print-ready covenant needs a 7-day marriage pass, a Doksi credit or a Doksi
plan; current prices are on <https://marriage.publifye.com/store>.

## What the tools do

Every tool is documented with its exact description, annotations and input schema — 30 in all,
generated from the service's own `tools/list`, never written by hand.

| Area | The question it answers | Tools |
|---|---|---|
| **[Catalogue](tools/catalogue.md)** | What kinds exist, and what does this one require? | 4 |
| **[Compose and validate](tools/documents.md)** | Is this document well formed, and what does it render to? | 3 |
| **[Issue, share and deliver](tools/delivery.md)** | How does someone else get at it, and how do I take it back? | 6 |
| **[Signatures](tools/signatures.md)** | Who still has to sign, and by which link? | 7 |
| **[Assets](tools/assets.md)** | How do I get a logo or a mark into a document? | 2 |
| **[Your documents](tools/kept.md)** | What have I kept, and how do I tidy or recover it? | 5 |
| **[Access and credits](tools/credits.md)** | Will it print clean, and what does it cost? | 3 |

Machine-readable: **[tools.json](tools.json)** carries all 30 with full JSON Schema, plus every
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
