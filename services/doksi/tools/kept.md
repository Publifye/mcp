# Your documents

**What have I kept, and how do I tidy or recover it?** 5 Doksi MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://doksi.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`doc_list`](#doc_list) | read | List the documents YOUR customer account has kept (issued), newest first: id, your private… |
| [`doc_rename`](#doc_rename) | write | Give one of YOUR kept documents a private name (1-80 characters) |
| [`doc_trash`](#doc_trash) | read | List YOUR deleted documents that can still be restored, with the moment each is purged for… |
| [`doc_delete`](#doc_delete) | write | Delete one of YOUR kept documents |
| [`doc_restore`](#doc_restore) | write | Restore one of YOUR deleted documents from the trash, within its restore window |

---

## `doc_list`

**Doc List** — read-only, idempotent, closed-world · access: `read`.

List the documents YOUR customer account has kept (issued), newest first: id, your private name, kind, title, issue date and the link. Only your own documents; deleted ones are in doc_trash. Requires a customer login.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `kind` | string | no | Only documents of this kind, e.g. covenant |
| `occasion` | string | no | Only covenants of this occasion, e.g. marriage |

## `doc_rename`

**Doc Rename** — writes, closed-world · access: `write`.

Give one of YOUR kept documents a private name (1-80 characters), e.g. "Anna & Erik — church copy". The name is only for your list: it is never printed on the document, never in its link, never in any mail to anyone else.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The document id |
| `name` | string | yes | The new name |

## `doc_trash`

**Doc Trash** — read-only, idempotent, closed-world · access: `read`.

List YOUR deleted documents that can still be restored, with the moment each is purged for good.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `kind` | string | no | Only documents of this kind, e.g. covenant |
| `occasion` | string | no | Only covenants of this occasion, e.g. marriage |

## `doc_delete`

**Doc Delete** — writes, closed-world · access: `write`.

Delete one of YOUR kept documents. At once its link, every temporary share link and every open signing request over it stop working. It moves to your trash (doc_trash) and can be restored with doc_restore for 7 days; after that it is purged for good (the purge is announced in advance, never silent).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The document id |

## `doc_restore`

**Doc Restore** — writes, closed-world · access: `write`.

Restore one of YOUR deleted documents from the trash, within its restore window. It gets a NEW link; the link it had before stays dead.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The document id |

---

*Generated from the live `tools/list` of the release serving production (0.1.85) on 2026-09-29.
Regenerate rather than edit by hand.*
