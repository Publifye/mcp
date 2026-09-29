# Finding the law

**Which law or regulation is this, and where is the wording that matters?** 2 Lexar MCP tools, listed below with the exact description
and input schema the server itself returns. Endpoint: `https://lexar-api.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get access.

| Tool | What it does |
|---|---|
| [`resolve`](#resolve) | Resolve a document ID, Lovdata citation, title, short title (ferieloven), abbreviation… |
| [`search`](#search) | Search source provisions and blocks in Norwegian; kind=keyword searches accepted labels… |

---

## `resolve`

**Resolve** — read-only, idempotent, closed-world.

For a law name or loose reference; a citation goes straight to read. Resolve a document ID, Lovdata citation, title, short title (ferieloven), abbreviation (aml) bokmål/nynorsk law-name form (arbeidsmiljølova) or printed chapter citation (NL/lov/2005-06-17-62/kap10; positional KAPITTEL_N addresses carry printed_chapter). Each candidate carries match_kind, confidence and resolution=unique|ambiguous|unresolved; near misses are suggestions only and no implicit choice is made. Ambiguous candidates (here and in search's exact tier) list current consolidated text before announcements, then by dataset, document and source node (candidate_order); that order states no legal effect. Every candidate carries in_force (true|false|unknown) with in_force_basis, and candidates in force are listed first. Example: resolve id=ferieloven; resolve id="aml § 15-7 annet ledd" — a written reference in either order (or aml 15-7, § 15-7 (2)) resolves to the provision; ledd/bokstav/nr are reported as scope, and read of the same text reads just the ledd; several §§ return one result each. Next: read id={candidate citation}; outline id={document_id}.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `id` | string | no |  |
| `max_bytes` | integer | no |  |
| `snapshot_id` | string | no |  |

## `search`

**Search** — read-only, idempotent, closed-world.

Plain-language questions start here. Search source provisions and blocks in Norwegian; kind=keyword searches accepted labels with evidence handles (type= narrows). Inflections fold both ways. queries=[..] (max 8) fuses phrasings into ONE list (matched_queries). Exact citations, legacy IDs, aliases (ferieloven, aml) and "name § number" rank first. id= keeps the search inside one act: a document ID, citation, or a name or reference only one act carries (id_scope says which; a shared name is refused). Compact hits: rank, citation (pass straight to read: it reads exactly the hit), title, short_title, heading_path, kind (lov/forskrift/EU-rettsakt/Lovtidend), excerpt (exact node-text prefix), score, in_force, matched, forarbeider_total (+forarbeider_hidden). matched says which terms hit WHERE (title/heading/body/compound/forarbeider_context/lay_vocabulary). in_force true|false|unknown from Lovdata's commencement header (in_force_basis, in_force_from); false never ranks above a same-named act in force. detail=full adds address, ranking, role, source_url, offsets, unit_kind. Every page, empty too, carries diagnostics: searched/matched/dropped/expanded/rescued terms, empty_reason, not_in_force_warning; filters_excluded_all_matches adds excluded_by and a next_action without that filter. Default role=body; amendment_note|amendment_text search change blocks. Unknown role/kind/language/detail: invalid_filter. Example: search query="rett til ferie". Next: read id={citation}; connections id={same}.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `detail` | string | no |  |
| `id` | string | no |  |
| `kind` | string | no |  |
| `language` | string | no |  |
| `max_bytes` | integer | no |  |
| `queries` | array | no |  |
| `query` | string | no |  |
| `role` | string | no |  |
| `snapshot_id` | string | no |  |
| `type` | string | no |  |

---

*Generated from the live `tools/list` (0.1.96) on 2026-09-29. Regenerate rather than edit by hand.*
