# Your covenants

**Which covenants have I kept, and how do I tidy or recover them?** 6 Marriage Covenant MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://marriage.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`covenant_list`](#covenant_list) | read | List the customer's own kept marriage covenants, newest first: id, private name, title, d… |
| [`covenant_get`](#covenant_get) | read | Read one of the customer's covenants: its link, private name and the exact covenant JSON… |
| [`covenant_rename`](#covenant_rename) | write | Give one of the customer's covenants a private name (1-80 characters), e.g |
| [`covenant_delete`](#covenant_delete) | write | Delete one of the customer's covenants |
| [`covenant_trash`](#covenant_trash) | read | List the customer's deleted covenants that can still be restored, with when each is purge… |
| [`covenant_restore`](#covenant_restore) | write | Restore a deleted covenant from the trash within its 7 days |

---

## `covenant_list`

**Covenant List** — read-only, idempotent, closed-world · access: `read`.

List the customer's own kept marriage covenants, newest first: id, private name, title, date and link. Deleted ones are in covenant_trash.

*No parameters.*

## `covenant_get`

**Covenant Get** — read-only, idempotent, closed-world · access: `read`.

Read one of the customer's covenants: its link, private name and the exact covenant JSON it was made from. To change it, edit that JSON and compose again (a new covenant); a kept PDF never changes.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The covenant id (from covenant_compose or covenant_list) |

## `covenant_rename`

**Covenant Rename** — writes, closed-world · access: `write`.

Give one of the customer's covenants a private name (1-80 characters), e.g. "Anna & Erik — church copy". Only for their list: never printed, never in the link, never in any mail.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The covenant id |
| `name` | string | yes | The new name |

## `covenant_delete`

**Covenant Delete** — writes, closed-world · access: `write`.

Delete one of the customer's covenants. Its link, every share link and every open signing request stop working at once. It stays restorable for 7 days (covenant_trash, covenant_restore); after that it is purged for good.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The covenant id (from covenant_compose or covenant_list) |

## `covenant_trash`

**Covenant Trash** — read-only, idempotent, closed-world · access: `read`.

List the customer's deleted covenants that can still be restored, with when each is purged for good.

*No parameters.*

## `covenant_restore`

**Covenant Restore** — writes, closed-world · access: `write`.

Restore a deleted covenant from the trash within its 7 days. It gets a NEW link; the one it had before stays dead.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The covenant id (from covenant_compose or covenant_list) |

---

*Generated from the live `tools/list` of the release serving production (0.1.38) on 2026-10-10.
Regenerate rather than edit by hand.*
