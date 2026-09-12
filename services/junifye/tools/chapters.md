# Chapters — Junifye MCP tools

**Create, order, version, diff and revert chapters.** 14 tools, listed below with the exact description and input
schema the server itself returns. Endpoint: `https://junifye.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`chapter_create`](#chapter-create) | Add a new empty chapter to a book |
| [`chapter_delete`](#chapter-delete) | Move a chapter to the TRASH |
| [`chapter_diff`](#chapter-diff) | Show what changed between two saved versions of a chapter — READ-ONLY (no revert, no re-render) |
| [`chapter_get_source`](#chapter-get-source) | Read the WHOLE chapter at once as round-trippable source — one call instead of block_list +… |
| [`chapter_history`](#chapter-history) | List a chapter's recent saved versions (newest first): version number, content checksum,… |
| [`chapter_list`](#chapter-list) | List chapters in book seq order |
| [`chapter_move`](#chapter-move) | Re-sequence a chapter inside its book to 1-based position `seq` (1 = first) |
| [`chapter_questions`](#chapter-questions) | List the questions linked to a specific chapter — the set you would be WARNED about before… |
| [`chapter_restore`](#chapter-restore) | Bring a soft-deleted chapter back out of the trash — its text, its title, its full version… |
| [`chapter_revert`](#chapter-revert) | Undo: revert a chapter to a previous version (from chapter_history) |
| [`chapter_set_source`](#chapter-set-source) | Replace a chapter's ENTIRE content from whole-chapter source text — blocks separated by a… |
| [`chapter_set_title`](#chapter-set-title) | Rename a chapter |
| [`chapter_transfer`](#chapter-transfer) | MOVE a whole chapter into a DIFFERENT BOOK — for splitting a book, lifting a thread into its… |
| [`chapter_version_get`](#chapter-version-get) | Read a PAST version of a chapter as round-trippable source (same shape as chapter_get_source)… |

---

## `chapter_create`

**Chapter Create** — writes, closed-world.

Add a new empty chapter to a book. book_id MUST be the 'idb...' value from book_create.id — passing the UUID returns 'not found'. Title CANNOT start with 'Chapter ' (renderer auto-numbers).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id returned by book_create.id (NOT the uuid). |
| `title` | string | yes | Chapter title; must not start with 'Chapter ' (the renderer auto-numbers). Prefer a SHORT title of a few words; long titles wrap in the heading, running head, … |

## `chapter_delete`

**Chapter Delete** — writes, closed-world.

Move a chapter to the TRASH. It leaves the book immediately (gone from chapter_list, the reader, the PDF and every export), but its text, its title and its full version history are KEPT for 30 days and can be brought back with chapter_restore — find it again with chapter_list(include_deleted=true). After that it is permanently purged. Its NOTES go to the trash with it and come back on restore — they are destroyed only at purge. Pass delete_notes=false to promote them to book-level notes IMMEDIATELY instead, so they survive the purge too. Question links are the one thing a restore does NOT bring back. A SUBSTANTIAL chapter (many blocks) additionally requires confirm=true, and the refusal tells you exactly how much content and history is at stake. Bumps book.version so the next PDF fetch lazy-re-renders.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `confirm` | boolean | no | Required (true) only for a chapter with substantial content; a small stub deletes without it. Set it once you have told the user what the refusal said is at st… |
| `delete_notes` | boolean | no | Default true: the chapter's notes go to the trash with it (restored by chapter_restore, destroyed only when the chapter is purged). Set false to promote them t… |

## `chapter_diff`

**Chapter Diff** — read-only, idempotent, closed-world.

Show what changed between two saved versions of a chapter — READ-ONLY (no revert, no re-render). With NO version args it diffs the LAST edit (current vs the version before it), so chapter_diff(chapter_id) answers "what did my last edit change?". Pass block_id to scope the diff to ONE section (paragraph/heading/…): it returns that section's before/after text plus an inline word delta (removed = [-…-], added = [+…+]), matching the section across the edit even though block ids are re-minted (by id when stable, else by position). Without block_id it returns a whole-chapter line diff (- removed / + added). See chapter_history for version numbers.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `block_id` | string | no | Optional: scope to ONE section. Use the block_id as it appears in the newer version (chapter_get_source / block_list); it is matched back across the edit. |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `from_version` | integer | no | Older version (default: the one just before to_version). |
| `to_version` | integer | no | Newer version (default: current). |

## `chapter_get_source`

**Chapter Get Source** — read-only, idempotent, closed-world.

Read the WHOLE chapter at once as round-trippable source — one call instead of block_list + block_get_source per block. PICK THE SHAPE BY WHAT YOU ARE ABOUT TO DO, and nothing needs reassembling: shape='blocks' (the DEFAULT) to edit block by block — returns {chapter_id, blocks:[{block_id, type, source, source_editable}], count, checksum}, and each block_id goes straight into block_set_source or block_patch_text; shape='flat' to replace the whole chapter — returns {chapter_id, source, count, checksum, source_editable} and you hand that exact `source` string back to chapter_set_source unchanged. Only ONE form comes back, because they are the same text: the flat form IS the per-block sources joined by a BLANK LINE. If you do reassemble it yourself, the separator is a BLANK line — a single newline makes the whole chapter parse as ONE block. Each block's `source` round-trips through block_set_source(chapter_id, block_id, source), so this is THE tool for whole-document review, bulk revision, and translation: read every block's source here, transform the prose, then write each block back by its block_id. Inline original-language/reference spans appear as \hebrew{…}, \greek{…}, \strongs{…}, \bref{…}, \latin{…} islands — when translating, change the surrounding text but keep those macros AND their contents intact. A chapter in the TRASH is still readable here and comes back with deleted:true plus a deleted_note — treat that text as deleted, not as part of the book.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `shape` | string | no | Which form of the text to return — pick the one matching your next write. 'blocks' (default) = every block with its block_id, for block_set_source / block_patc… |

## `chapter_history`

**Chapter History** — read-only, idempotent, closed-world.

List a chapter's recent saved versions (newest first): version number, content checksum, author, timestamp, and which is current. History keeps the last N versions, where N is the OWNING BOOK's history_limit (default 120, max 360, set with book_set history_limit); a superseded version also expires after 7 days (the current version never expires). Pair with chapter_revert to undo a bad edit.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `limit` | integer | no | Max rows to return (default 50, max 200). Omit it, or pass 0, for the default. A NEGATIVE limit is rejected, not clamped. |
| `offset` | integer | no | 0-based row offset for the next page. Omit for the first page; pass the previous offset+limit while has_more is true. A NEGATIVE offset is rejected. |

## `chapter_list`

**Chapter List** — read-only, idempotent, closed-world.

List chapters in book seq order. Returns lean projection per chapter: {id, book_id, title, seq, current_version, updated_at}. No checksum surfaced — concurrency is server-side. Pass include_deleted=true to ALSO list chapters currently in the trash (deleted=true, with deleted_at and restorable_until, plus deleted_reason when there is one to give — e.g. "merged into idc…") — that is how you find the chapter_id to hand to chapter_restore. NOTE: trashed entries are appended after the live ones with seq:0, and `total` counts EVERYTHING returned — so with include_deleted=true it is live+trashed, not the book's chapter count. `deleted_count` gives the trashed portion; live chapters = total - deleted_count.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |
| `include_deleted` | boolean | no | Default false. When true, soft-deleted chapters still inside the trash window are appended to the list, each tagged deleted:true — restore one with chapter_res… |

## `chapter_move`

**Chapter Move** — writes, closed-world.

Re-sequence a chapter inside its book to 1-based position `seq` (1 = first). The whole book is reflowed so chapters stay densely ordered with no gaps or ties — `seq` can land a chapter BETWEEN any two others, and out-of-range values clamp to first/last. Returns the new chapter order. Bumps book.version so the next PDF fetch lazy-re-renders.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `seq` | integer | yes | 1-based target position (1 = first chapter). Clamped to [1, chapter_count]. |

## `chapter_questions`

**Chapter Questions** — read-only, idempotent, closed-world.

List the questions linked to a specific chapter — the set you would be WARNED about before deleting or heavily editing it (deleting the chapter auto-detaches these; editing its content flags them stale for review).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chapter_id` | string | yes | The 'idc...' chapter id. |

