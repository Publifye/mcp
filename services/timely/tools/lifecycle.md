# Export, import and the bin

**How is a programme backed up, restored, or taken down?** 7 Timely MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://timely.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`timely_export`](#timely-export) | read | Backup of ONE programme, returned INLINE: 'json_string' (the exact file bytes, complete,… |
| [`timely_export_all`](#timely-export-all) | read | Backup of ALL programmes of one account (plus organisation.json) as ONE zip at a REST do… |
| [`timely_export_schema`](#timely-export-schema) | read | The embedded JSON Schema that every export validates against and that timely_import ENFO… |
| [`timely_import`](#timely-import) | write | Create a NEW programme from a schema-verified JSON export. ONLY JSON that validates agai… |
| [`timely_delete`](#timely-delete) | write | Move a programme (kind programme, id) or the organisation page (kind organisation) to th… |
| [`timely_restore`](#timely-restore) | write | Restore ONE item from the bin (timely_trash_list) exactly as it was: its address, publis… |
| [`timely_trash_list`](#timely-trash-list) | read | The bin: programmes and organisation pages that were deleted, newest first, with purge_a… |

---

## `timely_export`

**Timely Export** — read-only, idempotent, closed-world · access: `read`.

Backup of ONE programme, returned INLINE: 'json_string' (the exact file bytes, complete, lossless, schema timely-programme-export/v1; json_sha256 covers exactly these bytes; restore with timely_import json_string + sha256) and/or 'text' (for people only; never importable), with sha256, byte sizes and a summary. The owner's organisation is included in the JSON under 'organisation', marked as organisation data. Read-only; see operator_guide BACKUP.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `format` | string | no | json, text or both (default both) |
| `id` | string | yes | Programme id |

## `timely_export_all`

**Timely Export All** — read-only, idempotent, closed-world · access: `read`.

Backup of ALL programmes of one account (plus organisation.json) as ONE zip at a REST download_url: no login needed, expires in one hour, treat it like a password. Returns expires_at, file count, total bytes and the manifest (sha256 per file). Staff: owner for a customer, or scope all_customers for everyone. See operator_guide BACKUP.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `format` | string | no | json, text or both (default both) |
| `include_organisation` | boolean | no | Include organisation.json (default true) |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. |
| `scope` | string | no | owner (default: one account) or all_customers (staff only) |

## `timely_export_schema`

**Timely Export Schema** — read-only, idempotent, closed-world · access: `read`.

The embedded JSON Schema that every export validates against and that timely_import ENFORCES. Validate before importing. kind: programme (default), organisation or bundle; version defaults to the current one; every shipped version stays available.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `kind` | string | no | programme, organisation or bundle |
| `version` | string | no | e.g. timely-programme-export/v1 |

## `timely_import`

**Timely Import** — writes, closed-world · access: `write`.

Create a NEW programme from a schema-verified JSON export. ONLY JSON that validates against timely_export_schema is accepted: never text, zip garbage or HTML. It never overwrites or changes an existing programme, picks a free slug if taken, and lands as a DRAFT (never published). ALWAYS call with dry_run:true first, show the user what would be created, then dry_run:false. A refusal lists every problem with its JSON path; nothing is written. Organisation data in the export is NOT imported (use timely_org_set). Staff disaster recovery: mode "restore" (see operator_guide DISASTER RESTORE).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bundle_base64` | string | no | mode restore: a whole timely_export_all zip, base64 (max 48 MiB) |
| `bundle_url` | string | no | An /export/<token> link from timely_export_all |
| `dry_run` | boolean | yes | true: validate and report only, write nothing |
| `export` | object | no | An export JSON object (e.g. a .json file's parsed content); prefer json_string |
| `json_string` | string | no | The exact text of an exported .json file, or timely_export's json_string unchanged (use with sha256) |
| `mode` | string | no | copy (default): a NEW programme as a draft. restore (staff only, disaster recovery): write it back exactly with its original id, address, owner and published version, only where id AND address are unused |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. |
| `pick_slug` | string | no | With bundle_url: which programme |
| `restore_token` | string | no | mode restore: the token from the dry run of this same input |
| `sha256` | string | no | Optional checksum of json_string: timely_export's json_sha256 or the file's sha256 in manifest.json |
| `slug` | string | no | Optional new address; a free one is chosen if taken |

## `timely_delete`

**Timely Delete** — writes, closed-world · access: `write`.

Move a programme (kind programme, id) or the organisation page (kind organisation) to the BIN. It leaves every public address at once and can be restored with timely_restore for the bin period (timely_trash_list shows purge_at); after that it is deleted permanently. Deleting the organisation does NOT touch programmes. ONLY on the user's explicit request; confirm must be true. Use generation from timely_get / timely_org_get.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `confirm` | boolean | yes | Must be true: the user asked for this deletion |
| `generation` | integer | yes | Current generation |
| `id` | string | no | Programme id (kind programme) |
| `kind` | string | yes | programme or organisation |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. |

## `timely_restore`

**Timely Restore** — writes, closed-world · access: `write`.

Restore ONE item from the bin (timely_trash_list) exactly as it was: its address, published version and history come back. Refused if its address is in use now.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `from_purge_hold` | boolean | no | Staff only: bring back an item purged in the last 48 hours |
| `id` | string | yes | Id from timely_trash_list |
| `kind` | string | yes | programme or organisation |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. |

## `timely_trash_list`

**Timely Trash List** — read-only, idempotent, closed-world · access: `read`.

The bin: programmes and organisation pages that were deleted, newest first, with purge_at (when it is deleted permanently). limit 1..100 (default 25); pass next_cursor back as cursor.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no | next_cursor from the previous page |
| `limit` | integer | no | Page size |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-22, version 0.1.173. Regenerate rather than edit by hand.*
