# Hebrew and Greek

**What is this word, grammatically and lexically — voice, person, stem, lemma, and what the lexicons say?** 9 Darash MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://darash-api.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`get_morphology`](#get-morphology) | Get word-by-word morphological analysis (grammatical parsing) for a Bible verse |
| [`strongs_in_verse`](#strongs-in-verse) | Extract all Strong's numbers from a verse |
| [`get_strongs`](#get-strongs) | Get Strong's concordance entry with full scholarly lexicon data |
| [`reverse_strongs`](#reverse-strongs) | Find Strong's numbers from an English word |
| [`search_strongs`](#search-strongs) | Find all KJV verses containing a specific Strong's number |
| [`search_strongs_definition`](#search-strongs-definition) | Search Strong's concordance entries by keyword in definitions |
| [`get_related_strongs`](#get-related-strongs) | Get all words related to a Strong's number — synonyms, antonyms, derived forms, and root words |
| [`etymology_tree`](#etymology-tree) | Trace the etymology of a Strong's number through multiple levels |
| [`hebrew_pictographs`](#hebrew-pictographs) | Get the ancient pictographic meanings of Hebrew letters |

---

## `get_morphology`

**Get Morphology** — read-only, idempotent, closed-world.

Get word-by-word morphological analysis (grammatical parsing) for a Bible verse. Returns each original Hebrew/Greek word with its Strong's number, morphology code, and human-readable description (e.g., 'Verb, Aorist, Active, Indicative, 3rd Person, Singular'). Covers all 66 books. For what a parsed word means across all its occurrences, follow it into word_study.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ref` | string | yes | Verse reference (e.g., 'Genesis 1:1', 'John 3:16') |

## `strongs_in_verse`

**Strongs In Verse** — read-only, idempotent, closed-world.

Extract all Strong's numbers from a verse. Returns every Hebrew/Greek word with its Strong's number, lemma, transliteration, and short definition. Quick way to see everything in a verse.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ref` | string | yes | Verse reference (e.g., 'Genesis 1:1', 'John 3:16') |

## `get_strongs`

**Get Strongs** — read-only, idempotent, closed-world.

Get Strong's concordance entry with full scholarly lexicon data. Returns: def_short (one-line gloss), def_long (detailed definitions), usage (KJV translations), abbott_smith (full Abbott-Smith Greek lexicon for NT words, or Brown-Driver-Briggs for OT words — about half the Hebrew entries carry the OpenScriptures BDB article, the rest STEPBible's abridged BDB; where a Strong's number covers more than one homonym every branch is returned, each labelled with its extended Strong's key such as H2617a / H2617b), lsj (Liddell-Scott-Jones classical Greek lexicon showing usage in secular Greek literature — Greek words only), step_gloss (one-word translation), plus etymology, pronunciation, and morphology data. def_short orients you; the lexical case itself lives in lookup_dictionary('thayer', ...) (Greek) or word_study, and usage is settled by search_strongs.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `language` | string | no | Language: 'hebrew' or 'greek' (optional if using H/G prefix) |
| `number` | string | yes | Strong's number with prefix (e.g., 'H430' for Hebrew, 'G2316' for Greek) |

## `reverse_strongs`

**Reverse Strongs** — read-only, idempotent, closed-world.

Find Strong's numbers from an English word. Given a word like 'goad' or 'love', returns all Hebrew/Greek Strong's entries whose KJV usage contains that word. The reverse of get_strongs.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `language` | string | no | Language filter: 'hebrew', 'greek', or 'both' (default: both) |
| `query` | string | yes | English word to search (e.g., 'goad', 'love', 'faith', 'mercy') |

## `search_strongs`

**Search Strongs** — read-only, idempotent, closed-world.

Find all KJV verses containing a specific Strong's number. Word study tool for Hebrew (H) and Greek (G) concordance research.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | integer | no | Maximum results (default: 50, max: 200) |
| `number` | string | yes | Strong's number with prefix (e.g., 'H430' for Hebrew Elohim, 'G26' for Greek agape) |

## `search_strongs_definition`

**Search Strongs Definition** — read-only, idempotent, closed-world.

Search Strong's concordance entries by keyword in definitions. Find Greek/Hebrew words by meaning (e.g., 'love', 'faith', 'glory'). Searches short definitions, detailed definitions, literal meanings, and KJV usage. A match's def_short orients you; take the candidate into word_study before resting an argument on it.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `language` | string | no | Language filter: 'hebrew', 'greek', or 'both' (default: both) |
| `limit` | integer | no | Maximum results (default: 50, max: 200) |
| `query` | string | yes | Keyword to search in definitions (e.g., 'love', 'faith', 'mercy', 'glory') |

## `get_related_strongs`

**Get Related Strongs** — read-only, idempotent, closed-world.

Get all words related to a Strong's number — synonyms, antonyms, derived forms, and root words. Walks the cross-reference and derivation graph in one call.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `language` | string | no | Language: 'hebrew' or 'greek' (optional if using H/G prefix) |
| `number` | string | yes | Strong's number with prefix (e.g., 'H430' for Hebrew, 'G26' for Greek agape) |

## `etymology_tree`

**Etymology Tree** — read-only, idempotent, closed-world.

Trace the etymology of a Strong's number through multiple levels. Walks 'see' references and derivation links recursively, building a tree of related words up to 3 levels deep (configurable). One call replaces multiple get_related_strongs calls.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `depth` | integer | no | Maximum tree depth (default: 3, max: 5) |
| `language` | string | no | Language: 'hebrew' or 'greek' (optional if using H/G prefix) |
| `number` | string | yes | Strong's number with prefix (e.g., 'H430' for Hebrew, 'G26' for Greek) |

## `hebrew_pictographs`

**Hebrew Pictographs** — read-only, idempotent, closed-world.

Get the ancient pictographic meanings of Hebrew letters. Each of the 22 Hebrew consonants originated as a picture (proto-Sinaitic script, c. 1800 BC). Pass a Hebrew word to see what each letter originally depicted. Example: תורה = Crossed sticks (covenant mark) → Tent peg (secure) → Head (person/first) → Man with arms raised (behold/reveal). Sources: proto-Sinaitic inscriptions, Egyptian hieroglyphic correspondences, traditional letter names preserved in the Talmud and Greek alphabet.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `word` | string | yes | Hebrew word, letter, or Strong's number (e.g., 'תורה', 'א', 'H430', 'H8451') |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
