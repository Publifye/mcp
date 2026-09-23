# Languages and history

**Do the language editions agree, and what changed?** 9 Vitae MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://vitae.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`parity_check`](#parity_check) | read | Compare two language editions STRUCTURALLY and report where they disagree: {in_parity:bo… |
| [`versions_get`](#versions_get) | read | Read how deep this CV's history goes: {cv_id} -> {max_versions, default, per_edition:[{l… |
| [`versions_set`](#versions_set) | write | Set how deep this CV's history goes: {cv_id, max_versions, confirm_destroy?}.   RAISING … |
| [`cv_history`](#cv_history) | read | List the retained versions of one edition, newest first: {versions:[{hash, at, by}]}.   … |
| [`cv_changelog`](#cv_changelog) | read | The history AS A CHANGELOG: what actually changed at each edit, newest first.   {cv_id, … |
| [`cv_diff`](#cv_diff) | read | Compare ANY two points in the history, however far apart: {cv_id, lang, from\|since, to?\|… |
| [`cv_revert`](#cv_revert) | write | Restore one edition to an earlier version: {cv_id, lang, hash}.   Hashes come from cv_hi… |
| [`cv_restore`](#cv_restore) | write | Roll the WHOLE CV back to how it stood at a moment in time: {cv_id, at}.   This is the s… |
| [`cv_cherry_pick`](#cv_cherry_pick) | write | Take ONE thing back from a past version, leaving everything else alone: {cv_id, lang, ha… |

---

## `parity_check`

**Parity Check** — read-only, idempotent, closed-world · access: `read`.

Compare two language editions STRUCTURALLY and report where they disagree: {in_parity:bool, divergences:[{path, a, b, message}]}.
  Prose is expected to differ — that is what an edition IS. What must not differ is the skeleton: the same roles in the same order, the same dates, and the same ones marked ongoing. A reader of either edition must learn the same facts.
  The check that matters most: one edition saying a role is CURRENT while the other says it ended. Run by hand three times in one session against the old app, it found a real defect.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `lang_a` | string | yes |  |
| `lang_b` | string | yes |  |

## `versions_get`

**Versions Get** — read-only, idempotent, closed-world · access: `read`.

Read how deep this CV's history goes: {cv_id} -> {max_versions, default, per_edition:[{lang, retained}]}.
  365 by default — a year of daily edits, far more than a CV sees. History is never a paid feature and never expires with a subscription.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |

## `versions_set`

**Versions Set** — writes, closed-world · access: `write`.

Set how deep this CV's history goes: {cv_id, max_versions, confirm_destroy?}.
  RAISING it is free and takes effect on the next edit. LOWERING it evicts immediately and IRREVERSIBLY — the versions beyond the new depth are gone, and their bodies are deleted once nothing else references them.
  So a lowering call is REFUSED unless confirm_destroy names the exact number of versions it will destroy. Call it once without that field to be told the number; the service will not guess that you meant it.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `confirm_destroy` | integer | no | required when LOWERING: the exact number of versions this will destroy |
| `cv_id` | string | yes |  |
| `max_versions` | integer | yes | retained edits per edition; 365 is the default |

## `cv_history`

**CV History** — read-only, idempotent, closed-world · access: `read`.

List the retained versions of one edition, newest first: {versions:[{hash, at, by}]}.
  365 edits per language edition, for every user on every plan, always — history is not a paid feature and never expires with a subscription. Eviction is strictly oldest-first; the newest edit is never the one dropped.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `lang` | string | yes |  |

## `cv_changelog`

**CV Changelog** — read-only, idempotent, closed-world · access: `read`.

The history AS A CHANGELOG: what actually changed at each edit, newest first.
  {cv_id, lang, limit?} -> [{hash, at, by, text, changes:[{section, key, kind, label, summary}]}]
  `text` is the human-readable rendering; `changes` is the structured form to act on. kind is added | removed | modified | ambiguous.
  `removed` is the interesting one: it is what USED to be in the CV, which is exactly what you are looking at when you want something back — feed its `key` straight to cv_cherry_pick.
  `ambiguous` is the one you CANNOT act on: two or more entries share that employer and start date, so the service will not guess which one moved and cv_cherry_pick will refuse the key. Fix it with entry_update, or pick the whole section.
  CHEAP. Each edit's diff was recorded when the edit happened, so this reads pointers and summaries only and decompresses no documents. Comparing versions that are NOT adjacent is cv_diff, which does have to decompress.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `lang` | string | yes |  |
| `limit` | integer | no | how many recent edits to return; default 50 |

## `cv_diff`

**CV Diff** — read-only, idempotent, closed-world · access: `read`.

Compare ANY two points in the history, however far apart: {cv_id, lang, from|since, to?|until?}.
  Address the ends by HASH (from/to) or by TIME (since/until) — "what changed since yesterday" is the common question and should not require looking up hashes first.
  COSTS TWO READS REGARDLESS OF THE GAP. Comparing across 89 edits decompresses the two EDGE versions and diffs them; it does not walk the 88 in between. So asking for a wide range is cheap, and the answer is the NET change — if you added a role and removed it again, it will not appear.
  Entries are matched by EMPLOYER + START DATE, not by position: a role that moved because a newer job was added is still the same role.
  include_documents also returns BOTH full documents, for when you want to read them side by side rather than only what differs. Off by default — a CV is several kB each.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `from` | string | no | older version hash, from cv_changelog |
| `include_documents` | boolean | no | also return both full documents |
| `lang` | string | yes |  |
| `since` | string | no | RFC3339 time instead of a from-hash: the newest version at or before this moment |
| `to` | string | no | newer version hash; omit for the current document |
| `until` | string | no | RFC3339 time instead of a to-hash |

## `cv_revert`

**CV Revert** — writes, closed-world · access: `write`.

Restore one edition to an earlier version: {cv_id, lang, hash}.
  Hashes come from cv_history. The revert is itself an edit: it becomes the newest version, so reverting is never destructive and can be undone by reverting again.
  Reverts ONE language. Check parity_check afterwards, or the editions will disagree.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `hash` | string | yes | a hash from cv_history |
| `lang` | string | yes |  |

## `cv_restore`

**CV Restore** — writes, closed-world · access: `write`.

Roll the WHOLE CV back to how it stood at a moment in time: {cv_id, at}.
  This is the snapshot restore. cv_revert restores ONE edition, which is not the same thing: reverting each language separately walks the document through states it was never actually in, and a failure halfway leaves it in one of them permanently.
  Every edition is resolved to its newest version at or before `at`, then all of them are written ALL OR NOTHING. An edition with no version that old is LEFT ALONE, not emptied — "did not exist yet" and "was empty" are different facts and the service will not guess between them.
  Non-destructive: the restore is itself an edit, so it becomes the newest version and you can undo it by restoring to a moment before it. Bounded by the retained depth (versions_get) — anything evicted is genuinely gone.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `at` | string | yes | RFC3339 timestamp, e.g. 2026-08-11T09:00:00Z. Times come from cv_history. |
| `cv_id` | string | yes |  |

## `cv_cherry_pick`

**CV Cherry Pick** — writes, closed-world · access: `write`.

Take ONE thing back from a past version, leaving everything else alone: {cv_id, lang, hash, section, key}.
  The surgical alternative to cv_revert (whole edition) and cv_restore (whole document). The realistic case: you cut a role for one application and want it back without undoing everything since.
  section is work | education | summary | skills | languages | certificates. For work and education, `key` names ONE entry and comes from cv_diff or cv_changelog. The other sections are replaced whole, because they are lists people rewrite as a unit and merging them item by item would invent an ordering nobody chose.
  A restored role is reinserted in DATE ORDER, not appended — a CV is read by recency, and a 2019 role sitting after a 2025 one looks wrong in a way its owner may not notice before sending it.
  An ordinary edit: validated, versioned, undoable. It changes ONE language, so run parity_check after.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `hash` | string | yes | the version to take it from |
| `key` | string | no | required for work and education: the entry key from cv_diff |
| `lang` | string | yes |  |
| `section` | string | yes |  |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-24, version 0.2.63. Regenerate rather than edit by hand.*
