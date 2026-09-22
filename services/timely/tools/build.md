# Build and render

**Create, edit, restyle, preview — and where approval stops.** 5 Timely MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://timely.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`timely_create`](#timely-create) | write | PROGRAMME only (organisation info lives in timely_org_*). Create a programme draft; sele… |
| [`timely_edit`](#timely-edit) | write | PROGRAMME only (organisation info lives in timely_org_*). Atomically apply explicit oper… |
| [`timely_set_theme`](#timely-set-theme) | write | Set the public programme and widget appearance immediately (not PDF styling). Use genera… |
| [`timely_render`](#timely-render) | write | Always render the current draft afresh through Doksi, even when a PDF already exists. Re… |
| [`draft_approve`](#draft-approve) | write | AI/MCP callers CAN approve and publish with this tool; no browser or signed confirmation… |

---

## `timely_create`

**Timely Create** — writes, closed-world · access: `write`.

PROGRAMME only (organisation info lives in timely_org_*). Create a programme draft; select an exact meeting count or date period. No publication occurs. Call operator_guide first for exact content and bounded-series examples.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content` | object | yes | Programme content: title, language, timezone, selection, grouping, events and bounded series |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. |
| `slug` | string | yes | Public slug |

## `timely_edit`

**Timely Edit** — writes, closed-world · access: `write`.

PROGRAMME only (organisation info lives in timely_org_*). Atomically apply explicit operations against base_hash. This tool never publishes; approval is a separate explicit user-confirmed action.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `base_hash` | string | yes | Expected current content hash |
| `dry_run` | boolean | no | Validate and return proposed draft/diffs without storing a revision or changing state |
| `id` | string | yes | Programme id |
| `operations` | array | yes | Typed changes including shift_events, event, series, selection, grouping, style, timezone or title; call operator_guide for exact examples |

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

Always render the current draft afresh through Doksi, even when a PDF already exists. Replaces the preview on the SAME draft revision without changing its content. Returns the new PDF and a one-hour download URL. Does not create a draft, approve, or publish. Use timely_get_pdf to download an existing render. Published/historical revisions cannot be re-rendered in place.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Programme id |
| `revision` | integer | yes | Current draft revision number |

## `draft_approve`

**Draft Approve** — writes, closed-world · access: `write`.

AI/MCP callers CAN approve and publish with this tool; no browser or signed confirmation page is required. PUBLISH ONLY AFTER EXPLICIT USER APPROVAL. Never call automatically after editing/rendering. First show the exact revision, PDF download link and intended public address, flag unresolved assumptions, and ASK the user whether to publish. A general edit request is NOT consent. Set user_confirmed=true only after an affirmative answer for this exact revision/PDF. If anything changes, ask again. A new draft public_slug removes the old public URL; warn about broken old links/printed QR codes before asking. Publishes the stored PDF without re-rendering.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content_hash` | string | yes | Exact content hash shown for approval |
| `id` | string | yes | Programme id |
| `pdf_hash` | string | yes | Exact rendered PDF hash shown for approval |
| `revision` | integer | yes | Exact revision confirmed by the user |
| `user_confirmed` | boolean | yes | True ONLY after explicit user confirmation for this exact revision and PDF |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-22, version 0.1.173. Regenerate rather than edit by hand.*
