# Covers, images and figures

**Covers, logos, figures and uploads.** 22 Junifye MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://junifye.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`author_page_get`](#author_page_get) | Get YOUR public author-page state: display name (page_name override, else your directory… |
| [`author_page_set`](#author_page_set) | Set YOUR public author-page state: `bio` (max 2000 chars — the blurb shown on /a/<handle>),… |
| [`authors_list`](#authors_list) | List every author whose PUBLIC page is LIVE (they opted in AND have at least one listed book)… |
| [`description_status`](#description_status) | Check the GENERATED book description job for one of your books |
| [`dict_add`](#dict_add) | Create a new Dictionary entry |
| [`dict_delete`](#dict_delete) | Delete a Dictionary entry |
| [`dict_get`](#dict_get) | Get a Dictionary entry |
| [`dict_list`](#dict_list) | List all Dictionary entries for a book |
| [`dict_reorder`](#dict_reorder) | Set the manual sequence for all Dictionary entries |
| [`dict_update`](#dict_update) | Replace a Dictionary entry's body |
| [`figure_upload_begin`](#figure_upload_begin) | Begin a VECTOR FIGURE (SVG) upload placed in a specific chapter |
| [`house_style`](#house_style) | THE one-stop authoring guide — read this ONCE before writing or vetting a book and you have… |
| [`image_upload_begin`](#image_upload_begin) | Begin an image upload that will be placed in a specific chapter |
| [`indexnow_run`](#indexnow_run) | ADMIN |
| [`indexnow_status`](#indexnow_status) | ADMIN |
| [`owner_logo_upload_begin`](#owner_logo_upload_begin) | Begin uploading YOUR brand logo — the image shown on the social share card (og:image) of every… |
| [`rotate_share_links`](#rotate_share_links) | ADMIN |
| [`source_syntax`](#source_syntax) | Return the grammar of the round-trippable block source used by block_get_source /… |
| [`sync_resolve`](#sync_resolve) | Mark a chapter (or the whole book) reconciled across all language editions — i.e |
| [`sync_status`](#sync_status) | Cross-edition drift report for a TRANSLATED book: which chapters were edited in one language… |
| [`user_contact_get`](#user_contact_get) | Get the CALLER's own contact info from pubcontacts (name, email, phone, address, bio, etc.) |
| [`user_contact_set_field`](#user_contact_set_field) | Update ONE field on the CALLER's own contact (name, phone, address, website, bio, etc.) |

---

## `author_page_get`

**Author Page Get** — read-only, idempotent, closed-world.

Get YOUR public author-page state: display name (page_name override, else your directory name), bio, handle, the public URL (/a/<handle>), whether the page is LIVE, the count of listed books, and whether an author image is set. Also returns `state` — 'live' or 'preview' — with `state_detail` saying why: an author page is PREVIEW until you switch it on AND have at least one listed book. A preview 404s for the world but renders for YOU at the same URL when signed in as that author, so you never have to publish it to see how it looks. Derived from the authenticated caller — no parameter targets another user. Set the text with author_page_set; set the image with owner_logo_upload_begin.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

## `author_page_set`

**Author Page Set** — writes, closed-world.

Set YOUR public author-page state: `bio` (max 2000 chars — the blurb shown on /a/<handle>), `page_name` (max 120 chars — a display-name override, e.g. a church or organisation name; the page falls back to your directory name when empty), and/or `public`. **NEVER set `public` yourself unless the author has explicitly asked to go live — going public is the AUTHOR'S decision, never one you infer from them tidying up a bio, a name or an image.** Preview is a perfectly good resting state, not an unfinished one; leaving a page in preview is a correct outcome. What `public:true` actually does: /a/<handle> becomes readable by ANYONE with the link, it enters the public sitemap so search engines discover and index it over time, and it exposes the bio, the display name, the author image and a card for EVERY listed book. `public:false` returns it to PREVIEW — it 404s for the world and leaves the sitemap, while still rendering for the author themselves at the same URL. The switch is reversible and loses nothing, BUT a page that has been live can already have been crawled: un-publishing removes it going forward, it does not retract what a search engine has already cached. That asymmetry is why the first switch to live is the author's to make. Only the fields you pass change; pass an empty string to CLEAR a text field. An over-long value is REJECTED with the limit, never truncated. To set the author image, use owner_logo_upload_begin instead. Returns the updated author-page state.

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
| `bio` | string | no | Author-page bio, max 2000 chars. Empty string clears it. |
| `page_name` | string | no | Display-name override (e.g. an organisation/church name), max 120 chars. Empty string clears it. |
| `public` | boolean | no | Author pages are opt-in (hidden by default). true publishes /a/<handle> — world-readable and added to the sitemap for search engines; false returns it to previ… |

## `authors_list`

**Authors List** — read-only, idempotent, closed-world.

List every author whose PUBLIC page is LIVE (they opted in AND have at least one listed book) — the same set the public /authors index shows. Returns each author's `handle`, `name` (display name), `listed_books` count, `url` (/a/<handle>), and `has_logo`, sorted by name. PAGED: `total` is every live author, `count` is this page, and `has_more` says whether to fetch another with offset. This is a READ over ALL authors; to view or manage YOUR OWN page use author_page_get / author_page_set.

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
| `limit` | integer | no | Max rows to return (default 50, max 200). Omit it, or pass 0, for the default. A NEGATIVE limit is rejected, not clamped. |
| `offset` | integer | no | 0-based row offset for the next page. Omit for the first page; pass the previous offset+limit while has_more is true. A NEGATIVE offset is rejected. |

## `description_status`

**Description Status** — read-only, idempotent, closed-world.

Check the GENERATED book description job for one of your books. A description is written automatically — from the book's OWN chapters, one model pass per chapter then one to compose — when a book is published with an EMPTY description; an author's own description is never overwritten, and a book that already has one starts no job. Returns state ('running', 'done' or 'failed'), how many chapters have been summarised so far, a rough eta_seconds while it runs, and on success the generated `description` (already saved on the book, and editable like any other field — see book_set). Also returns `classify_en`: the SAME content in English, never shown to a reader, produced for subject classification because BISAC headings are English and feeding them a Norwegian description mis-files the book. Returns state 'none' when no job has ever run for this book.

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
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid in public URLs). |

## `dict_add`

**Dict Add** — writes, closed-world.

Create a new Dictionary entry. body is plain-text/markdown — split on blank lines, each chunk becomes a paragraph in the entry definition. transliteration is optional. Term normalisation is per-script (Latin case-insensitive; Hebrew NFC+strip-nikud; Greek NFC+case-insensitive+strip-marks; Strong's H/G+strip-leading-zeros; numbers numeric value). Duplicates rejected with hint.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `body` | string | yes | Definition text. Blank-line-separated paragraphs become separate paragraph blocks. |
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |
| `term` | string | yes | The dictionary headword exactly as stored (see dict_list). |
| `transliteration` | string | no | Optional Latin-script transliteration shown beside the term. |

## `dict_delete`

**Dict Delete** — writes, closed-world.

Delete a Dictionary entry. term addresses ONE entry by the entry's own term as the glossary spells it, or by its stored key (normalized_term, from dict_list). A term that folds onto SEVERAL entries (two vowel/accent-distinct words sharing one lookup form) is REFUSED with both candidates named — NOTHING is deleted; re-issue naming one of them. Also rejected if any chapter still references the entry via \gref{} (error includes chapter list).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |
| `term` | string | yes | The entry's own term as the glossary spells it, or its stored key (normalized_term, from dict_list). A form that folds onto two entries is refused, never guess… |

## `dict_get`

**Dict Get** — read-only, idempotent, closed-world.

Get a Dictionary entry. body is the markdown reconstructed from the entry's stored blocks (paragraphs joined by blank lines). used_in lists the chapter ids whose text references this term via \gref{}. ADDRESSING (identical for dict_get / dict_update / dict_delete / dict_reorder and for \gref{}): term names ONE entry by the entry's own term, by its stored key (normalized_term, e.g. 'חסד-2' when two vowel-distinct words share a lookup form), or by the plain folded form when only one entry folds there. If the term folds onto SEVERAL entries the call is REFUSED (reason dict_term_ambiguous) naming each candidate and the exact term= that addresses it — no entry is picked for you, and nothing is read, changed or deleted. The stored key is an ADDRESS: the page always shows the entry's own term.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |
| `term` | string | yes | The entry's own term as the glossary spells it, or its stored key (normalized_term, from dict_list). A form that folds onto two entries is refused, never guess… |

## `dict_list`

**Dict List** — read-only, idempotent, closed-world.

List all Dictionary entries for a book. sort=alpha (default) | order | recent. Each entry carries provenance: source_dict_id is "" for a book-local authored term (via dict_add) and "idy…" for a term snapshotted from that connected Lexifye dictionary; source_entry_sha is the exact Lexifye definition checksum the snapshot was built from — so a caller can tell local from imported and pin exact provenance (see book_get.glossary_import for the dict/version/scope that built the snapshot). normalized_term is the entry's STORED KEY — the exact address for \gref{} when two vowel/accent-distinct words fold to one lookup form (חֵסֵד → 'חסד', חָסַד → 'חסד-2'); the page always renders the entry's own term, never the key. If any reference in the book's text fails to resolve, unresolved_grefs lists it with the fix.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |
| `limit` | integer | no | Max rows to return (default 50, max 200). Omit it, or pass 0, for the default. A NEGATIVE limit is rejected, not clamped. |
| `offset` | integer | no | 0-based row offset for the next page. Omit for the first page; pass the previous offset+limit while has_more is true. A NEGATIVE offset is rejected. |
| `sort` | string | no |  |

## `dict_reorder`

**Dict Reorder** — writes, closed-world.

Set the manual sequence for all Dictionary entries. terms MUST contain EVERY term in the book exactly once, each addressed by the entry's own term or by its stored key (normalized_term, from dict_list). A term that folds onto several entries is REFUSED naming them; nothing is reordered.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |
| `terms` | array | yes | The FULL list of headwords in the desired order — every existing term exactly once. |

## `dict_update`

**Dict Update** — writes, closed-world.

Replace a Dictionary entry's body. body is markdown; paragraphs are blank-line separated. The entire definition is replaced — there is no per-paragraph diff. term addresses ONE entry by the entry's own term or by its stored key (normalized_term, from dict_list); a form that folds onto two vowel/accent-distinct entries is REFUSED (dict_term_ambiguous) naming both, so an update can never land on the wrong word.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `body` | string | yes | The entry's body text (markdown-lite, same grammar as source_syntax prose). |
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |
| `term` | string | yes | The entry's own term as the glossary spells it, or its stored key (normalized_term, from dict_list). A form that folds onto two entries is refused, never guess… |

## `figure_upload_begin`

**Figure Upload Begin** — writes, closed-world.

Begin a VECTOR FIGURE (SVG) upload placed in a specific chapter. Like image_upload_begin but for an SVG diagram/line-art that renders as live inline vector in the HTML reader + EPUB and a crisp raster in the PDF. Returns a one-time {reqid, url}: a PERSON OPENs the url (browser upload page) or an AI POSTs the bytes — `curl -X POST <url> -F file=@figure.svg` (or `--data-binary @figure.svg`). The server SANITIZES the SVG (strips <script>, event handlers, external references, DOCTYPE) and REJECTS — never silently — anything the pure-Go print rasterizer can't reproduce faithfully: live <text> (convert type to outlines first), gradients, filters, masks, patterns. Keep to paths, shapes, strokes, dashes, solid fills, opacity so it renders IDENTICALLY in all three outputs. On success it stores the figure, auto-appends a :figure block to the chapter, and returns the figure_id + a reader link. NOTHING is added unless the upload succeeds. Single-use, expires in 30 min; bytes stream over REST, never through MCP.

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
| `book_id` | string | yes | The 'idb...' id of the book. |
| `chapter_id` | string | yes | The 'idc...' chapter the figure will be appended to on a successful upload. |

## `house_style`

**House Style** — read-only, idempotent, closed-world.

THE one-stop authoring guide — read this ONCE before writing or vetting a book and you have everything: Junifye's editorial ruleset (what a publishable book is — finished edited prose, never raw transcripts/stutters/leftover HTML entities like &gt;&gt;), structure (book vs document, chapters + sub-chapter headings), scripture conventions (real faithfully-cited refs; ONE quote per :bible block, commentary in its own paragraph), a worked example of a simple chapter, how glossary terms link (and how a \gref{…} reference addresses exactly one entry), AND the complete block/span markup grammar (the same content as source_syntax, appended). The vetter judges on these same grounds. No arguments.

## `image_upload_begin`

**Image Upload Begin** — writes, closed-world.

Begin an image upload that will be placed in a specific chapter. The REQUEST says WHERE (chapter_id); on a successful upload the image is auto-appended to that chapter (no separate block_add_image needed). Returns a one-time {reqid, url}: a PERSON OPENs the url in a browser (polished upload page with live progress) and picks a PNG/JPEG; an AI POSTs the bytes — `curl -X POST <url> -F file=@fig.png` (or `--data-binary @fig.png`). The server validates + normalises (PNG/JPEG only, oversized auto-downscaled, metadata stripped), stores it, places it, and returns the image_id + a reader link. NOTHING is added to the chapter unless the upload succeeds. Single-use, expires in 30 min; bytes stream over REST, never through MCP.

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
| `book_id` | string | yes | The 'idb...' id of the book. |
| `chapter_id` | string | yes | The 'idc...' chapter the image will be appended to on a successful upload. |

## `indexnow_run`

**Indexnow Run** — writes.

ADMIN. Trigger an IndexNow submission now. full=true clears the stored content digests and resubmits EVERY URL (the one-time bootstrap); otherwise only content changed since the last run is submitted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `full` | boolean | no | Resubmit all URLs (bootstrap), not just changes. |

## `indexnow_status`

**Indexnow Status** — writes.

ADMIN. Last IndexNow run for this site (public books + sellables): added/changed/removed URL counts, how many were submitted, and whether it was a baseline/skip. Read-only.

## `owner_logo_upload_begin`

**Owner Logo Upload Begin** — writes, closed-world.

Begin uploading YOUR brand logo — the image shown on the social share card (og:image) of every book you own, in place of the default author-initials monogram. Returns a one-time {reqid, url}: a PERSON OPENs the url in a browser (upload page) and picks a PNG; an AI POSTs the bytes — `curl -X POST <url> --data-binary @logo.png` (or `-F file=@logo.png`). PNG only (transparency preserved); the server validates + normalises and rejects anything else, never silently. On success it stores the logo against YOUR account and refreshes the share cards of all your books. The logo is per-OWNER and isolated — this only ever sets the caller's own logo. Single-use, expires in 30 min; bytes stream over REST, never through MCP.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

## `rotate_share_links`

**Rotate Share Links** — writes, closed-world.

ADMIN. Rotate a book's PUBLIC links so previously shared ones stop working — the enforcement teeth behind an unpublish/takedown. The short code ALWAYS rotates (old /<code> 404s). rotate_uuid (default true) also re-mints the content UUID so EVERY previously shared reader + PDF URL 404s, purges the old on-disk artifacts, and re-renders under the new UUID. rotate_print (default false) does the same for the obscured print PDF. Returns the NEW url/short_url/html_url/light_url/dark_url plus the old→new ids. NOTE: copies already DOWNLOADED cannot be recalled. Typical flow: book_set listed=false (unpublish) → rotate_share_links.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the book whose links to rotate. |
| `rotate_print` | boolean | no | Also rotate the obscured print UUID (default false). |
| `rotate_uuid` | boolean | no | Re-mint the content UUID too (default true) — 404s all shared reader+PDF URLs. Set false to rotate only the short code. |

## `source_syntax`

**Source Syntax** — read-only, idempotent, closed-world.

Return the grammar of the round-trippable block source used by block_get_source / chapter_get_source (read) and block_set_source (write): block prefixes (#, :bible, :quote, :footnote, :list, :math) and inline spans (*emph*, **strong**, [H1234], [h:hebrew], [g:greek], [l:latin], [ref:…], [a:text|url]), plus how a glossary reference (\gref{…}) resolves to ONE Glossary entry — including addressing a specific entry by its stored key when several share a lookup form. Call this once before authoring or translating so the source you write validates. No arguments.

## `sync_resolve`

**Sync Resolve** — writes, closed-world.

Mark a chapter (or the whole book) reconciled across all language editions — i.e. record the CURRENT source of each edition's chapter as the new sync baseline, so it stops showing up in sync_status. Call this AFTER you have propagated an edit into the lagging edition. With chapter_id: resolves just that chapter PAIR (snapshots every edition's chapter at that position). WITHOUT chapter_id: seeds/refreshes the baseline for EVERY chapter in the family at once — use this once on an already-aligned title to establish the starting fixed point, or to declare 'everything is in sync now'. Returns the count and the chapter ids snapshotted. Requires write access. This does NOT change any book content or re-render — it only moves the reconcile fixed point. NOTE: resolving does not itself translate anything; it asserts the editions are aligned as they currently stand, so only call it once they actually are.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | Any edition's 'idb…' id. The whole translation family is resolved together. |
| `chapter_id` | string | no | Optional. A chapter id ('idc…') in ANY edition: resolves that one chapter pair across all editions. Omit to seed/refresh the baseline for the entire book famil… |

## `sync_status`

**Sync Status** — read-only, idempotent, closed-world.

Cross-edition drift report for a TRANSLATED book: which chapters were edited in one language edition but not yet reconciled in the others. Pass any edition's book_id ('idb…'); the whole translation family (original + every edition linked via book_set_translation_of) is examined. Chapters are paired ACROSS editions by position in chapter order. For every chapter where at least one edition has moved off its last-reconciled baseline, you get, PER edition: changed (bool), current_version, baseline_version, a same-language line diff of what changed since baseline (`diff`, only for the side that changed — there is no cross-language diff, by design), and `current_source` (the full current flat source of BOTH editions, so you can rewrite the lagging one). reason is `edited` (a side changed since baseline), `no_baseline` (this chapter pair has never been reconciled — run sync_resolve to set the fixed point), or `unpaired` (the editions have a different chapter count at this position). A chapter with no drift is omitted. If the book has no linked edition, status is `standalone` and there is nothing to sync (link one with book_set_translation_of). After you propagate an edit, call sync_resolve to clear it. READ-ONLY.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | Any edition's 'idb…' id (from book_create.id). The whole translation family is reported, not just this edition. |

## `user_contact_get`

**User Contact Get** — read-only, idempotent, closed-world.

Get the CALLER's own contact info from pubcontacts (name, email, phone, address, bio, etc.). Derived from authenticated user_id — there is no parameter for specifying a different user. Auto-registers a minimal Contact in pubcontacts if the PubHub user has none (creates with just email from the PubHub user record).

## `user_contact_set_field`

**User Contact Set Field** — writes, closed-world.

Update ONE field on the CALLER's own contact (name, phone, address, website, bio, etc.). EMAIL CANNOT be set via this tool — it requires the pubcontacts confirmation flow (anti-hijack). The target Contact is derived from the authenticated user_id; there is NO parameter for specifying a different contact.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | yes |  |
| `value` | string | yes | The value to set, as a string. |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
