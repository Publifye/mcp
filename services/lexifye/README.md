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

## Your work

See **[DATA-HANDLING.md](DATA-HANDLING.md)**.

## Plans

Lexifye is sold on its own and bundled with Junifye, with a free trial.
**Current plans and prices are on <https://lexifye.publifye.com>**, which is the only place they
are authoritative. They are deliberately not duplicated here.
