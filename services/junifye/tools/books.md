# Books and editions — Junifye MCP tools

**Create a book, read it back, publish it, link its translations.** 34 tools, listed below with the exact description and input
schema the server itself returns. Endpoint: `https://junifye.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`book_cover_generate`](#book-cover-generate) | Generate a cover for a book and set it: an image model draws a background from the book's OWN… |
| [`book_cover_refresh`](#book-cover-refresh) | Re-set the title, author and imprint mark over the artwork ALREADY STORED for this book, and… |
| [`book_cover_restore`](#book-cover-restore) | Revert this book's cover to a previous version, from book_cover_versions |
| [`book_cover_status`](#book-cover-status) | Poll a running or finished cover generation |
| [`book_cover_upload_begin`](#book-cover-upload-begin) | Begin uploading the front COVER ART for ONE book |
| [`book_cover_versions`](#book-cover-versions) | List the covers this book USED and can still be reverted to |
| [`book_create`](#book-create) | Create a new book or document |
| [`book_delete`](#book-delete) | Soft-delete a book into a trash window of 30 days (restore with book_restore) |
| [`book_epub_check`](#book-epub-check) | Inspect the metadata of a book's ACTUAL BUILT EPUB — the file a store would receive — and… |
| [`book_export_begin`](#book-export-begin) | Begin a book export |
| [`book_files`](#book-files) | List EVERY file this book can hand over — one call, with metadata and staleness |
| [`book_freeze`](#book-freeze) | ADMIN |
| [`book_get`](#book-get) | Get book metadata + artifact URLs: url (the PRIMARY link to share — the short permalink that… |
| [`book_get_source`](#book-get-source) | Read MANY chapters' round-trippable source in ONE call — the whole book by default, or a subset |
| [`book_grep`](#book-grep) | Find WHERE a string occurs in a book, one result per occurrence, each attributed to its BLOCK… |
| [`book_group_add`](#book-group-add) | Attach a GROUP to a book so every member of the group becomes a content editor of it (resolved… |
| [`book_group_remove`](#book-group-remove) | Detach a GROUP from a book — its members lose the group-derived edit access to that book (any… |
| [`book_import_begin`](#book-import-begin) | Begin a book import |
| [`book_isbn_assign`](#book-isbn-assign) | Assign a REAL, pool-allocated ISBN-13 to a published book |
| [`book_list`](#book-list) | List books with sort + pagination + visibility filter |
| [`book_logo_upload_begin`](#book-logo-upload-begin) | Begin uploading a logo for ONE book's social share card (og:image) — it OVERRIDES your… |
| [`book_outline`](#book-outline) | Cheap PLANNING view of a book BEFORE reading content: each chapter's size + block count, plus… |
| [`book_publish_to_store`](#book-publish-to-store) | Put this book ON THE SHELF — register it for sale on the storefront and upload the EPUB a… |
| [`book_questions`](#book-questions) | List every question this book answers (across all its chapters + any whole-book answers) |
| [`book_replace`](#book-replace) | Find-and-replace a LITERAL text string across EVERY chapter of a book — fix a recurring typo,… |
| [`book_restore`](#book-restore) | Restore a soft-deleted book within its trash window (30 days) — re-adds it to all listings and… |
| [`book_retract_from_store`](#book-retract-from-store) | Take this book OFF the shelf |
| [`book_revision_close`](#book-revision-close) | Close a revision window on YOUR published book — refreeze its text as the new canonical… |
| [`book_revision_open`](#book-revision-open) | Open a REVISION WINDOW on YOUR published book so you can edit its (otherwise canonical,… |
| [`book_search`](#book-search) | Search visible books |
| [`book_set`](#book-set) | Atomically set ONE book field by key |
| [`book_set_buy_links`](#book-set-buy-links) | Set WHERE a reader can buy this book — every channel, not just ours |
| [`book_set_translation_of`](#book-set-translation-of) | Link a book as a translation/edition of an ORIGINAL book so the two appear as language… |
| [`book_unfreeze`](#book-unfreeze) | Lift a book freeze |

---

## `book_cover_generate`

**Book Cover Generate** — writes, closed-world.

Generate a cover for a book and set it: an image model draws a background from the book's OWN description and subject codes, then junifye composes the title, author and owner logo over it. ASYNC — returns immediately with a job you poll via book_cover_status; the run is a text-model call, an image-model call and a typesetting pass, which is tens of seconds.
REFUSES a book that already has a cover unless replace=true: an author's own cover is not overwritten on a whim. Also refuses a book with no description, because the description is what the image is drawn from — write one (or let publish_request generate one) first.
The background is checked for lettering before it is used: image models add text despite being told not to, junifye sets the title itself, and a store's review rejects a cover with garbled pseudo-words on it. Owner-only.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of YOUR book. Not the public UUID. |
| `replace` | boolean | no | Overwrite an existing cover. Default false, which refuses rather than replacing what the author put there. |

## `book_cover_refresh`

**Book Cover Refresh** — writes, closed-world.

Re-set the title, author and imprint mark over the artwork ALREADY STORED for this book, and replace the cover with the result. FREE and repeatable: it does not call an image model and cannot change the picture.
This is the counterpart to book_cover_generate, and they are deliberately separate tools because they are different acts: generate DRAWS A NEW PICTURE and costs an image-model call; refresh only re-typesets the one you have. Use refresh after changing a title, author or imprint, or after junifye's cover typography improves.
ONE BOOK, ONE COVER. It never touches other language editions. Sharing one cover across editions is a decision for a person to make deliberately, edition by edition — Apple does not recommend it, so junifye will not do it for you.
TITLE SIZE AND WEIGHT LIVE HERE. Pass title_scale and/or title_bold to re-typeset the SAME picture at a different size or weight — no image model, no re-upload, so it is the dial to spin when the fitted title crowds the artwork. Both are STORED on the book, so a later rename recomposes at the style you chose rather than reverting. Omit them to re-typeset at the book's current style.
Returns {refreshed:true, title_scale, title_bold} on success, or reason no_stored_artwork when the cover was uploaded finished and has no separable artwork to re-set type over. Owner-only.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of YOUR book. Not the public UUID, and not a sibling edition. |
| `title_bold` | boolean | no | Set the title in bold. Omit to keep the book's current setting. |
| `title_scale` | number | no | Title size as a MULTIPLIER of the size junifye fits by itself. 1.0 is that fitted size — already the largest the band holds — so this dial mostly goes DOWN. Ra… |

## `book_cover_restore`

**Book Cover Restore** — writes, closed-world.

Revert this book's cover to a previous version, from book_cover_versions. The current cover is NOT destroyed — it is itself snapshotted first, so a restore is reversible too (an author can keep testing covers). What comes back is byte-for-byte what was on file: the composed image plus, when that cover had one, its separable artwork — so a later book_cover_refresh re-typesets over the RIGHT picture.
seq must be a STRING, copied verbatim from book_cover_versions — it is a 19-digit UnixNano timestamp, too large to survive a JSON float round-trip (treating it as a number silently corrupts it and the restore fails to find the version). Refuses a seq that is not retained: never snapshotted, or past its 90-minute window and already GC'd — list with book_cover_versions first. Owner-only.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of YOUR book. |
| `seq` | string | yes | The version to restore, as a STRING copied verbatim from book_cover_versions. |

## `book_cover_status`

**Book Cover Status** — read-only, idempotent, closed-world.

Poll a running or finished cover generation. Returns {state: running|done|failed, stage, eta_seconds, prompt, error}. Safe to call repeatedly.
eta_seconds is measured from how long the last SUCCESSFUL cover took on this deployment, not guessed; 0 means there is no history to estimate from yet, which should be shown as 'no estimate' rather than 'almost done'. `prompt` is what the image model was actually asked for, so a cover can be adjusted deliberately rather than only re-rolled. Owner-only.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of YOUR book. |

## `book_cover_upload_begin`

**Book Cover Upload Begin** — writes, closed-world.

Begin uploading the front COVER ART for ONE book. Returns a one-time {reqid, url, expect}: a PERSON OPENs the url (browser upload page) and picks a PNG/JPEG; an AI POSTs the bytes — `curl -X POST <url> --data-binary @cover.png` (or `-F file=@cover.jpg`).

READ `expect` BEFORE YOU EXPORT THE IMAGE. It carries min_px + dpi computed from THIS book's own trim and bleed, and the upload is REJECTED if the file does not meet them. Sizing it right the first time costs nothing; discovering it afterwards means a reprint.

⚠ THE MISTAKE EVERYONE MAKES: the wrap scales front art to fill the panel INCLUDING BLEED, not the trim. Art exported at trim size is stretched — 300 dpi at 170×240 mm becomes 283 dpi at 180×250 mm, under spec, silently. Always size to TRIM + BLEED. `expect.min_px` already does that arithmetic for you.

WHAT IS CHECKED ON RECEIPT (each returns a structured error with got/required and a `fix`):
  • format — PNG or JPEG only
  • resolution — reason=too_few_pixels, with got_effective_dpi so you can see how soft it would print
  • shape — reason=wrong_aspect_ratio if it is more than 2% off the panel; the art FILLS the panel, so a mismatch crops or stretches it
  • size + a 60 MP decompression-bomb guard
  • transparency — an alpha channel returns a WARNING, not a refusal: it prints, but flatten it or the transparent areas composite unpredictably
NOTE the embedded pHYs/JFIF "dpi" tag is NOT trusted — it is self-reported and routinely wrong. Effective resolution is pixels ÷ printed size, which is what the pixel check measures.

The ORIGINAL bytes are stored unmodified (print-grade, never re-encoded or downscaled — the wrap generator needs the true pixels), shown TOPSIDE on the HTML reader, and downloadable at a stable url (`<reader-base>/<uuid>-cover`). This art is what print_set composes onto the FRONT panel of the wrap cover.

COMPOSE_TITLE — the one-stop path for an AI that can draw but cannot typeset. Pass compose_title=true and push BARE ARTWORK: junifye sets this book's title and author over it in the book's own script (Arabic, Hebrew, CJK and Indic all shape correctly — it is the engine that sets the books) and stores the result at the retail 1600x2560, which every store accepts. The response says composed:true so you can tell what you got. Leave it OFF for a finished cover that already has type on it, or the title is set twice.

This is NOT the social share image (og:image) — that is the separate owner logo; the two never mix. Single-use, expires in 30 min; bytes stream over REST, never through MCP.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the book to set the cover for. |
| `compose_title` | boolean | no | The pushed image is BARE ARTWORK and junifye should set the title and author over it, storing the result at the retail 1600x2560. Default false, which stores t… |
| `title_bold` | boolean | no | Set the title in bold. Default false. Stored on the book alongside title_scale. Meaningless without compose_title=true. |
| `title_scale` | number | no | Title size, as a MULTIPLIER of the size junifye fits by itself. 1.0 (the default) is that fitted size, which is already the largest the title band holds — so t… |

## `book_cover_versions`

**Book Cover Versions** — writes, closed-world.

List the covers this book USED and can still be reverted to. When a cover is replaced (book_cover_generate replace=true, or a new upload via book_cover_upload_begin), the old cover — its composed image AND, when present, the separable artwork it was composed from — is kept on file for 90 minutes. This lists every such retained cover, newest first, with its seq (the handle to restore with), when it was replaced, and how long it remains revertible. Covers past the window are already gone and are never listed.
seq is returned as a STRING and book_cover_restore expects it as a string — copy it verbatim. It is a 19-digit UnixNano timestamp, too large to survive a JSON float round-trip, so treating it as a number silently corrupts it. Owner-only.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of YOUR book. |

## `book_create`

**Book Create** — writes, closed-world.

Create a new book or document. Returns BOTH an id (idb...) and a uuid:
  • id   — use this for every subsequent MCP call (chapter_create, book_set_*, etc.)
  • uuid — appears ONLY in the public PDF URL https://junifye.publifye.com/<uuid>-light.pdf
NEVER pass uuid to other tools as book_id — they expect the 'idb...' value.
book_type: 'book' = cover + TOC + numbered chapters; 'document' = title + flowing sections (memo/article style). Default is 'book'.
language: closed BCP-47 enum that drives body font, hyphenation, and text direction. Supported language codes: af (Afrikaans), am (Amharic), ar (Arabic, RTL), bn (Bengali), cs (Czech), da (Danish), de (German), el (Greek), en (English, default), es (Spanish), fa (Farsi (Persian), RTL), fil (Filipino), fr (French), he (Hebrew, RTL), hi (Hindi), hu (Hungarian), hy (Armenian), id (Indonesian), is (Icelandic), it (Italian), ja (Japanese), kn (Kannada), ko (Korean), nb (Norwegian Bokmål), nl (Dutch), nn (Norwegian Nynorsk), pa (Punjabi), pl (Polish), pt (Portuguese), ro (Romanian), ru (Russian), sv (Swedish), sw (Swahili), ta (Tamil), te (Telugu), th (Thai), tr (Turkish), uk (Ukrainian), ur (Urdu, RTL), vi (Vietnamese), zh (Chinese). Empty = en. RTL codes (he/ar/fa) flip page numbers to the RTL outer edge and swap the body font (Ezra SIL for Hebrew; Amiri for Arabic + Farsi).
New books default to listed=false. The UUID is the access token: anyone with the URL can fetch the PDF, but the book is hidden from public listings until you call book_set(key='listed', value='true'). Reversible.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `author` | string | no | Author name as it should appear (plain text). |
| `book_type` | string | no | book = classical multi-chapter style (cover page + TOC + numbered chapters + page break per chapter). document = plain title + flowing sections (no cover, no T… |
| `cover_url` | string | no | Optional external cover image URL (http(s)); uploading via book_cover_upload_begin is preferred. |
| `language` | string | no | BCP-47 language code. Omit to default to en (English, LTR). RTL codes: he (Hebrew), ar (Arabic), fa (Farsi/Persian), ur (Urdu). nb = Norwegian Bokmål, nn = Nor… |
| `origin` | string | no | PROVENANCE — whose words are these? original (DEFAULT) = the owner's own authored work. transcript = captured EXTERNAL material copied in verbatim (e.g. a YouT… |
| `origin_label` | string | no | For origin=transcript: short human attribution, e.g. 'YouTube — <channel name>' (max 120 chars). |
| `origin_url` | string | no | For origin=transcript: the canonical source link (e.g. the YouTube video URL). http(s) only. |
| `slug` | string | no | Optional URL slug; auto-derived from the title when omitted. |
| `subtitle` | string | no | Optional descriptive line under the title on the cover + title page (max 140 chars). This is where a longer explanatory phrase belongs, e.g. 'A Biblical Theolo… |
| `title` | string | yes | Book title — the cover headline (max 60 chars). Keep it SHORT and punchy; put the longer descriptive line in subtitle. |
| `translation_of` | string | no | Optional: the 'idb...' id of an EXISTING book this new book is a translation/edition of. Links them as language editions of one title — a language picker on th… |

## `book_delete`

**Book Delete** — writes, closed-world.

Soft-delete a book into a trash window of 30 days (restore with book_restore). The book is removed from all listings immediately; after that it is permanently purged. A public (listed) book can ONLY be deleted by an admin — owners cannot remove published work. A book under an ADMIN HOLD (book_freeze) cannot be deleted at all, by its owner OR by an admin: the refusal quotes the hold's date and reason. Lift it with book_unfreeze first, or use admin_book_delete for an erasure that must proceed despite the hold.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |

## `book_epub_check`

**Book EPUB Check** — read-only, idempotent, closed-world.

Inspect the metadata of a book's ACTUAL BUILT EPUB — the file a store would receive — and report whether it is complete for EPUB 3 and, separately, for Apple Books. Reads OEBPS/content.opf out of the packaged .epub (building it first if none is cached), so it answers what the file DECLARES rather than what the book record intended; those differ whenever a source (taxonomy subjects, the imprint, the description) was absent at build time.
Returns per-field presence for dc:identifier, dc:title, dc:language, dc:creator, dc:publisher, dc:description and dc:subject, plus two flags that are NOT the same bar: epub3_metadata_complete (the format is satisfied) and apple_metadata_ready (Apple would accept it). A book can be the first and not the second — an EPUB with no description or subject is entirely valid and Apple refuses it.
Also reports identifier_is_isbn (Apple keys the listing on the ISBN, so a urn:uuid identifier means no ISBN has been assigned yet) and has_cover_image (Apple requires a cover, and the delivery package cannot be built without one). `problems` lists every reason in plain words. READ-ONLY: builds nothing that is not already needed to inspect, delivers nothing, changes nothing. Run this BEFORE apple_delivery_begin.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the book to inspect. Not the public UUID. |

## `book_export_begin`

**Book Export Begin** — read-only, idempotent, closed-world.

Begin a book export. Returns a one-time {reqid, url, method:GET}: GET the url (e.g. `curl -L <url> -o book.json`) to download the whole book as an editable bundle — per chapter a flat Markdown-ish `source` + an id-independent `checksum`, plus a book `merkle_root`. The ticket is single-use and expires in 30 minutes. Large books stream over REST, never through MCP. Edit the file by hand, then push it back with book_import_begin.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id. |

## `book_files`

**Book Files** — read-only, idempotent, closed-world.

List EVERY file this book can hand over — one call, with metadata and staleness. Answers the print question directly: the entries with for_print=true are exactly what a printer needs (the interior and the full wrap cover), and nothing else. Also lists the distribution formats (reader PDF light/dark, EPUB, TXT, TeX) and the uploaded cover art, each marked for_print=false.

Each entry carries a stable `key` — e.g. "epub" or "print_cover:drukatava_170x240" — plus url, mime, and a `meta` block whose contents depend on the kind: pages/trim/bleed/colour for an interior, spine and sheet size for a wrap cover, pixel size for cover art.

STALENESS: a derived file carries stale=true when it was built from an older version of the book — the single most dangerous object here is a press file that looks finished and is wrong by however much the book moved since. Re-render with print_set(book_id), or simply fetch the URL (the artifact lazily re-renders on fetch).

READ-ONLY and cheap: it NEVER renders. It reports what exists; it does not create it. A file that has not been generated is simply absent, and print artifacts appear here the moment print_set produces them.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the public uuid). |

## `book_freeze`

**Book Freeze** — writes, closed-world.

ADMIN. Place a book under an OPERATOR HOLD — for abuse review, a legal dispute, or an investigation. The hold locks ALL content edits (owner and group alike, overriding listed/publicly_editable) AND blocks the book's removal: while it stands, book_delete is refused for the owner and an admin alike, and the automatic reapers (inactivity TTL, the trash sweep) skip the book so it cannot expire out from under the hold. The hold travels with the book across admin_book_transfer, and survives a delete/restore round trip and a rebuild from export. Read access is never affected. Lifted by an admin with book_unfreeze. The ONE way to remove a held book is the deliberate, loudly-audited admin_book_delete (hard purge, for a legal erasure that must proceed despite the hold). Pass `reason` — it is quoted back verbatim in every refusal, so it answers the owner's support question instead of generating one.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the book to freeze. |
| `reason` | string | no | Free-text reason for the hold, shown verbatim to anyone whose edit or delete it refuses (e.g. "pending abuse review", "DMCA claim #1183"). Max 200 chars. Stron… |

## `book_get`

**Book Get** — read-only, idempotent, closed-world.

Get book metadata + artifact URLs: url (the PRIMARY link to share — the short permalink that 301s to the reader; the explicit UUID forms are returned alongside, never instead), uuid_url (the full <uuid>.html reader — the stable, unguessable link that IS the access barrier for a PRIVATE book; for a private book `url` already equals this, so NEVER shorten it; for a PUBLISHED book give the short `url`, not uuid_url), short_url + slug_url (SHORT shareable aliases for PUBLISHED books; short_url is what `url` surfaces when published), light_url/dark_url (PDF themes — every reader picks a theme), epub_url (the reflowable EPUB 3 for Kindle / Apple Books / Kobo), txt_url (the pure plain-text export — opens anywhere, free even when downloads are gated), print_url, tex_url, and editions[]. short_url is a random unguessable permalink present on every book; slug_url is the readable title slug, present (non-empty) only on LISTED books. DEEP-LINKING INTO THE READER: to link from another book (or anywhere) to a specific spot here, append an anchor — '#<block_id>' for a SECTION (every block_list id IS the reader's stable per-section anchor) or '#ch-<N>' for the Nth chapter (1-based) — to ANY of url / short_url / slug_url / uuid_url (all resolve the fragment identically). e.g. an [a:see §3|<short_url>#<block_id>] link in book X pointing into book Y. Section anchors are stable across edits; the chapter '#ch-N' is positional (shifts if chapters reorder), so prefer a block_id. EDITORIAL: also returns editorial_status ('' = not in review, 'ready' = waiting for an editor, 'approved' = signed off) + editorial_editor (the assigned editor's name). This is the opt-in editorial-review workflow — set it / assign an editor with editorial_set, and an editor lists what is waiting for them with editorial_list(assigned_to:'mine').

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |

## `book_get_source`

**Book Get Source** — read-only, idempotent, closed-world.

Read MANY chapters' round-trippable source in ONE call — the whole book by default, or a subset. Use this (not a chapter_get_source loop) for whole-book review, translation, or cross-chapter consistency. Returns {book_id, chapters:[{chapter_id, index, title, blocks:[{block_id,type,source}], count, source}], returned, selected, total_chapters, total_bytes, payload_bytes, limit_bytes, shape, truncated}. `source_editable` appears on a block ONLY when it is not source-editable, with a note naming the tool to use instead. `index` is the 0-based position in book order. Each chapter's shape is IDENTICAL to chapter_get_source, so write edits back per block via block_set_source(block_id) or per chapter via chapter_set_source. Each chapter's text is returned ONCE, in one of two shapes. shape='blocks' (default) gives every block with its block_id — the handle you write back through (block_set_source, block_patch_text) and the block's anchor in the published reader. shape='flat' gives the whole-chapter source only: leanest, written back with chapter_set_source, but without ids. They are the same text — the flat form is the per-block sources joined by a BLANK LINE — so join them yourself rather than asking for both. The response is capped on payload_bytes, the real measured JSON: whole chapters are returned in order until the next would exceed limit_bytes, then truncated:true and `next_from_index` gives the page to fetch next with book_get_source(book_id, from_index=…). A single chapter larger than the cap is reported (not dumped) — read it block-by-block. Select with chapter_ids (exact subset) OR from_index+limit (paging). Call book_outline first for the exact page plan. Read-only.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id. |
| `chapter_ids` | array | no | Optional exact subset of 'idc...' chapter ids to read (returned in book order). Takes precedence over from_index/limit. Every id must belong to this book. |
| `from_index` | integer | no | Optional 0-based position in book order to start from. Use next_from_index from a truncated response to page through a large book. |
| `limit` | integer | no | Optional max number of chapters to return (still also bounded by the byte cap). |
| `shape` | string | no | Which form of each chapter's text to return — never both, since one is derivable from the other. 'blocks' (default) = every block with its block_id, type and s… |

## `book_grep`

**Book Grep** — read-only, idempotent, closed-world.

Find WHERE a string occurs in a book, one result per occurrence, each attributed to its BLOCK — the tool to use before any revision pass. book_search(content=true) only answers WHETHER a book mentions something and names one chapter; this names every block.

Matching is FOLDED by default — case-, diacritic- and accent-insensitive, so 'dap' finds 'Dåp'. Pass regex=true for RE2 (Go regexp: linear time, no catastrophic backtracking, so any pattern is safe); a regex is matched literally against the text and is NOT folded, because a caller writing a character class means it.

exclude_bible_headers=true drops the CITATION line of a scripture block and keeps its verse text. Use it for any scripture-reference query — searching 'Romerne' otherwise returns the reference line of every verse quoted and buries the prose that discusses it.

Each match carries chapter_id, chapter_title, block_id, block_type, the matched text, a context window, and the byte offset within the block. `total` counts ALL matches in the book before paging, `returned` counts the ones in this response, and `truncated` says whether more exist beyond it — so you can tell a complete answer from a partial one instead of assuming. A page is bounded by BOTH your limit and a measured byte budget, so it can come back shorter than you asked for; when it does, `truncated_by` says which bound was hit and `next_offset` is the offset to continue from.

Pair with block_patch_text: grep to find the exact block ids, then patch each one. Do NOT hand-roll regex over chapter_get_source to work out where something is.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id (NOT the public uuid). |
| `chapter_ids` | array | no | Restrict to these chapters. Empty = whole book. |
| `exclude_bible_headers` | boolean | no | Skip the citation of scripture blocks, keep the verse text. |
| `limit` | integer | no | Max matches per page (default 500, max 2000). A COUNT, not a size — the response is ALSO capped on measured bytes, so a page may come back shorter than the lim… |
| `offset` | integer | no | Matches to skip, for paging. |
| `pattern` | string | yes | Literal text, or an RE2 pattern when regex=true. |
| `regex` | boolean | no | Treat pattern as RE2. Not folded. |

## `book_group_add`

**Book Group Add** — writes, closed-world.

Attach a GROUP to a book so every member of the group becomes a content editor of it (resolved live — membership changes take effect instantly). Book owner only, and you must BELONG to the group you are attaching (you can only share via groups you are in). Idempotent.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book` | string | yes | The 'idb...' id from book_create.id (NOT the uuid). |
| `group_id` | string | yes | The 'grp...' id of a group you belong to (group_list). |

