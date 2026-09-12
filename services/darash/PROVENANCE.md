# Dataset provenance

**Every dataset Darash serves records which printed work it is, which edition, how the text
reached us, under what licence — and what is *not* established about it.**

Generated from the live `list_dicts` response on 2026-09-13. Nothing here is hand-written: call
`list_dicts` yourself and you get the same records, field for field.

## How to read the `identification` field

| Value | Means |
|---|---|
| `verified` | The text has been collated against the printed edition it claims to be. |
| `conventional` | Title and author are as distributed, and have **not** been collated. |
| `probable` | Consistent with the content and widely reported, not independently confirmed. |

One of those is a finding. The other two are inheritances. We label them differently because
they *are* different, and because a reader deciding how much weight a gloss can carry needs to
know which one they are holding.

A field reading `UNKNOWN — not established` is an honest gap. An empty field would be
uncheckable; a confident-looking guess would be worse than either.

---

## The verified one: Thayer

**A Greek-English Lexicon of the New Testament, being Grimm's Wilke's Clavis Novi Testamenti, translated, revised and enlarged**  
Joseph Henry Thayer (translator, reviser, editor); after C. L. W. Grimm's revision of C. G. Wilke's Clavis  
*Harper & Brothers, New York, 1889 — Corrected Edition. Read from the title page of our own scan, not assumed.*

| | |
|---|---|
| Entries | 5,870 |
| Identification | **verified** |
| Licence | public domain (published 1889; J. H. Thayer d. 1901) |
| Imported | 2026-09-02 |

**Method.** Page-image transcription of all 716 body pages, two independent passes collated (98.91% agreement over 856,793 tokens), segmented into entries, every entry proven a verbatim, non-overlapping, in-order slice of its own page. References were modernised ("Matthew 27:24", never "Mt. xxvii. 24") under a PROSE INVARIANT: strip book names, abbreviations and numerals from before and after, and the remaining words must be identical. An entry whose prose changed by one word is REJECTED, not published, and 94 entries where no rewrite passed keep the deterministic expander's baseline instead. Each entry records which of the two produced its served text (modern_refs_source) and which rule produced its Strong's number (strongs_match: exact, normalised, second-pass, ambiguous or none). Imported into this blob by cmd/thayer_import, which verifies the source SHA-256 before it writes anything.

**Source.** git.dixt.io/nor/thayer-lexicon, build commit 24de0cb77ce73a677aa8b165f05d8478dfe2de65, file out/entries_4_final.jsonl (sha256 f03f0b8e5d2deda209247e597155c05d4599a0dcda30b14d9a67d3b1ab5a7376). Built from public-domain page scans of the 1889 print (archive.org), with a second physical copy of the same stereotype plates used to adjudicate contested glyphs.

**What is and is not established.** 5,870 entries; 5,529 carry a Strong's number (3,779 by exact headword match, 1,648 normalised, 102 by a second pass over unambiguous lemma variants). 341 do not, and 14 of those carry candidates rather than a guess — an ambiguous headword REFUSES to resolve. Verification is not uniform: every entry has been read by a model reader and the corpus is census-proven against the published dictionary (Greek characters and terminal asterisks exactly equal, sha bijection 5,870/5,870), but only a small number of pages have been collated line by line against the image by eye. Measured on the 13 pages that were independently transcribed twice, Greek-bearing token disagreement runs at 0.19% — roughly two per page — mostly accent, iota subscript and συν-/συγ- assimilation. One illegible Josephus digit is kept as "?": flagged, never filled. Reference modernisation is not uniform either: 5,776 entries are gemini-dual-witnessed, 94 carry the deterministic expander's baseline because no rewrite passed the prose invariant, and each entry says which it is. Citation triage found and fixed four real ink-fill digit errors (3 read as 8), each proven against the second copy's page image and never against Scripture; the residual ~660 citation flags are the measured benign classes — Thayer follows the critical text, darash indexes the Received Text.

