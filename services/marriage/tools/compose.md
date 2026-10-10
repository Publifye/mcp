# Check, preview and make

**Is the covenant right, what will it look like, and how is the print-ready one made?** 3 Marriage Covenant MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://marriage.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`covenant_validate`](#covenant_validate) | read | Check a covenant and get EVERY problem at once, each with its JSON path, why it matters a… |
| [`covenant_preview`](#covenant_preview) | read | Show the couple their covenant WITHOUT keeping it: returns a link to the PDF, valid for o… |
| [`covenant_compose`](#covenant_compose) | write | Make the PRINT-READY covenant and keep it as the customer's own: returns its id, a perman… |

---

## `covenant_validate`

**Covenant Validate** — read-only, idempotent, closed-world · access: `read`.

Check a covenant and get EVERY problem at once, each with its JSON path, why it matters and how to fix it (missing = not filled in yet; malformed = filled in wrongly). Nothing is rendered for the couple or kept. Free.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | The whole covenant JSON, as covenant_requirements describes it. kind and occasion are always covenant and marriage (filled in if you leave them out; anything else is refused). |

## `covenant_preview`

**Covenant Preview** — read-only, idempotent, closed-world · access: `read`.

Show the couple their covenant WITHOUT keeping it: returns a link to the PDF, valid for one hour. Without a live marriage pass or Doksi plan this is the FREE, WATERMARKED preview (credits pay for covenant_compose, not for previews) — a picture of the page with a preview watermark burned in (PREVIEW on an English covenant, FORHÅNDSVISNING on a Norwegian one), not for printing; tell them so before they open it. With a live pass or plan it is the print-ready page. Counts toward the free daily call allowance.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | The whole covenant JSON, as covenant_requirements describes it. kind and occasion are always covenant and marriage (filled in if you leave them out; anything else is refused). |

## `covenant_compose`

**Covenant Compose** — writes, closed-world · access: `write`.

Make the PRINT-READY covenant and keep it as the customer's own: returns its id, a permanent link and its private name. Needs a paid path: a live marriage pass (unlimited marriage covenants for 7 days) or a Doksi plan — or use_credit:true to spend ONE credit. Without one it is refused with where to buy; covenant_access_status shows the customer's status and the live prices, and the watermarked preview stays free. ALWAYS send a request_id (new for each covenant); after a network error retry with the SAME request_id and arguments: you get the same covenant back and are never charged twice. name is an optional private label (1-80 characters, never printed); default: the names and the date. Validate first.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | The whole covenant JSON (kind covenant, occasion marriage) |
| `name` | string | no | Optional private name for the customer's list, e.g. "Anna & Erik — church copy" |
| `request_id` | string | yes | Unique id for this covenant (1-128 letters, digits, . _ -); reuse it on a retry |
| `use_credit` | boolean | no | Spend one credit for this covenant (for a customer without a pass or plan) |

---

*Generated from the live `tools/list` of the release serving production (0.1.38) on 2026-10-10.
Regenerate rather than edit by hand.*