## `book_group_remove`

**Book Group Remove** — writes, closed-world.

Detach a GROUP from a book — its members lose the group-derived edit access to that book (any who are ALSO individual guests, or members of another attached group, keep access via that path). Book owner only. Idempotent.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book` | string | yes | The 'idb...' id from book_create.id (NOT the uuid). |
| `group_id` | string | yes | The 'grp...' id to detach (book_get / guest_list shows attached groups). |

## `book_import_begin`

**Book Import Begin** — writes, closed-world.

Begin a book import. Returns a one-time {reqid, url, method:POST}: POST your edited export bundle to the url (e.g. `curl -X POST <url> --data-binary @book.json`). The server runs a conflict-safe 3-way gate PER CHAPTER and returns a manifest: applied | skipped-unchanged | conflict | rejected-invalid | unmatched | untouched. Only chapters you actually changed are written; chapters changed on the server since your export are reported as conflicts (never clobbered); a malformed chapter is rejected atomically; nothing is ever deleted. Single-use, expires in 30 minutes.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the book to import into. |

## `book_isbn_assign`

**Book ISBN Assign** — writes, closed-world.

Assign a REAL, pool-allocated ISBN-13 to a published book. It identifies the DIGITAL edition: it becomes the book's colophon ISBN line and the EPUB's metadata, and Publifye is named as publisher of that edition. It does NOT put a barcode on the printed cover — the print cover's EAN-13 is built from the book's own print_isbn (book_set key=print_isbn), which is the PRINT edition's number and always the author's own; Publifye does not issue it. Your paid plan includes an ISBN for EACH of your books — there is no separate allowance to buy or to be granted. What governs is a rule: ONE ISBN PER BOOK (never a second), and as many ISBNs as your plan allows you books. It is DEFAULT-DENIED and multi-gated — a call must clear EVERY gate, and each refusal names the exact next step:
  • the feature must be enabled on this deployment (else reason isbn_unavailable — ask the operator);
  • you must be on the PAID Junifye plan (else isbn_requires_paid_plan — no exceptions, not even admin);
  • the book must exist, be YOURS, and be SUBSTANTIALLY COMPLETE — a cover, a title, an author, a description, a language, and at least 1500 words of body text. It does NOT have to be published, and it is NOT frozen by taking a number: you keep editing afterwards, and you can (and should) get the ISBN BEFORE putting the book on a shelf, because the retail gate requires one. Short of the bar it is refused with isbn_book_incomplete listing exactly what is missing. A book under an operator hold is refused with isbn_book_on_hold; a transcript is never eligible; and a book that already has an ISBN returns its existing one with assigned=false (one ISBN per book, permanently);
  • the book must have no OTHER publisher on record. Our ISBN prefix is Publifye's, so a book carrying it is published by Publifye: a book whose imprint already names a different publisher is refused with isbn_book_has_another_publisher (a work published by someone else cannot take our number);
  • you must have room: you may hold as many ISBNs as your plan allows you books, so a caller whose books are all numbered already is refused with isbn_book_cap_reached (check with isbn_status);
  • your author profile must be complete: a linked contact with a full legal name (else isbn_registration_info_missing — complete your contact profile);
  • and LAST, the book must LOOK FINISHED — no chapter empty of content, and the text must not read as a draft (placeholder/TODO, truncated mid-sentence). Refused with isbn_book_incomplete naming what to fix, or isbn_completeness_unavailable when the check itself cannot run, which means 'not yet' rather than 'go ahead'. An admin call bypasses this one check;
  • the AUTHOR must have ACCEPTED the publisher terms for this book (else isbn_acknowledgement_required, which returns them in full). YOU CANNOT GIVE THAT ACCEPTANCE — there is no argument to this tool that accepts on the author's behalf, deliberately: taking OUR ISBN means PUBLIFYE STANDS AS PUBLISHER of the work (Norwegian legal deposit attaches to Publifye, the ISBN can never be re-issued, the book can never expire) and the author warrants that this is a NEW work nobody else publishes. That is their statement about their book, and it is the evidence in any dispute, so it must be theirs. Show them the terms in full, then have THEM accept — by ticking the box on their book page in the junifye web UI, or by telling an operator, who records the acceptance they actually gave. Then call this tool again.
On success returns {isbn, assigned:true, isbns:{used,cap}}; the colophon line and the EPUB metadata pick the number up automatically, while the printed cover's barcode continues to follow print_isbn. Idempotent per book (a repeat call returns the same ISBN and never draws a second).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id (from book_create.id) of YOUR book to assign an ISBN to. Not the public UUID. The book does NOT need to be published first. |

## `book_list`

**Book List** — read-only, idempotent, closed-world.

List books with sort + pagination + visibility filter. PROVENANCE: every row carries `origin` — original = the owner's own authored work; transcript = captured EXTERNAL material (e.g. a YouTube talk copied in verbatim), i.e. SOMEONE ELSE'S WORDS. Handle a transcript doc as source material only: quote it WITH attribution, never present its text as the owner's writing, never mix it unattributed into an original book; it cannot be published. Filter by provenance with origin_filter (all|original|transcript, default all). Defaults: sort=updated_at_desc (newest first), limit=20, offset=0, visibility_filter=all, detail=lean. Paginated: limit is 1..100 (hard-capped at 100) — the whole library never comes back in one call; page with offset while has_more is true. Each row is LEAN by default (id, title, author, book_type, listed, owner_id, updated_at, url) so a big shelf stays light; pass detail=full for the complete book record, or book_get for one book's full detail + artifact URLs. Visibility: all = books you own + books SHARED WITH YOU as a guest editor + all public books; owned_only = only books you own; owned_or_guest = books you own OR are a guest editor on (your full editable shelf, no public); public_only = listed books from anyone. popularity_desc ranks most-downloaded first.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `detail` | string | no | Per-book detail. lean (DEFAULT) returns just the browse-and-pick fields (id, title, author, book_type, listed, owner_id, updated_at, url) — small enough that a… |
| `limit` | integer | no | Max results per page (1..100; higher values are capped to 100 — the response echoes the applied limit). Omit it, or pass 0, for the tool's default. A NEGATIVE … |
| `offset` | integer | no | 0-based pagination offset. Omit it for the first page. A NEGATIVE offset is rejected rather than treated as 0 — see `limit`. |
| `origin_filter` | string | no | Provenance filter: all (default) mixes both with each row TAGGED by origin; original = only the owner's authored works; transcript = only captured external mat… |
| `sort` | string | no |  |
| `visibility_filter` | string | no |  |

## `book_logo_upload_begin`

**Book Logo Upload Begin** — writes, closed-world.

Begin uploading a logo for ONE book's social share card (og:image) — it OVERRIDES your account/owner logo for this book only. Returns a one-time {reqid, url}: a PERSON OPENs the url (browser upload page) and picks a PNG; an AI POSTs the bytes — `curl -X POST <url> --data-binary @logo.png` (or `-F file=@logo.png`). PNG only (transparency preserved). On success it stores the logo for THIS book and refreshes this book's share card. Card fallback when unset: owner logo → author-initials monogram → Junifye flame. This is the SHARE-CARD logo, NOT the book COVER (book_cover_upload_begin, shown in the HTML reader) — the two never mix. Single-use, expires in 30 min; bytes stream over REST, never through MCP.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the book to set the share-card logo for. |

## `book_outline`

**Book Outline** — read-only, idempotent, closed-world.

Cheap PLANNING view of a book BEFORE reading content: each chapter's size + block count, plus the exact pages book_get_source will return. Returns {book_id, total_chapters, total_bytes, total_payload_bytes_estimate, limit_bytes, shape, chapters:[{index, chapter_id, title, block_count, source_bytes, payload_bytes_estimate, oversized}], pages:[{from_index, to_index, chapters, bytes, payload_bytes_estimate, oversized?}], page_count}. source_bytes is the prose; payload_bytes_estimate is roughly what that chapter costs as JSON in a book_get_source response of the same shape — the prose plus per-block envelope at shape=blocks, the prose alone at shape=flat — and that is the number limit_bytes caps. It is an ESTIMATE and runs LOW on text full of quotes, &, < or >: treat pages[] as a plan for how many calls a full read takes, and always follow next_from_index from the real book_get_source response, which enforces the limit exactly. Use it to know the whole book's size up front, pick chapters to pull (book_get_source chapter_ids=…), see how many book_get_source(from_index=…) calls a full read needs (one per page), and spot an oversized chapter (oversized:true → read it block-by-block, not via book_get_source). Pass the SAME shape you intend to give book_get_source or the page plan will not match: shape='flat' drops the per-block envelope, so more chapters fit per page. Read-only and SMALL — the response carries NO chapter text, so it is safe even for a huge book.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id. |
| `shape` | string | no | Plan for this book_get_source shape. 'blocks' (default) counts the per-block envelope; 'flat' counts the prose alone. Must match the shape you will actually ca… |

## `book_publish_to_store`

**Book Publish To Store** — writes, closed-world.

Put this book ON THE SHELF — register it for sale on the storefront and upload the EPUB a buyer downloads. Call it again after any edit: it is an idempotent UPDATE, not a second release. One work has one ISBN, the ISBN is the product's identity, and the same product is updated in place forever.

REQUIRES the book to be opted in (book_set key=store_enabled value=true), which is itself gated on the operator approving the author, the book clearing store_readiness, and the AUTHOR accepting the retail terms. The acceptance is re-checked HERE against the current text: if the book was edited after being opted in, publishing is refused until the author accepts again — otherwise buyers would receive a version nobody agreed to sell.

The EPUB is rendered FRESH as part of this call, so what goes on the shelf is always the current text. Renders take time; a large book can take a while.

Returns {book_id, sku, storefront, object_key, published:true, warnings}.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `allow_shrink` | boolean | no | Publish even though the new EPUB is far smaller than the one on sale. The size floor exists because a half-finished render still produces a VALID, small EPUB, … |
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the public uuid). |
| `prices` | object | no | OPTIONAL per-currency price in MINOR units keyed by lowercase ISO 4217, e.g. {"nok":8900,"eur":799}. A storefront lists a product in a country ONLY if it holds… |

## `book_questions`

**Book Questions** — read-only, idempotent, closed-world.

List every question this book answers (across all its chapters + any whole-book answers). Use it to see a book's discovery footprint.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | An 'idb...' id or a public UUID. |

## `book_replace`

**Book Replace** — writes, closed-world.

Find-and-replace a LITERAL text string across EVERY chapter of a book — fix a recurring typo, rename a term, update a date. Case-sensitive, literal (not regex). Operates on each chapter's source text and re-validates: a chapter whose result would be malformed is REJECTED (atomic — that chapter is left unchanged), never silently corrupted. Returns a per-chapter manifest: applied (with count) | skipped-unchanged | rejected-invalid | not-editable. Each changed chapter is checksum-gated and creates a new revertable version (see chapter_history/chapter_revert). By DEFAULT it matches WHOLE WORDS ONLY (word boundaries): find="Gen" hits "Gen" but NEVER "Genesis" or any substring -- the safe way to rename, thinking around words not blind characters (set whole_word=false for a raw substring replace). ALWAYS preview first: preview=true is a DRY RUN that returns per-chapter match counts and changes NOTHING; then re-run without preview to apply.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |
| `find` | string | yes | Exact literal text to find. |
| `preview` | boolean | no | Dry run: report per-chapter match counts WITHOUT changing anything (default false). Always preview a rename first. |
| `replace` | string | yes | Replacement text (may be empty to delete the word). |
| `whole_word` | boolean | no | Match whole words only via word boundaries (default TRUE -- the safe rename behaviour; false = raw substring replace). |

## `book_restore`

**Book Restore** — writes, closed-world.

Restore a soft-deleted book within its trash window (30 days) — re-adds it to all listings and makes its URLs live again. DO NOT call this on your own initiative: restoring a deleted book is the human's decision. If an edit fails because a book is deleted, TELL the user and call book_restore ONLY when they explicitly ask you to. Same access rule as delete: a public (listed) book can only be restored by an admin; a private book by its owner (or admin). After the window the book is purged and cannot be restored.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the deleted book. |

## `book_retract_from_store`

**Book Retract From Store** — writes, closed-world.

Take this book OFF the shelf. It is unlinked from the storefront and marked not-purchasable, which removes it from the shop's catalogue and from its Google product feed.

WHAT IT DOES NOT DO, deliberately: it does not delete the EPUB, and it does not reach into anyone's purchases. A reader who bought the book keeps it and can still re-download it. Retracting stops NEW sales; it is not a recall, and the bytes are a separate, admin-confirmed decision.

Also turns store_enabled off, so the book does not sit opted-in while off the shelf. Reversible: publish it again with book_publish_to_store.

Returns {book_id, sku, storefront, retracted:true}.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the book to take off sale. |

## `book_revision_close`

**Book Revision Close** — writes, closed-world.

Close a revision window on YOUR published book — refreeze its text as the new canonical version (frozen=1, lock_reason 'revision_closed'). Call this when you've finished the edits you opened with book_revision_open. Idempotent: if the book is already frozen it's a no-op. Only for a LISTED book you own. Returns {book_id, frozen:true, lock_reason}.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id of YOUR listed book (NOT the public uuid). |

## `book_revision_open`

**Book Revision Open** — writes, closed-world.

Open a REVISION WINDOW on YOUR published book so you can edit its (otherwise canonical, frozen) text. Publishing freezes the text as canonical; this lifts that freeze temporarily. You get up to 10 self-service revision windows per book — each open consumes one. When done editing, call book_revision_close to refreeze the new canonical text. Only works on a LISTED book you own that is currently frozen as 'published' (or 'revision_closed' from a previous cycle). Past the 10-window limit you'll be refused (reason revision_limit_reached) and further revisions need an operator (admin book_unfreeze). Returns {book_id, revisions_used, revisions_left, frozen:false}.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id of YOUR listed book (NOT the public uuid). |

## `book_search`

**Book Search** — read-only, idempotent, closed-world.

Search visible books. Matches title + author always; pass content=true to also scan body text (a disk scan — slower, use when you need to find a book by something inside it). CONTENT SEARCH IS NOT EXHAUSTIVE, and this is the single most important thing to know about it: it answers WHETHER a book mentions something and names ONE chapter per book — the first that matched — with no block granularity. It is the right tool for "which of my books talk about X" and the WRONG one for "where does X occur": for that use book_grep(book_id, pattern), which returns every occurrence with its block_id, the handle you actually edit through. Reading a single matched_in chapter as the only place a term appears is how a revision pass silently misses most of its work. scope picks which books: local (your own + books shared with you as a guest editor), public (listed books from anyone), or all (default = local + public). Paginated (limit 1..100 default 20, offset) and sortable (relevance|updated|title). Each hit is LEAN by default (browse fields incl. `origin`); pass detail=full for the complete record. TWO DIFFERENT AXES, never conflate them: (1) `origin` = PROVENANCE, whose words these are — origin=original is the owner's authored work; origin=transcript is captured EXTERNAL material (someone else's words, e.g. a YouTube talk) — treat transcript hits as attributable SOURCES, never as the owner's writing, never publishable. (2) `match_scope` = whose shelf the hit came off — match_scope=local means YOU own the book; match_scope=public means ANOTHER owner does (it reached you either as a listed public book or as one shared with you as a guest editor). A guest-editable book you do not own is therefore match_scope=public even under scope=local. Both keys are on every hit, in lean and in detail=full. The response-level `scope` echoes the scope ARGUMENT you searched under, and `counts` {local, public} counts match_scope across ALL matches (not just this page) — neither says anything about provenance. Matching is case-, diacritic- and accent-insensitive (folded substring: 'dap' finds 'dåp', 'jose' finds 'José', unpointed Hebrew matches pointed text) — still plain substring, never fuzzy. Every hit carries match_field (title|author|content); a content hit also carries matched_in {chapter_id, chapter_title, snippet} — chapter_id is the reader/deep-link anchor, so you can jump straight to the match.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content` | boolean | no | also search inside book body text (slower disk scan) |
| `detail` | string | no | Per-hit detail: lean (default, browse fields) or full (complete record). |
| `language` | string | no | optional ISO code filter, e.g. en, fa, ar |
| `limit` | integer | no | Max results per page (1..100; higher values are capped to 100 — the response echoes the applied limit). Omit it, or pass 0, for the tool's default. A NEGATIVE … |
| `offset` | integer | no | 0-based pagination offset. Omit it for the first page. A NEGATIVE offset is rejected rather than treated as 0 — see `limit`. |
| `q` | string | yes | The search text. Matching is case-, diacritic- and accent-insensitive substring ('dap' finds 'dåp') — multi-word queries must match contiguously. |
| `scope` | string | no | local=books you own or are a guest editor on, public=listed books from anyone, all=both (default) |
| `sort` | string | no |  |

