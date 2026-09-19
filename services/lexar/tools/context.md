# Context and coverage

**What does it connect to, what do its terms mean, and how much of the corpus can you rely on?** 3 Lexar MCP tools, listed below with the exact description
and input schema the server itself returns. Endpoint: `https://lexar-api.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get access.

| Tool | What it does |
|---|---|
| [`connections`](#connections) | Read outgoing source-provided cross-references, including unresolved and ambiguous targets |
| [`terms`](#terms) | Browse source wordforms by prefix (without a prefix, forms containing numerals are skipped;… |
| [`status`](#status) | Read the published snapshot: per-capability readiness with concrete causes (body search,… |

---

## `connections`

**Connections** — read-only, idempotent, closed-world.

Read outgoing source-provided cross-references, including unresolved and ambiguous targets. A source link does not by itself establish a legal interpretation. Example: connections id=NL/lov/2005-06-17-62 (a provision citation selects its whole document; each edge's from names the source node). Incoming links are not offered. Next: read id=<candidate citation> for a resolved target; resolve id=<target> for an unresolved one.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `id` | string | no |  |
| `max_bytes` | integer | no |  |
| `snapshot_id` | string | no |  |

## `terms`

**Terms** — read-only, idempotent, closed-world.

Browse source wordforms by prefix (without a prefix, forms containing numerals are skipped; any prefix lists them); min_blocks hides forms indexed in fewer units (such as one-off codes), and stopword=true marks forms ignored for ranking. These are corpus vocabulary, not verified definitions or synonyms. Example: terms prefix=ferie. Next: search query=<form>.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `max_bytes` | integer | no |  |
| `min_blocks` | integer | no |  |
| `prefix` | string | no |  |
| `snapshot_id` | string | no |  |

## `status`

**Status** — read-only, idempotent, closed-world.

Read the published snapshot: per-capability readiness with concrete causes (body search, resolution, keyword search, published metadata, revisions, annotations, publication), corpus composition, languages, acquisition dates and cross-reference resolution counts. id=<document ID or citation> reports that target instead: legal-effect uncertainty with verbatim in-force source facts, coverage (nodes, outgoing references by state; incoming unavailable), source freshness, enrichment availability and versions. dataset=<name> reports that dataset's coverage boundary and acquisition; id and dataset are exclusive. Memory read; no Redis or network access. Example: status id=NL/lov/2005-06-17-62. Next: search or resolve to start research; read id=<same> view=metadata for all source facts.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no |  |
| `dataset` | string | no |  |
| `id` | string | no |  |
| `max_bytes` | integer | no |  |
| `snapshot_id` | string | no |  |

---

*Generated from the live `tools/list` on 2026-09-16. Regenerate rather than edit by hand.*
