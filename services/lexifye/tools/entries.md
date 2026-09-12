# Entries and definitions — Lexifye MCP tools

**The lemma and sense tree, with per-definition history, diff and revert.** 20 tools, listed below with the exact description and input
schema the server itself returns. Endpoint: `https://lexifye.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`definition_add`](#definition-add) | Add a definition to an entry |
| [`definition_add_source`](#definition-add-source) | Create a definition from markup source in ONE call — the definition_add twin for the source… |
| [`definition_delete`](#definition-delete) | Delete a definition |
| [`definition_diff`](#definition-diff) | Compare two versions of a definition (from/to version numbers via definition_history),… |
| [`definition_get_source`](#definition-get-source) | Return a definition's content as round-trippable markup source (the grammar source_syntax… |
| [`definition_history`](#definition-history) | List the retained version history of a definition (the last 20 saves, 7-day window), newest… |
| [`definition_move`](#definition-move) | Reorder a definition within its entry's sense order (rendered 1., 2., 3.) |
| [`definition_restore`](#definition-restore) | Restore a soft-deleted definition to its original position in its entry's sense order, with… |
| [`definition_revert`](#definition-revert) | Restore a definition to a past version n (from definition_history), recorded as a NEW version… |
| [`definition_set_source`](#definition-set-source) | Replace a definition's content by parsing markup source (the grammar source_syntax documents) |
| [`definition_update`](#definition-update) | Replace a definition's content |
| [`entry_add`](#entry-add) | Add a term entry to a dict |
| [`entry_delete`](#entry-delete) | Delete an entry and all of its definitions from a dict |
| [`entry_get`](#entry-get) | Look a term UP in a dict and return the matching entry (or entries) with their definitions… |
| [`entry_list`](#entry-list) | List a dict's entries (summary only: id, term, translit, seq — NO definitions; use dict_get… |
| [`entry_move`](#entry-move) | Reorder an entry within its dict's display order |
| [`entry_rename`](#entry-rename) | Rename an entry's term (and optionally its transliteration) |
| [`entry_reorder`](#entry-reorder) | Set a dict's ENTIRE entry display order in one call — the bulk twin of entry_move (which… |
| [`entry_restore`](#entry-restore) | Restore a soft-deleted entry to its original position, with every definition, every… |
| [`entry_search`](#entry-search) | Find entries in ONE dictionary by a text fragment — the way to locate an entry when you do NOT… |

---

## `definition_add`

**Definition Add** — writes, closed-world.

Add a definition to an entry. content is an array of blocks (paragraph|heading|list) each holding spans (text, emph, bold, hebrew, greek, strong, bref, link). A list block may also carry items — the per-item span groups, so one bullet can hold emphasis, a Strong's code and a Greek word; concatenated they must equal spans, and you omit items when every item is a single span. Prefer definition_add_source, which writes this shape for you from the markup grammar. Returns the created definition including its sha256 token.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content` | array | yes |  |
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |

## `definition_add_source`

**Definition Add Source** — writes, closed-world.

Create a definition from markup source in ONE call — the definition_add twin for the source grammar (source_syntax). Parses the markup into content blocks, validates, and appends the definition to the entry. Returns the created definition including its sha256.
  WHAT GOES IN source: the definition's whole text as MARKUP, which is PARSED into content blocks (blank lines split paragraphs; *emph*, **bold**, [H1234], [h:…], [g:…], [ref:…], [a:text|url], # headings, - lists) rather than stored verbatim — call source_syntax for the grammar. `body` and `content` are accepted aliases for this same field; passing two spellings at once is refused, and structured block arrays go to definition_add, not here.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `body` | string | no | Accepted ALIAS for source — the same field, under the name a sibling tool uses for it. Pass source; passing two spellings at once is refused rather than resolv… |
| `content` | string | no | Accepted ALIAS for source — the same field, under the name a sibling tool uses for it. Pass source; passing two spellings at once is refused rather than resolv… |
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |
| `source` | string | yes | The definition's full text as markup source; PARSED, not stored verbatim. See source_syntax. |

