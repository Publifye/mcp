# Junifye — book and study authoring MCP server for Claude, Cursor and any MCP client

**Junifye lets an AI assistant write a structured book with you — chapters, blocks, headings,
Scripture quotations, tables, figures — and then publish it as a print-ready PDF, an EPUB 3, a web
reader and more, from one source. It runs as a hosted MCP server over HTTPS.**

| | |
|---|---|
| Endpoint | `https://junifye.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open · or `X-API-Key` |
| Registry | [`pro.publifye/junifye`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) ([server.json](server.json)) |
| Product site | <https://junifye.publifye.com> |
| What it solves | <https://publifye.com/junifye> |
| Capability tools | **151** ([full schemas](tools.json)) |

## What the tools do

Every tool is documented with its exact description, annotations and input schema —
151 in all, generated from the service's own `tools/list`, never written by hand.

| Area | The question it answers | Tools |
|---|---|---|
| **[Books and editions](tools/books.md)** | Create a book, read it back, publish it, link its translations. | 34 |
| **[Chapters](tools/chapters.md)** | Create, order, version, diff and revert chapters. | 14 |
| **[Blocks and spans](tools/content.md)** | The authoring surface: paragraphs, headings, quotations, lists, tables, figures, and inline markup. | 34 |
| **[Print, ISBN and store](tools/publishing.md)** | Press-ready output, real ISBN-13 assignment, and retail publishing. | 9 |
| **[Groups, guests and notes](tools/collaboration.md)** | Share a book, invite an editor, keep private working notes. | 38 |
| **[Covers, images and figures](tools/assets.md)** | Covers, logos, figures and uploads. | 22 |

Machine-readable: **[tools.json](tools.json)** carries all 151 callable tools (151 capability, 0 session/cache) with full JSON Schema, plus every excluded bucket listed by name so the count is auditable.


## Connect

```jsonc
{ "mcpServers": { "junifye": { "type": "http", "url": "https://junifye.publifye.com/mcp" } } }
```

See **[../../docs/connect.md](../../docs/connect.md)**.

## What makes it different from asking a model to write a book

**The AI never touches JSON or LaTeX.** Authoring happens through block and span tools against a
plain-text source grammar, so the model edits meaning and the system owns the typesetting.

**Scripture quotations are verified, not remembered.** A Bible-quote block resolves against Darash.
A misquotation or a wrong Strong's number is rejected at write time rather than discovered in print.
This is the single most common failure when a language model writes about the Bible, and it is
closed here by construction.

**One source, many outputs.** Reader PDFs in light and dark, a press-ready print interior with the
correct binding gutter, a full wrap cover, EPUB 3, TXT, TeX, an HTML reader and a JSON bundle.

**Print that a printer will accept.** Printer presets, spine formula, gutter ladder, bleed, PDF/X
and a low-DPI press report before you send the file.

**Real ISBN-13 assignment** from an allocated registrant pool — not a placeholder.

**Right-to-left typesetting for Hebrew, Arabic, Persian and Urdu**, done as real typesetting with
an explicit LTR-island span, not a CSS direction flip.

**Versioning you can rely on** — word-level diff, revert, freeze, and linked language editions.

## Your work

See **[DATA-HANDLING.md](DATA-HANDLING.md)** for what the service guarantees about recovering,
exporting and deleting the material you write.

## Plans

Junifye is sold on its own and bundled with Lexifye, with a free trial.
**Current plans and prices are on <https://junifye.publifye.com>**, which is the only place they
are authoritative. They are deliberately not duplicated here.
