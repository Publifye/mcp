# Your CVs

**Which CVs do you have, and how do you bring one in or take it out?** 9 Vitae MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://vitae.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`cv_create`](#cv_create) | write | Create a CV: {cv_id, slug, name, langs[]}. Returns the new document.   It lands UNPUBLIS… |
| [`cv_list`](#cv_list) | read | List the CVs you own: {cvs:[{id, slug, visibility, langs, updated_at, unpublish_at?}]}. … |
| [`cv_get`](#cv_get) | read | Read one CV edition: {cv:{...}, document:{JSON Resume}, entries:{work:[...], education:[… |
| [`cv_set`](#cv_set) | write | Change a CV's ADDRESS and appearance: {cv_id, slug?, theme?}. At least one of them.   TH… |
| [`cv_validate`](#cv_validate) | read | Validate a JSON Resume document WITHOUT storing it. Returns {valid:true} or every proble… |
| [`cv_import`](#cv_import) | write | REPLACE one edition wholesale with a supplied JSON Resume document: {cv_id, lang, docume… |
| [`import_stage`](#import_stage) | write | Stage an import for review WITHOUT writing anything: {cv_id, editions:{lang: document}, … |
| [`import_confirm`](#import_confirm) | write | Apply an import that is waiting for confirmation: {cv_id, stage_id?}.   Call it WITHOUT … |
| [`cv_export`](#cv_export) | read | Export a CV as JSON Resume — the anti-lock-in promise (spec §5): owners export their own… |

---

## `cv_create`

**CV Create** — writes, closed-world · access: `write`.

Create a CV: {cv_id, slug, name, langs[]}. Returns the new document.
  It lands UNPUBLISHED, always. Publishing is a separate deliberate act (visibility_set published) — nothing here is visible to anyone until its owner says so.
  Creates one empty JSON Resume edition per language, all carrying the same basics.name, because the editions must name the same person.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `langs` | array | yes |  |
| `name` | string | yes | the person's name, as published |
| `slug` | string | yes | the public URL segment; must be free |

## `cv_list`

**CV List** — read-only, idempotent, closed-world · access: `read`.

List the CVs you own: {cvs:[{id, slug, visibility, langs, updated_at, unpublish_at?}]}.
  visibility is "published" or "unpublished" — the only two states (a legacy stored link/public reads as published, private/password as unpublished). unpublish_at appears only when visibility_set was given a ttl. The old `indexable` field is gone: nothing is ever search-indexed.
  Returns YOUR documents only — ownership is checked per document against the caller's identity, and `tool_access_levels` are service-wide roles, not per-document permission (spec §8.1). Reads the per-user index, never a key scan.

*No parameters.*

## `cv_get`

**CV Get** — read-only, idempotent, closed-world · access: `read`.

Read one CV edition: {cv:{...}, document:{JSON Resume}, entries:{work:[...], education:[...]}}.
  `entries` is the ADDRESS BOOK — each item carries `key` ("Employer@2025-04"), `fingerprint` and `index`. Pass the key to entry_update, entry_delete, entry_update_pair or entry_delete_pair. Do not build a key by hand and do not use a bare index: entries are sorted by date, so a position can move between reading and writing.
  The OWNER view — complete, unredacted. What a non-owner sees comes from the single redaction function and is a different shape; do not confuse the two.
  Returns an error rather than an empty document when the edition does not exist: absent and empty are different answers.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes | the document id |
| `lang` | string | yes | language edition, e.g. "en" or "no" |

## `cv_set`

**CV Set** — writes, closed-world · access: `write`.

Change a CV's ADDRESS and appearance: {cv_id, slug?, theme?}. At least one of them.
  THE OLD ADDRESS STOPS RESOLVING AND THERE IS NO REDIRECT. That is deliberate (spec §4): a redirect from the old name proves that a named person's CV moved here, which is itself a disclosure. Anyone holding the old link gets the same "nothing here" as a stranger guessing.
  What does NOT lapse is publication. Renaming changes where the CV answers; it does not unpublish it, and visibility is untouched — use visibility_set for that.
  REFUSES a slug that is already taken and REFUSES a reserved word (health, mcp, admin, cv, api, …) rather than mangling it into something free. A slug that shadowed a route would replace a working page with someone's CV.
  Does NOT change the PERSON'S NAME. That lives in basics.name inside each language edition — change it with cv_import, or copy it from your account with contact_sync.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `slug` | string | no | the new public URL segment: letters, digits, - and _ , max 64. Must be free and not reserved. |
| `theme` | string | no | render theme id: lowercase letters, digits and - , max 32 |

## `cv_validate`

**CV Validate** — read-only, idempotent, closed-world · access: `read`.

Validate a JSON Resume document WITHOUT storing it. Returns {valid:true} or every problem found at once.
  Use before cv_import to see what would be rejected. The service REJECTS malformed documents rather than repairing them (principle 3), so this is how you find out what to fix.
  Reports ALL problems, not the first — an agent driving this cannot see the file, and one error per round trip makes fixing an import a dozen calls.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | the JSON Resume document to check |

## `cv_import`

**CV Import** — writes, closed-world · access: `write`.

REPLACE one edition wholesale with a supplied JSON Resume document: {cv_id, lang, document}.
  THIS IS A WHOLE-DOCUMENT REPLACE, NOT A MERGE. Everything not in `document` is GONE — including edits made after you read the document. To change one role or course use entry_update / education_update instead; reach for cv_import only when you genuinely mean to replace the entire edition.
  PASS `expect_source_hash` — take it from cv_get and the import REFUSES to run if the stored edition changed in between, instead of silently reverting the change. Importing over an EXISTING edition without it is refused outright; use `replace_unconditionally` only for a first import or to repair a quarantined edition.
  Validated at the gate — a malformed document is REJECTED, never repaired by guessing. Use cv_validate first to see every problem at once.
  The previous content becomes a version, so an import can be undone with cv_revert.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `document` | object | yes | a JSON Resume v1 document — the COMPLETE edition, since this replaces rather than merges |
| `expect_source_hash` | string | no | the source_hash from the cv_get you based this document on. REQUIRED IN PRACTICE when the edition already exists: without it, or without replace_unconditionally, the import is refused rather than overwriting blind. |
| `lang` | string | yes |  |
| `replace_unconditionally` | boolean | no | discard whatever is stored without checking. For a FIRST import, or for repairing an edition so broken that cv_get quarantines it and no source_hash can be obtained. Never the convenient way to skip the check. |

## `import_stage`

**Import Stage** — writes, closed-world · access: `write`.

Stage an import for review WITHOUT writing anything: {cv_id, editions:{lang: document}, source?}. Returns the stage_id and what it would change.
  THE PRODUCER FOR import_confirm, and the safe way to replace several editions at once: nothing is written until you confirm, every edition is validated now rather than at apply time, and the source_hash of each target is recorded so a confirmation cannot silently overwrite an edit made while you were reviewing.
  Prefer this over cv_import when replacing MORE THAN ONE edition — cv_import writes one language immediately, and two of those cannot be made atomic. Prefer entry_update / education_update over both when changing a single entry.
  One pending import per CV: staging again replaces what was waiting.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `editions` | object | yes | lang -> a complete JSON Resume v1 document, e.g. {"en":{...},"no":{...}}. Each REPLACES that whole edition. |
| `source` | string | no | where this came from, for the audit trail and the review screen — e.g. "linkedin", "jsonresume", "hand-edited". Defaults to "mcp". |

## `import_confirm`

**Import Confirm** — writes, closed-world · access: `write`.

Apply an import that is waiting for confirmation: {cv_id, stage_id?}.
  Call it WITHOUT stage_id to see what is pending — which editions, how many roles, and the stage_id. Call it again WITH that stage_id to apply. Nothing is written on the first call.
  The stage_id names exactly the content you reviewed. If a newer upload replaced it in between, the id no longer matches and the call is REFUSED rather than applying something you did not look at.
  It also REFUSES if a target edition changed after staging — the preview lists those under `changed_since_staged`. Confirming would discard edits made while the import waited, so say replace_unconditionally if that is genuinely what you mean.
  Every edition is validated BEFORE any is written, and a single invalid edition refuses the whole import — a malformed document is rejected, never repaired by guessing.
  Recoverable: what each edition held becomes a version first, so cv_history and cv_revert bring the old content back. Use cv_validate to see what is wrong with a rejected import.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `replace_unconditionally` | boolean | no | apply even though editions changed after staging, discarding those changes. The preview names them under changed_since_staged; read them first. |
| `stage_id` | string | no | the id from the pending listing. Omit to see what is pending without writing anything. |

## `cv_export`

**CV Export** — read-only, idempotent, closed-world · access: `read`.

Export a CV as JSON Resume — the anti-lock-in promise (spec §5): owners export their own data in full, free, on every plan, and export is NEVER metered.
  OWNER ONLY. This tool refuses anyone else outright rather than returning a redacted view — a non-owner who wants the public document reads the public URL, which goes through internal/redact.ForPublic, the same redaction that serves the page and the PDF.
  Output validates against the published JSON Resume schema, so it renders in any third-party theme.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `allow_partial` | boolean | no | return the editions that ARE readable, with an explicit problems list, instead of refusing. Default false: a partial export must never be mistaken for a whole one. |
| `cv_id` | string | yes |  |
| `lang` | string | no | one edition; omit for all |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-24, version 0.2.63. Regenerate rather than edit by hand.*