## `definition_delete`

**Definition Delete** — writes, closed-world.

Delete a definition. sha256_of_old MUST match the current stored sha256.

--- SOFT BY DEFAULT ---
  The definition moves to the entry's trash: it leaves the sense order and every rendered artifact, but its content and its WHOLE VERSION HISTORY stay — definition_history and definition_diff go on answering for it, and definition_restore puts it back at its original position for 30 days. (That is the point: before this, history protected you against a bad edit and gave you nothing at all against a delete.)
  Browse the bin with trash_list.

--- purge=true ---
  IRREVERSIBLE. Destroys the definition and every retained version of it, right now.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `def_id` | string | no | DEPRECATED ALIAS for definition_id. Still accepted; pass definition_id instead. |
| `definition_id` | string | yes |  |
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |
| `purge` | boolean | no | IRREVERSIBLE hard delete, version history included. Omit for the recoverable default. |
| `sha256` | string | no | Accepted alias for sha256_of_old — the same optimistic-lock token, under the name definition_set_source / definition_revert / entry_rename use for it. Errors f… |
| `sha256_of_old` | string | yes |  |

## `definition_diff`

**Definition Diff** — read-only, idempotent, closed-world.

Compare two versions of a definition (from/to version numbers via definition_history), returning each version's markup source plus a unified line diff (lines prefixed ' ' unchanged, '-' removed, '+' added). Read-level for a LIVE definition; a soft-deleted one requires editor access, since the diff renders content the author has already deleted.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `definition_id` | string | yes |  |
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |
| `from` | integer | yes |  |
| `to` | integer | yes |  |

## `definition_get_source`

**Definition Get Source** — read-only, idempotent, closed-world.

Return a definition's content as round-trippable markup source (the grammar source_syntax documents). Pair with definition_set_source for edit-and-push revision. Returns {dict_id, entry_id, definition_id, source, sha256} — quote sha256 on definition_set_source so a concurrent edit is caught. Read-level for a LIVE definition; one whose entry is in the trash requires editor access.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `definition_id` | string | yes |  |
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |

## `definition_history`

**Definition History** — read-only, idempotent, closed-world.

List the retained version history of a definition (the last 20 saves, 7-day window), newest first. Each version carries {n, sha256, author_name, ts} — NO content (call definition_diff to compare, or definition_revert to restore). Read-level for a LIVE definition; a soft-deleted one requires editor access, since its history is content the author has already deleted.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `definition_id` | string | yes |  |
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |

## `definition_move`

**Definition Move** — writes, closed-world.

Reorder a definition within its entry's sense order (rendered 1., 2., 3.). to_index is 0-based (0 = first) and clamped. Returns {ok, definition_id, to_index} where to_index is where the definition ACTUALLY landed — when the request was out of range the reply also carries requested_index, clamped:true and a note.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `def_id` | string | no | DEPRECATED ALIAS for definition_id. Still accepted; pass definition_id instead. |
| `definition_id` | string | yes |  |
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |
| `to_index` | integer | yes |  |

## `definition_restore`

**Definition Restore** — writes, closed-world.

Restore a soft-deleted definition to its original position in its entry's sense order, with its version history intact. Works for 30 days after definition_delete. Call trash_list for what is restorable.
  If the ENTRY is in the trash too, this is refused and entry_restore is the call to make — it brings every definition back with it, and restoring one alone would leave it invisible.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `def_id` | string | no | DEPRECATED ALIAS for definition_id. Still accepted; pass definition_id instead. |
| `definition_id` | string | yes |  |
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |

## `definition_revert`

**Definition Revert** — writes, closed-world.

Restore a definition to a past version n (from definition_history), recorded as a NEW version — history is never destroyed. Carries the SAME optimistic lock as an edit: sha256 MUST match the definition's CURRENT sha256 (from dict_get). Returns the new current definition.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `definition_id` | string | yes |  |
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |
| `n` | integer | yes |  |
| `sha256` | string | yes | The definition's CURRENT sha256 (optimistic lock). |

## `definition_set_source`

**Definition Set Source** — writes, closed-world.

