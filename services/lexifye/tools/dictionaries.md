# Dictionaries

**Create a dictionary, set its fields, freeze it, recover it.** 14 Lexifye MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://lexifye.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`dict_create`](#dict_create) | Create a new dictionary |
| [`dict_delete`](#dict_delete) | Delete a dict |
| [`dict_enrich`](#dict_enrich) | Run Darash Strong's enrichment on a dict NOW: scan its definitions for referenced… |
| [`dict_freeze`](#dict_freeze) | ADMIN |
| [`dict_get`](#dict_get) | Fetch a dict by id with a PAGE of its entries and their definitions inlined |
| [`dict_group_add`](#dict_group_add) | Attach a GROUP to a dict so every member of the group becomes a content editor of it (resolved… |
| [`dict_group_remove`](#dict_group_remove) | Detach a GROUP from a dict — its members lose the group-derived edit access to that dict (any… |
| [`dict_list`](#dict_list) | List the dictionaries you OWN, newest first |
| [`dict_list_for_user`](#dict_list_for_user) | SERVICE/ADMIN ONLY |
| [`dict_replace`](#dict_replace) | Find-and-replace a LITERAL string across EVERY definition of a dictionary — fix a recurring… |
| [`dict_restore`](#dict_restore) | Restore a soft-deleted dict, with every entry, definition, version history and private note… |
| [`dict_set_field`](#dict_set_field) | Atomically set ONE field on a dict by key |
| [`dict_transfer`](#dict_transfer) | Hand ownership of YOUR dictionary to another user |
| [`dict_unfreeze`](#dict_unfreeze) | ADMIN |

---

## `dict_create`

**Dict Create** — writes, closed-world.

Create a new dictionary. Author is stamped from the caller's pubcontacts Contact. author_bio is an optional opt-in paragraph (<=500 chars) printed under the title-page date; default empty. language is an optional BCP-47 tag (e.g. 'grc', 'he', 'nb') for the dictionary's primary language.

--- WHO CAN REACH IT ---
  There is no visibility setting and no public dictionary. Every dictionary is readable AND editable by exactly one set: you, the guest editors you add, and members of a group you attach. Its artifact URLs (.json/.html/.epub/.tex/.pdf) require that same membership. Authorised Publifye services may READ it service-to-service (lexifye is the ecosystem's system of record); they can never write or administer it.

--- OWNER (owner_id: SERVICE/ADMIN ONLY) ---
  Normally omit it: the owner is stamped from the authenticated caller, and a user creating a dictionary owns it.
  A TRUSTED SERVICE (a registered service key with no idu_ of its own — junifye's bridge is exactly this) has no identity to own a dictionary with, so it passes owner_id = the 'idu…' of the signed-in author it is creating on behalf of. Same trust boundary as dict_list_for_user, and the plan cap is charged to that owner, not the service. A regular user key passing owner_id is refused: you may only create dictionaries for yourself.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `author_bio` | string | no |  |
| `language` | string | no |  |
| `owner_id` | string | no | SERVICE/ADMIN ONLY: the pubhub 'idu…' id to own the new dict (on-behalf create). Omit as a user — the owner is your own identity. |
| `title` | string | yes |  |

## `dict_delete`

**Dict Delete** — writes, closed-world.

Delete a dict. Requires admin (owner).

--- SOFT BY DEFAULT ---
  The dict moves to the trash: it leaves every listing but keeps every entry, definition, version history and private note, and dict_restore brings it back whole for 30 days. List what is in there with dict_list(include_deleted=true) — you do not need to have kept the id.
  The plan slot is freed immediately.

--- purge=true ---
  IRREVERSIBLE. Hard-purges the dict, every entry and definition, all indexes, the collab rosters, the audit stream, the rendered artifacts and the <uuid>.json export, right now. Use it only when the content genuinely must not remain — never as a tidier version of the default.
  It also records a durable PURGE TOMBSTONE, so the dictionary does not come back from the disaster-recovery mirror the way it used to. The mirror is add-only, so the stored copy is SUPPRESSED rather than deleted; ask an operator for admin_purge_tombstone(action:"redact") if the content must actually leave it. The purge is refused outright if the tombstone cannot be recorded — nothing is destroyed in that case.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes | The 'idy...' id of the dict. |
| `id` | string | no | DEPRECATED ALIAS for dict_id. Still accepted; pass dict_id instead. |
| `purge` | boolean | no | IRREVERSIBLE hard delete. Omit for the recoverable default. |

## `dict_enrich`

**Dict Enrich** — writes, closed-world.

Run Darash Strong's enrichment on a dict NOW: scan its definitions for referenced original-language words (Strong's codes in `strong` spans, and hebrew/greek spans carrying a code), pull their lexicon data from darash, and add them as real auto entries (native lemma + SBL transliteration + a composed definition). Manually-authored entries always win a term collision; auto entries whose reference has vanished are reconciled away.

depth (optional, 0..4) overrides the dict's strongs_depth for THIS run only: 0 OFF · 1 referenced words only · 2 referenced + one derivation/related hop · 3-4 deeper. depth=0 really is off — nothing is scanned, created or reconciled, and the report says so in `note`; it is NOT the same as omitting depth, which uses the dict's own strongs_depth. A one-shot dict_enrich may go deeper (up to 4) than the automatic background enrich (which never exceeds 2). Also runs automatically (debounced) after definition edits — call this to force it or to request a deeper pass.

A pass only ever removes what it could itself have CREATED. An auto entry made by a deeper pass, or one whose creating depth is unknown, is left alone and counted in `kept_deeper` — so a deliberate depth-4 enrichment survives every later depth-2 automatic pass instead of being destroyed by it. And if any single pass ever decides more than 50 entries went orphaned at once, it purges NONE of them and says so in `purge_refused` + `note`.

Returns a report: {dict_id, depth, codes_resolved, created, kept, removed, kept_deeper, purge_refused, skipped_manual, skipped_script_spans, capped} — plus `note` when the run deliberately did nothing (depth 0) or refused a mass purge.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `depth` | integer | no |  |
| `dict_id` | string | yes |  |

## `dict_freeze`

**Dict Freeze** — writes, closed-world.

ADMIN. Apply a CANONICAL LOCK to a dictionary — the recoverable take-down. Use this FIRST when responding to an abuse report: it stops the dictionary being changed while you investigate, and destroys nothing.
  WHILE FROZEN, NOBODY may write to it — not a guest editor, not a group member, and NOT ITS OWNER. Content edits, guest and group management, transfer, delete AND restore are all refused, with a distinct 'frozen' reason so an author is not sent hunting for a permissions problem that does not exist.
  READING IS UNAFFECTED. dict_get, entry_list and every artifact route keep working for the people already entitled to them. A freeze takes a dictionary out of PLAY, it does not hide it — hiding it is what dict_delete does, and destroying it is admin_dict_delete.
  Locking the OWNER out of delete/transfer as well is a deliberate divergence from junifye's book_freeze (which locks writes only): a hold the subject of an investigation can dissolve by deleting the evidence, or by handing the dictionary to a second account, is not a hold.
  An operator keeps every intervention — admin_dict_transfer, admin_guest_remove, admin_dict_delete and dict_unfreeze all still work on a frozen dictionary.
  Reversible with dict_unfreeze, which puts everything back exactly as it was. Idempotent: re-freezing with the same reason writes no second audit row.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes | The 'idy...' id of the dict to freeze (NOT the uuid). Find one with admin_dict_list. |
| `reason` | string | no | Why the hold exists — a ticket reference and one line (max 200 chars). Strongly recommended: it is shown to the owner in the refusal they will receive, and an … |

## `dict_get`

**Dict Get** — read-only, idempotent, closed-world.

Fetch a dict by id with a PAGE of its entries and their definitions inlined. Each definition includes sha256 — quote it on subsequent definition_update/delete calls.

--- PAGINATION (entries) ---
  limit (default 50, max 200) + offset walk the entries in display order. The reply always carries entry_total, limit, offset and has_more, so a truncated read is never silent: has_more=true means there ARE more entries and you have not seen them. This tool used to inline EVERY entry, which made it unusable on a large dictionary — a 14,153-entry dict failed outright while dict_list and entry_list stayed fast. For metadata only, pass limit=0. For headwords without definition bodies, entry_list is cheaper; to find an entry without knowing its headword, use entry_search.

--- WHO MAY READ ---
  Its owner, its guest editors, and members of any group attached to it — nobody else. There is no public dictionary and no anonymous read. Knowing the id is NOT access; a caller outside that set gets 'forbidden' whether or not the dict exists. Same rule for entry_list, entry_get, definition_get_source, audit_list and every artifact URL.

--- CONDITIONAL FETCH (if_version) ---
  Pass if_version = the `version` you last received and, when the dict has NOT changed since, the reply is the compact {id, version, not_modified:true} instead of the whole tree — the 304 of this API. version bumps on EVERY mutation that changes rendered output (entry add/rename/move/reorder/delete, definition add/update/move/delete/revert, and title/language/author_bio edits), so an unchanged version means unchanged content. Private notes deliberately do NOT bump it — they never render.
  Omit if_version (or pass a stale one) and the response shape is exactly as before. The not-modified reply carries no artifact URLs, so omit if_version when you need those.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes | The 'idy...' id of the dict. |
| `id` | string | no | DEPRECATED ALIAS for dict_id. Still accepted; pass dict_id instead. |
| `if_version` | integer | no | Conditional fetch: the version you already hold. Equal to the dict's current version => {id, version, not_modified:true} instead of the payload. |
| `limit` | integer | no | How many entries to inline, in display order. 0 = metadata only. Check has_more. |
| `offset` | integer | no | Entry offset in display order. |

## `dict_group_add`

**Dict Group Add** — writes, closed-world.

Attach a GROUP to a dict so every member of the group becomes a content editor of it (resolved live — membership changes take effect instantly). Dict owner only, and you must BELONG to the group you are attaching. Idempotent.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes | The 'idy...' id from dict_create.id (NOT the uuid). |
| `group_id` | string | yes | The 'grp...' id of a group you belong to (group_list). |

## `dict_group_remove`

**Dict Group Remove** — writes, closed-world.

Detach a GROUP from a dict — its members lose the group-derived edit access to that dict (any who are ALSO individual guests, or members of another attached group, keep access via that path). Dict owner only. Idempotent.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes | The 'idy...' id from dict_create.id (NOT the uuid). |
| `group_id` | string | yes | The 'grp...' id to detach (guest_list shows attached groups). |

## `dict_list`

**Dict List** — read-only, idempotent, closed-world.

List the dictionaries you OWN, newest first. There is no public catalogue: filter=public no longer exists, and filter=all is accepted only as a synonym for 'own'. Dictionaries shared WITH you (via a group or a guest grant) are not in this list — the dashboard and the group/guest tools surface those. Paginates via limit (default 50, max 200) + offset. Response shape: {items, total, limit, offset, has_more}.

--- TRASH (include_deleted) ---
  Pass include_deleted=true to ALSO get your soft-deleted dictionaries in an added `deleted` array — id, title, entry/definition counts, deleted_at and days_remaining — so a dict_delete you want to undo can be found without having written its idy… id down. items/total/has_more keep meaning exactly what they meant (the live library); the deleted array is unpaginated and always OLDEST FIRST, so the one closest to grace expiry is at the top. Restore with dict_restore.
  It is EDITOR-level and OWNER-SCOPED: it needs a write-capable credential and only ever lists dictionaries you own. filter does not apply to it.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `filter` | string | no | Accepted for compatibility; both values mean 'the dicts you own'. |
| `include_deleted` | boolean | no | Also return YOUR soft-deleted dicts in a 'deleted' array (the account trash bin). Requires a write-capable credential. |
| `limit` | integer | no |  |
| `offset` | integer | no |  |

## `dict_list_for_user`

**Dict List For User** — read-only, idempotent, closed-world.

SERVICE/ADMIN ONLY. List every dictionary a given user can work with — the union of dicts they OWN, are a GROUP member of, and are a GUEST editor of — deduped and each tagged with its relation ('owner' | 'group' | 'guest'), owner-first then by title. This is the on-behalf listing a trusted service (e.g. junifye authenticating as itself) calls to render a dictionary PICKER for a signed-in author, so a human never pastes a raw idy… id. LEAN projection for a dropdown: {id, uuid, title, language, entry_count, version, relation} — NO entries or definitions (use dict_get for those). A user with no dictionaries returns {dicts:[], count:0} — an empty list is a valid answer, not an error. NOT for a regular user asking about themselves: a user lists their own dicts with dict_list (default filter=own). Response: {user_id, dicts, count}.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `user_id` | string | yes | The pubhub 'idu…' id of the user to list dictionaries for (the signed-in author). Resolve a name with guest_find_user; never an email. |

## `dict_replace`

**Dict Replace** — writes, closed-world.

Find-and-replace a LITERAL string across EVERY definition of a dictionary — fix a recurring typo, rename a term, update a date. One call instead of one edit per definition.
  ALWAYS PREVIEW FIRST: preview=true is a DRY RUN that reports what WOULD change and writes nothing. Then re-run without it.
  WHOLE WORDS BY DEFAULT: find="Gen" hits "Gen" and "Gen." but NEVER "Genesis" — a rename thinks around words, not blind characters. Set whole_word=false for a raw substring replace. Case-SENSITIVE, literal, NOT a regular expression.
  SPAN INTERNALS ARE PROTECTED, and this differs from junifye's book_replace on purpose. Only the PROSE a reader sees is rewritten (text, *emph*, **bold**, and a link's visible label). A Strong's code [H2617], the code/transliteration/original word inside [h:…] and [g:…], a [ref:John 3:16] target and a link's URL are STRUCTURE and are left untouched — so replacing "John" does not silently rewrite your Bible references, and replacing "hesed" does not rewrite a transliteration. To change a headword use entry_rename; to change a span's internals use definition_set_source.
  PER-DEFINITION MANIFEST: units[] reports applied (with count) | would-apply (preview) | skipped-unchanged | rejected-invalid | not-editable | skipped. Each definition is ATOMIC: the result is re-validated first, and one whose result would be malformed (or over the 64 KB definition limit) is reported rejected-invalid and left exactly as it was.
  UNDOABLE: every changed definition is checksum-gated against concurrent editors and creates a new revertable version — definition_history / definition_revert put any single one back.
  Soft-deleted entries and definitions are not touched and are not listed; they are frozen by design (see trash_list).
  The audit stream records ONE dict_replace row for the whole run, not one per definition — a 213-definition edit is one editorial decision, and per-definition detail lives in definition_history.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes | The 'idy...' id of the dict. |
| `find` | string | yes | Exact literal text to find (case-sensitive, not a regex). |
| `preview` | boolean | no | Dry run: report what would change and write NOTHING. Always preview a rename first. |
| `replace` | string | yes | Replacement text. May be empty to delete the word. |
| `whole_word` | boolean | no | Match whole words only (DEFAULT true — the safe rename). false = raw substring replace. |

## `dict_restore`

**Dict Restore** — writes, closed-world.

Restore a soft-deleted dict, with every entry, definition, version history and private note exactly as they were. Works for 30 days after dict_delete. Requires admin (owner), like dict_delete. Find the id with dict_list(include_deleted=true) — the trash bin of your account.
  The PLAN CAP applies: a restore occupies a concurrent-dict slot exactly as a create does, so restoring while you are already at your limit is refused, naming what to delete or purge first. (It is refused, never partial — the dictionary stays in the trash for the rest of its 30 days.)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes | The 'idy...' id of the soft-deleted dict, from dict_list(include_deleted=true). |
| `id` | string | no | DEPRECATED ALIAS for dict_id. Still accepted; pass dict_id instead. |

## `dict_set_field`

**Dict Set Field** — writes, closed-world.

Atomically set ONE field on a dict by key.
  There is NO visibility key: dictionaries are never public, so there is nothing to publish. A dictionary is readable and editable by its owner, its guest editors, and members of an attached group — and by nobody else.

--- PRESENTATION KEYS (OWNER ONLY) ---
  How the dictionary TYPESETS, in every format. Owner-only for the same reason `language` is: they decide whether and how the document sets at all, so a guest editor must not be able to break every PDF of a dict they do not own.
  page_size    a4 (screen default) | letter | 6x9 (trade print)
  font_size    body size in points, 8..18. Below 8 a lexicon is unreadable; above 18 is a large-print edition, which is a different book.
  entry_break  continuous (default) | page = a new page per entry. Suits a few long articles; ruinous for thousands of short ones.
  interlink    true|false (on/off accepted). When on, a word used in a definition becomes a link to its own entry in this dictionary — in the reader, the EPUB and the reader PDF; suppressed in the print interior, where a hyperlink is invisible and still costs an annotation. Membership in this dictionary is the whole test: a Strong's code is linked exactly like a headword, and matching uses the same fold as entry_get (unpointed Hebrew finds the pointed lemma, g26/G0026 land on one entry). An entry never links to itself. Absent is OFF: it changes the text a reader sees.
  interlink_scope  all (default) | first. Which occurrences link, once interlink is on. all = EVERY occurrence. first = only the first mention of a given entry within each entry. Absent means all. Measured on a 128-entry themed word-study dictionary, all vs first was 48 links against 43, over the same 25 pages, and moved not one line break. On a GENERAL dictionary it is a different matter: where the headwords are ordinary words (a, the, of, he, one, man, god, word, love, life…), a 50-entry sample simulated 3,328 links under `first` alone — one every ten words in the worst entry — and `all` is higher still. For that kind of content set `first`, or leave interlink off, and render ONE PAGE before rendering the rest.
  Read them back in dict_get under `layout`. Omitted keys keep the shipped defaults — a dictionary that never sets one renders exactly as it always has.

--- AUTHOR-BIO KEY (OWNER ONLY) ---
  author_bio (string, 0..500 chars). Opt-in paragraph printed in italic below the title-page date. Empty clears it. NEVER auto-populate — only set when the author explicitly asks to.

--- LANGUAGE KEY (OWNER ONLY) ---
  language (BCP-47 tag, e.g. 'grc', 'he', 'nb'; empty clears). The dictionary's primary language, and the switch that decides how the document TYPESETS — an RTL tag flips the direction of every rendered format. A guest editor may change content but not that, so this key is owner-only (a guest gets 'forbidden'), unlike title and strongs_depth.

--- TITLE KEY (editor level: owner, guest editors, group members) ---
  title (1..200 chars). The dictionary's name, on every cover and dashboard row.

--- STRONGS-DEPTH KEY (editor level) ---
  strongs_depth ('0'..'4' as a string). Darash Strong's auto-enrichment depth: 0 off · 1 referenced words only · 2 default (automatic, content-driven) · 3-4 deeper on request. Depth >2 never runs automatically — the background enrich clamps to 2; request a deeper one-shot with dict_enrich.

value is always a string.

--- OPTIMISTIC LOCK ---
  For the content fields title, language, and author_bio you MUST pass `expected` = the field's CURRENT value (from dict_get). Field-scoped: an unrelated field change never conflicts. A mismatch is rejected (stale) with the current value so you can refetch and retry. strongs_depth takes no expected.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes | The 'idy...' id of the dict. |
| `expected` | string | no | REQUIRED for title/language/author_bio: the field's current value (optimistic lock). |
| `id` | string | no | DEPRECATED ALIAS for dict_id. Still accepted; pass dict_id instead. |
| `key` | string | yes |  |
| `value` | string | yes |  |

## `dict_transfer`

**Dict Transfer** — writes, closed-world.

Hand ownership of YOUR dictionary to another user. Owner only — the mirror of group_transfer, which already lets you hand over a group.
  THE RECIPIENT MUST ALREADY BE A COLLABORATOR on this dict: an individual guest editor, or a member of a group attached to it. That is the same consent shape group_transfer uses ("the new owner must already be a member") and it is what stops a dictionary being pushed onto somebody who never agreed to hold it. Add them first with guest_add, or attach a group you both belong to with dict_group_add.
  WHAT MOVES: the dictionary leaves your library and joins theirs, and every owner-only right goes with it — delete/restore, guest and group management, language, author_bio, and this tool. You keep NOTHING unless you are also a guest or in an attached group.
  WHAT STAYS: guest editors and attached groups carry over, so the work in progress is not interrupted. The recipient's own guest grant becomes redundant and is dropped (an owner is not their own guest). The response reports both counts — the new owner can drop any of it with guest_remove / dict_group_remove.
  The recipient is NOTIFIED (notice_list). This is not reversible by you afterwards: only the new owner can transfer it back.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes | The 'idy...' id of a dict you own (NOT the uuid). |
| `new_owner_id` | string | no | DEPRECATED ALIAS for to_owner. Still accepted; pass to_owner instead. |
| `to_owner` | string | yes | The recipient's lexifye user id (pubhub 'idu...') from guest_list or guest_find_user. NOT an email. (admin_dict_transfer's to_owner also resolves a username; t… |

## `dict_unfreeze`

**Dict Unfreeze** — writes, closed-world.

ADMIN. Lift a dict_freeze. Everything returns exactly as it was — the freeze changed no content, so there is nothing to restore. Idempotent: unfreezing a dictionary that is not frozen is a no-op and says so.
  ADMIN-ONLY, with no owner-reopenable case. junifye's book_unfreeze is write-level because junifye ALSO auto-locks a book after 30 days of inactivity and an owner must be able to reopen their own soft lock. lexifye has no auto-lock: the only thing that ever freezes a dictionary here is an operator, so the only thing that lifts one is an operator. A write-level unfreeze would hand the subject of an investigation the key to their own hold.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes | The 'idy...' id of the frozen dict. List open holds with admin_dict_list(frozen:true). |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
