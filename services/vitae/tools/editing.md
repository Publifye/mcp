# Editing a CV

**How do you change what the CV says?** 12 Vitae MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://vitae.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`basics_set`](#basics_set) | write | Set the identity and contact block: {cv_id, basics:{name?, label?, email?, phone?, url?,… |
| [`section_set`](#section_set) | write | Replace a whole non-work section in one edition: {cv_id, lang, section, items}.   sectio… |
| [`entry_add`](#entry_add) | write | Append a WORK role to one language edition (for a degree or course use education_add): {… |
| [`entry_update`](#entry_update) | write | Replace one WORK role in one edition: {cv_id, lang, key \| index, entry}.   WORK ONLY. Fo… |
| [`entry_delete`](#entry_delete) | write | Remove one WORK role from one edition: {cv_id, lang, key \| index}.   ADDRESS IT BY `key`… |
| [`entry_move`](#entry_move) | write | Reorder a role within one edition: {cv_id, lang, from, to}.   ONLY MEANINGFUL BETWEEN RO… |
| [`entry_add_pair`](#entry_add_pair) | write | Append the SAME role to two language editions, atomically across both or neither: {cv_id… |
| [`entry_update_pair`](#entry_update_pair) | write | Replace the SAME role in both editions, atomically: {cv_id, key \| index, entry_a, entry_… |
| [`entry_delete_pair`](#entry_delete_pair) | write | Remove the SAME role from both editions, atomically: {cv_id, key, lang_a, lang_b}.   Bot… |
| [`education_add`](#education_add) | write | Add one education entry to one edition: {cv_id, lang, entry}.   entry: {institution, stu… |
| [`education_update`](#education_update) | write | Replace one education entry: {cv_id, lang, key \| index, entry}.   EDUCATION ONLY. For a … |
| [`education_delete`](#education_delete) | write | Remove one education entry: {cv_id, lang, key \| index}.   ADDRESS BY `key`. A delete aim… |

---

## `basics_set`

**Basics Set** — writes, closed-world · access: `write`.

Set the identity and contact block: {cv_id, basics:{name?, label?, email?, phone?, url?, location?}, lang?}.
  A PARTIAL UPDATE, unlike most write tools here: only the keys you send are touched, and sending a key with "" CLEARS it. That is the difference between adding a phone number and removing one, and a whole-block replace could not express the second.
  OMIT `lang` to write EVERY edition, which is the right default — a phone number, an email and a city are the same facts in every language, and the editions must name the same person. Pass `lang` only for something genuinely language-specific, such as `label`, and run parity_check after.
  The summary is NOT here: use section_set(section="summary"). basics.image and basics.profiles are §6 always-hidden and are not settable.
  Unknown or camelCase keys are REFUSED, never dropped — a silently ignored `countryCode` is a contact detail the owner believes they set.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `basics` | object | yes | snake_case. name, label, email, phone, url, location{city, region, country_code, address, postal_code}. Only the keys present are changed; "" clears a field. |
| `cv_id` | string | yes |  |
| `lang` | string | no | one edition; OMIT to write them all |

## `section_set`

**Section Set** — writes, closed-world · access: `write`.

Replace a whole non-work section in one edition: {cv_id, lang, section, items}.
  section is one of: skills, languages, certificates, summary. Replaces the section outright — read it with cv_get first if you mean to append.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `items` | array | no | for skills/languages/certificates; "Name: a, b, c" is split into name and keywords |
| `lang` | string | yes |  |
| `section` | string | yes |  |
| `text` | string | no | for summary |

## `entry_add`

**Entry Add** — writes, closed-world · access: `write`.

Append a WORK role to one language edition (for a degree or course use education_add): {cv_id, lang, entry:{name, position, start_date, end_date?, summary?, highlights?[]}}.
  OMIT end_date for an ongoing role. An empty string is REJECTED, not read as "ongoing" — JSON Resume expresses ongoing by the ABSENCE of the key, and guessing which the author meant is the coercion this service refuses.
  Single-language writes are the ESCAPE HATCH, not the default: prefer entry_add_pair, because parity between editions is the thing this service is for. Run parity_check after.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `entry` | object | yes |  |
| `lang` | string | yes |  |

## `entry_update`

**Entry Update** — writes, closed-world · access: `write`.

Replace one WORK role in one edition: {cv_id, lang, key | index, entry}.
  WORK ONLY. For a degree or a course use education_update — the sections are addressed separately, and a key that exists in education is simply not found here.
  ADDRESS IT BY `key` ("Employer@2025-04", from cv_get/cv_diff/cv_changelog). Entries are sorted by date on every write, so an INDEX read a moment ago can point at a different role by the time you write — that has overwritten the wrong job on a real CV. A key does not depend on order.
  If you must use `index`, send `fingerprint` (from cv_get) and the write is REFUSED if that slot now holds something else.
  ONE LANGUAGE ONLY. To change a role in both editions use entry_update_pair, which writes both or neither — two separate calls can leave the editions divergent, which is the thing parity exists to prevent.
  Fields are snake_case: start_date, end_date. To mark a role FINISHED supply end_date; to mark it ONGOING omit the key entirely.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `entry` | object | yes |  |
| `fingerprint` | string | no | content hash of the entry you read, from cv_get; refuses the write if the slot moved |
| `index` | integer | no | 0-based position in work[]; prefer key |
| `key` | string | no | Employer@YYYY-MM — preferred, survives reordering |
| `lang` | string | yes |  |

## `entry_delete`

**Entry Delete** — writes, closed-world · access: `write`.

Remove one WORK role from one edition: {cv_id, lang, key | index}.
  ADDRESS IT BY `key` ("Employer@2025-04"). Entries are sorted by date, so an index can move between reading and writing — and a delete aimed at a stale position removes a job the caller never looked at. With `index`, send `fingerprint` from cv_get and the delete is refused if the slot moved.
  Recoverable: the previous state is a version, so cv_history and cv_revert bring it back. 365 edits per edition on every plan.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `fingerprint` | string | no | content hash from cv_get |
| `index` | integer | no |  |
| `key` | string | no | Employer@YYYY-MM — preferred |
| `lang` | string | yes |  |

## `entry_move`

**Entry Move** — writes, closed-world · access: `write`.

Reorder a role within one edition: {cv_id, lang, from, to}.
  ONLY MEANINGFUL BETWEEN ROLES THAT START IN THE SAME MONTH. Entries are stored and rendered in reverse-chronological order, applied on every write and again on every render, so a move that contradicts the dates is undone immediately. It is REFUSED rather than silently reverted, and the refusal names entry_update — if a role is in the wrong place, its DATES are wrong, and fixing the order without fixing the dates would leave the CV lying about when the work happened.
  Two roles that began the same month keep whatever order you give them: the sort is stable, so that is the case this tool is for.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `from` | integer | yes |  |
| `lang` | string | yes |  |
| `to` | integer | yes |  |

## `entry_add_pair`

**Entry Add Pair** — writes, closed-world · access: `write`.

Append the SAME role to two language editions, atomically across both or neither: {cv_id, lang_a, entry_a, lang_b, entry_b}.
  THE DEFAULT WAY TO ADD A ROLE. Parity between editions is this service's differentiator, and a role added to one language only is how a CV quietly starts saying different things to different readers.
  Refused before anything is written if the two entries would leave the editions structurally diverged — different dates, or one ongoing and one ended. Prose and job titles are expected to differ; that is what a translation IS.
  On any failure mid-write, BOTH editions are rolled back to what they were.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `entry_a` | object | yes | the role as written in lang_a |
| `entry_b` | object | yes | the SAME role as written in lang_b — same dates, same ongoing state |
| `lang_a` | string | yes |  |
| `lang_b` | string | yes |  |

## `entry_update_pair`

**Entry Update Pair** — writes, closed-world · access: `write`.

Replace the SAME role in both editions, atomically: {cv_id, key | index, entry_a, entry_b, lang_a, lang_b}.
  Both editions or neither. Two separate entry_update calls can leave the languages divergent — this cannot, and it refuses if the result would not be in parity.
  ADDRESS BY `key` ("Employer@2025-04"): entries are sorted by date, so an index can point at a different role by the time the write lands, and the two editions need not even hold that role at the same position.
  Fields are snake_case: start_date, end_date. Omit end_date for an ongoing role.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `entry_a` | object | yes |  |
| `entry_b` | object | yes |  |
| `index` | integer | no | fallback only; prefer key |
| `key` | string | no | Employer@YYYY-MM — preferred; resolved per edition |
| `lang_a` | string | yes |  |
| `lang_b` | string | yes |  |

## `entry_delete_pair`

**Entry Delete Pair** — writes, closed-world · access: `write`.

Remove the SAME role from both editions, atomically: {cv_id, key, lang_a, lang_b}.
  Both editions or neither. Deleting a role from one language and forgetting the other is how a CV comes to say different things to different readers.
  Recoverable: the previous state of each edition is a version, so cv_history and cv_revert bring it back.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `key` | string | yes | Employer@YYYY-MM, from cv_get or cv_changelog |
| `lang_a` | string | yes |  |
| `lang_b` | string | yes |  |

## `education_add`

**Education Add** — writes, closed-world · access: `write`.

Add one education entry to one edition: {cv_id, lang, entry}.
  entry: {institution, study_type, area, start_date, end_date, url, score, courses}. Snake_case — sending JSON Resume's studyType or startDate is REFUSED rather than dropped.
  Inserted in date order automatically; there is no position to choose. Studies still in progress OMIT end_date entirely.
  Adding the same entry to both editions? Do both, then parity_check.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `entry` | object | yes |  |
| `lang` | string | yes |  |

## `education_update`

**Education Update** — writes, closed-world · access: `write`.

Replace one education entry: {cv_id, lang, key | index, entry}.
  EDUCATION ONLY. For a job use entry_update.
  ADDRESS BY `key` ("NTNU in Trondheim@2003-08", from cv_get's `entries`). Entries are sorted by date, so an index can point at a different entry by the time the write lands.
  The entry REPLACES the old one wholly — send every field you want to keep, or it is dropped.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `entry` | object | yes |  |
| `index` | integer | no |  |
| `key` | string | no | Institution@YYYY-MM — preferred |
| `lang` | string | yes |  |

## `education_delete`

**Education Delete** — writes, closed-world · access: `write`.

Remove one education entry: {cv_id, lang, key | index}.
  ADDRESS BY `key`. A delete aimed at a stale position removes something the caller never looked at.
  Recoverable: the previous state is a version, so cv_history and cv_revert bring it back.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `index` | integer | no |  |
| `key` | string | no |  |
| `lang` | string | yes |  |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-24, version 0.2.63. Regenerate rather than edit by hand.*