Replace a definition's content by parsing markup source (the grammar source_syntax documents). sha256 MUST match the current stored token (quote the one from definition_get_source / dict_get) — a mismatch means someone else edited it; refetch and retry. Parse errors name the offending block/construct. Returns the updated definition including its new sha256.
  WHAT GOES IN source: the definition's whole text as MARKUP, which is PARSED into content blocks (blank lines split paragraphs; *emph*, **bold**, [H1234], [h:…], [g:…], [ref:…], [a:text|url], # headings, - lists) rather than stored verbatim — call source_syntax for the grammar. `body` and `content` are accepted aliases for this same field; passing two spellings at once is refused, and structured block arrays go to definition_update, not here.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `body` | string | no | Accepted ALIAS for source — the same field, under the name a sibling tool uses for it. Pass source; passing two spellings at once is refused rather than resolv… |
| `content` | string | no | Accepted ALIAS for source — the same field, under the name a sibling tool uses for it. Pass source; passing two spellings at once is refused rather than resolv… |
| `definition_id` | string | yes |  |
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |
| `sha256` | string | yes | The current sha256 token (optimistic lock). From definition_get_source or dict_get. |
| `source` | string | yes | The definition's full text as markup source; PARSED, not stored verbatim. See source_syntax. |

## `definition_update`

**Definition Update** — writes, closed-world.

Replace a definition's content. sha256_of_old MUST match the current stored sha256 — quote the one returned by dict_get. Mismatch is rejected (refetch and retry).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content` | array | yes |  |
| `def_id` | string | no | DEPRECATED ALIAS for definition_id. Still accepted; pass definition_id instead. |
| `definition_id` | string | yes |  |
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |
| `sha256` | string | no | Accepted alias for sha256_of_old — the same optimistic-lock token, under the name definition_set_source / definition_revert / entry_rename use for it. Errors f… |
| `sha256_of_old` | string | yes |  |

## `entry_add`

**Entry Add** — writes, closed-world.

Add a term entry to a dict. term must be unique within the dict (case-insensitive). translit is an optional romanization of the term (e.g. 'logos' for λόγος) for glossary rendering.

