# Assets

**How do I get a logo or a mark into a document?** 2 Doksi MCP tools, listed with the exact description and
input schema the server itself returns. Endpoint: `https://doksi.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`asset_upload_begin`](#asset-upload-begin) | write | Reserve an id for a mark — a signature, a logo, a seal, a letterhead — and get back the … |
| [`asset_status`](#asset-status) | read | Where a mark is: awaiting_upload, processing, ready, or failed with the reason.

A docum… |

---

## `asset_upload_begin`

**Asset Upload Begin** — writes, closed-world · access: `write`.

Reserve an id for a mark — a signature, a logo, a seal, a letterhead — and get back the URL to POST the image to. THE ID COMES FIRST and the bytes follow: this call moves no image data.

FORMATS: send PNG or JPEG. It is stored as PNG with transparency whatever you send. SVG is refused — export it to PNG first; at 300 dpi a vector mark loses nothing at print size.

Ask for several at once with `slots`: a letterhead and a signature is ONE call, not two conversational turns.

THE SLOT DECLARES THE SIZE — signature (62×12 mm), logo (50×14 mm), seal (28×28 mm), letterhead (80×18 mm). A larger upload buys a better-resolution mark in the same box, never a bigger one, so adding a signature never reflows a page.

Near-white is keyed out to transparent on intake and the mark is trimmed to its ink, because a scan on white paper is an opaque rectangle that would cover the ruled line it sits on. Pass keep_background for a crest designed on a coloured field, which keying would destroy.

Then POST the bytes; HTTP 202 means stored and processing asynchronously. Poll asset_status until ready or failed before rendering. HTTP 503 with Retry-After means capacity is busy; retry the same upload ticket. A ticket is single-use and expires in 30 minutes; a failed upload SPENDS it, so a retry needs a fresh begin.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `keep_background` | boolean | no | Do not key out the background. For a mark designed on a coloured field. |
| `slot` | string | no | One of: signature, logo, seal, letterhead |
| `slots` | array | no | Several slots in one call, instead of `slot`. |

## `asset_status`

**Asset Status** — read-only, idempotent, closed-world · access: `read`.

Where a mark is: awaiting_upload, processing, ready, or failed with the reason.

A document may reference a mark that is not ready yet — that is a normal transient state, not a validation failure. A FAILED mark is a validation failure, and the reason says what to fix.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The asset id from asset_upload_begin |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-20, version 0.1.54. Regenerate rather than edit by hand.*
