# Finding the law

**Which law or regulation is this, and where is the wording that matters?** 2 Lexar MCP tools, listed below with the exact description
and input schema the server itself returns. Endpoint: `https://lexar-api.publifye.pro/mcp`.
See [connect](../../../docs/connect.md) to get access.

| Tool | What it does |
|---|---|
| [`resolve`](#resolve) | Resolve a document ID, Lovdata citation, title, short title (ferieloven), abbreviation (aml)… |
| [`search`](#search) | Search legal source provisions and blocks with Norwegian lexical ranking, or kind=keyword for… |

---

## `resolve`

**Resolve** — read-only, idempotent, closed-world.

Resolve a document ID, Lovdata citation, title, short title (ferieloven), abbreviation (aml) bokmål/nynorsk law-name form (arbeidsmiljølova) or printed chapter citation (NL/lov/2005-06-17-62/kap10; Lovdata's positional KAPITTEL_N addresses carry printed_chapter). Each candidate carries match_kind, confidence and resolution=unique|ambiguous|unresolved; near misses are suggestions only. Multiple matches are candidates; no implicit choice is made. Ambiguous candidates, here and in search's exact tier, list current consolidated text before announcements, then by dataset, document and source node (candidate_order); this order is not a statement of legal effect. Example: resolve id=ferieloven. Next: read id=<candidate citation or document_id>; outline id=<document_id>.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `id` | string | no |  |
| `max_bytes` | integer | no |  |
| `snapshot_id` | string | no |  |

## `search`

**Search** — read-only, idempotent, closed-world.

Search legal source provisions and blocks with Norwegian lexical ranking, or kind=keyword for accepted labels with evidence handles (exact, whole-word, then 4+ letter parts: ferie finds feriepenger; type=<annotation type> narrows). Plain queries match any substantive term and rank by BM25F relevance (title, heading, body) × query-term coverage × document tier; every hit shows these factors in ranking. Exact citations and legacy IDs, law names from the resolve alias table (ferieloven, aml, arbeidsmiljølova), "name § number" and "name kapittel number" (the chapter the law prints, match_kind=printed_chapter) rank first. An unknown role, kind or language returns invalid_filter naming the valid values. Every page, empty too, carries diagnostics: searched, matched and dropped terms and empty_reason. Default role is body; role=amendment_note or role=amendment_text (Lovdata change blocks; instruction parts of acts declared amending by title and changesToDocuments, not their commencement text) searches those, and role_excluded counts what body search left out; roles are structural, not legal effect. Each excerpt is an exact prefix of the hit node's decoded text, inline citation wording included, ending at a word boundary (excerpt_end_byte; excerpt_truncated=true when read has more). Returns attribution and a bounded continuation cursor. Example: search query="rett til ferie". Next: read id=<address.citation or document_id> (node_id for a block) for exact wording; connections id=<same> for its links.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `id` | string | no |  |
| `kind` | string | no |  |
| `language` | string | no |  |
| `max_bytes` | integer | no |  |
| `query` | string | no |  |
| `role` | string | no |  |
| `snapshot_id` | string | no |  |
| `type` | string | no |  |

---

*Generated from the live `tools/list` on 2026-09-16. Regenerate rather than edit by hand.*