## `book_set`

**Book Set** — writes, closed-world.

Atomically set ONE book field by key. Three categories of keys are accepted:

--- METADATA KEYS ---
  title (1..60 — the cover headline, keep it short), subtitle (0..140 — optional descriptive line under the title on the cover/title page), author (0..500), author_bio (0..500 — opt-in paragraph printed in italic under the title-page author line; NEVER auto-populate, set only when the author explicitly asks), slug, book_type (book|document — book = cover+TOC+chapters, document = plain title + flowing sections), language (closed enum: Supported language codes: af (Afrikaans), am (Amharic), ar (Arabic, RTL), bn (Bengali), cs (Czech), da (Danish), de (German), el (Greek), en (English, default), es (Spanish), fa (Farsi (Persian), RTL), fil (Filipino), fr (French), he (Hebrew, RTL), hi (Hindi), hu (Hungarian), hy (Armenian), id (Indonesian), is (Icelandic), it (Italian), ja (Japanese), kn (Kannada), ko (Korean), nb (Norwegian Bokmål), nl (Dutch), nn (Norwegian Nynorsk), pa (Punjabi), pl (Polish), pt (Portuguese), ro (Romanian), ru (Russian), sv (Swedish), sw (Swahili), ta (Tamil), te (Telugu), th (Thai), tr (Turkish), uk (Ukrainian), ur (Urdu, RTL), vi (Vietnamese), zh (Chinese). Empty = en. RTL codes flip page numbers + swap body font), cover_url, description (0..2000 — the WEB/SEO summary), back_cover_text (0..1200 — the PRINT back-cover blurb; separate from description on purpose, because a summary written for search engines makes a poor back cover. Set it and the back panel typesets it IN FULL, keeping blank-line paragraph breaks; leave it empty and the panel falls back to an excerpt of description), isbn (0..32 — a valid ISBN prints a real EAN-13 on the back panel; without one the book cannot be sold through trade channels).

