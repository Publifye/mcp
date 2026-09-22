# Read a programme

**What is published, what is drafted, and what changed?** 6 Timely MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://timely.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`timely_list`](#timely_list) | read | List the programmes of one account (yours unless staff pass owner) in id order, 25 per p… |
| [`timely_get`](#timely_get) | read | PROGRAMME only (organisation info: timely_org_*). Published and draft revision headers a… |
| [`timely_history`](#timely_history) | read | Revision headers, newest first (or kind:"audit": the audit trail), 25 per page; pass nex… |
| [`timely_edit_history`](#timely_edit_history) | read | Your programme's per-call workflow history, newest first, including checkpoints and clar… |
| [`timely_get_pdf`](#timely_get_pdf) | read | One-hour download URL (anyone holding it can download) for an existing PDF of any revisi… |
| [`timely_get_widget`](#timely_get_widget) | read | PROGRAMME widget: URL, copyable iframe HTML, allowed websites, language and state. The o… |

---

## `timely_list`

**Timely List** — read-only, idempotent, closed-world · access: `read`.

List the programmes of one account (yours unless staff pass owner) in id order, 25 per page (limit 1..30); pass next_cursor back as cursor until it is empty. Staff: owner "*" pages EVERY customer's programmes the same way.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no | next_cursor from the previous page |
| `limit` | integer | no | Page size |
| `owner` | string | no | Staff only: customer owner id or organisation id (idg…) Staff may pass "*" for all customers. |

## `timely_get`

**Timely Get** — read-only, idempotent, closed-world · access: `read`.

PROGRAMME only (organisation info: timely_org_*). Published and draft revision headers and URLs. For ONE revision (revision, default the draft) include: meetings (paged by meetings_cursor, meetings_limit ≤500), content, changes, artifact_history.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Programme id |
| `include` | array of string | no | meetings, content, changes, artifact_history |
| `meetings_cursor` | string | no | meetings_next_cursor |
| `meetings_limit` | integer | no | Default 100 |
| `revision` | integer | no | For include (default: draft, else published) |

## `timely_history`

**Timely History** — read-only, idempotent, closed-world · access: `read`.

Revision headers, newest first (or kind:"audit": the audit trail), 25 per page; pass next_cursor back as cursor. include:["bodies"] for full revisions.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no | next_cursor |
| `id` | string | yes | Programme id |
| `include` | array of string | no | bodies |
| `kind` | string | no | revisions (default) or audit |
| `limit` | integer | no |  |

## `timely_edit_history`

**Timely Edit History** — read-only, idempotent, closed-world · access: `read`.

Your programme's per-call workflow history, newest first, including checkpoints and clarification questions. 25 per page (limit 1..100); pass next_cursor back as cursor.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no | next_cursor from the previous page |
| `id` | string | yes | Programme id |
| `limit` | integer | no | Page size |

## `timely_get_pdf`

**Timely Get PDF** — read-only, idempotent, closed-world · access: `read`.

One-hour download URL (anyone holding it can download) for an existing PDF of any revision, exactly as stored; never renders or publishes. Revision from timely_get or timely_history.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Programme id |
| `pdf_hash` | string | no | Optional previous PDF hash from artifact_history |
| `revision` | integer | yes | Rendered revision number |

## `timely_get_widget`

**Timely Get Widget** — read-only, idempotent, closed-world · access: `read`.

PROGRAMME widget: URL, copyable iframe HTML, allowed websites, language and state. The ordinary widget needs NO organisation information (it sits inside their own website); only full-page mode and timely_org_homepage show it. preview_url needs the owner's session; the public widget shows approved content only.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Programme id |
