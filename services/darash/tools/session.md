# Session, figures and health

**How do I check the service, send feedback, and manage the figures I have stored?** 8 Darash MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://darash-api.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`get_health`](#get_health) | Get service info, health, statistics, product page URL, and documentation link |
| [`submit_feedback`](#submit_feedback) | Submit a user testimonial about Darash |
| [`view_delete`](#view_delete) | Delete a stored figure immediately |
| [`view_freeze`](#view_freeze) | Mark a stored figure as permanently preserved (never expires) |
| [`view_info`](#view_info) | Return metadata about a single stored figure: id, Bible ref, title, size, created-at, exp… |
| [`view_list`](#view_list) | List all stored figures (SVG/HTML overlays) in the public view store |
| [`view_set_ttl`](#view_set_ttl) | Set (extend or shrink) the TTL of a stored figure relative to NOW |
| [`view_unfreeze`](#view_unfreeze) | Revert a frozen figure back to a normal TTL-bound entry |

---

## `get_health`

**Get Health** — read-only, idempotent, closed-world.

Get service info, health, statistics, product page URL, and documentation link. Call this first to understand what Darash is and what data is available.[END]

*No parameters.*

## `submit_feedback`

**Submit Feedback** — read-only, idempotent, open-world.

Submit a user testimonial about Darash. Ask the user for: 1) A short comment (1-2 sentences) about their experience, 2) Their name or alias (for display), 3) Their location/city and country, 4) A 1-5 star rating — suggest one based on their sentiment. Examples: 'The ELS findings blew my mind — billion-to-one odds encoded in Genesis', 'Finally a Bible tool that goes beyond English translations', 'Simple to set up, extraordinarily deep'. If the user has already submitted feedback, this tool returns a thank-you message. Only ask ONCE per session, and only after the user has seen meaningful results.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `comment` | string | yes | User's testimonial (1-2 sentences, max 500 chars) |
| `country` | string | no | User's country (e.g., 'Norway', 'USA', 'UK') |
| `location` | string | no | User's city or region (e.g., 'Oslo', 'Texas', 'London') |
| `name` | string | no | User's name or alias for display (default: Anonymous) |
| `stars` | integer | yes | Rating 1-5 (1=poor, 3=good, 5=extraordinary). Suggest based on user's sentiment. |

## `view_delete`

**View Delete** — writes, destructive, closed-world.

Delete a stored figure immediately. Removes both the in-memory entry and the Redis persistence (if the entry was frozen). After delete, the /view/<id> URL returns 404. Idempotent: deleting an already-gone entry returns ok=false but is not an error.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `view_id` | string | yes | The 32-character hex id from the /view/<id> URL. |

## `view_freeze`

**View Freeze** — writes, idempotent, closed-world.

Mark a stored figure as permanently preserved (never expires). The figure is persisted to Redis under darash:frozen:<view_id> and rehydrated automatically on service restart, so the /view/<view_id> URL remains live forever. Use this when a figure is publication-worthy and must outlast the default 72-hour TTL. Idempotent: calling twice does nothing extra. To revert, use view_unfreeze.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `view_id` | string | yes | The 32-character hex id from the /view/<id> URL (or the 'url' field returned by els_verse_overlay). |

## `view_info`

**View Info** — read-only, idempotent, closed-world.

Return metadata about a single stored figure: id, Bible ref, title, size, created-at, expires-at (omitted when frozen), and frozen boolean. Read-only complement to view_list when you already know the view_id.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `view_id` | string | yes | The 32-character hex id from the /view/<id> URL. |

## `view_list`

**View List** — read-only, idempotent, closed-world.

List all stored figures (SVG/HTML overlays) in the public view store. Returns each entry's id, optional Bible ref, optional title, size in bytes, created-at timestamp, expires-at (omitted when frozen), and a frozen boolean. Use frozen_only=true to filter to permanently-frozen entries. Use this to audit what figures are currently live, identify which ones to freeze for long-term preservation, or to find a specific figure by Bible reference. Frozen figures survive service restarts via Redis-backed persistence; non-frozen figures expire on a TTL (72h default).[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `frozen_only` | boolean | no | When true, return only frozen entries (skip TTL-bound entries). Default false (return all active entries). |

## `view_set_ttl`

**View Set TTL** — writes, idempotent, closed-world.

Set (extend or shrink) the TTL of a stored figure relative to NOW. Works on both TTL-bound and frozen entries (a frozen entry will be unfrozen as a side effect when its TTL is reset). Use this to extend a 72-hour figure to '30d' for short-term sharing without committing to permanent freeze. To make permanent, use view_freeze. To remove now, use view_delete.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ttl` | string | yes | New TTL relative to NOW. Accepts Go duration strings: '72h', '30d', '7d', '1h'. Required. |
| `view_id` | string | yes | The 32-character hex id from the /view/<id> URL. |

## `view_unfreeze`

**View Unfreeze** — writes, idempotent, closed-world.

Revert a frozen figure back to a normal TTL-bound entry. Removes the Redis persistence and re-applies the requested TTL relative to NOW. After unfreezing, the figure will expire at the new ExpiresAt; if you want it gone immediately, use view_delete.[END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ttl` | string | no | Time-to-live to apply on unfreeze. Accepts Go duration strings: '72h', '30d' (treated as 720h), '7d' (treated as 168h). Default '72h'. |
| `view_id` | string | yes | The 32-character hex id from the /view/<id> URL. |

---

*Generated by `scripts/render_reference.py` from the live `tools/list`, version 0.11.146, captured 2026-09-29 (see [tools.json](../tools.json)). Regenerate rather than edit by hand.*