**A note on the asterisk.** Thayer's terminal asterisk is CONTENT, not punctuation: it asserts that every New Testament occurrence of the word is cited in the entry. It is preserved, and the corpus build disqualifies any rewrite that changes an entry's asterisk count — a model once pattern-completed twelve of them onto entries whose pages have none. Thayer held Unitarian views; on deity-of-Christ passages (G2316, G166) read him as the careful philologist he was and take the theology elsewhere.

**Per-entry ledger.** out/verified.jsonl in git.dixt.io/nor/thayer-lexicon — per entry: the printed-text sha256, the pages, and what verified it. The same per-entry sha256 and pdf_pages travel on every DictEntry served here, so one definition can be checked against one page.

| Strong's number matched by | Count |
|---|---|
| exact headword | 3779 |
| normalised | 1648 |
| second pass over unambiguous variants | 102 |
| ambiguous — candidates offered, NOT resolved | 14 |
| none | 327 |

The Strong's numbers are **our editorial addition**, from STEPBible TBESG (CC BY 4.0). The 1889
print contains none.

---

## Strong's lexicons

### `greek_lex` — Strong's Greek Dictionary of the New Testament, augmented with STEPBible's Translators Brief lexicon (TBESG), the full Abbott-Smith Manual Greek Lexicon, and the Translators Formatted full LSJ (TFLSJ)

| | |
|---|---|
| Kind | Strong's lexicon |
| Entries | 5,523 |
| Author | James Strong (1890); G. Abbott-Smith (1922); Liddell-Scott-Jones; brief lexicon and LSJ formatting by Tyndale House Cambridge scholars |
| Edition | Strong 1890; Abbott-Smith 3rd ed. 1937 (1st ed. 1922); STEPBible-Data as cloned into ~/repos/STEPBible-Data — the upstream commit was not recorded and is UNKNOWN — not established |
| Licence | Strong 1890 and Abbott-Smith are public domain. STEPBible TBESG and TFLSJ: CC BY 4.0 — Data from STEP Bible (www.STEPBible.org), Tyndale House, Cambridge. |
| Identification | conventional — title/author as distributed; not collated against a print edition |
| Imported | MySQL fields: UNKNOWN — not established; STEPBible/Abbott-Smith merges: UNKNOWN — not established; def_long replaced 2026-09-02 |

**Source.** number, lemma, transliteration, pronunciation, def_short, def_lit, derivation, see, comment and usage: bibledb MySQL table `lexicon_greek` (upstream distribution not established). def_long: STEPBible TBESG "Gloss" column. abbott_smith: full Abbott-Smith TEI XML (github.com/translatable-exegetical-tools/Abbott-Smith), falling back to TBESG "Meaning". lsj: STEPBible TFLSJ. step_gloss: TBESG "Gloss".

**Method.** SQL export via LoadFromMySQL → loadLexicon, then MergeSTEPBibleLexicons and MergeFullAbbottSmith. def_long was REPLACED on 2026-09-02 by cmd/lexicon_gloss_rebuild, a surgical rewrite of this one blob key that copies every other top-level field through as raw msgpack it never decodes — `make sync` was NOT run, because it silently drops any dataset whose sources are absent.

**Known gaps.** 5,523 entries. WHAT def_long USED TO BE IS THE GAP THAT WAS CLOSED: until 2026-09-02 it served the gloss set withdrawn from the `thayer` key the same day — probably Blue Letter Bible's Outline of Biblical Usage, public-domain status never established, arrived through bolls.life. It was archived verbatim first (sources/archived-darash-greek-lex-def-long/ in git.dixt.io/nor/thayer-lexicon, 5,523 entries, sha256 574dc4cb6b72da668a3fc90d375d86831426be918da1d2f327ef967c37d44566) and only then replaced. Still not established: which upstream distribution populated the MySQL table, when it was imported, and which STEPBible-Data commit the merges read. def_short, def_lit, derivation, comment and usage are Strong's own text and were not touched.

**Note.** A stale blob cannot bring the old def_long back: isWithdrawnGlossList fingerprints it at LOAD time by shape and the store empties the field rather than serving it.