COLOPHON:
  darash_credit (auto | on | off, default auto) — whether the colophon credits Darash as the Scripture and original-language source. AUTO means it follows ACTUAL USAGE, re-checked on every render: the credit appears only where the text carries Strong's spans ([h:H…] / [g:G…]), which is what Darash produces and nobody types by hand. A :bible block does NOT count — a verse may have been typed in from any Bible, and crediting Darash for that would be false. Most books use no Darash at all and are never credited. Set on/off to override.
  The junifye line in the colophon is NOT removable — it is a condition of using the service, and it is a colophon in the ordinary sense (how the book was made), not an advertisement.

PRINT EDITIONS — junifye issues ISBNs for DIGITAL editions only; a printed edition is yours:
  imprint (0..120) — the PUBLISHER NAME printed on the spine and back cover. Defaults to the author. This is not decoration: legal deposit attaches to the publisher named on the object, so whoever appears here is the publisher of that printed book. "Publifye"/"Junifye" are RESERVED and rejected — a Publifye imprint in print is available by arrangement with an operator, never self-served.
  print_isbn (0..32) — the PRINT edition's own ISBN, which you supply. Print and digital editions need DIFFERENT ISBNs, so the wrap cover barcodes THIS one and never the digital `isbn`. A valid number prints a real EAN-13 bottom-right; leave it empty and no barcode is drawn. Checksum-validated, because a wrong number becomes a barcode that scans to somebody else's book.
  Printing anything creates YOUR legal-deposit duty: three copies to Nasjonalbiblioteket, Henrik Ibsens gate 110, Oslo, by publication date. We file the DIGITAL deposit for you; the printed one is yours.

