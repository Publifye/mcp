# Reading it

**What does the provision actually say, and how is the document put together?** 2 Lexar MCP tools, listed below with the exact description
and input schema the server itself returns. Endpoint: `https://lexar-api.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get access.

| Tool | What it does |
|---|---|
| [`read`](#read) | Read exact legal wording or metadata |
| [`outline`](#outline) | The table of contents under id (a document or any unit read takes): parts, chapters,… |

---

## `read`

**Read** — read-only, idempotent, closed-world.

Read the chosen hit before answering; quote only this. Read exact legal wording or metadata. id: a citation, a hit's citation, or a reference resolve answers uniquely (aml § 15-7, aml 15-7; "aml § 15-7 annet ledd" reads just that ledd; resolved says what it was read as). view=text (default): exact spans of the node's decoded text, half-open UTF-8 start_byte/end_byte, node_bytes. The text has no space or newline where ledd, paragraphs or headings meet: view=paragraphs gives the same text and offsets, one segment per printed unit; quote unit by unit. Segments end at sentence/word boundaries, at most max_bytes/8; continued=true means an unbroken token was split. breaks lists the unit breaks inside a segment; ends_paragraph marks one stopping at a break. ledd names every ledd the segment covers: index (the source's own number, never disagreeing with marker), provision, node_id, byte range; ledd_count rides the first segment. marked=printed: marker is a verbatim prefix of the wording; forms "(2)" "2." "2)" "2 ". unnumbered: none printed, cite by position, invent none. view=metadata pages metadata; view=notes: source has none, records return theirs; start_byte/end_byte: forarbeider windows only. With a store (status), a provision's FIRST segment adds forarbeider pointers, _total/_more/_truncated; a ranked store keeps one per document, adds _hidden/_notice/_enacting/_sources. Law offsets never move. Example: read id=NL/lov/2005-06-17-62/§14-9. Next: connections id={same}; outline id={doc}; status id={same}.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `end_byte` | integer | no |  |
| `id` | string | no |  |
| `include_notes` | boolean | no |  |
| `max_bytes` | integer | no |  |
| `node_id` | integer | no |  |
| `revision` | string | no |  |
| `snapshot_id` | string | no |  |
| `start_byte` | integer | no |  |
| `view` | string | no |  |

## `outline`

**Outline** — read-only, idempotent, closed-world.

For structure, not answers. The table of contents under id (a document or any unit read takes): parts, chapters, provisions and appendices, the id's own unit first, each with citation (read and outline accept it), heading (≤120 B, …=cut), node_id, depth and children (units beneath; outline its citation to go deeper). depth=1 (default) to 3 levels. printed_chapter gives the chapter a section heading prints; book/chapter/article-addressed laws and treaties add printed_structure with printed_book, printed_chapter and printed_article, only where citation and heading agree. A forarbeider id (status lists id namespaces) lists that document's headings: heading, read; designation/session once per page. Continue with cursor alone. Example: outline id=NL/lov/2005-06-17-62. Next: read id={citation}; outline id={citation}.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `depth` | integer | no |  |
| `id` | string | no |  |
| `max_bytes` | integer | no |  |
| `snapshot_id` | string | no |  |

---

*Generated from the live `tools/list` (0.1.96) on 2026-09-29. Regenerate rather than edit by hand.*
