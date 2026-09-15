# Codes and freshness

**Which filter values exist, and which edition of the register is this?** 2 Brreg MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://brreg.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | What it does |
|---|---|
| [`code_list`](#code-list) | Filter-value discovery with counts from the current snapshot: list org_form, municipality,… |
| [`snapshot_status`](#snapshot-status) | Snapshot readiness and provenance: snapshot_id, acquired_at, age and stale flag, source ETag… |

---

## `code_list`

**Code List** — read-only, idempotent, closed-world.

Filter-value discovery with counts from the current snapshot: list org_form, municipality, nace or sector; optional query matches a code prefix or description text. Use the codes as entity_search filters. Example: code_list list=org_form query=aksje. Next: entity_search org_form=[<code>]. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `compact` | boolean | no | One-line text summary instead of duplicated JSON. |
| `cursor` | string | no | Next-page token; send it alone (max_bytes, compact allowed). |
| `fields` | array | no | Top-level item fields to return (orgnr kept). |
| `limit` | integer | no | Items per page (1-100, default 50). |
| `list` | string | yes | Which code list. |
| `max_bytes` | integer | no | Response byte budget (default 24576; above 49152 services with compact only). |
| `query` | string | no | Code prefix or description text. |
| `snapshot_id` | string | no | Pin a snapshot (else snapshot_expired). |

## `snapshot_status`

**Snapshot Status** — read-only, idempotent, closed-world.

Snapshot readiness and provenance: snapshot_id, acquired_at, age and stale flag, source ETag and Last-Modified per dataset, record counts (enheter, underenheter, enk, public_bodies, deleted), build and ranking version, suppression count, memory state, caller plane and access level, licence, scope and exclusions. detail=true adds per-tool latency, cursor state, suppression reconcile and removals watcher status. Memory read only. Example: snapshot_status. Next: entity_search or entity_resolve. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `detail` | boolean | no | Add memory, latency, suppression and watcher detail. |

---

*Generated from the customer-plane `tools/list` of the release serving production on 2026-09-15. Regenerate rather than edit by hand.*
