# What is recorded

**Which books exist, and how much has been read aloud?** 4 Audio Bible MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://audiobible.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`list_books`](#list_books) | read | Every book of the canon with its chapter count, in canon order. The canon is loaded from… |
| [`search_chapters`](#search_chapters) | read | The site's own chapter search: what a reader typing 'john 3', '1 sam' or 'ps 23' into th… |
| [`chapter_status`](#chapter_status) | read | Whether one chapter's audio exists, and what it was made from. With no arguments it answ… |
| [`coverage`](#coverage) | read | How much of the Bible has actually been generated and how much is still pending. Read st… |

---

## `list_books`

**List Books** — read-only, idempotent, closed-world · access: `read`.

Every book of the canon with its chapter count, in canon order. The canon is loaded from darash, never written down in this service, so it cannot disagree with the text.

*No parameters.*

## `search_chapters`

**Search Chapters** — read-only, idempotent, closed-world · access: `read`.

The site's own chapter search: what a reader typing 'john 3', '1 sam' or 'ps 23' into the single search field at the top of every page would be offered.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | integer | no | Maximum suggestions. |
| `query` | string | yes | What the reader typed. |

## `chapter_status`

**Chapter Status** — read-only, idempotent, closed-world · access: `read`.

Whether one chapter's audio exists, and what it was made from. With no arguments it answers for Genesis 1 and says so.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book` | string | no | Book slug, e.g. 'genesis' or 'first-samuel'. Call list_books for all 66. |
| `chapter` | integer | no | Chapter number within the book. |

## `coverage`

**Coverage** — read-only, idempotent, closed-world · access: `read`.

How much of the Bible has actually been generated and how much is still pending. Read straight off the audio volume, so it stays true even when the index is empty.

*No parameters.*

---

*Generated from the service's own tool registry on the source serving production on
2026-09-22, version 0.1.113. Regenerate rather than edit by hand.*
