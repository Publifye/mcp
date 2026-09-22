# Organisation and homepage

**What does the organisation's shared page say, and how does it become a homepage?** 8 Timely MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://timely.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`timely_org_get`](#timely-org-get) | read | ORGANISATION (shared by all programmes, web only, never in the PDF). Read the organisati… |
| [`timely_org_set`](#timely-org-set) | write | ORGANISATION (shared by all programmes, web only, never in the PDF). Replace the organis… |
| [`timely_org_set_display`](#timely-org-set-display) | write | ORGANISATION (shared by all programmes, web only, never in the PDF). Choose what visitor… |
| [`timely_org_add_website`](#timely-org-add-website) | write | ORGANISATION (shared by all programmes, web only, never in the PDF). Append ONE website … |
| [`timely_org_homepage`](#timely-org-homepage) | read | ORGANISATION (shared by all programmes, web only, never in the PDF). Everything to make … |
| [`timely_org_logo_import`](#timely-org-logo-import) | write | ORGANISATION (shared by all programmes, web only, never in the PDF). Set the organisatio… |
| [`timely_org_logo_upload_begin`](#timely-org-logo-upload-begin) | write | ORGANISATION (shared by all programmes, web only, never in the PDF). Start a single-use … |
| [`timely_logo_status`](#timely-logo-status) | read | ORGANISATION (shared by all programmes, web only, never in the PDF). Poll an organisatio… |

---

## `timely_org_get`

**Timely Org Get** — read-only, idempotent, closed-world · access: `read`.

ORGANISATION (shared by all programmes, web only, never in the PDF). Read the organisation: the complete record, its generation (needed by timely_org_set), paused state and its homepage URLs. include:["audit"] adds the audit trail newest first, include:["bin_history"] what was deleted, restored and permanently deleted (title and date only). Each extra pages on its own: audit_limit/audit_cursor (pass audit_next_cursor back) and bin_history_limit/bin_history_cursor (pass bin_history_next_cursor back), 1..100, default 25. For customers, actor reads you, Publifye, system or another account. Only needed when Timely is the organisation's homepage (the full page, /o/ link or downloaded index.html). The ordinary programme widget does NOT need it: it sits inside the website they already have, which already says who they are, where and how to reach them. Saving is immediate, needs no approval and never changes a PDF. Read operator_guide (ORGANISATION) first.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `audit_cursor` | string | no | audit_next_cursor from the previous call |
| `audit_limit` | integer | no | Audit page size |
| `bin_history_cursor` | string | no | bin_history_next_cursor from the previous call |
| `bin_history_limit` | integer | no | Bin history page size |
| `include` | array | no | Optional extras: "audit", "bin_history" |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. |

## `timely_org_set`

**Timely Org Set** — writes, closed-world · access: `write`.

ORGANISATION (shared by all programmes, web only, never in the PDF). Replace the organisation information with the COMPLETE record: read timely_org_get, change only what the user asked, send everything back with the generation you read. Omitted fields are CLEARED. A stale generation is refused; read again and reapply. Refusals list every problem with its exact path. Or send ONLY paused (true/false) with the generation to pause or resume every public page of the organisation. Only needed when Timely is the organisation's homepage (the full page, /o/ link or downloaded index.html). The ordinary programme widget does NOT need it: it sits inside the website they already have, which already says who they are, where and how to reach them. Saving is immediate, needs no approval and never changes a PDF. Read operator_guide (ORGANISATION) first.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `generation` | integer | yes | generation from timely_org_get |
| `organisation` | object | no | The COMPLETE organisation object: name, tagline (240 chars each); what/where/when/how each {text ≤240, detail ≤500}; contact {email, phone ≤40: digits, spaces, + - ( )}; visit/postal/org_line arrays of ≤6 lines ≤160 chars; links ≤3 {label ≤80, url https}; slug (optional short address, lowercase); homepage_origins (exact https origins); homepage_programmes (programme ids in display order, [] = automatic). OMITTED FIELDS ARE CLEARED. Required unless paused is sent. |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. |
| `paused` | boolean | no | Only this: true hides the homepage and every programme page, PDF and widget calmly until false |

## `timely_org_set_display`

**Timely Org Set Display** — writes, closed-world · access: `write`.

ORGANISATION (shared by all programmes, web only, never in the PDF). Choose what visitors see, for the whole organisation, in one widget mode: full (the homepage and every full-page widget) or programme (every ordinary programme widget, also next). Switches: show_org_info, show_contact, show_logo, show_title, show_addresses, show_links, show_org_line, show_place, show_speaker. Defaults: full shows everything; programme shows only the programme, with place and speaker. A programme can still make its own choice with timely_set_widget_identity, which wins for that programme. A switched-off item is removed from the page HTML entirely, not hidden with CSS. Supply at least one switch or inherit; omitted switches keep their value; inherit resets named switches to the mode default. Uses generation from timely_org_get; the organisation must be saved first. Immediate, audited, no approval, never changes a PDF.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `generation` | integer | yes | generation from timely_org_get |
| `inherit` | array | no | Switch names to reset so they follow the mode default again, e.g. ["show_place"] |
| `mode` | string | yes | full or programme |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. |
| `show_addresses` | boolean | no | Show the Visit and Post addresses at the bottom. Omit to keep the current value. |
| `show_contact` | boolean | no | Show the organisation email address and phone number. Omit to keep the current value. |
| `show_links` | boolean | no | Show the organisation's links (social media, podcast) at the bottom. Omit to keep the current value. |
| `show_logo` | boolean | no | Show the organisation logo in the heading. Omit to keep the current value. |
| `show_org_info` | boolean | no | Show the one-line description and What / Where / When / How with their details. Omit to keep the current value. |
| `show_org_line` | boolean | no | Show the organisation details line at the bottom, e.g. organisation number. Omit to keep the current value. |
| `show_place` | boolean | no | Show each meeting's place. Omit to keep the current value. |
| `show_speaker` | boolean | no | Show each meeting's speaker, including a speaker repeated after a dash in the title. Omit to keep the current value. |
| `show_title` | boolean | no | Show the organisation name (or programme title) and the time zone line in the heading. Omit to keep the current value. |

## `timely_org_add_website`

**Timely Org Add Website** — writes, closed-world · access: `write`.

ORGANISATION (shared by all programmes, web only, never in the PDF). Append ONE website to homepage_origins (the sites allowed to show the homepage), without changing anything else. Only add a website the user asked for. Accepts example.org or https://www.example.org. Uses generation from timely_org_get. Only needed when Timely is the organisation's homepage (the full page, /o/ link or downloaded index.html). The ordinary programme widget does NOT need it: it sits inside the website they already have, which already says who they are, where and how to reach them. Saving is immediate, needs no approval and never changes a PDF. Read operator_guide (ORGANISATION) first.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `generation` | integer | yes | generation from timely_org_get |
| `origin` | string | yes | The website, e.g. https://www.example.org |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. |

## `timely_org_homepage`

**Timely Org Homepage** — read-only, idempotent, closed-world · access: `read`.

ORGANISATION (shared by all programmes, web only, never in the PDF). Everything to make Timely the organisation's homepage: the index.html source to upload, upload instructions to relay to the user verbatim, the shareable homepage URL, embed code for an existing website, and which websites are allowed and which still need adding (timely_org_add_website). Read-only. Only needed when Timely is the organisation's homepage (the full page, /o/ link or downloaded index.html). The ordinary programme widget does NOT need it: it sits inside the website they already have, which already says who they are, where and how to reach them. Saving is immediate, needs no approval and never changes a PDF. Read operator_guide (ORGANISATION) first.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `lang` | string | no | Page language for index.html (default en) |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. |
| `site` | string | no | Optional: the website the file will live on, e.g. https://www.example.org |

## `timely_org_logo_import`

**Timely Org Logo Import** — writes, closed-world · access: `write`.

ORGANISATION (shared by all programmes, web only, never in the PDF). Set the organisation LOGO from a public HTTPS image URL (PNG/JPEG ≤5 MiB, ≤16 MP). Timely downloads it with SSRF protection and hosts it publicly; confirm_public must be true. It appears on the homepage and full-page widget at once, and new programmes use it in their PDF; existing programmes and PDFs are NOT changed. Poll timely_logo_status. Only needed when Timely is the organisation's homepage (the full page, /o/ link or downloaded index.html). The ordinary programme widget does NOT need it: it sits inside the website they already have, which already says who they are, where and how to reach them. Saving is immediate, needs no approval and never changes a PDF. Read operator_guide (ORGANISATION) first.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `confirm_public` | boolean | yes | Confirm the logo may be hosted publicly |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. |
| `url` | string | yes | Public HTTPS image URL |

## `timely_org_logo_upload_begin`

**Timely Org Logo Upload Begin** — writes, closed-world · access: `write`.

ORGANISATION (shared by all programmes, web only, never in the PDF). Start a single-use upload of the organisation LOGO: returns upload_url; POST the raw PNG/JPEG bytes within 30 minutes, then poll timely_logo_status. Never put image bytes into MCP. confirm_public must be true. Existing programmes and PDFs are NOT changed. Only needed when Timely is the organisation's homepage (the full page, /o/ link or downloaded index.html). The ordinary programme widget does NOT need it: it sits inside the website they already have, which already says who they are, where and how to reach them. Saving is immediate, needs no approval and never changes a PDF. Read operator_guide (ORGANISATION) first.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `confirm_public` | boolean | yes | Confirm the logo may be hosted publicly |
| `owner` | string | no | Staff only: organisation id (idg…) or owner id of the customer to act for (see admin_org_list). Leave it out for your own account. |

## `timely_logo_status`

**Timely Logo Status** — read-only, idempotent, closed-world · access: `read`.

ORGANISATION (shared by all programmes, web only, never in the PDF). Poll an organisation logo job_id until status is ready (logo_url is live now) or failed (with a fix). Never approves or publishes anything.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `job_id` | string | yes | Job from timely_org_logo_import or timely_org_logo_upload_begin |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-22, version 0.1.173. Regenerate rather than edit by hand.*
