# Groups, guests and notes

**Share a dictionary, invite an editor, keep private notes.** 26 Lexifye MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://lexifye.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`audit_list`](#audit-list) | The dict's CHANGE HISTORY: who changed what, and when |
| [`group_accept`](#group-accept) | Accept an invite to a group (you become a member and gain content-edit access to every dict… |
| [`group_admin_set`](#group-admin-set) | Grant or revoke ADMIN on a group member (admins can invite, rename, and remove non-admin… |
| [`group_autoshare_set`](#group-autoshare-set) | Toggle YOUR autoshare on a group |
| [`group_create`](#group-create) | Create a GROUP — a named set of lexifye users you can later attach to a dict (dict_group_add)… |
| [`group_decline`](#group-decline) | Decline an invite to a group (drops the pending invite; you do NOT join) |
| [`group_delete`](#group-delete) | Delete a group |
| [`group_get`](#group-get) | Get one group in detail: members (with display names), each member's admin/owner flag,… |
| [`group_invite`](#group-invite) | Invite a lexifye user to a group |
| [`group_invite_cancel`](#group-invite-cancel) | Withdraw a pending group invite |
| [`group_leave`](#group-leave) | Leave a group you are a member of |
| [`group_list`](#group-list) | List the GROUPS you belong to — [{id, name, owner, member_count, role, autoshare}] where role… |
| [`group_member_remove`](#group-member-remove) | Remove a member from a group |
| [`group_rename`](#group-rename) | Rename a group |
| [`group_transfer`](#group-transfer) | Hand ownership of a group to another MEMBER |
| [`guest_add`](#guest-add) | Invite a lexifye user as a GUEST EDITOR of a dict — they get CONTENT-edit access… |
| [`guest_find_user`](#guest-find-user) | Find lexifye users by NAME to invite as guest editors or group members |
| [`guest_list`](#guest-list) | List the collaborators of a dict |
| [`guest_remove`](#guest-remove) | Remove a GUEST EDITOR from a dict — revokes their content access and drops the dict from their… |
| [`note_delete`](#note-delete) | Delete a PRIVATE note at (anchor, key) |
| [`note_get`](#note-get) | Fetch a PRIVATE note (summary + full body) at (anchor, key) |
| [`note_list`](#note-list) | List PRIVATE note summaries (no bodies), newest first |
| [`note_patch`](#note-patch) | Append text to an existing PRIVATE note's body (a convenience wrapper over note_set append=true) |
| [`note_set`](#note-set) | Set (upsert) a PRIVATE authoring note on a dict (anchor=idy…) or entry (anchor=idj…) |
| [`notice_dismiss`](#notice-dismiss) | Clear ALL of YOUR pending notices (after reading them with notice_list) |
| [`notice_list`](#notice-list) | List YOUR pending notices (newest first) — the one-shot lines left when a group membership… |

---

## `audit_list`

**Audit List** — read-only, idempotent, closed-world.

The dict's CHANGE HISTORY: who changed what, and when. Newest first, paginated. EDITOR-level (write), exactly like trash_list and for the same reason: this is editorial history, not content — it names the people who edited the dictionary — so it is limited to those who could have made the edits (owner, guest editors, group members). Reading a dictionary and knowing who worked on it are separate questions, and the read tier also carries the service-to-service lane, which exists to pull content and not personnel. A soft-deleted dict's history is unreadable until dict_restore brings it back.
  This is the companion to trash_list: that one says what is still recoverable, this one says who deleted it and when (and, for a row purged after its grace window, that it was the retention sweep rather than a person).

--- EVENT SHAPE ---
  id — the stream cursor; pass it back as `before` for the next (older) page, or as `after` to poll for what has happened since.
  ts — unix seconds. op — the mutation (dict_create, entry_add, entry_delete, entry_restore, entry_purge, definition_add/update/move/delete/restore/purge, dict_set_*, dict_delete/restore, dict_import, guest_add/remove, group_add/remove).
  actor / actor_name — the pubhub user who made the change, resolved to a display name where one is known. Background work names itself: system:sweep (a trash row purged after its 30-day grace), system:enrich (darash auto-entries), system:import (a rebuild from the S3 export).
  entry_id / def_id / fields — what the op touched; `fields` carries the op-specific payload (term, defs, notes_promoted, …).

--- RETENTION ---
  The stream is capped at the newest 2000 events per dict, so it is an operational log, not an archive; `trimmed:true` means older rows have been dropped. What a dict CONTAINED is durable elsewhere (the <uuid>.json export + its versioned S3 object); how a definition changed is definition_history.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `actor` | string | no | Optional exact actor filter (an idu... user id, or system:sweep / system:enrich / system:import). |
| `after` | string | no | An event id; returns events strictly NEWER than it (polling for what has changed since). |
| `before` | string | no | An event id from a previous page; returns events strictly OLDER than it. |
| `dict_id` | string | yes |  |
| `limit` | integer | no | 1-200 events (default 50). |
| `op` | string | no | Optional exact op filter, e.g. entry_delete. |

## `group_accept`

**Group Accept** — writes, closed-world.

Accept an invite to a group (you become a member and gain content-edit access to every dict the group is attached to). You must have a pending invite — see group_list.pending_invites.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `group_id` | string | yes | The 'grp...' id of a group you were invited to (group_list.pending_invites). |
| `user_id` | string | no | ADMIN ONLY: accept/decline on behalf of this invited user (support operation). Omit to act as yourself. |

## `group_admin_set`

**Group Admin Set** — writes, closed-world.

Grant or revoke ADMIN on a group member (admins can invite, rename, and remove non-admin members). Owner only. The target must already be a member.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `admin` | boolean | yes | true = grant admin, false = revoke admin. |
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `user_id` | string | yes | The member's lexifye user id (from group_get.members). |

## `group_autoshare_set`

**Group Autoshare Set** — writes, closed-world.

Toggle YOUR autoshare on a group. With autoshare ON, every NEW dict you create is automatically attached to this group (its members can edit it). You must be a member. Pass apply_existing=true (with on=true) to ALSO attach the group to ALL dicts you currently own — the response reports how many were newly attached. Turning autoshare OFF only stops FUTURE auto-attach; it does NOT detach dicts already attached (use dict_group_remove for those).

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apply_existing` | boolean | no | Only with on=true: also attach the group to every dict you already own now. Default false. |
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `on` | boolean | yes | true = auto-attach this group to your future dicts; false = stop auto-attaching. |
| `user_id` | string | no | ADMIN ONLY: set autoshare on behalf of this member (support operation). Omit to act as yourself. |

## `group_create`

**Group Create** — writes, closed-world.

Create a GROUP — a named set of lexifye users you can later attach to a dict (dict_group_add) so every member becomes a content editor of that dict at once. You become the group's owner (and first member). Invite others with group_invite; they must group_accept before they are members. Returns {id:'grp...', name}.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | A short human name for the group (required, max 80 chars), e.g. 'Lexicon Team'. |

## `group_decline`

**Group Decline** — writes, closed-world.

Decline an invite to a group (drops the pending invite; you do NOT join). You must have a pending invite — see group_list.pending_invites.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `group_id` | string | yes | The 'grp...' id of a group you were invited to (group_list.pending_invites). |
| `user_id` | string | no | ADMIN ONLY: accept/decline on behalf of this invited user (support operation). Omit to act as yourself. |

## `group_delete`

**Group Delete** — writes, closed-world.

Delete a group. Owner only. This detaches the group from every dict it is attached to (those dicts lose group-editing) and removes it for all members. Irreversible.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `group_id` | string | yes | The 'grp...' id from group_list. |

## `group_get`

**Group Get** — read-only, idempotent, closed-world.

Get one group in detail: members (with display names), each member's admin/owner flag, member_count, attached_dicts_count, and YOUR role + autoshare. Owners/admins additionally see pending_invites and the attached_dict_ids. Only members (or someone you've invited) may view a group.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `group_id` | string | yes | The 'grp...' id from group_create.id or group_list. |

## `group_invite`

**Group Invite** — writes, closed-world.

Invite a lexifye user to a group. Owner or admin only. The invitee is NOT a member until they group_accept (find their user_id with guest_find_user). Rejects inviting an existing member.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `user_id` | string | yes | The lexifye user id (pubhub 'idu...') from guest_find_user. NOT an email. |

## `group_invite_cancel`

**Group Invite Cancel** — writes, closed-world.

Withdraw a pending group invite. Owner or admin only. Idempotent, and HONEST about it: the reply carries cancelled:true only when an invite was actually pending. With nothing pending it returns cancelled:false and the invitee is NOT notified — they never get a 'your invitation was withdrawn' notice for an invitation they never had.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `user_id` | string | yes | The invited user's lexifye user id (from group_get pending_invites). |

## `group_leave`

**Group Leave** — writes, closed-world.

Leave a group you are a member of. Leaving also DETACHES the group from every dict YOU own. The owner cannot leave — transfer the group (group_transfer) or delete it (group_delete) first.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `group_id` | string | yes | The 'grp...' id from group_list. |

## `group_list`

**Group List** — read-only, idempotent, closed-world.

List the GROUPS you belong to — [{id, name, owner, member_count, role, autoshare}] where role is owner/admin/member and autoshare is YOUR auto-attach opt-in — plus pending_invites: groups you have been invited to but not yet accepted (group_accept / group_decline).

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

## `group_member_remove`

**Group Member Remove** — writes, closed-world.

Remove a member from a group. The OWNER may remove any member (except themselves — use group_transfer or group_delete); an ADMIN may remove only non-admin members. Removing a member also DETACHES the group from every dict that member OWNS (their dicts stop being group-editable); dicts owned by others stay attached.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `user_id` | string | yes | The member's lexifye user id (from group_get.members). |

## `group_rename`

**Group Rename** — writes, closed-world.

Rename a group. Owner or admin only.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `name` | string | yes | New name (required, max 80 chars). |

## `group_transfer`

**Group Transfer** — writes, closed-world.

Hand ownership of a group to another MEMBER. Owner only. The new owner must already be a member; you (the old owner) stay a member and keep admin.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `group_id` | string | yes | The 'grp...' id from group_list. |
| `user_id` | string | yes | The new owner's lexifye user id — must already be a member (group_get.members). |

## `guest_add`

**Guest Add** — writes, closed-world.

Invite a lexifye user as a GUEST EDITOR of a dict — they get CONTENT-edit access (entries/definitions) and the dict appears on THEIR dashboard; they never get delete/restore, group attach/detach, transfer, language, author_bio, or the ability to manage other guests. Owner-only. Find the user_id with guest_find_user. Idempotent (re-adding is a no-op).

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes | The 'idy...' id from dict_create.id (NOT the uuid). |
| `user_id` | string | yes | The lexifye user id (pubhub 'idu...') from guest_find_user. NOT an email. |

## `guest_find_user`

**Guest Find User** — writes, closed-world.

Find lexifye users by NAME to invite as guest editors or group members. Returns [{user_id, name, username}] for DISCOVERABLE users whose name/handle contains the query. Use the returned user_id with guest_add / group_invite. Empty/blank query returns nothing.
Matching ignores case AND diacritics on both sides, so 'jorn', 'Jørn' and 'JØRN' all find the same person (æ→ae, ø→o, å→a, ß→ss, é→e …).
TWO KINDS OF USER ARE NEVER RETURNED: (1) YOURSELF — the caller is always excluded, since you never need to invite yourself to your own dict; (2) anyone who has marked themselves not-findable, who never appears in anyone's search. So an empty result means 'nobody else discoverable matches', not 'no such user'.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | A name (or part of one) to search for among lexifye users. |

## `guest_list`

**Guest List** — read-only, idempotent, closed-world.

List the collaborators of a dict. Returns guests: the individual GUEST EDITORS [{user_id, name}], AND groups: the GROUPS attached to the dict [{id, name, member_count}] (every member of an attached group is also an editor). Owner-only. The owner is NOT in either list.
  READ level: seeing who can reach your own dictionary is reading, not writing, so a read-scope credential is enough. The OWNER-ONLY gate is unchanged and is what actually protects the roster — guest_add / guest_remove remain write.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes | The 'idy...' id from dict_create.id (NOT the uuid). |

## `guest_remove`

**Guest Remove** — writes, closed-world.

Remove a GUEST EDITOR from a dict — revokes their content access and drops the dict from their library. Owner-only. Idempotent.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes | The 'idy...' id from dict_create.id (NOT the uuid). |
| `user_id` | string | yes | The guest's lexifye user id (from guest_list). |

## `note_delete`

**Note Delete** — writes, closed-world.

Delete a PRIVATE note at (anchor, key). Editor-only.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `anchor` | string | yes |  |
| `dict_id` | string | yes |  |
| `key` | string | no |  |

## `note_get`

**Note Get** — read-only, idempotent, closed-world.

Fetch a PRIVATE note (summary + full body) at (anchor, key). Editor-only. Returns {note, content}.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `anchor` | string | yes |  |
| `dict_id` | string | yes |  |
| `key` | string | no | slot; default 'main' |

## `note_list`

**Note List** — read-only, idempotent, closed-world.

List PRIVATE note summaries (no bodies), newest first. Omit anchor to list the whole dict; pass a dict/entry id to filter to that anchor. Editor-only.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `anchor` | string | no | optional dict/entry id filter |
| `dict_id` | string | yes |  |
| `limit` | integer | no |  |
| `offset` | integer | no |  |

## `note_patch`

**Note Patch** — writes, closed-world.

Append text to an existing PRIVATE note's body (a convenience wrapper over note_set append=true). Optionally updates the subject. Editor-only.
  WHAT GOES IN append: the text to ADD to the existing body, as PLAIN TEXT, stored verbatim. Notes are never parsed as markup and never rendered into any artifact, so [h:H2617:ḥesed:חֶסֶד] stays those literal characters. `content`, `body` and `source` are accepted aliases for this same field; passing two spellings at once is refused. The canonical name stays `append` because it says what the call DOES — note_set(content) replaces, note_patch(append) adds.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `anchor` | string | yes |  |
| `append` | string | yes | The text to append to the note's body, as PLAIN TEXT — never parsed as markup, never rendered. |
| `body` | string | no | Accepted ALIAS for append — the same field, under the name a sibling tool uses for it. Pass append; passing two spellings at once is refused rather than resolv… |
| `content` | string | no | Accepted ALIAS for append — the same field, under the name a sibling tool uses for it. Pass append; passing two spellings at once is refused rather than resolv… |
| `dict_id` | string | yes |  |
| `key` | string | no |  |
| `source` | string | no | Accepted ALIAS for append — the same field, under the name a sibling tool uses for it. Pass append; passing two spellings at once is refused rather than resolv… |
| `subject` | string | no |  |

## `note_set`

**Note Set** — writes, closed-world.

Set (upsert) a PRIVATE authoring note on a dict (anchor=idy…) or entry (anchor=idj…). Notes are editor-only and NEVER render into any artifact or the public JSON — use them for research, TODOs, provenance. key is an optional slot (default 'main') so one anchor can hold several notes. subject is a short one-line header. append=true concatenates onto the existing body instead of replacing.
  WHAT GOES IN content: the note's body as PLAIN TEXT, stored and returned verbatim. It is NOT parsed as markup and NOT rendered anywhere — write [h:H2617:ḥesed:חֶסֶד] into a note and those literal characters are what you get back, so keep markup for definition_set_source. `body` and `source` are accepted aliases for this same field; passing two spellings at once is refused.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `anchor` | string | yes | idy… (dict) or idj… (entry) — the note's owner |
| `append` | boolean | no |  |
| `body` | string | no | Accepted ALIAS for content — the same field, under the name a sibling tool uses for it. Pass content; passing two spellings at once is refused rather than reso… |
| `content` | string | yes | The note's body, stored as PLAIN TEXT — never parsed as markup, never rendered. |
| `dict_id` | string | yes |  |
| `key` | string | no | slot; default 'main' |
| `source` | string | no | Accepted ALIAS for content — the same field, under the name a sibling tool uses for it. Pass content; passing two spellings at once is refused rather than reso… |
| `subject` | string | no |  |

## `notice_dismiss`

**Notice Dismiss** — writes, closed-world.

Clear ALL of YOUR pending notices (after reading them with notice_list). Idempotent — dismissing an empty inbox succeeds. Returns {ok:true}.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

## `notice_list`

**Notice List** — read-only, idempotent, closed-world.

List YOUR pending notices (newest first) — the one-shot lines left when a group membership change affects you (invited to / removed from / handed / deleted-out-from-under a group). Non-destructive: call notice_dismiss to clear them. Returns {notices:[...], count}.

--- IDENTIFIERS ---
Dict id = 'idy...', entry id = 'idj...', definition id = 'idf...', group id = 'grp...'. Always pass the type-matching id. A dict also has a uuid (8-4-4-4-12) used ONLY in artifact download URLs (which are NOT public — every one takes the same membership gate), never in MCP calls. A user id is a pubhub 'idu...' value (resolve names with guest_find_user), never an email.

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
