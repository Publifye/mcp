# Build and render

**Create, edit, restyle, preview — and where approval stops.** 5 Timely MCP tools, listed with the exact description and
input schema the server itself returns. Endpoint: `https://timely.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`timely_create`](#timely-create) | write | Create a programme draft; select an exact meeting count or date period. No publication o… |
| [`timely_edit`](#timely-edit) | write | Atomically apply explicit operations against base_hash. ISAC cannot approve or publish. |
| [`timely_set_theme`](#timely-set-theme) | write | Set the public programme and widget appearance immediately (not PDF styling). Use genera… |
| [`timely_render`](#timely-render) | write | Render the current draft through Doksi and retain the exact preview PDF. |
| [`draft_approve`](#draft-approve) | write | Human approval only: use the signed confirmation page and explicitly confirm the preview… |

---

## `timely_create`

**Timely Create** — writes, closed-world · access: `write`.

Create a programme draft; select an exact meeting count or date period. No publication occurs.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content` | object | yes | Programme content: title, language, timezone, selection, grouping, events and bounded series |
| `slug` | string | yes | Public slug |

## `timely_edit`

**Timely Edit** — writes, closed-world · access: `write`.

Atomically apply explicit operations against base_hash. ISAC cannot approve or publish.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `base_hash` | string | yes | Expected current content hash |
| `id` | string | yes | Programme id |
| `operations` | array | yes | Typed event, series, selection, grouping, style or title changes |

## `timely_set_theme`

**Timely Set Theme** — writes, closed-world · access: `write`.

Set the public programme and widget appearance immediately (not PDF styling). Use generation from timely_get. Theme: mode light/dark/auto; font system/serif/mono; light and dark palettes each accept background, text and accent as #RRGGBB. Omitted values reset to defaults. Text and accent require 4.5:1 contrast. Changes are audited; meeting content and publication are untouched.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `generation` | integer | yes | Expected generation from timely_get |
| `id` | string | yes | Programme id |
| `theme` | object | yes | mode, font, light:{background,text,accent}, dark:{background,text,accent} |

## `timely_render`

**Timely Render** — writes, closed-world · access: `write`.

Render the current draft through Doksi and retain the exact preview PDF.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Programme id |
| `revision` | integer | yes | Draft revision number |

## `draft_approve`

**Draft Approve** — writes, closed-world · access: `write`.

Human approval only: use the signed confirmation page and explicitly confirm the preview. MCP callers cannot approve.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Programme id |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-20, version 0.1.27. Regenerate rather than edit by hand.*