## `chapter_restore`

**Chapter Restore** — writes, closed-world.

Bring a soft-deleted chapter back out of the trash — its text, its title, its full version history AND its notes return intact, and it is re-appended as the LAST chapter of the book (its old position is NOT restored, because the other chapters may have moved meanwhile; use chapter_move to place it). Find restorable chapters with chapter_list(book_id, include_deleted=true). DO NOT call this on your own initiative: restoring is the human's decision — if an edit fails because a chapter is in the trash, TELL the user and call chapter_restore ONLY when they explicitly ask. Question links do NOT come back (re-link with question_link), and notes that chapter_delete(delete_notes=false) promoted to book level stay at book level — they were never deleted. Only works inside the trash window (30 days); after that the chapter is purged and unrecoverable.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the book the chapter belongs to. |
| `chapter_id` | string | yes | The 'idc...' id of the deleted chapter, from chapter_list(include_deleted=true). |

## `chapter_revert`

**Chapter Revert** — writes, closed-world.

Undo: revert a chapter to a previous version (from chapter_history). NON-DESTRUCTIVE — it restores that version's content as a NEW current version, so the reverted-from edit stays in history and can itself be reverted. The whole chapter is replaced atomically. Errors if the version is no longer available (beyond the book's history_limit — default 120, max 360 — or expired after 7 days).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `version` | integer | yes | The version number to restore (see chapter_history). |

