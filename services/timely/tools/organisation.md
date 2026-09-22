# Organisation and homepage

**What does the shared organisation page say, and how does it become a homepage?** 8 Timely MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://timely.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`timely_org_get`](#timely-org-get) | read | ORGANISATION (shared by all programmes, web only, never in the PDF). The complete record… |
| [`timely_org_set`](#timely-org-set) | write | ORGANISATION (shared by all programmes, web only, never in the PDF). Replace the organis… |
| [`timely_org_set_display`](#timely-org-set-display) | write | ORGANISATION (shared by all programmes, web only, never in the PDF). What visitors see i… |
| [`timely_org_add_website`](#timely-org-add-website) | write | ORGANISATION (shared by all programmes, web only, never in the PDF). Append ONE website … |
| [`timely_org_homepage`](#timely-org-homepage) | read | ORGANISATION (shared by all programmes, web only, never in the PDF). To make Timely the … |
| [`timely_org_logo_import`](#timely-org-logo-import) | write | ORGANISATION (shared by all programmes, web only, never in the PDF). Set the LOGO from a… |
| [`timely_org_logo_upload_begin`](#timely-org-logo-upload-begin) | write | ORGANISATION (shared by all programmes, web only, never in the PDF). Single-use LOGO upl… |
| [`timely_logo_status`](#timely-logo-status) | read | ORGANISATION (shared by all programmes, web only, never in the PDF). Poll an organisatio… |

---

## `timely_org_get`

**Timely Org Get** — read-only, idempotent, closed-world · access: `read`.

ORGANISATION (shared by all programmes, web only, never in the PDF). The complete record, generation (for timely_org_set), paused state and homepage URLs. Opt-in: include ["audit"] and/or ["bin_history"], each paged by its own *_cursor/*_limit (default 25). Not needed for the ordinary programme widget (it sits inside the website they already have). Immediate, no approval, never changes a PDF. operator_guide topic organisation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `audit_cursor` | string | no | audit_next_cursor |
| `audit_limit` | integer | no |  |
| `bin_history_cursor` | string | no | bin_history_next_cursor |
| `bin_history_limit` | integer | no |  |
| `include` | array of string | no | audit, bin_history |
| `owner` | string | no | Staff only: customer owner id or organisation id (idg…) |

## `timely_org_set`

**Timely Org Set** — writes, closed-world · access: `write`.

ORGANISATION (shared by all programmes, web only, never in the PDF). Replace the organisation with the COMPLETE record read from timely_org_get plus only the requested change, with its generation; OMITTED FIELDS ARE CLEARED; a stale generation is refused (read again). Or send only paused with the generation. Not needed for the ordinary programme widget (it sits inside the website they already have). Immediate, no approval, never changes a PDF. operator_guide topic organisation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `generation` | integer | yes | generation from timely_org_get |
| `organisation` | object | no | The COMPLETE record: name, tagline, what/where/when/how {text, detail}, contact {email, phone}, visit, postal, org_line, links, slug, homepage_origins, homepage_programmes ([] = automatic); limits: operator_guide topic organisation. OMITTED FIELDS ARE CLEARED. Required unless paused is sent. |
| `owner` | string | no | Staff only: customer owner id or organisation id (idg…) |
| `paused` | boolean | no | Alone: true hides every public page, PDF and widget until false |

## `timely_org_set_display`

**Timely Org Set Display** — writes, closed-world · access: `write`.

ORGANISATION (shared by all programmes, web only, never in the PDF). What visitors see in one mode (full: homepage and full-page widgets; programme: every programme widget), for all programmes; a programme's own choice (timely_set_widget_identity) wins. A hidden item is removed from the page HTML. Omitted switches keep their value; inherit resets to the mode default. Generation from timely_org_get. Immediate, never changes a PDF. operator_guide topic widget.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `generation` | integer | yes | generation from timely_org_get |
| `inherit` | array of string | no | Switch names to reset so they follow the mode default again, e.g. ["show_place"] |
| `mode` | string | yes | full or programme |
| `owner` | string | no | Staff only: customer owner id or organisation id (idg…) |
| `show_addresses` | boolean | no |  |
| `show_contact` | boolean | no |  |
| `show_links` | boolean | no |  |
| `show_logo` | boolean | no |  |
| `show_org_info` | boolean | no |  |
| `show_org_line` | boolean | no |  |
| `show_place` | boolean | no |  |
| `show_speaker` | boolean | no |  |
| `show_title` | boolean | no |  |

## `timely_org_add_website`

**Timely Org Add Website** — writes, closed-world · access: `write`.

ORGANISATION (shared by all programmes, web only, never in the PDF). Append ONE website the user asked for to homepage_origins (example.org or https://…), changing nothing else. Generation from timely_org_get. Not needed for the ordinary programme widget (it sits inside the website they already have). Immediate, no approval, never changes a PDF. operator_guide topic organisation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `generation` | integer | yes | generation from timely_org_get |
| `origin` | string | yes | The website, e.g. https://www.example.org |
| `owner` | string | no | Staff only: customer owner id or organisation id (idg…) |

## `timely_org_homepage`

**Timely Org Homepage** — read-only, idempotent, closed-world · access: `read`.

ORGANISATION (shared by all programmes, web only, never in the PDF). To make Timely the homepage: index.html to upload, upload instructions (relay verbatim), homepage URL, embed code, and origins_still_to_add. Read-only. Not needed for the ordinary programme widget (it sits inside the website they already have). Immediate, no approval, never changes a PDF. operator_guide topic organisation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `lang` | string | no | index.html language (default en) |
| `owner` | string | no | Staff only: customer owner id or organisation id (idg…) |
| `site` | string | no | Website the file will live on |

## `timely_org_logo_import`

**Timely Org Logo Import** — writes, closed-world · access: `write`.

ORGANISATION (shared by all programmes, web only, never in the PDF). Set the LOGO from a public HTTPS image (PNG/JPEG ≤5 MiB, ≤16 MP; confirm_public:true); new programmes use it in their PDF, existing PDFs never change. Poll timely_logo_status. Not needed for the ordinary programme widget (it sits inside the website they already have). Immediate, no approval, never changes a PDF. operator_guide topic organisation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `confirm_public` | boolean | yes | Confirm the logo may be hosted publicly |
| `owner` | string | no | Staff only: customer owner id or organisation id (idg…) |
| `url` | string | yes | Public HTTPS image URL |

## `timely_org_logo_upload_begin`

**Timely Org Logo Upload Begin** — writes, closed-world · access: `write`.

ORGANISATION (shared by all programmes, web only, never in the PDF). Single-use LOGO upload: returns upload_url; POST the raw PNG/JPEG within 30 minutes (never bytes in MCP), then poll timely_logo_status. confirm_public:true. Not needed for the ordinary programme widget (it sits inside the website they already have). Immediate, no approval, never changes a PDF. operator_guide topic organisation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `confirm_public` | boolean | yes | Confirm the logo may be hosted publicly |
| `owner` | string | no | Staff only: customer owner id or organisation id (idg…) |

## `timely_logo_status`

**Timely Logo Status** — read-only, idempotent, closed-world · access: `read`.

ORGANISATION (shared by all programmes, web only, never in the PDF). Poll an organisation logo job_id until status is ready (logo_url is live now) or failed (with a fix). Never approves or publishes anything.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `job_id` | string | yes | Job from timely_org_logo_import or timely_org_logo_upload_begin |
