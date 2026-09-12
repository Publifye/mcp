# Search

**Find it by wording, by meaning, or by how rare it is.** 4 Darash MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://darash-api.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`search`](#search) | Full-text search across Bible verses |
| [`semantic_search`](#semantic-search) | Three-layer semantic engine: (1) Finds KJV verses containing the query words |
| [`word_frequency`](#word-frequency) | Count how many times a Strong's number appears in the KJV tagged text |
| [`hapax_list`](#hapax-list) | List all hapax legomena — words that appear exactly once in the Bible |

---

## `search`

**Search** — read-only, idempotent, closed-world.

Full-text search across Bible verses. Surface hits are the doorway, not the study: strongs_in_verse on any hit reaches the lemma underneath.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bible` | string | yes | Bible translation (e.g., 'kjv', 'asv', 'web') |
| `limit` | integer | no | Maximum results (default: 50, max: 200) |
| `query` | string | yes | Search text |
| `scope` | string | no | Limit search to scope (e.g., 'ot', 'nt', 'Genesis', 'John') |

## `semantic_search`

**Semantic Search** — read-only, idempotent, closed-world.

Three-layer semantic engine: (1) Finds KJV verses containing the query words. (2) Builds a meaning cluster by mapping English→Strong's numbers via reverse lookup, then expanding one hop through etymology (synonyms, derived forms, root words). (3) Searches Hebrew words from the cluster as ELS Torah codes (skip 2-100). Returns: verses, strongs_matches (substring hits), meaning_cluster (the expanded word web with source tracing), and els_hits (Hebrew cluster words found encoded in Torah letters). Multi-word queries like 'faith hope love' search each word independently and merge results.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bible` | string | no | Bible translation for verse search (default: kjv) |
| `language` | string | no | Strong's language filter: 'hebrew', 'greek', or 'both' (default: both) |
| `query` | string | yes | Word or phrase to search by meaning (e.g., 'covenant', 'redeem', 'glory') |
| `strongs_limit` | integer | no | Max Strong's matches (default: 20, max: 50) |
| `verse_limit` | integer | no | Max verse results (default: 20, max: 100) |

## `word_frequency`

**Word Frequency** — read-only, idempotent, closed-world.

Count how many times a Strong's number appears in the KJV tagged text. Returns total frequency, OT/NT breakdown, and whether it's a hapax legomenon (appears only once). Essential for word studies.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `number` | string | yes | Strong's number with prefix (e.g., 'H430' for Hebrew Elohim, 'G26' for Greek agape) |

## `hapax_list`

**Hapax List** — read-only, idempotent, closed-world.

List all hapax legomena — words that appear exactly once in the Bible. Gold for word studies and identifying rare vocabulary. Filter by Hebrew, Greek, or both.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `language` | string | no | Language filter: 'hebrew', 'greek', or 'both' (default: both) |
| `limit` | integer | no | Maximum results (default: 100, max: 500) |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