### `hebrew_lex` — Strong's Hebrew and Aramaic Dictionary of the Old Testament, augmented with STEPBible's Translators Brief lexicon (TBESH) and the OpenScriptures Brown-Driver-Briggs

| | |
|---|---|
| Kind | Strong's lexicon |
| Entries | 8,674 |
| Author | James Strong (1890); Francis Brown, S. R. Driver, C. A. Briggs (1906); brief lexicon by Tyndale House Cambridge scholars |
| Edition | Strong 1890; BDB 1906 as digitised by the OpenScriptures Hebrew Bible project (github.com/openscriptures/HebrewLexicon); STEPBible-Data as cloned into ~/repos/STEPBible-Data — the upstream commit of neither was recorded and is UNKNOWN — not established |
| Licence | Strong 1890 and BDB 1906 are public domain; the OpenScriptures digitisation is CC BY 4.0 (openscriptures.org). STEPBible TBESH: CC BY 4.0 — Data from STEP Bible (www.STEPBible.org), Tyndale House, Cambridge. |
| Identification | conventional — title/author as distributed; not collated against a print edition |
| Imported | MySQL fields: UNKNOWN — not established; STEPBible/BDB merges: UNKNOWN — not established; def_long replaced and abbott_smith regenerated 2026-09-02 |

**Source.** number, lemma, transliteration, pronunciation, def_short, def_lit, derivation, see, comment, usage and part_of_speech: bibledb MySQL table `lexicon_hebrew` (upstream distribution not established). def_long: STEPBible TBESH "Gloss" column. abbott_smith: OpenScriptures BDB article per homonym branch, with TBESH "Meaning" where longer. step_gloss: TBESH "Gloss".

**Method.** SQL export via LoadFromMySQL → loadLexicon, then MergeSTEPBibleLexicons and MergeFullBDB. abbott_smith was REGENERATED on 2026-09-02 by cmd/hebrew_bdb_rebuild through the FIXED import path (commit 08d6d35): LexicalIndex.xml's homonym letter is no longer discarded, so H2617 חֶסֶד now shows חֶסֶד I "goodness, kindness" AND חֶסֶד II "shame" instead of whichever cross-reference happened to precede the other in the file. 543 lemmas changed; every one of them gained a labelled homonym branch, and no single-sense lemma moved. def_long was REPLACED the same day by cmd/lexicon_gloss_rebuild. Both are surgical rewrites of this one blob key that copy every other top-level field through as raw msgpack they never decode — `make sync` was NOT run, because it silently drops any dataset whose sources are absent.

**Known gaps.** 8,674 entries. def_long carried the Hebrew half of the same withdrawn corpus as greek_lex. There is no archived Hebrew witness to diff against — darash never served it under a dictionary key — so the identification rests on three things, each recomputable by `python3 scripts/measure_withdrawn_similarity.py` in git.dixt.io/nor/thayer-lexicon, which states its method in full. (1) The import path: one loadLexicon reads the same `data`→`def`→`long` column out of both tables, and STEPBible enters through a different function into different fields. (2) The editorial signature both halves share — darash's copy expands abbreviations both upstreams leave short: 132 of the 8,674 entries contain "figuratively" and NOT ONE contains "fig.", against TBESH's 162 entries containing "fig." and none containing "figuratively". (3) What TBESH has that this text lacks: TBESH rewrote every proper name's gloss as Tyndale's own prosopography ("A man living at the time of Exile and Return, only mentioned at Est.9.8; son of: Haman…"), and 1,450 of the 8,131 comparable numbers carry it in TBESH while def_long still holds the old one-line gloss ("a son of Haman"). Text derived FROM TBESH cannot be missing 1,450 of TBESH's own articles. A SIMILARITY FIGURE CANNOT SETTLE THIS, and the one recorded here until 2026-09-02 ("NOT TBESH — 39.6% byte-identical, median similarity 0.806") pointed the wrong way as well as being unreproducible: remeasured against TBESH's "Meaning" column, stripped of numbering, HTML and cross-reference apparatus, the withdrawn text is 49.4% byte-identical with median similarity 0.986. Both descend from the same abridged Brown-Driver-Briggs — TBESH says so of itself — so distance was never going to separate them. Archived verbatim first (sources/archived-darash-hebrew-lex-def-long/ in git.dixt.io/nor/thayer-lexicon, 8,674 entries, sha256 df153764a3793c0b30424f331c667c8f5ca4972abcc3be288dbb46196cd8a88c). H3328 יִצְחַר carries no def_long and never did. Still not established: which upstream distribution populated the MySQL table, when it was imported, and which STEPBible-Data / HebrewLexicon commits the merges read. def_short and the other Strong's fields were not touched.

