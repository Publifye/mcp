# Export, import and the bin

**How is a programme backed up, restored, or taken down?** 7 Timely MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://timely.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`timely_export`](#timely-export) | read | Backup of ONE programme: a summary plus signed one-hour download links (json_url restora… |
| [`timely_export_all`](#timely-export-all) | read | Backup of ALL programmes of one account (plus organisation.json) as ONE zip at a downloa… |
| [`timely_export_schema`](#timely-export-schema) | read | The embedded JSON Schema that every export validates against and that timely_import ENFO… |
| [`timely_import`](#timely-import) | write | Create a NEW draft programme from a JSON export that validates against timely_export_sch… |
| [`timely_delete`](#timely-delete) | write | ONLY on the user's explicit request (confirm:true): move a programme (kind programme, id… |
| [`timely_restore`](#timely-restore) | write | Restore ONE item from the bin (timely_trash_list) exactly as it was: its address, publis… |
| [`timely_trash_list`](#timely-trash-list) | read | The bin: programmes and organisation pages that were deleted, newest first, with purge_a… |

---

## `timely_export`

**Timely Export** — read-only, idempotent, closed-world · access: `read`.

Backup of ONE programme: a summary plus signed one-hour download links (json_url restorable, text_url for people). inline:true also returns json_string, the exact file bytes json_sha256 covers (restore with timely_import json_string + sha256). Read-only; see operator_guide topic backup.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `format` | string | no | json, text or both (default both) |
| `id` | string | yes | Programme id |
| `inline` | boolean | no | Also return the file content (json_string / text) |

## `timely_export_all`

**Timely Export All** — read-only, idempotent, closed-world · access: `read`.

Backup of ALL programmes of one account (plus organisation.json) as ONE zip at a download_url (no login, one hour: treat it like a password) with a sha256 manifest. Staff: owner, or scope all_customers. operator_guide topic backup.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `format` | string | no | json, text or both (default both) |
| `include_organisation` | boolean | no | Include organisation.json (default true) |
| `owner` | string | no | Staff only: customer owner id or organisation id (idg…) |
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

Create a NEW draft programme from a JSON export that validates against timely_export_schema (never text or HTML); never overwrites or publishes; a taken slug gets a free one; organisation data is not imported. ALWAYS dry_run:true first and show the user, then dry_run:false. A refusal lists every problem by JSON path and writes nothing. Staff: mode restore (operator_guide topic staff).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bundle_base64` | string | no | restore: timely_export_all zip, base64 (≤48 MiB) |
| `bundle_url` | string | no | timely_export_all's download_url |
| `dry_run` | boolean | yes | true: validate and report only, write nothing |
| `export` | object | no | Parsed export object; prefer json_string |
| `json_string` | string | no | Exact export file text (with sha256) |
| `json_url` | string | no | timely_export's json_url |
| `mode` | string | no | copy (default) or restore (staff) |
| `owner` | string | no | Staff only: customer owner id or organisation id (idg…) |
| `pick_slug` | string | no | With bundle_url: which programme |
| `restore_token` | string | no | mode restore: the token from the dry run of this same input |
| `sha256` | string | no | json_sha256 of json_string |
| `slug` | string | no | Optional new address; a free one is chosen if taken |

## `timely_delete`

**Timely Delete** — writes, closed-world · access: `write`.

ONLY on the user's explicit request (confirm:true): move a programme (kind programme, id) or the organisation (kind organisation; programmes untouched) to the BIN. It leaves every public address at once; timely_restore brings it back until purge_at (timely_trash_list); after that it is deleted permanently. Generation from timely_get / timely_org_get.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `confirm` | boolean | yes | Must be true: the user asked for this deletion |
| `generation` | integer | yes | Current generation |
| `id` | string | no | Programme id (kind programme) |
| `kind` | string | yes | programme or organisation |
| `owner` | string | no | Staff only: customer owner id or organisation id (idg…) |

## `timely_restore`

**Timely Restore** — writes, closed-world · access: `write`.

Restore ONE item from the bin (timely_trash_list) exactly as it was: its address, published version and history come back. Refused if its address is in use now.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `from_purge_hold` | boolean | no | Staff only: bring back an item purged in the last 48 hours |
| `id` | string | yes | Id from timely_trash_list |
| `kind` | string | yes | programme or organisation |
| `owner` | string | no | Staff only: customer owner id or organisation id (idg…) |

## `timely_trash_list`

**Timely Trash List** — read-only, idempotent, closed-world · access: `read`.

The bin: programmes and organisation pages that were deleted, newest first, with purge_at (when it is deleted permanently). limit 1..100 (default 25); pass next_cursor back as cursor.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | string | no | next_cursor from the previous page |
| `limit` | integer | no | Page size |
| `owner` | string | no | Staff only: customer owner id or organisation id (idg…) |
