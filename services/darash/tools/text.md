# Reading the text — Darash MCP tools

**Which verse, chapter or book does the text actually contain, and how do translations differ?** 11 tools, listed below with the exact description and input
schema the server itself returns. Endpoint: `https://darash-api.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`get_verse`](#get-verse) | Get verse(s) by reference |
| [`get_chapter`](#get-chapter) | Get entire chapter with all verses[END] |
| [`get_book`](#get-book) | Get entire book with all chapters and verses[END] |
| [`list_books`](#list-books) | List all 66 books of the Bible with chapters and testament |
| [`list_bibles`](#list-bibles) | List all 59 Bible translations with metadata (abbreviation, name, language, year)[END] |
| [`get_bible`](#get-bible) | Get detailed metadata and complete structure for a Bible translation (books, chapters per… |
| [`compare_verses`](#compare-verses) | Compare the same verse across multiple Bible translations in one call |
| [`export_bible`](#export-bible) | Export an entire Bible translation as structured JSON |
| [`export_bible_book`](#export-bible-book) | Export a single book from a Bible translation as structured JSON |
| [`verse_to_position`](#verse-to-position) | INVERSE of position_to_verse: given a Torah verse reference, return its exact letter-offset… |
| [`position_to_verse`](#position-to-verse) | INVERSE OF els tool position-output: given a raw Torah LETTER OFFSET, return the verse… |

---

## `get_verse`

**Get Verse** — read-only, idempotent, closed-world.

Get verse(s) by reference. Supports single verse, verse range within chapter, or count-based cross-chapter fetching. Scripture interprets Scripture: follow a verse into get_cross_refs for its web of parallels, and into strongs_in_verse for the original words.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bible` | string | yes | Bible translation (e.g., 'kjv', 'asv', 'web') |
| `count` | integer | no | Number of verses to fetch starting from ref. Enables cross-chapter reading (e.g., ref='John 3:16', count=25 returns through John 4:2). If omitted, uses range f… |
| `ref` | string | yes | Verse reference (e.g., 'John 3:16', 'Gen 1:1-5') |

## `get_chapter`

**Get Chapter** — read-only, idempotent, closed-world.