**Note.** Extended Strong's letters are the homonym axis and are preserved in both def_long and abbott_smith. A bare H-number can be two different words.


---

## Dictionaries

13 dictionaries are served. 12 are described in full below.

| Key | Work | Entries | Identification |
|---|---|---|---|
| `webster` | Webster's Unabridged Dictionary of the English Language | 176,021 | probable — consistent with the content and widely reported, but NOT independently confirmed |
| `isbe` | The International Standard Bible Encyclopaedia | 9,350 | conventional — title/author as distributed; not collated against a print edition |
| `thayer` | A Greek-English Lexicon of the New Testament, being Grimm's Wilke's Clavis Novi Testamenti, translated, revised and enlarged | 5,870 | verified |
| `navestb` | Nave's Topical Bible | 5,320 | conventional — title/author as distributed; not collated against a print edition |
| `smith` | Smith's Bible Dictionary | 4,560 | conventional — title/author as distributed; not collated against a print edition |
| `easton` | Easton's Illustrated Bible Dictionary | 3,947 | conventional — title/author as distributed; not collated against a print edition |
| `fausset` | Fausset's Bible Dictionary | 3,946 | conventional — title/author as distributed; not collated against a print edition |
| `hitchcock` | Hitchcock's New and Complete Analysis of the Holy Bible (Bible Names Dictionary) | 2,737 | conventional — title/author as distributed; not collated against a print edition |
| `ats` | American Tract Society Bible Dictionary | 2,299 | conventional — title/author as distributed; not collated against a print edition |
| `hawker` | The Poor Man's Concordance and Dictionary to the Sacred Scriptures | 1,449 | conventional — title/author as distributed; not collated against a print edition |
| `torrey` | The New Topical Text Book | 621 | conventional — title/author as distributed; not collated against a print edition |
| `bullinger` | Figures of Speech Used in the Bible | 183 | conventional — title/author as distributed; not collated against a print edition |

`wilsons` is served but is **not described here**: it is the one source whose rights
position we have not established, and it is under review. We would rather say that than
publish a licence claim we cannot stand behind.

---

### `webster` — Webster's Unabridged Dictionary of the English Language

| | |
|---|---|
| Kind | dictionary |
| Entries | 176,021 |
| Author | Noah Webster (orig.); later revisers not established |
| Edition | UNKNOWN — not established — the 1828 and the 1913 Revised Unabridged both circulate as 'Webster unabridged' and this text has not been pinned to either |
| Licence | public domain on either candidate edition (1828 / 1913) |
| Identification | probable — consistent with the content and widely reported, but NOT independently confirmed |
| Imported | UNKNOWN — not established |

**Source.** bibledb MySQL table `entries` (word, wordtype, definition), active rows only (upstream distribution not established)

**Method.** SQL export via LoadFromMySQL → loadWebster; wordtype prefixed to the definition as "(type) text"

**Known gaps.** EDITION IS THE GAP: darash's own tool text has called this "Webster 1828"; that is an assumption, not a finding. It is a general English dictionary, not a Bible dictionary.


### `isbe` — The International Standard Bible Encyclopaedia

