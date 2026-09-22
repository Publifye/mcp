# Blocks and spans

**The authoring surface: paragraphs, headings, quotations, lists, tables, figures, and inline markup.** 34 Junifye MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://junifye.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`block_add_bible_quote`](#block_add_bible_quote) | Add a scripture block quote |
| [`block_add_figure`](#block_add_figure) | Add a VECTOR figure block — one author-supplied SVG that renders as live inline vector in BOTH… |
| [`block_add_general_quote`](#block_add_general_quote) | Add a non-scripture block quote (Church Father, theologian, hymn writer, web source) |
| [`block_add_heading`](#block_add_heading) | Add a heading block — this is how you make SUB-CHAPTERS inside a chapter |
| [`block_add_image`](#block_add_image) | Add an image/figure block that renders in BOTH the PDF and the HTML reader |
| [`block_add_list`](#block_add_list) | Add a list initialised with one item (item_idx=0) containing one text span |
| [`block_add_paragraph`](#block_add_paragraph) | Add a paragraph initialised with one text span |
| [`block_add_stat`](#block_add_stat) | Add a stat block (percentage "rings", a donut chart per item) initialised with ONE ring; build… |
| [`block_add_table`](#block_add_table) | Add a tabular grid in ONE call |
| [`block_delete`](#block_delete) | Delete a block by its stable id (e.g |
| [`block_get_source`](#block_get_source) | Return one block as round-trippable source text (markdown-ish) |
| [`block_list`](#block_list) | Read-only chapter navigation |
| [`block_move`](#block_move) | Reorder blocks by id |
| [`block_patch_many`](#block_patch_many) | Apply MANY surgical patches to one chapter in a SINGLE version |
| [`block_patch_text`](#block_patch_text) | Surgically edit ONE block: replace `find` with `replace` inside that block's SOURCE (exactly… |
| [`block_set_source`](#block_set_source) | Replace a block's content by parsing source text |
| [`block_set_stat`](#block_set_stat) | Change a stat block's presentation without touching its rings: color… |
| [`block_set_table`](#block_set_table) | Replace an existing TABLE block's contents from STRUCTURED data — the only way to edit a table… |
| [`block_transfer`](#block_transfer) | MOVE whole sections (blocks) from one chapter to another — the two chapters may be in… |
| [`list_add_item`](#list_add_item) | Append (or insert at at_idx) a new row to a list block |
| [`list_delete_item`](#list_delete_item) | Delete row item_idx from a list block |
| [`list_move_item`](#list_move_item) | Reorder rows within a list block |
| [`span_add_bref`](#span_add_bref) | Append a Bible-reference link span |
| [`span_add_emph`](#span_add_emph) | Append italic-emphasis span |
| [`span_add_greek`](#span_add_greek) | Append Greek-script span (may contain accents + breathings) |
| [`span_add_hebrew`](#span_add_hebrew) | Append Hebrew-script span (may contain nikud) |
| [`span_add_latin`](#span_add_latin) | Append LTR Latin-script span |
| [`span_add_link`](#span_add_link) | Append an inline hyperlink span: a visible TITLE + a url |
| [`span_add_strong`](#span_add_strong) | Append bold-emphasis span |
| [`span_add_strongs`](#span_add_strongs) | Append a Strong's-concordance code span |
| [`span_add_text`](#span_add_text) | Append (or insert at at_idx) a plain-text span |
| [`span_delete`](#span_delete) | Delete the span at idx within the target block |
| [`span_move`](#span_move) | Reorder spans within a block |
| [`stat_add_item`](#stat_add_item) | Append a ring to an existing stat block |

---

## `block_add_bible_quote`

**Block Add Bible Quote** — writes, closed-world.

Add a scripture block quote. ref shape: '[1-3 ]Book Chap[:Verse[-Verse]]' — Book is 2-30 Unicode letters (English, Norwegian, German, Greek, etc.) and may include spaces, dots, hyphens. Examples: 'John 3:16', '1 Corinthians 13:1-13', 'Revelation 22:13', 'Åpenbaringen 1:8'. translation optional (e.g. 'ESV'). text is the verse text — OPTIONAL: if you omit text and instead pass bible (a translation code from darash's list_bibles, e.g. 'NB2026', 'WEB', 'kjv'), the verse text is fetched automatically from darash and text is never left empty. Pass text explicitly to quote a specific wording (or when darash is unavailable).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bible` | string | no | darash translation code (list_bibles) to auto-fetch the verse text when text is omitted, e.g. NB2026 / WEB / kjv |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `insert_after` | string | no | Optional 'blk...' id — place the new block immediately AFTER this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `insert_before` | string | no | Optional 'blk...' id — place the new block immediately BEFORE this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `ref` | string | yes | The Bible reference, e.g. 'John 3:16' or 'Rom 6:1-4' (localized book names/abbreviations accepted). |
| `text` | string | no | Plain text content (source markup like *…* or [a:…] is NOT parsed here — use the span tools or block_set_source for markup). |
| `translation` | string | no | Optional translation code, e.g. 'WEB', 'nb2026' — omit for the book's default. |

## `block_add_figure`

**Block Add Figure** — writes, closed-world.

Add a VECTOR figure block — one author-supplied SVG that renders as live inline vector in BOTH the HTML reader and the EPUB, and as a crisp high-DPI raster in the PDF (one artifact → three faithful outputs). For book-native line-art (grids, axes, geometric figures, diagrams). figure_id is the content-addressed id returned by figure_upload_begin (e.g. "a1b2…e9.svg") — upload the SVG FIRST via figure_upload_begin, this only references it. SUPPORTED so it renders IDENTICALLY across all three outputs: paths, basic shapes, strokes, dashes, solid fills, opacity. NOT supported (rejected on upload, because the pure-Go print rasterizer can't reproduce them and they'd diverge web-vs-print): live <text> (convert type to outlines), gradients, filters, masks, patterns. caption is optional (shown under the figure + used as the accessible label). width is the display fraction of the text column (0.1–1.0, default 0.85). Use :image (block_add_image) for photos/raster art; use :figure for vector diagrams.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `caption` | string | no | Optional caption / accessible label. |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `figure_id` | string | yes | Content-addressed id from figure_upload_begin, e.g. 'a1b2...e9.svg' (a 64-char SHA256 hex + .svg). |
| `insert_after` | string | no | Optional 'blk...' id — place the new block immediately AFTER this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `insert_before` | string | no | Optional 'blk...' id — place the new block immediately BEFORE this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `width` | number | no | Display width as a fraction of the text column; default 0.85. |

## `block_add_general_quote`

**Block Add General Quote** — writes, closed-world.

Add a non-scripture block quote (Church Father, theologian, hymn writer, web source). author + cite optional; text required. url optional (http/https/mailto) — when set, the attribution (cite, or author if no cite) becomes a clickable link; a url with no author/cite is rejected.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `author` | string | no | Author name as it should appear (plain text). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `cite` | string | no | Optional source/citation line shown with the quote. |
| `insert_after` | string | no | Optional 'blk...' id — place the new block immediately AFTER this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `insert_before` | string | no | Optional 'blk...' id — place the new block immediately BEFORE this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `text` | string | yes | Plain text content (source markup like *…* or [a:…] is NOT parsed here — use the span tools or block_set_source for markup). |
| `url` | string | no | Optional source URL (http://, https:// or mailto:). Links the attribution. |

## `block_add_heading`

**Block Add Heading** — writes, closed-world.

Add a heading block — this is how you make SUB-CHAPTERS inside a chapter. The level (2-4) sets NESTING DEPTH, not an absolute size: the FIRST heading in a chapter is always the top sub-chapter level whatever number you pass, and a heading with a higher level than the one above it nests beneath it. The reader numbers them automatically and cleanly — 3.1, then 3.1.1 for a nested one — in both PDF and HTML, collapsible in the table of contents. You CANNOT produce broken "3.0.1" numbering: pick 2 for a sub-chapter, 3 to nest one under it, 4 deeper, and it always renders as a clean outline. insert_before/insert_after place it relative to a block id; omit both to append.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `insert_after` | string | no | Optional 'blk...' id — place the new block immediately AFTER this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `insert_before` | string | no | Optional 'blk...' id — place the new block immediately BEFORE this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `level` | integer | yes | Heading depth as RELATIVE structure: 1 = top section of this chapter, 2 = subsection, 3 = sub-subsection. Normalised per chapter for TOC numbering. |
| `text` | string | yes | Plain text content (source markup like *…* or [a:…] is NOT parsed here — use the span tools or block_set_source for markup). |

## `block_add_image`

**Block Add Image** — writes, closed-world.

Add an image/figure block that renders in BOTH the PDF and the HTML reader. image_id is the content-addressed id returned by image_upload_begin (e.g. "a1b2…e9.png") — upload the file FIRST via image_upload_begin, this only references it. caption is optional (shown under the image + used as the HTML alt text). width is the display fraction of the text column (0.1–1.0, default 0.85); it scales responsively on the web and to the trim in the PDF, so it is correct on any page size.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `caption` | string | no | Optional caption / alt text. |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `image_id` | string | yes | Content-addressed id from image_upload_begin, e.g. 'a1b2...e9.png' (a 64-char SHA256 hex + .png/.jpg). |
| `insert_after` | string | no | Optional 'blk...' id — place the new block immediately AFTER this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `insert_before` | string | no | Optional 'blk...' id — place the new block immediately BEFORE this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `width` | number | no | Display width as a fraction of the text column; default 0.85. |

## `block_add_list`

**Block Add List** — writes, closed-world.

Add a list initialised with one item (item_idx=0) containing one text span. ordered=true → numbered; ordered=false → bulleted. Extend with list_add_item for more rows, span_add_* for span content within an item.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `first_item_text` | string | yes | Plain text of the list's FIRST row (a list can't be empty); add more rows with list_add_item. |
| `insert_after` | string | no | Optional 'blk...' id — place the new block immediately AFTER this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `insert_before` | string | no | Optional 'blk...' id — place the new block immediately BEFORE this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `ordered` | boolean | yes | true = numbered list (1. 2. 3.), false = bullet list. |

## `block_add_paragraph`

**Block Add Paragraph** — writes, closed-world.

Add a paragraph initialised with one text span. Returns the new block_id (e.g. blk7a91...) — extend with span_add_* (any type) afterwards by passing that block_id.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `insert_after` | string | no | Optional 'blk...' id — place the new block immediately AFTER this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `insert_before` | string | no | Optional 'blk...' id — place the new block immediately BEFORE this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `text` | string | yes | Plain text content (source markup like *…* or [a:…] is NOT parsed here — use the span tools or block_set_source for markup). |

## `block_add_stat`

**Block Add Stat** — writes, closed-world.

Add a stat block (percentage "rings", a donut chart per item) initialised with ONE ring; build it up with stat_add_item. color = "plain" (book accent, default) | "scale" (coloured by percentage: low→red, mid→amber, high→green) | a "#RRGGBB" applied to every ring. size = small|medium|large (default medium). columns = 1|2 (default 1). description is an optional muted line under the label; item_color is an optional "#RRGGBB" for THIS ring only (overrides the block colour). One ring renders as a single hero; several as a 1- or 2-column list — identical in the HTML reader (SVG) and the PDF (TikZ).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `color` | string | no | plain \| scale \| #RRGGBB |
| `columns` | integer | no |  |
| `description` | string | no | Optional longer line under the stat label. |
| `insert_after` | string | no | Optional 'blk...' id — place the new block immediately AFTER this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `insert_before` | string | no | Optional 'blk...' id — place the new block immediately BEFORE this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `item_color` | string | no | optional #RRGGBB for this first ring only |
| `label` | string | yes | Short label under the stat ring (a few words). |
| `percent` | integer | yes | The statistic value 0..100 (renders as a donut ring). |
| `size` | string | no |  |

## `block_add_table`

**Block Add Table** — writes, closed-world.

Add a tabular grid in ONE call. rows = array of rows, each row = array of cell strings (one string per column). header = optional array of column-header strings (rendered bold, and used as the per-column label when the table stacks into cards on phones). align = optional per-column alignment array, each "left" | "center" | "right" (e.g. ["left","right"]); omit for all-left. caption = optional small-italic title. Best for SHORT, scannable data (labels, numbers, Hebrew/English/skip columns) — for prose comparisons prefer headings + lists, which read better in a single column. Keep to ≤12 columns. Ragged rows are padded automatically. Cells are plain text (Hebrew/Greek auto-detected); for bold/italic/refs inside a cell, author that data as a list instead.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `align` | array | no | Optional per-column alignment; omit for left. |
| `caption` | string | no | Optional caption text shown under the block. |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `header` | array | no | Optional column headers. |
| `insert_after` | string | no | Optional 'blk...' id — place the new block immediately AFTER this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `insert_before` | string | no | Optional 'blk...' id — place the new block immediately BEFORE this block. Omit both insert_* args to append at the chapter end; passing both is rejected. |
| `rows` | array | yes | Body rows; each row is an array of cell strings. |

## `block_delete`

**Block Delete** — writes, closed-world.

Delete a block by its stable id (e.g. blk7a91...). Returns error if no block has that id (e.g. another writer deleted it). Any notes pinned to this block follow to the next block (or the previous if it was last).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |

## `block_get_source`

**Block Get Source** — read-only, idempotent, closed-world.

Return one block as round-trippable source text (markdown-ish). Pair with block_set_source for edit-and-push revision. Block id is preserved by the server, not encoded in the source.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |

## `block_list`

**Block List** — read-only, idempotent, closed-world.

Read-only chapter navigation. Without block_id: returns {chapter_id, chapter_title, chapter_number, book_short_url, book_slug_url, blocks: [{id, type, summary, reader_url, reader_url_short}], count}. Each block's stable `id` is the handle for span_add_*/block_delete/block_move AND is its anchor in the published HTML reader. Each section ships BOTH a full and a short deep-link to the same spot: `reader_url` (canonical <uuid>.html#<id>) and `reader_url_short` (the pretty <slug-or-code>#<id> alias) — identical destination, pick by taste. CROSS-REFERENCING (e.g. an AI writing book X points at book Y) — two scenarios, both served here: (1) HARD link, for the clickable HTML reader: drop a section's `reader_url` (or `reader_url_short`) into an [a:text|url] link. (2) SOFT reference, for PDF/print where links can't be clicked so the reader needs to find it by hand: cite verbatim using `chapter_number` + `chapter_title` + the section `summary` — e.g. "as discussed in Chapter 3, 'The Doorway'". With block_id: returns the full structured contents of that one block (paragraph→spans, list→items, heading→text, etc.) as {chapter_id, block_id, block} — for AI inspection only; do NOT echo it back, use the block_* / span_* mutation tools. A chapter in the TRASH stays readable here and is returned with deleted:true plus a deleted_note — its text is NOT part of the book.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_id` | string | no | Optional. If present, return the full body of just that block instead of the summary list. |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `limit` | integer | no | Max rows to return (default 50, max 200). Omit it, or pass 0, for the default. A NEGATIVE limit is rejected, not clamped. |
| `offset` | integer | no | 0-based row offset for the next page. Omit for the first page; pass the previous offset+limit while has_more is true. A NEGATIVE offset is rejected. |

## `block_move`

**Block Move** — writes, closed-world.

Reorder blocks by id. block_id is moved to position relative to target_id according to position ('before' | 'after').

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `position` | string | yes |  |
| `target_id` | string | yes | The 'blk...' id the moved block is placed relative to (see `position`). |

## `block_patch_many`

**Block Patch Many** — writes, closed-world.

Apply MANY surgical patches to one chapter in a SINGLE version. Same exact-once semantics as block_patch_text, once per patch — this is not a mass find/replace, it is N specific edits committed together.

Use it whenever you have more than one edit in a chapter. One patch per round trip bumps a version each time: a real house-style pass cost 97 calls and 116 history entries for one logical change.

ALL-OR-NOTHING. If any patch fails — pattern absent, matched more than once, block missing, result malformed — NOTHING is written, and every patch's result is still returned so you can fix the bad one and resubmit the whole batch. A partial application is never possible.

preview=true runs every patch and reports what WOULD change without writing.

It stands down if a human holds the live-editor lock on ANY block the batch touches, naming who — the same courtesy as the single-block tools, checked across every target rather than just the first.

Find an edit's exact block ids with book_grep first. For TABLE/STAT blocks use block_set_table / block_set_stat; to replace a string across the WHOLE book use book_replace.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chapter_id` | string | yes | The idc… chapter holding every block in the batch. |
| `patches` | array | yes | The edits, applied in order to one in-memory copy. |
| `preview` | boolean | no | Report what would change and write nothing. |

## `block_patch_text`

**Block Patch Text** — writes, closed-world.

Surgically edit ONE block: replace `find` with `replace` inside that block's SOURCE (exactly the text block_get_source returns), without resending the whole block. `find` must match EXACTLY ONCE — zero or multiple matches ERROR (it never guesses which). Span a long run by eliding the middle with an ellipsis: find="In the beginning…the Word" matches from the unique left anchor through the right. `replace` may be empty to delete the matched span. The block_id is preserved, and the patched source is re-parsed + re-validated — a patch that would make the block malformed is rejected and the block is left unchanged. Read the block with block_get_source first to copy an exact snippet (call source_syntax for the grammar). For TABLE/STAT blocks use block_set_table / block_set_stat instead; to replace a string across the WHOLE book use book_replace.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_id` | string | yes | The blk… id of the block to patch (from block_list / block_get_source). |
| `chapter_id` | string | yes | The idc… chapter that holds the block. |
| `find` | string | yes | Exact source text to replace; must occur EXACTLY ONCE in the block's source. Use '…' (or '...') to span a long run: 'left…right' replaces from the unique left … |
| `replace` | string | yes | Replacement text. May be empty to delete the matched span. |

## `block_set_source`

**Block Set Source** — writes, closed-world.

Replace a block's content by parsing source text. The block_id is preserved (handle stays stable). Use to revise an existing block without delete+re-add. Call source_syntax for the source grammar. If the block carries an authoring note, the response includes its subject(s) under `notes` as a heads-up — read it (note_get) before overwriting a flagged section.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `source` | string | yes | The block/chapter SOURCE text in the junifye markup (see source_syntax for the grammar). |

## `block_set_stat`

**Block Set Stat** — writes, closed-world.

Change a stat block's presentation without touching its rings: color ("plain"|"scale"|"#RRGGBB"), size (small|medium|large), columns (1|2). Omit a field to keep it.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `color` | string | no | Ring color: 'plain' (theme default), 'scale' (green→red by value), or a '#rrggbb' hex. |
| `columns` | integer | no |  |
| `size` | string | no |  |

## `block_set_table`

**Block Set Table** — writes, closed-world.

Replace an existing TABLE block's contents from STRUCTURED data — the only way to edit a table (never block_set_source / pipe text). The block_id is preserved, so the section's stable anchor never changes. rows = array of rows, each an array of cell strings (one per column); header = optional column headers; align = optional per-column "left"|"center"|"right"; caption = optional small-italic title. Same hard gates as block_add_table: ≤5 columns, header cells ≤24 characters, plain-text cells only (no *, ** or [..] markup). Ragged rows are padded; blank cells are allowed.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `align` | array | no | Optional per-column alignment; omit for all-left. |
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `caption` | string | no | Optional caption text shown under the block. |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `header` | array | no | Optional column headers; each ≤24 characters. |
| `rows` | array | yes | Body rows; each row is an array of cell strings. |

## `block_transfer`

**Block Transfer** — writes, closed-world.

MOVE whole sections (blocks) from one chapter to another — the two chapters may be in DIFFERENT BOOKS. This is the primitive for reorganising material across a shelf: lifting a thread out of one title into another, splitting a book, or pulling an appendix into its own volume. Blocks keep their ids (so existing deep-links and #anchors still resolve) and keep their relative order regardless of the order you list them in. By default they land at the END of the target chapter; pass insert_after (a block id in the TARGET) to place them after a specific section, or position='start' for the top. The two writes are ordered — target first, then source — and the target is READ BACK to confirm the blocks are really there before anything is removed from the source, so a mid-flight failure can only ever leave the blocks in BOTH chapters, never in neither; the response tells you if that happened, with the exact ids to clean up. Images and figures inside the moved blocks are COPIED into the target book (assets are stored per book), and the move is refused outright if one cannot be copied — a block moved without its picture would render blank AND the source book's cleanup would later delete the only copy. To reorder blocks WITHIN one chapter use block_move instead; this tool refuses when from_chapter == to_chapter.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_ids` | array | yes | The 'blk...' ids to move, from block_list(from_chapter). They are moved in the order they appear in the SOURCE chapter, not the order given here. |
| `from_chapter` | string | yes | The 'idc...' chapter the blocks are currently in (from chapter_list / block_list). |
| `insert_after` | string | no | Optional. A block id in the TARGET chapter; the moved blocks land immediately after it. Omit to append at the end. |
| `position` | string | no | Where to place them when insert_after is not given: 'end' (default) or 'start'. |
| `to_chapter` | string | yes | The 'idc...' chapter to move them into. MAY belong to a different book — that is the point of this tool. Create it first with chapter_create if it does not exi… |

## `list_add_item`

**List Add Item** — writes, closed-world.

Append (or insert at at_idx) a new row to a list block. Each new row is initialised with one text span — content can be refined via span_add_* / span_delete with the returned item_idx.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `at_idx` | integer | no | Optional 0-based span position to INSERT at; omit to APPEND at the end. Out-of-range is rejected, never clamped. |
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `text` | string | yes | Plain text content (source markup like *…* or [a:…] is NOT parsed here — use the span tools or block_set_source for markup). |

## `list_delete_item`

**List Delete Item** — writes, closed-world.

Delete row item_idx from a list block.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `item_idx` | integer | yes | For LIST blocks only: the 0-based row the span lives in (rows come from block_get_source / list order). Omit for paragraph-like blocks; required for lists. |

## `list_move_item`

**List Move Item** — writes, closed-world.

Reorder rows within a list block.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `from_idx` | integer | yes | The 0-based index of the item to move (see block_get_source for current order). |
| `to_idx` | integer | yes | The 0-based index to move it TO (positions after removal; out-of-range is rejected). |

## `span_add_bref`

**Span Add Bref** — writes, closed-world.

Append a Bible-reference link span. ref shape: '[1-3 ]Book Chap[:Verse[-Verse]]' — Book is 2-30 Unicode letters (English, Norwegian, German, Greek, etc.) and may include spaces, dots, hyphens. Examples: 'John 3:16', 'Gen 1:1', '1 Corinthians 13:1-13', 'Revelation 22:13', 'Åpenbaringen 1:8', 'Song of Songs 2:1'. translation optional (e.g. 'ESV').

| Parameter | Type | Required | Description |
|---|---|---|---|
| `at_idx` | integer | no | Optional 0-based span position to INSERT at; omit to APPEND at the end. Out-of-range is rejected, never clamped. |
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `item_idx` | integer | no | For LIST blocks only: the 0-based row the span lives in (rows come from block_get_source / list order). Omit for paragraph-like blocks; required for lists. |
| `ref` | string | yes | The Bible reference, e.g. 'John 3:16' or 'Rom 6:1-4' (localized book names/abbreviations accepted). |
| `translation` | string | no | Optional translation code, e.g. 'WEB', 'nb2026' — omit for the book's default. |

## `span_add_emph`

**Span Add Emph** — writes, closed-world.

Append italic-emphasis span. Use for emphasis, titles of works, or foreign terms not covered by hebrew/greek.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `at_idx` | integer | no | Optional 0-based span position to INSERT at; omit to APPEND at the end. Out-of-range is rejected, never clamped. |
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `item_idx` | integer | no | For LIST blocks only: the 0-based row the span lives in (rows come from block_get_source / list order). Omit for paragraph-like blocks; required for lists. |
| `text` | string | yes | Plain text content (source markup like *…* or [a:…] is NOT parsed here — use the span tools or block_set_source for markup). |

## `span_add_greek`

**Span Add Greek** — writes, closed-world.

Append Greek-script span (may contain accents + breathings). Rendered in GFS Didot. text MUST contain actual Greek letters (e.g. λόγος) — a Latin transliteration is rejected, not swallowed; put a transliteration in span_add_latin or use the strongs+translit form.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `at_idx` | integer | no | Optional 0-based span position to INSERT at; omit to APPEND at the end. Out-of-range is rejected, never clamped. |
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `item_idx` | integer | no | For LIST blocks only: the 0-based row the span lives in (rows come from block_get_source / list order). Omit for paragraph-like blocks; required for lists. |
| `text` | string | yes | Plain text content (source markup like *…* or [a:…] is NOT parsed here — use the span tools or block_set_source for markup). |

## `span_add_hebrew`

**Span Add Hebrew** — writes, closed-world.

Append Hebrew-script span (may contain nikud). Rendered RTL with appropriate Hebrew font. text MUST contain actual Hebrew letters (e.g. דָּבָר) — a Latin transliteration is rejected, not swallowed; put a transliteration in span_add_latin or use the strongs+translit form.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `at_idx` | integer | no | Optional 0-based span position to INSERT at; omit to APPEND at the end. Out-of-range is rejected, never clamped. |
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `item_idx` | integer | no | For LIST blocks only: the 0-based row the span lives in (rows come from block_get_source / list order). Omit for paragraph-like blocks; required for lists. |
| `text` | string | yes | Plain text content (source markup like *…* or [a:…] is NOT parsed here — use the span tools or block_set_source for markup). |

## `span_add_latin`

**Span Add Latin** — writes, closed-world.

Append LTR Latin-script span. Use inside an RTL-primary book (language he/ar/fa) to embed a Latin word/phrase — it renders LTR with the default body font mid-paragraph. In a Latin-primary book the macro is a visual no-op; safe to call anyway.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `at_idx` | integer | no | Optional 0-based span position to INSERT at; omit to APPEND at the end. Out-of-range is rejected, never clamped. |
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `item_idx` | integer | no | For LIST blocks only: the 0-based row the span lives in (rows come from block_get_source / list order). Omit for paragraph-like blocks; required for lists. |
| `text` | string | yes | Plain text content (source markup like *…* or [a:…] is NOT parsed here — use the span tools or block_set_source for markup). |

## `span_add_link`

**Span Add Link** — writes, closed-world.

Append an inline hyperlink span: a visible TITLE + a url. This is the ONLY way to put a URL in the text — a bare http(s):// or mailto: address typed into plain paragraph text is hard-rejected, so the reader/PDF never shows a raw URL. The title is what readers see (rendered in the link colour — the same blue as the TOC) and clicking opens the url in a new tab. The title must be PLAIN TEXT: no brackets, braces, parentheses, pipes, angle brackets or backslashes ([ ] { } | \ ( ) < >); letters of ANY language are fine (it's normalised to NFC). BOTH text and url are required. url must be http://, https:// or mailto:user@host.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `at_idx` | integer | no | Optional 0-based span position to INSERT at; omit to APPEND at the end. Out-of-range is rejected, never clamped. |
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `item_idx` | integer | no | For LIST blocks only: the 0-based row the span lives in (rows come from block_get_source / list order). Omit for paragraph-like blocks; required for lists. |
| `text` | string | yes | visible link title (required, plain text — no [ ] { } \| \ ( ) < >) |
| `url` | string | yes | target URL — http://, https:// or mailto:user@host |

## `span_add_strong`

**Span Add Strong** — writes, closed-world.

Append bold-emphasis span. Use sparingly — Bringhurst convention reserves bold for key terms only.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `at_idx` | integer | no | Optional 0-based span position to INSERT at; omit to APPEND at the end. Out-of-range is rejected, never clamped. |
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `item_idx` | integer | no | For LIST blocks only: the 0-based row the span lives in (rows come from block_get_source / list order). Omit for paragraph-like blocks; required for lists. |
| `text` | string | yes | Plain text content (source markup like *…* or [a:…] is NOT parsed here — use the span tools or block_set_source for markup). |

## `span_add_strongs`

**Span Add Strongs** — writes, closed-world.

Append a Strong's-concordance code span. code MUST match ^[HG][0-9]{1,5}$ — e.g. H1697, G3056.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `at_idx` | integer | no | Optional 0-based span position to INSERT at; omit to APPEND at the end. Out-of-range is rejected, never clamped. |
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `code` | string | yes | The Strong's code, e.g. 'G907' (Greek) or 'H2881' (Hebrew). |
| `item_idx` | integer | no | For LIST blocks only: the 0-based row the span lives in (rows come from block_get_source / list order). Omit for paragraph-like blocks; required for lists. |

## `span_add_text`

**Span Add Text** — writes, closed-world.

Append (or insert at at_idx) a plain-text span. Use this for normal prose.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `at_idx` | integer | no | Optional 0-based span position to INSERT at; omit to APPEND at the end. Out-of-range is rejected, never clamped. |
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `item_idx` | integer | no | For LIST blocks only: the 0-based row the span lives in (rows come from block_get_source / list order). Omit for paragraph-like blocks; required for lists. |
| `text` | string | yes | Plain text content (source markup like *…* or [a:…] is NOT parsed here — use the span tools or block_set_source for markup). |

## `span_delete`

**Span Delete** — writes, closed-world.

Delete the span at idx within the target block. For list blocks pass item_idx (selects the row); for paragraph/footnote omit it.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `idx` | integer | yes | The 0-based span index within the block (count spans in block_get_source). |
| `item_idx` | integer | no | For LIST blocks only: the 0-based row the span lives in (rows come from block_get_source / list order). Omit for paragraph-like blocks; required for lists. |

## `span_move`

**Span Move** — writes, closed-world.

Reorder spans within a block. For list blocks pass item_idx (selects the row); for paragraph/footnote omit it.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `from_idx` | integer | yes | The 0-based index of the item to move (see block_get_source for current order). |
| `item_idx` | integer | no | For LIST blocks only: the 0-based row the span lives in (rows come from block_get_source / list order). Omit for paragraph-like blocks; required for lists. |
| `to_idx` | integer | yes | The 0-based index to move it TO (positions after removal; out-of-range is rejected). |

## `stat_add_item`

**Stat Add Item** — writes, closed-world.

Append a ring to an existing stat block. percent 0–100; label is the bold text; description is an optional muted line; color is an optional "#RRGGBB" for THIS ring (overrides the block colour). Returns the new item_idx.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_id` | string | yes | The 'blk...' block id (from block_list, or returned by the block_add_* call that created it). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `color` | string | no | optional #RRGGBB for this ring |
| `description` | string | no | Optional longer line under the stat label. |
| `label` | string | yes | Short label under the stat ring (a few words). |
| `percent` | integer | yes | The statistic value 0..100 (renders as a donut ring). |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
