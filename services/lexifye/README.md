# Lexifye — dictionary and glossary building MCP server for Claude, Cursor and any MCP client

**Lexifye keeps the words you study — your senses, your references, the Hebrew and Greek behind
them — as a real dictionary with revision history, and turns the same entries into a print-ready
book. It runs as a hosted MCP server over HTTPS.**

| | |
|---|---|
| Endpoint | `https://lexifye.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open · or `X-API-Key` |
| Registry | `pro.publifye/lexifye` |
| Product site | <https://lexifye.publifye.com> |
| What it solves | <https://publifye.com/lexifye> |
| Capability tools | **63** ([full schemas](tools.json)) |

## Connect

```jsonc
{ "mcpServers": { "lexifye": { "type": "http", "url": "https://lexifye.publifye.com/mcp" } } }
```

See **[../../docs/connect.md](../../docs/connect.md)**.

## The shape

**Dictionary → entry (lemma) → definition (sense).** Three levels, and the tool names say
`definition_*` where the reading register says "sense".

**Round-trippable markup.** The source grammar satisfies `parse(render(x)) == x`, so a definition
can be read out, edited and written back without drift.

**Strong's enrichment from Darash.** Cite `[H2617]` in a definition and the lemma, SBL
transliteration and gloss are written in for you.

**Six formats from one source** — light PDF, dark PDF, a 6×9″ print interior, EPUB 3, an HTML
reader and JSON.

**Sixteen typesettable scripts, three right-to-left** (Hebrew, Arabic, Persian), with real
bidirectional typesetting and a glyph gate that fails loudly rather than shipping tofu.

**Version history, diff and revert per definition**, plus guest editors with instant revoke.

**A note on visibility:** dictionary artifacts are credentialled. There is no public shareable
reader URL, by design.

## What the tools do

Every tool is documented with its exact description, annotations and input schema —
63 in all, generated from the service's own `tools/list`, never written by hand.

| Area | The question it answers | Tools |
|---|---|---|
| **[Dictionaries](tools/dictionaries.md)** | Create a dictionary, set its fields, freeze it, recover it. | 14 |
| **[Entries and definitions](tools/entries.md)** | The lemma and sense tree, with per-definition history, diff and revert. | 20 |
| **[Groups, guests and notes](tools/collaboration.md)** | Share a dictionary, invite an editor, keep private notes. | 26 |
| **[Markup and recovery](tools/authoring.md)** | The round-trippable source grammar, house style, and the trash. | 3 |

Machine-readable: **[tools.json](tools.json)** carries all 63 callable tools (63 capability, 0 session/cache) with full JSON Schema, plus every excluded bucket listed by name so the count is auditable.

## Your work

See **[DATA-HANDLING.md](DATA-HANDLING.md)**.

## Plans

Lexifye is sold on its own and bundled with Junifye, with a free trial.
**Current plans and prices are on <https://lexifye.publifye.com>**, which is the only place they
are authoritative. They are deliberately not duplicated here.

## Written about this work

- [Two arks, one word](https://blog.publifye.com/p/two-arks-one-word) — Norwegian calls Noah's vessel an ark and Moses'
  basket a *kiste*; Hebrew uses one word for both. Multiply that across thirty-six languages and
  you have the reason this service exists. Also in Norwegian, Spanish, Chinese and Korean.
