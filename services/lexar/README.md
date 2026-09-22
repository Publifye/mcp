# Lexar — Norwegian law as an MCP server for Claude, Cursor and any MCP client

**Lexar puts the current text of Norwegian law in front of an AI assistant: consolidated statutes
and central regulations from Lovdata, with the citation and the source URL attached to every
passage it returns. It is a research surface, not legal advice — it hands you the wording and tells
you what it does not cover.**

| | |
|---|---|
| Endpoint | `https://lexar-api.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open |
| Registry | [`pro.publifye/lexar`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) ([server.json](server.json)) |
| Product site | <https://lexar.publifye.com> |
| What it solves | <https://publifye.com/lexar> |
| Research tools | **7** ([full schemas](tools.json)) |

## Connect

```jsonc
{ "mcpServers": { "lexar": { "type": "http", "url": "https://lexar-api.publifye.com/mcp" } } }
```

The OAuth flow runs in the browser on first use. See **[../../docs/connect.md](../../docs/connect.md)**.

## The corpus

Measured on the live service, **2026-09-16**, via `status`:

| | |
|---|---|
| Documents | 6,859 |
| Current consolidated law | 5,871 — 759 statutes, 5,112 central regulations |
| Announcements (Norsk Lovtidend avd. I, 2026) | 988 |
| Indexed blocks | 457,743 |
| Distinct word forms | 301,140 |
| Cross-references extracted | 290,805 |
| Document aliases | 5,054 keys, 1,566 conventional forms |

Source acquired **2026-09-12** from the Lovdata publicData API. Source snapshot
`82cff3294c90969e6fc78393d5d24c842e5555ac323593904b104afe1c5e4f11`.

## What the tools do

Seven tools, and the number is fixed by specification rather than by what happened to get built —
richer capability goes into typed inputs and results, not into more tools.

| Area | The question it answers | Tools |
|---|---|---|
| **[Finding the law](tools/finding.md)** | Which law or regulation is this, and where is the wording that matters? | 2 |
| **[Reading it](tools/reading.md)** | What does the provision actually say, and how is the document put together? | 2 |
| **[Context and coverage](tools/context.md)** | What does it connect to, what do its terms mean, and how much can you rely on? | 3 |

Machine-readable: **[tools.json](tools.json)** carries all 7 with full JSON Schema, plus the
excluded buckets listed by name so the count is auditable.

**`resolve` never picks silently.** A law name or an ambiguous citation returns candidates, because
guessing which statute someone meant is the one failure a legal research tool must not have.

## What it does not cover — read this before you rely on it

**[PROVENANCE.md](PROVENANCE.md)** records the source, the licence, the measured corpus and the
gaps. The short version, because it decides whether Lexar can answer your question at all:

Not in the corpus: **court decisions**, **preparatory works** (*forarbeider*), **local
regulations**, **English translations**, and **historical consolidated versions**. So *no hit does
not mean no law* — it may mean the answer lives somewhere Lexar does not hold.

And a document being present is not proof that every provision in it is in force. Publication,
consolidation and legal commencement are three separate facts, and Lexar distinguishes them rather
than flattening them into one.

Lexar provides source text and navigation. It does not generate legal advice.

## Licence and attribution

Data from Lovdata under **[NLOD 2.0](https://data.norge.no/nlod/no/2.0)**, which permits commercial
reuse and redistribution under its own conditions.

> Inneholder data fra Lovdata under Norsk lisens for offentlige data (NLOD) 2.0.

Lexar sells hosted access, indexing, availability and operational service — **not** the corpus. The
underlying open legal data stays open, and nothing here restricts a right NLOD already grants you.
Lexar's own formatting, indexes and derived classifications are identified separately from the
source text.

## Plans

**Current plans and prices are on <https://lexar.publifye.com>**, which is the only place they are
authoritative. They are deliberately not duplicated here.
