# Reading it

**What does the provision actually say, and how is the document put together?** 2 Lexar MCP tools, listed below with the exact description
and input schema the server itself returns. Endpoint: `https://lexar-api.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get access.

| Tool | What it does |
|---|---|
| [`read`](#read) | Read exact legal source wording, published metadata or retained evidence |
| [`outline`](#outline) | List the complete source document tree, including appendices, tables and documents without… |

---

## `read`

**Read** — read-only, idempotent, closed-world.

Read exact legal source wording, published metadata or retained evidence. view=text (default) returns exact spans of the node's decoded text with start_byte/end_byte (half-open UTF-8 offsets into that text) and node_bytes. view=evidence: start_byte/end_byte are capture-time offsets into the whole document's decoded text (offset_base=document). current=true adds verified node_id with node_start_byte/node_end_byte, the view=text frame (current_start_byte/current_end_byte only if the document changed); current=false gives current_reason and no current offsets. Segments end at sentence or word boundaries and are at most max_bytes/8 bytes (3,072 at the 24 KiB default); metadata, note and quotation fields use fixed 128-byte segments. continued=true means a single unbroken token exceeded the segment and was split at a UTF-8 character boundary. A segment is presentation only: concatenate consecutive segments in order before quoting. view=metadata pages source metadata as small items; view=notes on a source ID states that source text has no notes, while metadata and evidence records return their notes with view=notes or include_notes=true. Administrators on the master can also read unpublished drafts. Resolve ambiguous citations first and follow cursor-only continuation. Example: read id=NL/lov/2005-06-17-62/§14-9. Next: connections id=<same> for cross-references; outline id=<document_id> for structure; status id=<same> for legal-effect uncertainty.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `id` | string | no |  |
| `include_notes` | boolean | no |  |
| `max_bytes` | integer | no |  |
| `node_id` | integer | no |  |
| `revision` | string | no |  |
| `snapshot_id` | string | no |  |
| `view` | string | no |  |

## `outline`

**Outline** — read-only, idempotent, closed-world.

List the complete source document tree, including appendices, tables and documents without numbered provisions. Each node carries its source citation and Lovdata anchor; anchors are positional HTML ids whose nouns (kapittel, paragraf) and numbers need not match the law. printed_chapter gives the chapter a section heading prints; book/chapter/article-addressed laws and treaties (NL/lov/1687-04-15/b1/k21/a15) add printed_structure with printed_book, printed_chapter and printed_article, stated only where the citation and the heading agree. read returns the same labels with a node's first segment. Requires id (document ID or citation) on the first call; continue with cursor alone. Example: outline id=NL/lov/2005-06-17-62. Next: read id=<document_id> node_id=<node_id>.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `id` | string | no |  |
| `max_bytes` | integer | no |  |
| `snapshot_id` | string | no |  |

---

*Generated from the live `tools/list` on 2026-09-16. Regenerate rather than edit by hand.*
