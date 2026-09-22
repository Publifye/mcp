# Listen, prepare and download

**Can the user hear this chapter, and can they keep it?** 6 Audio Bible MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://audiobible.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`get_chapter`](#get-chapter) | read | Read one chapter of the World English Bible: every verse's text, numbered, plus whether … |
| [`listen_link`](#listen-link) | read | Links for LISTENING to a chapter (optionally starting at a verse): the public reading pa… |
| [`prepare_chapter`](#prepare-chapter) | read | Have a chapter read aloud (recorded) if it is not already, using the same queue as the w… |
| [`chapter_progress`](#chapter-progress) | read | How far a chapter's recording has got, without starting anything. Safe to poll every few… |
| [`download_link`](#download-link) | read | A personal download link for recorded chapters, as an .opus file (one chapter) or a ZIP … |
| [`my_allowance`](#my-allowance) | read | The user's standing: plan, download allowance left in the rolling 24 hours and when the … |

---

## `get_chapter`

**Get Chapter** — read-only, idempotent, closed-world · access: `read`.

Read one chapter of the World English Bible: every verse's text, numbered, plus whether its audio is recorded. Quote the verses exactly as returned; do not paraphrase them as scripture. Free for any signed-in user.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book` | string | yes | Book slug such as 'genesis', 'john' or 'first-samuel'. Common names ('1 sam', 'psalm') are resolved. Call list_books for all 66. |
| `chapter` | integer | yes | Chapter number within the book, starting at 1. |

## `listen_link`

**Listen Link** — read-only, idempotent, closed-world · access: `read`.

Links for LISTENING to a chapter (optionally starting at a verse): the public reading page, which plays the audio with the verse highlighted, and the direct streaming audio URL with the verse's start and end in seconds. Listening is free and uses no download allowance. If the chapter is not recorded yet the result says so — call prepare_chapter.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book` | string | yes | Book slug such as 'genesis', 'john' or 'first-samuel'. Common names ('1 sam', 'psalm') are resolved. Call list_books for all 66. |
| `chapter` | integer | yes | Chapter number within the book, starting at 1. |
| `verse` | integer | no | Optional verse to start at. |

## `prepare_chapter`

**Prepare Chapter** — read-only, idempotent, closed-world · access: `read`.

Have a chapter read aloud (recorded) if it is not already, using the same queue as the website's Read button. Returns progress immediately; recording takes about one to two minutes — poll chapter_progress. Already-recorded or in-progress chapters cost nothing. Each user may commission 20 new chapters per UTC day through their assistant; do not loop over books — prepare only what the user asked to hear.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book` | string | yes | Book slug such as 'genesis', 'john' or 'first-samuel'. Common names ('1 sam', 'psalm') are resolved. Call list_books for all 66. |
| `chapter` | integer | yes | Chapter number within the book, starting at 1. |

## `chapter_progress`

**Chapter Progress** — read-only, idempotent, closed-world · access: `read`.

How far a chapter's recording has got, without starting anything. Safe to poll every few seconds while prepare_chapter's work runs.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book` | string | yes | Book slug such as 'genesis', 'john' or 'first-samuel'. Common names ('1 sam', 'psalm') are resolved. Call list_books for all 66. |
| `chapter` | integer | yes | Chapter number within the book, starting at 1. |

## `download_link`

**Download Link** — read-only, idempotent, closed-world · access: `read`.

A personal download link for recorded chapters, as an .opus file (one chapter) or a ZIP (several chapters — Annual plan). Give the user the URL: it works in their browser, expires (default 1 hour, max 24 hours), and is charged to their rolling 24-hour download allowance only when they OPEN it; opening it again before it expires is free. Chapters not yet recorded are listed as pending — call prepare_chapter for those first. Free plan: 4 chapters per rolling 24 hours, one at a time; Annual: 40, ZIP allowed.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book` | string | no | Book slug such as 'genesis', 'john' or 'first-samuel'. Common names ('1 sam', 'psalm') are resolved. Call list_books for all 66. |
| `chapter` | integer | no | Chapter number within the book, starting at 1. |
| `chapters` | array | no | Several chapters for one ZIP, each 'book/chapter' such as 'john/3' (Annual plan). Use instead of book+chapter. |
| `expires_in_seconds` | integer | no | Link lifetime, 60 to 86400. Default 3600. |

## `my_allowance`

**My Allowance** — read-only, idempotent, closed-world · access: `read`.

The user's standing: plan, download allowance left in the rolling 24 hours and when the next one frees up, chapter preparations left today, the assistant call quota, and where to upgrade. Call it before promising the user a download.

*No parameters.*

---

*Generated from the service's own tool registry on the source serving production on
2026-09-22, version 0.1.113. Regenerate rather than edit by hand.*
