# Read a programme

**What is published, what is drafted, and what changed?** 3 Timely MCP tools, listed with the exact description and
input schema the server itself returns. Endpoint: `https://timely.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`timely_list`](#timely-list) | read | List your programmes; published version first, history available separately. |
| [`timely_get`](#timely-get) | read | Current published programme and outstanding draft; use timely_history for older revision… |
| [`timely_history`](#timely-history) | read | Your programme's immutable revisions, changes and PDF references. |

---

## `timely_list`

**Timely List** — read-only, idempotent, closed-world · access: `read`.

List your programmes; published version first, history available separately.

*No parameters.*

## `timely_get`

**Timely Get** — read-only, idempotent, closed-world · access: `read`.

Current published programme and outstanding draft; use timely_history for older revisions.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Programme id |

## `timely_history`

**Timely History** — read-only, idempotent, closed-world · access: `read`.

Your programme's immutable revisions, changes and PDF references.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Programme id |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-20, version 0.1.27. Regenerate rather than edit by hand.*
