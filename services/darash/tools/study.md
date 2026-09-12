# Study and cross-reference — Darash MCP tools

**What else does Scripture say about this, and which words move together?** 6 tools, listed below with the exact description and input
schema the server itself returns. Endpoint: `https://darash-api.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`word_study`](#word-study) | THE recommended tool for studying any Greek or Hebrew word |
| [`verse_study`](#verse-study) | Complete verse analysis in one call |
| [`get_cross_refs`](#get-cross-refs) | Get cross-references for a verse (related passages) |
| [`get_synonyms`](#get-synonyms) | Get the semantic-neighbour set for a Strong's number, computed from the in-memory synonym… |
| [`synonym_stats`](#synonym-stats) | Health check for the synonym graph built at startup |
| [`co_occurrence`](#co-occurrence) | Find verses where two Strong's numbers appear together |

---

## `word_study`

**Word Study** — read-only, idempotent, closed-world.

THE recommended tool for studying any Greek or Hebrew word. Complete word study in ONE call — returns everything: Strong's definition, Abbott-Smith/BDB scholarly lexicon, LSJ classical Greek, Thayer's Greek-English Lexicon 1889 (for G numbers), frequency with OT/NT breakdown, etymology tree, reverse lookup (other words translated the same way), and sample verses. Use THIS instead of calling get_strongs + lookup_dictionary(thayer) + search_strongs separately. The 'thayer' field carries 'thayer_note' naming the edition — until 2026-09-02 that field held a modern gloss set that was not Thayer's text at all, so check the note rather than trusting the field name. Then sharpen it: get_synonyms for the near-synonyms, search_strongs to see the word live in its verses.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `number` | string | yes | Strong's number with prefix (e.g., 'H2617' for Hebrew chesed, 'G26' for Greek agape) |

## `verse_study`

**Verse Study** — read-only, idempotent, closed-world.

Complete verse analysis in one call. Returns: verse text, all Strong's numbers with definitions, word-by-word morphological parsing (tense, voice, mood, case, gender), and cross-references. Replaces 4 separate tool calls (get_verse + strongs_in_verse + get_morphology + get_cross_refs).[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bible` | string | no | Bible translation for verse text (default: kjv) |
| `ref` | string | yes | Verse reference (e.g., 'Romans 3:23', 'Genesis 1:1', 'John 3:16') |

## `get_cross_refs`

**Get Cross Refs** — read-only, idempotent, closed-world.

Get cross-references for a verse (related passages). Shared lemmas are usually the connection — strongs_in_verse on both ends often lights it up.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ref` | string | yes | Bible reference (e.g., 'John 3:16') |

## `get_synonyms`

**Get Synonyms** — read-only, idempotent, closed-world.

Get the semantic-neighbour set for a Strong's number, computed from the in-memory synonym graph built at startup. Three signals unioned: shared Hebrew/Greek root, definition-word overlap (≥3 shared content words in def_short+def_long), and KJV rendering overlap (≥2 shared translation tokens in the Usage field). Much denser than get_related_strongs (which is limited to the thin 'See' + derivation field) — typically 20-50 neighbours per common Hebrew verb vs 0-3 for get_related_strongs. Each edge is weighted 0..1 and tagged with its contributing source(s). Use this to expand a verse's thematic fingerprint for empirical tests.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `language` | string | no | 'hebrew' or 'greek' (optional if using H/G prefix) |
| `limit` | integer | no | Max neighbours returned (default 30, max 50) |
| `min_weight` | number | no | Drop edges below this weight (0..1). Default 0.3 = the same threshold the graph itself enforces. |
| `number` | string | yes | Strong's number with prefix (e.g., 'H2388' for chazak 'to be strong') |

## `synonym_stats`

**Synonym Stats** — read-only, idempotent, closed-world.

Health check for the synonym graph built at startup. Returns node counts, edge counts, mean/max degree per language, and build time. Use once to confirm the graph is populated; then use get_synonyms for actual queries.[END]

## `co_occurrence`

**Co Occurrence** — read-only, idempotent, closed-world.

Find verses where two Strong's numbers appear together. Useful for studying word pairs — e.g., kentron (G2759) + thanatos (G2288) to find 'sting of death'.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | integer | no | Maximum results (default: 50, max: 200) |
| `number1` | string | yes | First Strong's number (e.g., 'G2759') |
| `number2` | string | yes | Second Strong's number (e.g., 'G2288') |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