| | |
|---|---|
| Kind | dictionary |
| Entries | 9,350 |
| Author | James Orr (general editor) |
| Edition | Howard-Severance, 1915 |
| Licence | public domain (published 1915) |
| Identification | conventional — title/author as distributed; not collated against a print edition |
| Imported | UNKNOWN — not established |

**Source.** bibledb MySQL table `isbe` (upstream distribution not established)

**Method.** SQL export of (topic, text) rows via LoadFromMySQL → loadDictionary; no transcription, no editing

**Known gaps.** 1915 archaeology and higher-critical dating are dated; the 1979 revised ISBE is a different, copyrighted work and is NOT this


### `navestb` — Nave's Topical Bible

| | |
|---|---|
| Kind | dictionary |
| Entries | 5,320 |
| Author | Orville J. Nave |
| Edition | 1897 (Topical Bible Publishing) |
| Licence | public domain (published 1897) |
| Identification | conventional — title/author as distributed; not collated against a print edition |
| Imported | UNKNOWN — not established |

**Source.** bibledb MySQL table `navestb` (upstream distribution not established)

**Method.** SQL export of (topic, text) rows via LoadFromMySQL → loadDictionary; no transcription, no editing

**Known gaps.** verse references are KJV versification; not re-checked against darash's own book/verse grid


### `smith` — Smith's Bible Dictionary

| | |
|---|---|
| Kind | dictionary |
| Entries | 4,560 |
| Author | William Smith |
| Edition | 1863; revised/abridged editions circulate widely — the edition behind this text is not established |
| Licence | public domain (published 1863) |
| Identification | conventional — title/author as distributed; not collated against a print edition |
| Imported | UNKNOWN — not established |

**Source.** bibledb MySQL table `smith` (upstream distribution not established)

**Method.** SQL export of (topic, text) rows via LoadFromMySQL → loadDictionary; no transcription, no editing

**Known gaps.** which of the several Smith abridgments this is has NOT been established


### `easton` — Easton's Illustrated Bible Dictionary

| | |
|---|---|
| Kind | dictionary |
| Entries | 3,947 |
| Author | Matthew George Easton |
| Edition | 3rd edition, Thomas Nelson, 1897 |
| Licence | public domain (author d. 1894; work published 1897) |
| Identification | conventional — title/author as distributed; not collated against a print edition |
| Imported | UNKNOWN — not established |

**Source.** bibledb MySQL table `easton` (upstream distribution not established)

**Method.** SQL export of (topic, text) rows via LoadFromMySQL → loadDictionary; no transcription, no editing

**Known gaps.** upstream distribution and its transcription method not established; entry count not collated against a print edition


### `fausset` — Fausset's Bible Dictionary

| | |
|---|---|
| Kind | dictionary |
| Entries | 3,946 |
| Author | Andrew Robert Fausset |
| Edition | Hodder & Stoughton, 1878 |
| Licence | public domain (published 1878) |
| Identification | conventional — title/author as distributed; not collated against a print edition |
| Imported | UNKNOWN — not established |

**Source.** bibledb MySQL table `fausset` (upstream distribution not established)

**Method.** SQL export of (topic, text) rows via LoadFromMySQL → loadDictionary; no transcription, no editing


### `hitchcock` — Hitchcock's New and Complete Analysis of the Holy Bible (Bible Names Dictionary)

| | |
|---|---|
| Kind | dictionary |
| Entries | 2,737 |
| Author | Roswell D. Hitchcock |
| Edition | A. J. Johnson, 1869 |
| Licence | public domain (published 1869) |
| Identification | conventional — title/author as distributed; not collated against a print edition |
| Imported | UNKNOWN — not established |

**Source.** bibledb MySQL table `hitchcock` (upstream distribution not established)

**Method.** SQL export of (topic, text) rows via LoadFromMySQL → loadDictionary; no transcription, no editing

**Known gaps.** name etymologies are 19th-century and frequently disagree with modern Semitic philology; treat as historical, not lexical evidence


### `ats` — American Tract Society Bible Dictionary