Get entire chapter with all verses[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bible` | string | yes | Bible translation |
| `ref` | string | yes | Chapter reference (e.g., 'John 3', 'Genesis 1') |

## `get_book`

**Get Book** — read-only, idempotent, closed-world.

Get entire book with all chapters and verses[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bible` | string | yes | Bible translation (e.g., 'kjv', 'asv', 'web') |
| `book` | string | yes | Book name (e.g., 'Genesis', 'John', 'Psalms') |

## `list_books`

**List Books** — read-only, idempotent, closed-world.

List all 66 books of the Bible with chapters and testament. LEAN by default (id, name, abbr, chapters, testament, genre — no alias arrays, ~3x smaller); pass detail=full to include each book's alias list. Optionally specify language to get localized book names (38 languages available including greek, hebrew, norwegian, german, spanish, etc.). Pass an invalid language to see all available options.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `detail` | string | no | Per-book detail: 'lean' (default, browse fields only) or 'full' (adds the aliases array — the abbreviation variants get_verse/get_chapter accept) |
| `lang` | string | no | Language for book names (e.g., 'greek', 'hebrew', 'norwegian', 'german', 'spanish'). Also accepts 'language' as alias. Defaults to 'english' |
| `language` | string | no | Alias for 'lang' parameter |

## `list_bibles`

**List Bibles** — read-only, idempotent, closed-world.

List all 59 Bible translations with metadata (abbreviation, name, language, year)[END]

## `get_bible`

**Get Bible** — read-only, idempotent, closed-world.

Get detailed metadata and complete structure for a Bible translation (books, chapters per book, verses per chapter)[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `abbr` | string | yes | Bible abbreviation (e.g., 'kjv', 'asv', 'web') |

## `compare_verses`

**Compare Verses** — read-only, idempotent, closed-world.

Compare the same verse across multiple Bible translations in one call. Include 'kjs' for Strong's tagged text with clickable word study links. For Norwegian work nb2026 is the standard (Masoretic versification) — settle Norwegian usage against its text.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bibles` | string | yes | Comma-separated Bible translations to compare (e.g., 'kjv,asv,web,kjs') |
| `ref` | string | yes | Verse reference (e.g., 'John 3:16', 'Gen 1:1') |

## `export_bible`

**Export Bible** — read-only, idempotent, closed-world.

Export an entire Bible translation as structured JSON. Returns a single-use download URL (expires in 10 minutes). Includes all available books (66 for full Bibles, 27 for NT-only like Vulgate). Output includes verse numbers: {"verse": 1, "text": "..."}.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bible` | string | yes | Bible translation abbreviation (e.g., 'kjv', 'asv', 'web', 'italian', 'vulgate') |

## `export_bible_book`

**Export Bible Book** — read-only, idempotent, closed-world.

Export a single book from a Bible translation as structured JSON. Returns a single-use download URL (expires in 5 minutes). Output includes verse numbers: {"verse": 1, "text": "..."}.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bible` | string | yes | Bible translation abbreviation (e.g., 'kjv', 'asv', 'web', 'italian', 'vulgate') |
| `book` | string | yes | Book name (e.g., 'Genesis', 'John', 'Psalms', 'Revelation') |

## `verse_to_position`

**Verse To Position** — read-only, idempotent, closed-world.

INVERSE of position_to_verse: given a Torah verse reference, return its exact letter-offset window in the 304,805-letter Koren consonant text.

INPUT: ref = Torah verse like 'Genesis 32:11', 'Exodus 21:32', 'Deuteronomy 6:4'.
OUTPUT: { ref, book, book_name, chapter, verse, start_pos, length, end_pos, book_start_pos, pos_in_book, torah_length, text }
  • start_pos = first letter of verse (Torah offset, 0-indexed)
  • end_pos = exclusive end (= start_pos + length)
  • text = Hebrew consonants of the entire verse

USE WHEN:
  • You need the position window of a verse to check whether an ELS code passes through it.
  • Filtering els_search results: keep matches whose start_pos falls within [start_pos, end_pos) of the target verse.
  • Computing a multi-verse window (e.g., Gen 28:10..28:22): call once per endpoint and use [first.start_pos, last.end_pos).
  • Pairing with trace_els_code or position_to_verse for letter-by-letter verification of a finding.

GUARANTEES: Torah-only (Genesis–Deuteronomy). Linear scan of the 5,847-entry verse index — sub-millisecond. Non-Torah books, missing verses, or unparseable refs return precise errors with the valid format example.

VERSIFICATION: the ref is read in KOREN numbering, which equals the Masoretic everywhere except Exodus 20 and Deuteronomy 5 (Koren merges the four short commandments, so its later verses run three lower). Those responses carry mt_equivalent + grid_note, and a Masoretic verse number the shorter Koren chapter lacks (e.g. Exodus 20:24) errors with the Koren verse it maps to.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ref` | string | yes | Torah verse reference (e.g., 'Genesis 32:11', 'Exodus 21:32'). Required. Must be Genesis–Deuteronomy. |

## `position_to_verse`

**Position To Verse** — read-only, idempotent, closed-world.

INVERSE OF els tool position-output: given a raw Torah LETTER OFFSET, return the verse containing it plus exact verse boundaries and surrounding context.

INPUT: pos = 0-indexed letter position in the Koren Torah (304,805 Hebrew consonants total). Range 0..304804.
  pos=0     → first letter of Genesis 1:1 (ב of בראשית)
  pos=78064 → first letter of Exodus 1:1
  pos=141593 → first letter of Leviticus 1:1
  pos=186383 → first letter of Numbers 1:1
  pos=249913 → first letter of Deuteronomy 1:1
  pos=304804 → last letter of Deuteronomy 34:12

OUTPUT: { pos, letter, book (1-5), book_name, chapter, verse, ref, verse_start_pos, verse_length, verse_end_pos, offset_in_verse, book_start_pos, pos_in_book, torah_length, surface_word, target, versification }

VERSIFICATION: verse numbers are the KOREN letter grid, which equals the Masoretic numbering everywhere EXCEPT Exodus 20 and Deuteronomy 5, where Koren merges the four short commandments into one verse and every later verse sits three lower than the Masoretic. In those two chapters the response adds mt_equivalent and grid_note so a Koren ref is never silently taken for a Masoretic one.

USE WHEN:
  • You have a start_pos from els_search/els_discover/els_verse_codes and want the canonical verse + offset.
  • Annotating each letter of an ELS sequence (start_pos, start_pos+skip, start_pos+2*skip, ...) with where it lands.
  • Rendering or debugging grid coordinates back to chapter:verse.
  • Confirming whether a position falls 'inside' a target verse for proximity analysis.

GUARANTEES: O(log N) binary search over the 5,847-verse index. Always returns the exact verse — no clamping, no fallback. Out-of-range positions return a precise error explaining the valid range.

This is a Torah-only tool: positions are letter offsets in the Koren consonant text. For non-Torah books, parse a reference string with get_verse instead. The companion els_verse_codes / els_verse_signal tools take a reference and return positions; this tool reverses that mapping.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `pos` | integer | yes | 0-indexed letter position in the Koren Torah (range 0..304804). Required. Examples: 0 (first letter of Genesis 1:1), 78064 (start of Exodus), 304804 (last lett… |
| `target` | string | no | Which Torah text to read the letter from: 'real' (default — actual Koren Torah) or 'shuffled' (deterministically-shuffled control). Verse boundaries are identi… |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