## `chapter_set_source`

**Chapter Set Source** — writes, closed-world.

Replace a chapter's ENTIRE content from whole-chapter source text — blocks separated by a blank line (the form chapter_get_source returns as `source`). ATOMIC: if any block is malformed the whole chapter is rejected and NOTHING changes; the error names the offending block. This is the whole-chapter edit-and-push primitive (and the building block of import). Refused if the chapter currently holds a non-source-editable block (e.g. a table) so it can't be silently dropped — edit those via the block_* tools. Call source_syntax for the grammar.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `source` | string | yes | The whole chapter as source text; blocks separated by a blank line. |

## `chapter_set_title`

**Chapter Set Title** — writes, closed-world.

Rename a chapter. The new title is validated through the same rules as chapter_create (no leading 'Chapter ', must start with a letter, max 80 chars).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `title` | string | yes | New chapter title. Prefer a SHORT title of a few words; long titles wrap in the heading, running head, and TOC. Be concise but complete. |

## `chapter_transfer`

**Chapter Transfer** — writes, closed-world.

MOVE a whole chapter into a DIFFERENT BOOK — for splitting a book, lifting a thread into its own volume, or filing a chapter under the title it really belongs to. The chapter KEEPS its id, all its blocks and their ids, and its ENTIRE version history, because it is re-parented rather than copied: the alternative hand-rolled route (chapter_create + chapter_set_source + chapter_delete) mints a new id that breaks every anchor and deep link, restarts the history at version 1, and has a moment where the text is in neither book. This has no such moment — the move commits in ONE transaction, so the chapter is never in both books and never in neither. Its NOTES travel with it. It lands LAST in the target book; use chapter_move afterwards to position it. Images and figures are COPIED into the target book first (assets are stored per book) and the move is REFUSED if one cannot be, since a chapter moved without its pictures would render blank and the source book's cleanup would later delete the only copy. Also refused if the chapter uses glossary terms the target book's dictionary cannot resolve — add them with dict_add, or connect a shared dictionary, then retry. Questions in the SOURCE book that cited this chapter are detached (their text is kept) and reported. Requires write access to BOTH books, and both must have the SAME OWNER — a chapter carries its private notes and its whole draft history with it, so moving content between two owners is an administrator's act, not an editor's. A frozen or published book refuses, on either side.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chapter_id` | string | yes | The 'idc...' chapter to move, from chapter_list. It moves WHOLE — every block goes with it. |
| `to_book` | string | yes | The 'idb...' id of the book to move it INTO (from book_list / book_create.id — NOT the uuid in public PDF URLs). Must be a different book than the one it is in… |

## `chapter_version_get`

**Chapter Version Get** — read-only, idempotent, closed-world.

Read a PAST version of a chapter as round-trippable source (same shape as chapter_get_source) WITHOUT changing anything. Pair with chapter_history (version numbers) and chapter_diff. READ-ONLY: unlike chapter_revert it never makes the old version current or re-renders. Note: block ids are re-minted on some edits, so a section's id in an old version can differ from its id now — chapter_diff handles that matching for you.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chapter_id` | string | yes | The 'idc...' chapter id (from chapter_list / chapter_create — NOT a book id or block id). |
| `version` | integer | yes | Version number to read (see chapter_history). |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