| | |
|---|---|
| Kind | dictionary |
| Entries | 2,299 |
| Author | American Tract Society (corporate author) |
| Edition | 1859 |
| Licence | public domain (published 1859) |
| Identification | conventional — title/author as distributed; not collated against a print edition |
| Imported | UNKNOWN — not established |

**Source.** bibledb MySQL table `ats` (upstream distribution not established)

**Method.** SQL export of (topic, text) rows via LoadFromMySQL → loadDictionary; no transcription, no editing


### `hawker` — The Poor Man's Concordance and Dictionary to the Sacred Scriptures

| | |
|---|---|
| Kind | dictionary |
| Entries | 1,449 |
| Author | Robert Hawker |
| Edition | 1828 |
| Licence | public domain (author d. 1827; work published 1828) |
| Identification | conventional — title/author as distributed; not collated against a print edition |
| Imported | UNKNOWN — not established |

**Source.** bibledb MySQL table `hawker` (upstream distribution not established)

**Method.** SQL export of (topic, text) rows via LoadFromMySQL → loadDictionary; no transcription, no editing

**Known gaps.** devotional, not lexical; the author's own theology is present throughout and is not marked


### `torrey` — The New Topical Text Book

| | |
|---|---|
| Kind | dictionary |
| Entries | 621 |
| Author | Reuben Archer Torrey |
| Edition | Fleming H. Revell, 1897 |
| Licence | public domain (published 1897) |
| Identification | conventional — title/author as distributed; not collated against a print edition |
| Imported | UNKNOWN — not established |

**Source.** bibledb MySQL table `torrey` (upstream distribution not established)

**Method.** SQL export of (topic, text) rows via LoadFromMySQL → loadDictionary; no transcription, no editing

**Known gaps.** verse references are KJV versification; not re-checked against darash's own book/verse grid


### `bullinger` — Figures of Speech Used in the Bible

| | |
|---|---|
| Kind | dictionary |
| Entries | 183 |
| Author | Ethelbert William Bullinger |
| Edition | Eyre & Spottiswoode, 1898 |
| Licence | public domain (published 1898) |
| Identification | conventional — title/author as distributed; not collated against a print edition |
| Imported | 2026-04-06 |

**Source.** pre-extracted bullinger_clean.json, derived from a TheWord .dct.twm module (human-proofed text); see MergeBullinger for the search paths

**Method.** JSON import via MergeBullinger; entry Topic taken from the module's full_title field

**Known gaps.** the .twm module's own transcription accuracy has not been checked against the 1898 print edition


---

## Corrections

### 2026-09-02 — a dictionary served under the wrong name

Until this date Darash served, under the key `thayer`, a text that was not Thayer. It was in all
probability Blue Letter Bible's *Outline of Biblical Usage*, whose public-domain status was
never established, and it reached us through a source later found to be unreliable. The same
withdrawn gloss set also populated `def_long` on both Strong's lexicons.

All three were archived verbatim, with digests, **before** anything was replaced:

| What | Archive | SHA-256 |
|---|---|---|
| `thayer` (as served) | `sources/archived-darash-legacy-thayer/` | see repo ledger |
| `greek_lex.def_long` | `sources/archived-darash-greek-lex-def-long/ in git.dixt.io/nor/thayer-lexicon` | `574dc4cb6b72da668a3fc90d375d86831426be918da1d2f327ef967c37d44566` |
| `hebrew_lex.def_long` | `sources/archived-darash-hebrew-lex-def-long/ in git.dixt.io/nor/thayer-lexicon` | `df153764a3793c0b30424f331c667c8f5ca4972abcc3be288dbb46196cd8a88c` |

`thayer` was then replaced with the transcription described at the top of this file. A stale
cache cannot bring the old text back: the withdrawn gloss set is fingerprinted by shape at load
time and the field is emptied rather than served.

### Why this section exists

Because the provenance work is what found it. A feature list would not have. If you are
weighing whether to trust this data, the `known_gaps` field on every source above is written in
the same spirit — read it as the part we could not prove, not as boilerplate.