--- SOURCE (one-call authoring) ---
  source is optional prose: pass it and the entry's FIRST definition is created in the same call, so a term with a gloss costs one call instead of entry_add + definition_add. WHAT GOES IN IT: the definition's text as MARKUP, which is PARSED rather than stored verbatim — blank lines split it into paragraphs, and the full markup grammar is available (*emph*, **bold**, [H1234], [h:…], [g:…], [ref:…], [a:text|url], # headings, - lists). It goes through exactly the same parser as definition_add_source, so anything valid there is valid here; call source_syntax (or house_style) for the grammar.
  `body` and `content` are accepted aliases for this same field; passing two spellings at once is refused rather than resolved, because two bodies of prose are two documents.
  Markup errors are reported BEFORE the entry is created, so a rejected source never leaves a bare entry behind. Omit source to create the term alone and add senses later with definition_add / definition_add_source.
  A structured `content` BLOCK ARRAY is still refused: entry_add takes text, definition_add takes blocks.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `body` | string | no | Accepted ALIAS for source — the same field, under the name a sibling tool uses for it. Pass source; passing two spellings at once is refused rather than resolv… |
| `content` | string | no | Accepted ALIAS for source — the same field, under the name a sibling tool uses for it. Pass source; passing two spellings at once is refused rather than resolv… |
| `dict_id` | string | yes |  |
| `source` | string | no | Optional. The entry's first definition as markup source (blank-line-separated blocks); PARSED, not stored verbatim. See source_syntax. |
| `term` | string | yes |  |
| `translit` | string | no |  |

## `entry_delete`

**Entry Delete** — writes, closed-world.

Delete an entry and all of its definitions from a dict.

--- SOFT BY DEFAULT ---
  The entry moves to the dict's trash: it disappears from entry_list, dict_get, the rendered PDF/HTML/EPUB and the JSON export, but nothing is destroyed. Its definitions, their full version history and the private notes anchored to it all wait with it, and entry_restore brings the lot back for 30 days. The TERM is released immediately, so you can re-add it at once.
  Browse the bin with trash_list.

--- purge=true ---
  IRREVERSIBLE. Destroys the entry, every definition under it and every definition's version history, right now. Use it only when the content genuinely must not remain.
  Its private notes are then PROMOTED to dict level rather than deleted — the research about a lemma outlives the lemma. Pass delete_notes=true to destroy them too.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `delete_notes` | boolean | no | Only meaningful with purge=true: destroy the entry's private notes instead of promoting them to dict level. |
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |
| `purge` | boolean | no | IRREVERSIBLE hard delete. Omit for the recoverable default. |

## `entry_get`

**Entry Get** — read-only, idempotent, closed-world.

Look a term UP in a dict and return the matching entry (or entries) with their definitions inlined — the read you want when you know the word but not its idj_ id. Read-level: any caller with the dict id may look up.

--- MATCHING ---
  Identity first, then a folded fallback, so you find the word however you type it: Strong's ignores case and zero-padding (H0007 finds H7), Greek ignores accents/breathings and final-vs-medial sigma, Latin ignores case. Hebrew nikud folds for LOOKUP but not for identity — חֵסֵד (H2617, the noun) and חָסַד (H2616, the verb) are genuinely different words, so searching the unpointed חסד legitimately returns BOTH.

--- RESULT ---
  Always {dict_id, term, count, matches:[entry…]} with matches ordered by display order (seq). count is normally 1; count>1 means the folded fallback resolved to several distinct lemmas — pick by translit/definition, never assume matches[0]. A term with no match is an ERROR (not_found), like every other by-identifier read on this surface — it never comes back as an empty success you might mistake for an empty entry.
  This tool needs the WHOLE term. If you only have a fragment, or you are looking for a word used INSIDE a definition, call entry_search instead.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes |  |
| `term` | string | yes |  |

## `entry_list`

**Entry List** — read-only, idempotent, closed-world.

List a dict's entries (summary only: id, term, translit, seq — NO definitions; use dict_get for the full tree). Paginated via limit (default 100, max 500) + offset. Response: {items, total, limit, offset, has_more, sort}. Read-level: any caller with the dict id may list.

--- SORT ---
  sort=seq (default) — the authored display order, the one entry_move / entry_reorder maintain.
  sort=alpha — alphabetical by term. This is the SAME collation the rendered PDF/EPUB/HTML letter index uses, so an alpha page matches what a reader sees; for a multi-script lexicon it clusters by script (Latin, then Greek, then Hebrew, …) and by letter within each.
  Pagination means the same thing under either sort: total is the whole entry count and has_more reports whether entries remain past this page.

--- TRASH ---
  Soft-deleted entries are NEVER in items. Pass include_deleted=true to get them alongside, in an added `deleted` array (unpaginated, each with deleted_at and days_remaining) — items/total/limit/offset/has_more keep meaning exactly what they meant. trash_list is the fuller view (it covers deleted definitions too).
  include_deleted requires EDITOR access to the dict even though plain entry_list is read-level: the trash holds content the author has already removed from every reading surface.

--- LOOKING FOR SOMETHING SPECIFIC? ---
  Do not page a whole dictionary to find one word. entry_get resolves an EXACT term; entry_search finds entries by a text FRAGMENT (and, with content=true, by words inside definitions).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes |  |
| `include_deleted` | boolean | no | Also return the dict's soft-deleted entries in a 'deleted' array (the trash bin). |
| `limit` | integer | no |  |
| `offset` | integer | no |  |
| `sort` | string | no |  |

## `entry_move`

**Entry Move** — writes, closed-world.

Reorder an entry within its dict's display order. to_index is 0-based (0 = first) and clamped to the valid range. Returns {ok, entry_id, to_index} where to_index is where the entry ACTUALLY landed — when the request was out of range the reply also carries requested_index, clamped:true and a note.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |
| `to_index` | integer | yes |  |

## `entry_rename`

**Entry Rename** — writes, closed-world.

Rename an entry's term (and optionally its transliteration). term must stay unique within the dict (case-insensitive) — a collision with a DIFFERENT entry is rejected. Pass translit to also set/clear the romanization (empty string clears it); omit translit to leave it unchanged. Optimistic lock: pass sha256 = the entry's current lock token (the sha256 field on dict_get / entry_list entries, over term+translit); a mismatch is rejected (stale) with the current sha so you refetch and retry.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |
| `sha256` | string | yes | The entry's current (term+translit) lock token from dict_get/entry_list. |
| `term` | string | yes |  |
| `translit` | string | no |  |

## `entry_reorder`

**Entry Reorder** — writes, closed-world.

Set a dict's ENTIRE entry display order in one call — the bulk twin of entry_move (which repositions one entry and costs N calls to reorder N entries).
entry_ids is the new order, first to last. It must name EVERY entry of the dict exactly once: an unknown id, a repeated id, or a missing one is rejected and NOTHING is written, so a partial list can never leave the dict in an order you did not ask for. Call entry_list (limit=500, sort=seq) for the current ids, reorder that array, and send it back. Returns {ok, dict_id, count}.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes |  |
| `entry_ids` | array | yes | Every entry id of the dict exactly once, in the desired display order. |

## `entry_restore`

**Entry Restore** — writes, closed-world.

Restore a soft-deleted entry to its original position, with every definition, every definition's version history, and the private notes that were anchored to it. Works for 30 days after entry_delete. Call trash_list for what is restorable.

--- TERM COLLISIONS ---
  A restore is NEVER refused. If another entry took the term while this one sat in the trash, the incumbent KEEPS the uniqueness slot and the response names it as term_taken_by (trash_list flags the same thing as term_taken before you restore). The restored entry still comes back complete — in entry_list, dict_get, the export and every rendered artifact — but entry_get for that exact term will resolve to the incumbent, since lookup is identity-first. Resolve it with entry_rename on whichever of the two should change.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes |  |
| `entry_id` | string | yes |  |

## `entry_search`

**Entry Search** — read-only, idempotent, closed-world.

Find entries in ONE dictionary by a text fragment — the way to locate an entry when you do NOT know its exact headword (entry_get needs the exact term; this does not).
  MATCHING: literal substring, CASE- AND DIACRITIC-BLIND, so q="hesed" finds "ḥesed", q="dap" finds "dāp" and q="jorn" finds "Jørn". Not a regular expression — a literal fragment is what you want here and it is what you get.
  WHAT IS SEARCHED: entry terms and transliterations always (cheap). Pass content=true to ALSO search definition bodies — slower, since it reads every definition of the dictionary.
  RESULTS ARE METADATA, NOT CONTENT. Each hit is an ADDRESS: {entry_id, term, translit, where, definition_id?, matches}. `where` is "term", "translit" or "definition"; one entry can produce several hits. There are deliberately NO bodies and no snippets — fetch the ones you want with entry_get (by term) or definition_get_source (by definition_id). That keeps a 200-hit search in kilobytes and lets you pay only for what you read.
  Definition matching walks the WORDS A READER SEES, not the markup: a Strong's code, a [ref:…] target and a link URL are structure and are not searchable this way (so q="ref" does not match every Bible reference). Look a Strong's code up with entry_get — enrichment materialises codes as real entries.
  Soft-deleted entries and definitions are never returned; the trash is trash_list's job.
  Paginates via limit (default 20, max 100) + offset, in the dictionary's display order. Response: {hits, total, limit, offset, has_more, scanned, truncated}.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content` | boolean | no | Also search definition bodies (slower). Terms and transliterations are always searched. |
| `dict_id` | string | yes | The 'idy...' id of the dict to search. Required — there is no cross-dictionary search. |
| `limit` | integer | no |  |
| `offset` | integer | no |  |
| `q` | string | yes | Literal text to find. Case- and diacritic-blind; not a regex. |
| `scan_from` | integer | no | Resume the SCAN here. When truncated=true the reply carries next_scan_from; pass it back to continue through the rest of the dictionary. |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