SELLING A BOOK — these five work together:
  access (free | paid_download | gated, default free) — what a visitor may DO with the book:
      free          read online and download, no charge.
      paid_download PUBLIC AND EARNING — the reader stays OPEN and the files (EPUB/PDF) are sold. The message goes out freely and whoever wants it on their shelf pays. This is the shape Publifye's own catalogue uses.
      gated         the reader is withheld too: /<slug> serves a LANDING page instead, and the EPUB, PDF, TXT and TeX are all withheld with it. This is the ONLY state in which a book may be sold on Apple Books, because it is the only one where no free copy of the file exists. Leaving it (back to free or paid_download) is refused while apple_enabled is on or the book has been delivered.
    The last two TRUMP listed — the one thing that can gate a book already listed free, since listed is one-way and cannot be turned off. Set deliberately.
  line_spacing (1.0..2.0; UNSET = memoir \OnehalfSpacing, which is ~1.25 and NOT 1.5 — TeX's own baseline is already ~1.2) — body LEADING: the vertical gap between lines. It does NOT change type size, text block or margins; it changes how many lines fit in the SAME block, so it moves the page count and therefore the SPINE WIDTH. Set BELOW ~1.25 to tighten and save pages (1.15 is still comfortable); above it to open the page up. Do not guess the effect — re-run print_set and read the page count back. Re-run print_set regardless: the cover wrap is computed from the page count.
  buy_url (http/https, 0..500) — where the landing page's buy action points. junifye never takes payment; this links to the storefront listing. A payable book with no buy_url shows the landing page with nothing to click, so set both or neither.
  landing_cover_url (http/https, 0..500) — OVERRIDE the landing page's image. Leave empty to use the book's own cover, which is almost always right; override only when the print cover's trim and bleed decisions make a poor web hero.
  landing_theme (closed enum: house | ivory | ink, empty = house) — house is the warm default matching the reader, ivory is paper-pale and quiet, ink is a dark ground for a cover that carries its own colour. Deliberately a small set, not free styling: bounded choices keep a catalogue looking like one publisher.
  link_author_page (bool, DEFAULT TRUE) — bridges the landing page and the author page /a/<handle> in BOTH directions. Set false to let a book stand alone.

The landing page composes what the book already has — cover, title, subtitle, author, page count and back_cover_text as the blurb — so writing a good back_cover_text improves the shop page and the printed cover at once.
  origin (original|transcript) — PROVENANCE: original = the owner's own authored work (default); transcript = captured EXTERNAL material (e.g. a YouTube talk), someone else's words. A transcript doc is SOURCE material: quote WITH attribution, never present as the owner's writing, and it can NEVER be published (listed=true / publish_request are rejected while origin=transcript — flipping origin back to original is the deliberate, audited override). origin_url (http(s) source link, e.g. the YouTube video), origin_label (short attribution like 'YouTube — <channel>', max 120).

--- RENDER-SETTING KEYS ---
  ► FOR PHYSICAL PRINT, prefer the dedicated print_set tool — print_set(book_id, printer="lulu_6x9") sets page_size + bleed + print_ready in one atomic call AND renders a press-ready interior, then print_get reads its status. The raw keys below are the low-level escape hatch.
  page_size — a named size (A3|A4|A5|A6|B5|Letter|Legal) OR, when print_ready=1, ANY trim as 'WxH' in inches (e.g. 6x9, 5.5x8.5) or millimetres (e.g. 148x210mm). Set it to match your printer. Examples: Lulu 6×9 US trade paperback → page_size=6x9; Drukātava (EU short-run) A5 → page_size=A5 or 148x210mm. orientation (portrait|landscape), body_font_size (10..16).
  MARGINS (all millimetres, fractional allowed, range 10..80; 0 = use preset): margins_preset (narrow|normal|wide), margin_top_mm, margin_bottom_mm, margin_inner_mm (binding/gutter side — in print_ready it overrides the auto page-count gutter when set), margin_outer_mm.
  bleed_mm (print trim bleed added to every edge in print_ready mode; 0 = default 3 mm = Lulu/KDP, set 5 for Drukātava and most EU printers; range 0..10).
  print_ready (1|0 — flip to TRUE before sending to a printer (Lulu/IngramSpark/KDP/Drukātava): switches to ASYMMETRIC inner/outer margins for the binding gutter, CMYK K-only black body colour, and exact trim geometry + bleed. Required to use a WxH page_size). no_toc (1|0 — TOC is auto-included for books with 5+ chapters; small books (≤4) skip it as a heuristic. Set no_toc=1 to suppress TOC even on large books. Documents (book_type=document) never have a TOC regardless.). continuous_chapters (1|0 — book mode only, PDF layout. 1 = (a) chapters FLOW continuously instead of each starting on a new page → fewer pages, saves paper/print cost, AND (b) the chapter head becomes a tight one-line, LANGUAGE-AGNOSTIC "N · Title" — the localized "Chapter"/"Kapittel" word is dropped, leaving number · title on a single line. Chapter numbering and the TOC entry are kept. Default 0 = each chapter opens a NEW PAGE with the classic two-line "Chapter N" / Title head. document book_type already flows regardless.). chapter_flow (auto|on|off — the tri-state that SUPERSEDES continuous_chapters. auto (DEFAULT): small books (≤5 chapters) FLOW + get the one-line head automatically; bigger books keep the classic new-page two-line head. on: always flow. off: always new-page (override the small-book default). Authors set this to opt a small book out, or a big book in.). Chapter layout otherwise — title page, chapter numbering, running heads — is controlled by book_type (book vs document).

APPLE BOOKS — off unless you turn it on:
  cover_logo (bool, DEFAULT TRUE) — draw the imprint mark at the foot of the GENERATED cover. On by default because a publisher's mark belongs on a book it published; turn it OFF for an author publishing under their own name, where someone else's mark on the cover is simply wrong. Only affects covers junifye composes — a finished cover uploaded by the author is never touched. Takes effect on the next compose, which a title or author change triggers automatically.
  apple_enabled (bool, DEFAULT FALSE) — opt this book in to Apple Books delivery. Delivering to a live retail store is outward-facing and not cleanly reversible, so it is something you switch ON deliberately; it never happens because a default was left alone. Setting it true requires base_price_usd to already be set, AND access=gated: a book junifye serves free cannot also be sold in a shop, because the buyer would be paying for what the next visitor downloads for nothing. access=paid_download does NOT satisfy this yet — it declares the files are sold, but there is no checkout, so junifye still serves them free to everyone. Once a book has actually been DELIVERED, listed=true is refused forever: a delivered listing is not something junifye can retract.
  base_price_usd (4.99..28.00 for an author; an operator may go wider) — the ONE price you choose, in US dollars. It is NOT the price a reader in Norway or India pays: apple-service expands this single number into Apple's 51 territories, adjusting for local buying power and current currency rates, so a book costs less where money is worth less. You set one number; nobody sets fifty-one tiers by hand. Use apple_price_preview on apple-service to see exactly what it becomes everywhere before delivering.

RETAIL SHELF — off unless you turn it on:
  store_enabled (bool, DEFAULT FALSE) — offer this book FOR SALE on the junifye retail shelf. Turning it ON is gated three ways and the refusal names whichever one stopped you: (1) an operator must have approved the AUTHOR to sell (admin_retail_approve); (2) the book must clear its checklist — ISBN, price, cover, title/author/description/language, and access=gated; (3) the AUTHOR must have accepted the retail terms for THIS version of the text, which they do themselves on their book page — there is NO tool at any level that lets you accept for them (see retail_terms). Call store_readiness for the whole picture in one answer.
  Editing the book withdraws the acceptance, because what the author agreed to sell was a particular text; they are asked again before the new version sells.
  Turning it OFF is NEVER refused — a book must never be trapped on sale by a gate that has since stopped passing.

--- VISIBILITY KEY ---
  listed ('true' / 'false'). false (default): URL works for anyone with the UUID, book hidden from public listings, writes are owner-only. true: URL works for anyone AND the book appears in book_search + book_list(visibility_filter=public_only).

  WARNING — the `listed` key is the PUBLISH gate:
    - Setting listed=true SUBMITS the book for publication review — it does
      NOT publish instantly. The book's vet_state becomes 'pending' and an
      admin must approve it; on approval it goes public (appears in
      book_search + book_list public_only). This is the SAME as calling
      publish_request(book_id). Track the verdict (and any rejection reason)
      with vet_status. (Exception: an ADMIN caller's listed=true publishes
      IMMEDIATELY and is never queued — the response carries
      reviewed_by='admin_self' when the admin owns the book (a recorded
      SELF-approval: nobody else read it) or 'admin_override' when they
      do not. Skipping the queue does NOT skip the guards: an
      origin=transcript book is refused for an admin too.)
    - Once a book is public, that is IRREVERSIBLE for the OWNER — you cannot
      set listed back to false (the server returns visibility_locked). This
      is by design: no back-and-forth publishing. (Exception: an ADMIN
      caller's listed=false UNPUBLISHES immediately and without review —
      removes the book from the public library + search, drops its slug,
      revokes wiki editing, returns it to private. Already-downloaded
      copies / shared links / search-indexed pages are NOT recalled.)
    - A listed book is READ-ONLY to others — only YOU (the owner) can edit it.
      To allow group/wiki editing you must ALSO set publicly_editable=true
      (see the COLLABORATION KEY below).
    - A book under an EDITORIAL freeze (lock_reason=admin, or the
      30-day inactivity lock_reason=auto) cannot be published by ANY
      route — owner submit, admin publish, or vet approve all refuse
      with publication_frozen. Publishing never lifts a freeze:
      book_unfreeze must lift it first (auto = owner or admin; admin =
      admin only).
    - Confirm with the human before submitting.

--- COLLABORATION KEY ---
  publicly_editable ('true' / 'false'). Requires listed=true first. false (default): only the owner may edit a listed book. true: ANY authenticated user may edit it (group/wiki mode). Owner-settable and reversible. Admin can hard-lock a book against all edits via book_freeze (see admin tools).

--- GLOSSARY / DICTIONARY KEYS ---
  connected_dict — connect a CENTRAL lexifye dictionary so its terms render as this book's Glossary appendix. Pass a lexifye dict id (idy…) OR its uuid to connect (validated against lexifye — it must exist and be readable; any dict readable by id may be connected, ownership is not required), or the literal 'none' to disconnect. At compile the in-scope terms are SNAPSHOTTED into the book (frozen artifacts stay frozen; a recompile re-pulls the current dict). A book-local glossary term (dict_add) always WINS over an imported one on a name collision.
  glossary_scope (full | used | used_recursive) — which of the connected dict's entries land in the appendix. used_recursive (DEFAULT): terms occurring in the book text PLUS the closure of terms those definitions reference. used: only terms occurring in the book text. full: every entry in the dict. Ignored when no dict is connected.
  glossary_link (first | all | off) — how a glossary term's occurrences in the BODY text are auto-linked to its Glossary-appendix entry. first (DEFAULT): link only the FIRST occurrence of each term per chapter (read-friendly). all: link EVERY occurrence (dense reference works). off: no in-text auto-links at all (the appendix still renders, and a reference carried in the content itself — \gref{} — still resolves to its own entry; see source_syntax). Applies to book/HTML/EPUB; print never shows a link marker (the appendix is the print reference) regardless of this setting.

--- LIFECYCLE KEY ---
  history_limit (10..360, default 120) — how many chapter versions this book keeps for chapter_history / chapter_revert. Raise it for a book under heavy revision; 360 is the hard ceiling for every book. LOWERING IT TAKES EFFECT AT ONCE: the versions beyond the new depth are deleted on the spot, not left to age out, so a book never reports a shallower trail than it is holding. Undo depth is storage on every chapter, which is why the default is well under the ceiling.
  permanent ('1' / '0'). Books are garbage-collected after a window of inactivity by default (every read refreshes the clock, so books in active use never expire). Set permanent=1 to pin this book under the owner's account permanently — the retention sweeper skips it regardless of age. '0' restores normal expiry.

value accepts a string, boolean, or number — native true/false and numbers are coerced (e.g. value:true, value:12, value:"A5" all work; '1'/'0' for render booleans + permanent, 'true'/'false' for listed).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |
| `key` | string | yes |  |
| `value` | ['string', 'boolean', 'number', 'integer'] | yes | A string, boolean, or number — booleans/numbers are coerced (true→"true", 12→"12"). |

## `book_set_buy_links`

**Book Set Buy Links** — writes, closed-world.

Set WHERE a reader can buy this book — every channel, not just ours. Replaces the WHOLE list in one call: to add, resend the existing links plus the new one; to remove, omit it; to reorder, change the order numbers. Sending an empty list clears them all.

This is deliberately one tool rather than add/update/remove, so there is no index arithmetic to get wrong and reordering is free.

WHY IT MATTERS: junifye does not distribute. The author sells through Amazon, Apple, Kobo, a local bookshop, our store — wherever they like — and this list is what makes the book's landing page the single address that points to all of them. It is also what the QR code printed on the physical back cover resolves to, so these links outlive any one retailer.

EACH LINK: label (1..40, free-form — "Amazon", "Apple Books", "Kjøp direkte"; it is the button text, so name the SHOP, not the action), url (https only, max 500 — http is rejected because a printed QR code cannot be recalled), order (1-based display position; gaps and ties are fine and get renumbered densely, so you may leave it 0 and rely on the order you send).

Duplicate labels are rejected. Max 36 links — a runaway guard, not a target; most books list a handful.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the public uuid). |
| `links` | array | yes | The COMPLETE list, replacing whatever is stored. Empty array clears all buy links. |

## `book_set_translation_of`

**Book Set Translation Of** — writes, closed-world.

Link a book as a translation/edition of an ORIGINAL book so the two appear as language editions of one title — a language picker on the reader and on the library card lets readers switch between them. book_get then returns the full editions[] list.
Pass original_book_id="" to DETACH (make this book a standalone original again).
Rules (a flat star: one original, N editions): a book cannot be a translation of itself; you cannot point an edition at an original that is ITSELF a translation; a book that already HAS its own editions cannot become a translation. Owner-only; reversible.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the edition (the translation) to link. |
| `original_book_id` | string | no | The 'idb...' id of the original book this is a translation of. Pass an empty string to detach. |

## `book_unfreeze`

**Book Unfreeze** — writes, closed-world.

Lift a book freeze. An auto-lock (a public group-editable book idle past 30 days, lock_reason=auto) is reopenable by the book's OWNER or an admin, and reopening restarts the 30-day window. An admin HOLD (lock_reason=admin, see book_freeze) is admin-only — lifting it also restores the book's normal lifecycle: it becomes deletable again and the automatic reapers resume. Read access is never affected by a freeze.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the book to unfreeze. |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
