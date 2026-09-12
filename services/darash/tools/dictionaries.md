# Dictionaries — Darash MCP tools

**What do the reference works say, and which work is it?** 4 tools, listed below with the exact description and input
schema the server itself returns. Endpoint: `https://darash-api.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`list_dicts`](#list-dicts) | List all 13 Bible dictionaries |
| [`lookup_dictionary`](#lookup-dictionary) | Search 13 Bible dictionaries |
| [`multi_dict_lookup`](#multi-dict-lookup) | Search ALL 13 Bible dictionaries in one call |
| [`list_dict_topics`](#list-dict-topics) | List all topics in a dictionary with byte-based pagination |

---

## `list_dicts`

**List Dicts** — read-only, idempotent, closed-world.

List all 13 Bible dictionaries. Each carries its full provenance block (work, author, edition, source, method, licence, imported, identification, known gaps) — read it before quoting a definition as a named scholar's work. SHORTCUT: For Greek/Hebrew word study, use word_study tool instead — it combines get_strongs + Thayer + frequency + etymology in one call. For topical research: isbe (deep encyclopedia) → fausset (theology) → easton/smith (concise). For typology: wilsons (what symbols mean). For rhetoric: bullinger (figures of speech). For English: webster (unabridged; edition not pinned). NOTE: 'thayer' is Thayer's Greek-English Lexicon (Harper & Brothers, 1889 Corrected Edition), transcribed from the page images — installed 2026-09-02, replacing a short modern gloss set that had been served under Thayer's name and was not his text.[END]

## `lookup_dictionary`

**Lookup Dictionary** — read-only, idempotent, closed-world.

Search 13 Bible dictionaries. Every response carries the dictionary's provenance block — read it before quoting a definition as a named scholar's work. WORKFLOW: For Greek words, start with get_strongs for the basic definition, then use 'thayer' here for the deep lexicon (numbered senses, classical citations, prepositional constructions — keyed by G number like 'G26' AND by Greek headword like 'ἀγάπη'). For topics/concepts, start with 'isbe' (deep encyclopedia), then 'fausset' (theology/typology), then 'easton'/'smith' (concise). For biblical symbols/types (what silver, bread, fire, water MEAN typologically): 'wilsons'. For rhetorical figures (irony, metaphor, hendiadys): 'bullinger'. For name meanings: 'hitchcock'. For topical verse lists: 'navestb'. For KJV-era English: 'webster'. For devotional: 'hawker'. For doctrinal outlines: 'torrey'. NOTE on thayer: this is the genuine 1889 Corrected Edition, transcribed from the page images and installed 2026-09-02; it REPLACED a short modern gloss set that had circulated under Thayer's name for 14+ years and was not his text. Each entry carries the printed pages it was read off and the sha256 of its verbatim printed text, and the entry's terminal asterisk is Thayer's own claim that every NT occurrence is cited. Thayer held Unitarian views — on deity-of-Christ passages (G2316, G166) read the philology, take the theology elsewhere. Meet the lexicon in the text afterwards: search_strongs for usage, get_morphology at a cited verse.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dictionary` | string | yes | Dictionary: thayer (Thayer's Greek-English Lexicon 1889 — the ONLY dict that takes G numbers like 'G26', and it also takes the Greek headword), isbe (encyclope… |
| `query` | string | yes | Topic to look up |

## `multi_dict_lookup`

**Multi Dict Lookup** — read-only, idempotent, closed-world.

Search ALL 13 Bible dictionaries in one call. Returns consolidated results from every dictionary that has an entry for the topic. Saves making 13 separate lookup_dictionary calls.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | Topic to look up across all dictionaries (e.g., 'Paul', 'Jerusalem', 'faith') |

## `list_dict_topics`

**List Dict Topics** — read-only, idempotent, closed-world.

List all topics in a dictionary with byte-based pagination. Use to build client-side linking of dictionary terms. Fetches topics until max_bytes reached.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dictionary` | string | yes | Dictionary name (easton, smith, hitchcock, fausset, navestb, torrey, hawker, wilsons, ats, isbe, webster, bullinger, thayer) |
| `max_bytes` | integer | no | Max bytes for topics (default: 80KB, max: 100KB). Pagination by size ensures MCP compatibility. |
| `offset` | integer | no | Starting index (0-based, default: 0) |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
