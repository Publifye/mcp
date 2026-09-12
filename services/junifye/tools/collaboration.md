# Groups, guests and notes

**Share a book, invite an editor, keep private working notes.** 38 Junifye MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://junifye.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`edit_session_create`](#edit-session-create) | Open (or REUSE) a human WEB-EDITOR link for a book and return {session_id, url, pin, reused,… |
| [`edit_session_revoke`](#edit-session-revoke) | Immediately disable a web-editor link previously minted by edit_session_create (e.g |
| [`editorial_list`](#editorial-list) | List the books on YOUR editable shelf (books you own or are a guest editor on) that are IN the… |
| [`editorial_set`](#editorial-set) | Set a book's EDITORIAL review state — an opt-in, soft workflow separate from the admin… |
| [`group_accept`](#group-accept) | Accept an invite to a group (you become a member and gain content-edit access to every book… |
| [`group_admin_set`](#group-admin-set) | Grant or revoke ADMIN on a group member (admins can invite, rename, and remove non-admin… |
| [`group_autoshare_set`](#group-autoshare-set) | Toggle YOUR autoshare on a group |
| [`group_create`](#group-create) | Create a GROUP — a named set of Junifye users you can later attach to a book (book_group_add)… |
| [`group_decline`](#group-decline) | Decline an invite to a group (drops the pending invite; you do NOT join) |
| [`group_delete`](#group-delete) | Delete a group |
| [`group_get`](#group-get) | Get one group in detail: members (with display names), each member's admin/owner flag,… |
| [`group_invite`](#group-invite) | Invite a Junifye user to a group |
| [`group_invite_cancel`](#group-invite-cancel) | Withdraw a pending group invite |
| [`group_leave`](#group-leave) | Leave a group you are a member of |
| [`group_list`](#group-list) | List the GROUPS you belong to — [{id, name, owner, member_count, role, autoshare}] where role… |
| [`group_member_remove`](#group-member-remove) | Remove a member from a group |
| [`group_rename`](#group-rename) | Rename a group |
| [`group_transfer`](#group-transfer) | Hand ownership of a group to another MEMBER |
| [`guest_add`](#guest-add) | Invite a Junifye user as a GUEST EDITOR of a book — they get CONTENT-edit access… |
| [`guest_find_user`](#guest-find-user) | Find Junifye users by NAME to invite as guest editors |
| [`guest_list`](#guest-list) | List the collaborators of a book |
| [`guest_remove`](#guest-remove) | Remove a GUEST EDITOR from a book — revokes their content access and drops the book from their… |
| [`note_delete`](#note-delete) | Delete one authoring NOTE, addressed by anchor / block_id / key (same handle used to set it) |
| [`note_get`](#note-get) | Read one authoring NOTE in full (subject + body) — private scratch, never part of the rendered… |
| [`note_list`](#note-list) | List authoring NOTES (private scratch — never part of the rendered book) as a compact catalog… |
| [`note_patch`](#note-patch) | Surgically edit a NOTE without resending its whole body: replace `find` with `replace` |
| [`note_set`](#note-set) | Create, replace, or append an authoring NOTE — private scratch for you and the author… |
| [`question_add`](#question-add) | Create a discoverable question (e.g |
| [`question_delete`](#question-delete) | Permanently delete a question and all its answer edges (the referenced books/chapters are… |
| [`question_get`](#question-get) | Fetch one question by id OR slug, with its answer edges resolved (each answer names the… |
| [`question_link`](#question-link) | Attach an answer: this question is answered by book_id, optionally narrowed to chapter_id |
| [`question_list`](#question-list) | Browse questions newest-first, paginated |
| [`question_set`](#question-set) | Edit a question's text/tags/lang |
| [`question_unlink`](#question-unlink) | Detach one answer edge (book_id, optionally chapter_id) from a question |
| [`vet_decide`](#vet-decide) | ADMIN |
| [`vet_list`](#vet-list) | ADMIN |
| [`vet_status`](#vet-status) | Check whether a book has been approved for public listing, and — if it was rejected — WHY |
| [`vet_submit_result`](#vet-submit-result) | Report the verdict of an agentic publication-vetting session for a book |

---

## `edit_session_create`

**Edit Session Create** — writes, closed-world.

Open (or REUSE) a human WEB-EDITOR link for a book and return {session_id, url, pin, reused, expires_in_minutes}. Hand the url to the author — they edit one section at a time in a distraction-free browser editor. EVERY link is gated by a 4-digit PIN (returned here as `pin`): share the url and the pin SEPARATELY — the pin is typed by hand to open the editor (no paste). Four wrong PIN entries permanently disable the link; just call this again for a fresh url+pin. Calling again with the SAME editor_name for the same book hands back that person's EXISTING live link (reused=true) but ROTATES its pin to the one returned here. The link auto-locks after an idle window (default 60 minutes; settable via idle_minutes or in the editor). Saves are checksum-guarded and each section is locked while someone edits it, so two people can safely edit the same book at once. Pass open_at to deep-link straight to a section. editor_name labels the author for presence and version history.

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
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in PDF URLs). |
| `editor_name` | string | no | Optional display name of the human author, e.g. 'Øivind' — shown for presence and recorded as the version author. |
| `idle_minutes` | integer | no | Optional idle auto-lock window in minutes (5–1440). Omit to use the author's remembered preference, or the default. |
| `open_at` | string | no | Optional section id (a 'blk...' id — e.g. the one in the editor's copyable id-chip) to open the editor AT: appends #<id> so the link lands on that section. Omi… |

## `edit_session_revoke`

**Edit Session Revoke** — writes, closed-world.

Immediately disable a web-editor link previously minted by edit_session_create (e.g. once the author is finished). After this the URL shows the locked page. Idempotent — revoking an already-expired/unknown session still returns ok.

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
| `session_id` | string | yes | The session_id returned by edit_session_create. |

## `editorial_list`

**Editorial List** — read-only, idempotent, closed-world.

List the books on YOUR editable shelf (books you own or are a guest editor on) that are IN the editorial workflow — by default ONLY those waiting to be edited (status=ready), so it answers "what is mine to edit right now, and who is each one's editor?" instantly, not a dump of every book. Newest-marked first. Pass status=approved to see signed-off ones, or status=all for everything in the workflow. assigned_to filters by the editor a book is assigned to: "mine" = assigned to YOU (no need to know your id), or a specific user id (get ids from guest_find_user / guest_list / the editor_user_id this tool returns). editor filters by the editor NAME (substring, case-insensitive) — handy when you only know a name. Index-backed, so it stays instant at thousands of books. Each result carries title, editorial_status, editor + editor_user_id (the WHO), note, owner_id and the reader url.

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
| `assigned_to` | string | no | Filter by assigned editor: "mine" (assigned to you) or a specific Junifye user id. |
| `editor` | string | no | Optional: only books whose primary-editor NAME contains this (case-insensitive). |
| `limit` | integer | no | Max rows to return (default 50, max 200). Omit it, or pass 0, for the default. A NEGATIVE limit is rejected, not clamped. |
| `offset` | integer | no | 0-based row offset for the next page. Omit for the first page; pass the previous offset+limit while has_more is true. A NEGATIVE offset is rejected. |
| `status` | string | no | Which workflow state to list. Default "ready" = books needing edit. |

## `editorial_set`

**Editorial Set** — writes, closed-world.

Set a book's EDITORIAL review state — an opt-in, soft workflow separate from the admin publish/vet pipeline (not every book needs it). status: "ready" = mark it ready for an editor to review (it then shows up in editorial_list), "approved" = an editor has reviewed and signed off (call this AFTER editing), or "none" = remove it from the workflow. editor is the PRIMARY editor NAME — a guide (who we'd like to edit it), not an access lock; anyone with edit rights may still edit or approve. editor_user_id ASSIGNS a specific Junifye user as the editor: unless they are the owner they are automatically added as a guest editor (so they instantly gain edit access AND the book appears in THEIR editorial_list) — owner-only, since it grants access; use guest_find_user to resolve a name to a user id. note is an optional one-line brief. Returns the book's editorial state.

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
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid). |
| `editor` | string | no | Primary editor NAME — a soft guide (who should edit it), not an access lock. Pass "" to clear. Ignored if editor_user_id is given (the name is taken from that … |
| `editor_user_id` | string | no | Assign this Junifye user as the editor and (unless they're the owner) auto-add them as a guest editor so they gain edit access + see it in their editorial_list… |
| `note` | string | no | Optional one-line brief for the editor. Pass "" to clear. |
| `status` | string | no | ready = ready for editorial review; approved = editor signed off (set after editing); none = clear the workflow. |

## `group_accept`

**Group Accept** — writes, closed-world.

Accept an invite to a group (you become a member and gain content-edit access to every book the group is attached to). You must have a pending invite — see group_list.pending_invites.

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
| `group_id` | string | yes | The 'grp...' id of a group you were invited to (group_list.pending_invites). |
| `user_id` | string | no | ADMIN ONLY: accept/decline on behalf of this invited user (support operation — e.g. completing membership for a managed agent account). Omit to act as yourself. |

## `group_admin_set`

**Group Admin Set** — writes, closed-world.

Grant or revoke ADMIN on a group member (admins can invite, rename, and remove non-admin members). Owner only. The target must already be a member.

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
| `admin` | boolean | yes | true = grant admin, false = revoke admin. |
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `user_id` | string | yes | The member's Junifye user id (from group_get.members). |

## `group_autoshare_set`

**Group Autoshare Set** — writes, closed-world.

Toggle YOUR autoshare on a group. With autoshare ON, every NEW book you create is automatically attached to this group (its members can edit it). You must be a member. Pass apply_existing=true (with on=true) to ALSO attach the group to ALL books you currently own — the response reports how many were newly attached. Turning autoshare OFF only stops FUTURE auto-attach; it does NOT detach books already attached (use book_group_remove for those).

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
| `apply_existing` | boolean | no | Only with on=true: also attach the group to every book you already own now. Default false. |
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `on` | boolean | yes | true = auto-attach this group to your future books; false = stop auto-attaching. |
| `user_id` | string | no | ADMIN ONLY: set autoshare on behalf of this member (support operation for managed agent accounts). Omit to act as yourself. |

## `group_create`

**Group Create** — writes, closed-world.

Create a GROUP — a named set of Junifye users you can later attach to a book (book_group_add) so every member becomes a content editor of that book at once. You become the group's owner (and first member). Invite others with group_invite; they must group_accept before they are members. Returns {id:'grp...', name}.

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
| `name` | string | yes | A short human name for the group (required, max 80 chars), e.g. 'Proofreaders' or 'Youth Team'. |

## `group_decline`

**Group Decline** — writes, closed-world.

Decline an invite to a group (drops the pending invite; you do NOT join). You must have a pending invite — see group_list.pending_invites.

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
| `group_id` | string | yes | The 'grp...' id of a group you were invited to (group_list.pending_invites). |
| `user_id` | string | no | ADMIN ONLY: accept/decline on behalf of this invited user (support operation — e.g. completing membership for a managed agent account). Omit to act as yourself. |

## `group_delete`

**Group Delete** — writes, closed-world.

Delete a group. Owner only. This detaches the group from every book it is attached to (those books lose group-editing) and removes it for all members. Irreversible.

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
| `group_id` | string | yes | The 'grp...' id from group_list. |

## `group_get`

**Group Get** — writes, closed-world.

Get one group in detail: members (with display names), each member's admin/owner flag, member_count, attached_books_count, and YOUR role + autoshare. Owners/admins additionally see pending_invites and the attached_book_ids. Only members (or someone you've invited) may view a group.

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
| `group_id` | string | yes | The 'grp...' id from group_create.id or group_list. |

## `group_invite`

**Group Invite** — writes, closed-world.

Invite a Junifye user to a group. Owner or admin only. The invitee is NOT a member until they group_accept (find their user_id with guest_find_user). Rejects inviting an existing member.

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
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `user_id` | string | yes | The Junifye user id (pubhub user id) from guest_find_user. NOT an email. |

## `group_invite_cancel`

**Group Invite Cancel** — writes, closed-world.

Withdraw a pending group invite. Owner or admin only. Idempotent.

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
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `user_id` | string | yes | The invited user's Junifye user id (from group_get pending_invites). |

## `group_leave`

**Group Leave** — writes, closed-world.

Leave a group you are a member of. Leaving also DETACHES the group from every book YOU own. The owner cannot leave — transfer the group (group_transfer) or delete it (group_delete) first.

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
| `group_id` | string | yes | The 'grp...' id from group_list. |

## `group_list`

**Group List** — writes, closed-world.

List the GROUPS you belong to — [{id, name, owner, member_count, role, autoshare}] where role is owner/admin/member and autoshare is YOUR auto-attach opt-in — plus pending_invites: groups you have been invited to but not yet accepted (group_accept / group_decline). PAGED over the groups: `total`/`has_more` describe the memberships, not the invites (those are the caller's own short queue and are returned whole).

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

## `group_member_remove`

**Group Member Remove** — writes, closed-world.

Remove a member from a group. The OWNER may remove any member (except themselves — use group_transfer or group_delete); an ADMIN may remove only non-admin members. Removing a member also DETACHES the group from every book that member OWNS (their books stop being group-editable); books owned by others stay attached.

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
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `user_id` | string | yes | The member's Junifye user id (from group_get.members). |

## `group_rename`

**Group Rename** — writes, closed-world.

Rename a group. Owner or admin only.

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
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `name` | string | yes | New name (required, max 80 chars). |

## `group_transfer`

**Group Transfer** — writes, closed-world.

Hand ownership of a group to another MEMBER. Owner only. The new owner must already be a member; you (the old owner) stay a member and keep admin.

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
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `user_id` | string | yes | The new owner's Junifye user id — must already be a member (group_get.members). |

## `guest_add`

**Guest Add** — writes, closed-world.

Invite a Junifye user as a GUEST EDITOR of a book — they get CONTENT-edit access (chapters/blocks/sections) and the book appears in THEIR library + book-switcher; they never get publication, branding, print, delete, or the ability to manage other guests. Owner-only. Find the user_id with guest_find_user. Idempotent (re-adding is a no-op).

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
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid). |
| `user_id` | string | yes | The Junifye user id (pubhub user id) from guest_find_user. NOT an email. |

## `guest_find_user`

**Guest Find User** — writes, closed-world.

Find Junifye users by NAME to invite as guest editors. Returns [{user_id, name}] for DISCOVERABLE users whose name matches the query (a user can mark themselves not-findable, in which case they never appear here). Use the returned user_id with guest_add. Only existing Junifye users are findable. Empty/blank query returns nothing.

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
| `query` | string | yes | A name (or part of one) to search for among Junifye users. |

## `guest_list`

**Guest List** — writes, closed-world.

List the collaborators of a book. Returns guests: the individual GUEST EDITORS [{user_id, name}], AND groups: the GROUPS attached to the book [{id, name, member_count}] (every member of an attached group is also an editor). Owner-only. The owner is NOT in either list (they own the book outright).

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
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid). |
| `limit` | integer | no | Max rows to return (default 50, max 200). Omit it, or pass 0, for the default. A NEGATIVE limit is rejected, not clamped. |
| `offset` | integer | no | 0-based row offset for the next page. Omit for the first page; pass the previous offset+limit while has_more is true. A NEGATIVE offset is rejected. |

## `guest_remove`

**Guest Remove** — writes, closed-world.

Remove a GUEST EDITOR from a book — revokes their content access and drops the book from their library. Owner-only. Idempotent.

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
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid). |
| `user_id` | string | yes | The guest's Junifye user id (from guest_list). |

## `note_delete`

**Note Delete** — writes, closed-world.

Delete one authoring NOTE, addressed by anchor / block_id / key (same handle used to set it).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `anchor` | string | yes | The note's anchor (idc… chapter or idb… book). |
| `block_id` | string | no | Optional section pin (blk…). |
| `key` | string | no | Optional slot (default 'main'). |
| `work` | boolean | no | Set true to delete a WORK note (shared across the title's editions). |

## `note_get`

**Note Get** — read-only, idempotent, closed-world.

Read one authoring NOTE in full (subject + body) — private scratch, never part of the rendered book. Address it by the same anchor / block_id / key shown in note_list or block_list. orphaned=true means the note's pinned block no longer exists (a rare edge, e.g. after a chapter split) — its text is intact under the chapter; re-pin with note_set or remove with note_delete.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `anchor` | string | yes | The note's anchor (idc… chapter or idb… book). |
| `block_id` | string | no | Optional section pin (blk…), if the note was pinned to a block. |
| `key` | string | no | Optional slot (default 'main'). |
| `work` | boolean | no | Set true to read a WORK note (shared across the title's editions) instead of a per-book note. |

## `note_list`

**Note List** — read-only, idempotent, closed-world.

List authoring NOTES (private scratch — never part of the rendered book) as a compact catalog — subjects only, NO bodies — so it stays context-cheap however many notes exist. scope = a book id (idb…) for every note in the book, or a chapter id (idc…) for that chapter plus all its section notes. Each entry gives anchor / block_id / key / subject / size — scan subjects, then pull the one you want with note_get. An entry tagged chapter_trashed=true is anchored to a chapter that is in the TRASH: the note itself is intact, but the chapter is not part of the book right now (chapter_restore brings both back; a purge destroys both). Optional query filters to notes whose subject or body contains the text (matched entries include a snippet). A book-scope list also surfaces the title's shared WORK notes, tagged scope="work", AND the notes that live on the title's OTHER language editions, tagged scope="sibling" with the book_id / book_title / language they belong to — so research written once on one edition is never invisible from the others. A sibling entry is read with note_get(anchor=<its book_id or chapter anchor>) exactly like any other note; if it turns out to belong to ALL editions, re-file it with note_set(work=true).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | integer | no | Max rows to return (default 50, max 200). Omit it, or pass 0, for the default. A NEGATIVE limit is rejected, not clamped. |
| `offset` | integer | no | 0-based row offset for the next page. Omit for the first page; pass the previous offset+limit while has_more is true. A NEGATIVE offset is rejected. |
| `query` | string | no | Optional. Filter to notes whose subject or body contains this text. |
| `scope` | string | yes | A book id (idb…) for the whole book, or a chapter id (idc…) for that chapter plus its section notes. |

## `note_patch`

**Note Patch** — writes, closed-world.

Surgically edit a NOTE without resending its whole body: replace `find` with `replace`. find must match EXACTLY ONCE — zero or multiple matches return an error rather than guessing. To replace a long span, elide the middle with an ellipsis: find="John was…the beginning of" matches from the unique left text through to the right text. Address the note by the same anchor / block_id / key used in note_set.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `anchor` | string | yes | The note's anchor (idc… chapter or idb… book), same as note_set. |
| `block_id` | string | no | Optional section pin, same blk… id used when the note was set. |
| `find` | string | yes | Exact text to replace; must occur exactly once. Use '…' (or '...') to span: 'left…right' matches from the unique left anchor through the right anchor. |
| `key` | string | no | Optional slot (default 'main'). |
| `replace` | string | yes | Replacement text. |
| `work` | boolean | no | Set true to patch a WORK note (shared across the title's editions). |

## `note_set`

**Note Set** — writes, closed-world.

Create, replace, or append an authoring NOTE — private scratch for you and the author (research, TODOs, decisions, sources). Notes are NEVER rendered into the PDF/HTML and never appear in the published book; bodies are plain text, nothing to escape. anchor = a chapter id (idc…, from chapter_list) for a chapter/section note, or a book id (idb…) for a book-wide note — a block id (blk…) is NOT an anchor; pin a section via block_id. mode=append adds to the existing note instead of overwriting. Set work=true for a note shared across ALL language editions of the title (instead of just this book).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `anchor` | string | yes | WHERE the note attaches: a chapter id (idc…) for a chapter or section note, or a book id (idb…) for a book-wide note. A block id (blk…) is NOT an anchor — pass… |
| `block_id` | string | no | Optional. Pin the note to a section: a blk… id (from block_list) WITHIN the chapter anchor. If that block is deleted the note follows to the next block; a full… |
| `content` | string | yes | The note text. Plain readable UTF-8; never rendered into the book. |
| `key` | string | no | Optional slot (default 'main'). Use a distinct slug like 'todo' to keep more than one note at the same anchor/section. |
| `mode` | string | no | replace (default) overwrites the note; append adds a new line onto the existing body. |
| `subject` | string | no | Optional short one-line header shown in note_list / block_list so the note is findable without reading its body. |
| `work` | boolean | no | Set true to make this a WORK note — shared across ALL language editions of the title (anchor just identifies the family). Title-level, so block_id is not allow… |

## `question_add`

**Question Add** — writes, closed-world.

Create a discoverable question (e.g. "What does the Bible say about baptism?"). It starts with NO answers (status=orphaned) — link it to the book/chapter that answers it with question_link. tags are free-form topic labels (lower-cased + de-duped) for browse filtering. Returns the new question incl. its stable SEO slug.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `lang` | string | no | Optional BCP-47 language code, e.g. "en" or "nb". |
| `tags` | array | no | Optional topic labels, e.g. ["baptism","sacraments"]. |
| `text` | string | yes | The question as a reader would phrase it. |

## `question_delete`

**Question Delete** — writes, closed-world.

Permanently delete a question and all its answer edges (the referenced books/chapters are untouched). To remove only YOUR book's association, prefer question_unlink. Requires admin, or write access to a book this question answers.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The 'idq...' question id to delete. |

## `question_get`

**Question Get** — read-only, idempotent, closed-world.

Fetch one question by id OR slug, with its answer edges resolved (each answer names the book/chapter, its title, whether the book is publicly listed, and the reader path). Use this before question_set/question_link to see the current state.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | no | The 'idq...' question id. |
| `slug` | string | no | The SEO slug (alternative to id). |

## `question_link`

**Question Link** — writes, closed-world.

Attach an answer: this question is answered by book_id, optionally narrowed to chapter_id. short_answer is an optional ≤320-char teaser (the full answer lives in the book); rank orders competing answers (lower first). Re-linking the same book+chapter updates the teaser/rank in place. Requires WRITE access to the book. Marks the question live.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | An 'idb...' id or a public UUID. |
| `chapter_id` | string | no | Optional 'idc...' chapter id; omit for a whole-book answer. |
| `id` | string | yes | The 'idq...' question id. |
| `rank` | integer | no | Optional ordering (lower shown first). |
| `short_answer` | string | no | Optional ≤320-char teaser. |

## `question_list`

**Question List** — read-only, idempotent, closed-world.

Browse questions newest-first, paginated. Optional tag filter. Returns a light view (no answer edges — call question_get for those) plus total/offset/limit/has_more so a UI or agent can page through thousands snappily.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | integer | no | Page size (default 50, max 200). |
| `offset` | integer | no | Start index (default 0). |
| `tag` | string | no | Optional topic filter. |

## `question_set`

**Question Set** — writes, closed-world.

Edit a question's text/tags/lang. The slug is permanent (permalinks must not rot) and is NOT changed. Editing also clears the 'stale' flag (a linked chapter changed) — do this after reviewing the answers. Requires admin, or write access to a book this question answers.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The 'idq...' question id. |
| `lang` | string | no | Optional BCP-47 language code, e.g. "en". |
| `tags` | array | no | Replacement topic labels (replaces the existing set). |
| `text` | string | yes | The revised question text. |

## `question_unlink`

**Question Unlink** — writes, closed-world.

Detach one answer edge (book_id, optionally chapter_id) from a question. Removing the last answer leaves the question orphaned (its text is kept for re-linking), not deleted. Requires WRITE access to the book.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | An 'idb...' id or a public UUID — the book edge to detach. |
| `chapter_id` | string | no | Optional 'idc...' chapter id; omit to detach the whole-book edge. |
| `id` | string | yes | The 'idq...' question id. |

## `vet_decide`

**Vet Decide** — writes, closed-world.

ADMIN. Vet a pending publication request (see vet_list). decision=approve makes the book PUBLIC (sets listed=true, mints its share aliases, adds it to the public library + search) — this is irreversible, like the manual publish flip. decision=reject keeps the book private and records reason, which the owner sees via vet_status (so they can fix it and call publish_request again). reason is REQUIRED when rejecting, optional when approving. Returns {book_id, vet_state, listed, reason}. Valid for a book in vet_state=pending OR vet_state=stalled (one a past automated vetting round gave up on — it is waiting for exactly this human decision); any other state is refused.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the pending book (from vet_list). |
| `decision` | string | yes | approve = make it public (listed); reject = keep it private with a reason. |
| `reason` | string | no | Plain-text reason. REQUIRED for reject (the owner reads it via vet_status); optional for approve. |

## `vet_list`

**Vet List** — read-only, idempotent, closed-world.

ADMIN. List the books currently awaiting a publication-review decision — the queue fed by publish_request. It covers BOTH vet_state='pending' (queued, awaiting a decision) AND vet_state='stalled' (a PAST automated vetting round failed vet_attempts times and gave up; nothing automated will ever move those again). Each entry: {book_id, uuid, title, author, owner_id, language, vet_state, vet_attempts, vet_reason}. The response also carries {count, stalled, reviewed_by} — how many of the returned entries are stalled, and who decides this queue: reviewed_by='human' means automated vetting is switched OFF, so EVERY book listed here is waiting on you and vet_decide is the only thing that will move it; 'agent' means pending books also get an automated pass. This queue holds NON-ADMIN submissions only: an admin's own publish_request publishes immediately and is recorded as a self-approval, so it never appears here — a non-empty queue means outside authors are waiting. Decide each with vet_decide(approve|reject), which is valid for pending AND stalled. Read-only.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | integer | no | Optional cap on how many queued books to return, 1..500. Omitted means 500, not unlimited — the queue is a work list, not an export. |
| `offset` | integer | no | 0-based offset into the queue, for walking past the first page. A NEGATIVE offset is rejected. |
| `state` | string | no | Optional filter. 'pending' = live automated rounds only; 'stalled' = only books whose automated vetting gave up and need a human. Omit for the whole queue. |

## `vet_status`

**Vet Status** — read-only, idempotent, closed-world.

Check whether a book has been approved for public listing, and — if it was rejected — WHY. Returns {book_id, vet_state, vet_reason, listed} — plus reviewed_by while the book is queued (see below). vet_state is one of: '' (private, never submitted), 'pending' (queued for a review decision after publish_request), 'stalled' (a PAST automated vetting round failed repeatedly and gave up — the book is STILL in the review queue awaiting a human; vet_reason holds the failure detail, and calling publish_request again requeues it), 'approved' (an admin approved it — it is now publicly listed), 'rejected' (an admin declined — vet_reason explains why; fix it and call publish_request again). listed mirrors whether the book is currently public. While vet_state is 'pending' or 'stalled' the response also carries reviewed_by: 'human' = automated vetting is switched OFF on this deployment, so an admin reads the book personally and nothing automated will touch it; 'agent' = an automated vetting session reads it first. ADMIN-ONLY: when called by an admin, the response also includes vet_history — the retrospective audit of what review actually happened (an automated vetting session's method + findings, or a line recording that an admin published it with NO review round), empty for a book only ever reviewed by a human; vet_decided_by — the user id that settled it; and self_approved — true when an APPROVED book was published by its own owner acting as admin, i.e. nobody else read it. Non-admin callers (incl. the owner) never see those three keys; they are omitted entirely.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |

## `vet_submit_result`

**Vet Submit Result** — writes, closed-world.

Report the verdict of an agentic publication-vetting session for a book. GATED BY A DEPLOYMENT SWITCH: while agentic vetting is switched off this tool refuses EVERY call (reason='agentic_vetting_disabled') and publication review is human-only — admins decide the queue with vet_list + vet_decide. Check vet_status.reviewed_by ('human' vs 'agent') or publish_request's reviewed_by before assuming a session is expected. Called by the background vetting agent (NOT by authors): supply the book_id and the one-time token from the vetting prompt, result=approve|reject, a reason (REQUIRED on reject), and optionally a history (the internal audit summary of what you checked and how). On approve the book goes PUBLIC exactly as an admin approve does (listed=true, aliases, public library + search). reason is PUBLIC (owner reads it via vet_status); history is ADMIN-ONLY (only admins see it via vet_status) and persists for later retrospect. Only the configured vetting agent or an admin may call this. Returns {book_id, vet_state, listed, reason}.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the book being vetted (from the vetting prompt). |
| `history` | string | no | ADMIN-ONLY internal audit summary (optional): WHAT you verified and HOW — your method, the specific darash lookups you ran, and what you found / any problems. … |
| `reason` | string | no | PUBLIC verdict explanation — the owner reads it via vet_status. REQUIRED on reject — cite the specific problem (chapter + the inaccurate reference/wording). Op… |
| `result` | string | yes | approve = the scriptural content is sound + accurately cited → the book goes public; reject = keep it private with a reason. |
| `token` | string | yes | The one-time round token from the vetting prompt — echo it back VERBATIM. It ties this verdict to the current pending round; a stale/unknown token is rejected. |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
