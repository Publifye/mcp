# Context and coverage

**What does it connect to, what do its terms mean, and how much of the corpus can you rely on?** 3 Lexar MCP tools, listed below with the exact description
and input schema the server itself returns. Endpoint: `https://lexar-api.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get access.

| Tool | What it does |
|---|---|
| [`connections`](#connections) | Read outgoing source-provided cross-references, including unresolved and ambiguous targets |
| [`terms`](#terms) | Browse source wordforms by prefix (without a prefix, forms containing numerals are… |
| [`status`](#status) | Read the published snapshot: per-capability readiness and causes, the forarbeider store… |

---

## `connections`

**Connections** — read-only, idempotent, closed-world.

After read: exceptions, definitions elsewhere. Read outgoing source-provided cross-references, including unresolved and ambiguous targets. A provision or chapter id gives ITS OWN edges; scope=document, or a document id, gives the whole act's. The page's connections object states scope and edges; each edge's from carries citation, the provision its citing text is in. kind=forarbeider instead pages one provision citation's preparatory-works pointers, best first, each with read (pass it back to read: the window, with designation, session, licence, attribution, forarbeider_build and, first segment, chain, or chain_omitted=true: no room), kind (heuristic), designation, session, heading_path (…=cut); only as exceptions: tier, confidence, window, cite_at, same_act, document_law, hidden. include_low_confidence=true adds cells hand-labelled under 85% precision; an empty default page says low_confidence and gives that call as next_action. On a ranked store (status ranking) quoted law text and duplicate windows are hidden by default, include_hidden=true lists them labelled, and the page's forarbeider object states total, hidden counts, sources and, if none shown, a notice and the enacting document. Prop./Ot.prp. after 2005 are mostly NOT held: in a chain they are designations with held=false, never text. Example: connections id=NL/lov/2005-06-17-62/§15-7 (incoming links are not offered). Next: read id={candidate citation}; resolve id={unresolved target}.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `id` | string | no |  |
| `include_hidden` | boolean | no |  |
| `include_low_confidence` | boolean | no |  |
| `kind` | string | no |  |
| `max_bytes` | integer | no |  |
| `scope` | string | no |  |
| `snapshot_id` | string | no |  |

## `terms`

**Terms** — read-only, idempotent, closed-world.

Find the statutory form of a not_in_corpus word. Browse source wordforms by prefix (without a prefix, forms containing numerals are skipped; any prefix lists them); min_blocks hides forms indexed in fewer units (such as one-off codes), and stopword=true marks forms ignored for ranking. These are corpus vocabulary, not verified definitions or synonyms. Example: terms prefix=ferie. Next: search query={form}.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `max_bytes` | integer | no |  |
| `min_blocks` | integer | no |  |
| `prefix` | string | no |  |
| `snapshot_id` | string | no |  |

## `status`

**Status** — read-only, idempotent, closed-world.

Not needed per question. Read the published snapshot: per-capability readiness and causes, the forarbeider store (loaded or not_loaded with its cause, documents by type, build id, tier policy, ranking or unranked, attribution), corpus composition, languages, acquisition dates and cross-reference resolution counts. id=<document ID or citation> reports that target instead: legal-effect uncertainty with verbatim in-force source facts, coverage (nodes, outgoing references by state; incoming unavailable), source freshness and enrichment versions. dataset=<name> reports that dataset's coverage boundary and acquisition; id and dataset are exclusive. Memory read; no Redis or network access. Example: status id=NL/lov/2005-06-17-62. Next: search or resolve; read id={same} view=metadata.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `dataset` | string | no |  |
| `id` | string | no |  |
| `max_bytes` | integer | no |  |
| `snapshot_id` | string | no |  |

---

*Generated from the live `tools/list` (0.1.96) on 2026-09-29. Regenerate rather than edit by hand.*
