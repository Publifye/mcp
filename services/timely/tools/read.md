# Read a programme

**What is published, what is drafted, and what changed?** 5 Timely MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://timely.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`timely_list`](#timely-list) | read | List the programmes of one account (yours unless staff pass owner) in id order, 25 per p… |
| [`timely_get`](#timely-get) | read | PROGRAMME only. Current published programme and outstanding draft, plus a READ-ONLY orga… |
| [`timely_history`](#timely-history) | read | Your programme's immutable revisions (newest first, with changes and PDF references) or,… |
| [`timely_get_pdf`](#timely-get-pdf) | read | Get a one-hour download URL for an existing rendered PDF, including private drafts and h… |
| [`timely_get_widget`](#timely-get-widget) | read | PROGRAMME widget. The ordinary programme widget shows only the programme and needs NO or… |

---

## `timely_list`

**Timely List** — read-only, idempotent, closed-world · access: `read`.

List the programmes of one account (yours unless staff pass owner) in id order, 25 per page (limit 1..100); pass next_cursor back as cursor until it is empty. Staff: owner "*" pages EVERY customer's programmes the same way.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no | next_cursor from the previous page |
| `limit` | integer | no | Page size |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. Staff may pass "*" for all customers. |

## `timely_get`

**Timely Get** — read-only, idempotent, closed-world · access: `read`.

PROGRAMME only. Current published programme and outstanding draft, plus a READ-ONLY organisation summary (organisation info lives in timely_org_*; edit it with timely_org_set, never through a programme). Use timely_history for older revisions and timely_get_pdf with id and revision to download any rendered PDF. Use timely_get_widget for embed code and widget settings.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Programme id |

## `timely_history`

**Timely History** — read-only, idempotent, closed-world · access: `read`.

Your programme's immutable revisions (newest first, with changes and PDF references) or, with kind:"audit", its audit trail. 25 per page (limit 1..100); pass next_cursor back as cursor.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no | next_cursor from the previous page |
| `id` | string | yes | Programme id |
| `kind` | string | no | revisions (default) or audit |
| `limit` | integer | no | Page size |

## `timely_get_pdf`

**Timely Get PDF** — read-only, idempotent, closed-world · access: `read`.

Get a one-hour download URL for an existing rendered PDF, including private drafts and historical revisions. Requires programme ownership (or staff admin). Returns the exact stored artifact; does not approve, publish, or re-render. Anyone given the URL can download that PDF until expiry. Specify the revision from timely_get or timely_history.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Programme id |
| `pdf_hash` | string | no | Optional previous PDF hash from artifact_history |
| `revision` | integer | yes | Rendered revision number |

## `timely_get_widget`

**Timely Get Widget** — read-only, idempotent, closed-world · access: `read`.

PROGRAMME widget. The ordinary programme widget shows only the programme and needs NO organisation information: it sits inside the website the organisation already has. Only the full-page mode (and the organisation homepage, timely_org_homepage) shows organisation info above the programme. Get your widget URL, copyable iframe HTML, allowed websites, language options and publication state. Private preview_url requires your Timely account session and never publishes. Public widget shows only approved content.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Programme id |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-22, version 0.1.173. Regenerate rather than edit by hand.*
