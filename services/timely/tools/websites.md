# Websites and widgets

**Where may the programme appear, and how does it look there?** 3 Timely MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://timely.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`timely_add_website`](#timely-add-website) | write | Append one owner-requested HTTPS website origin without removing or reordering existing … |
| [`timely_set_widget`](#timely-set-widget) | write | PROGRAMME widget websites only (organisation homepage websites are timely_org_add_websit… |
| [`timely_set_widget_identity`](#timely-set-widget-identity) | write | PROGRAMME widget display: choose, for THIS programme and one widget mode, what visitors … |

---

## `timely_add_website`

**Timely Add Website** — writes, closed-world · access: `write`.

Append one owner-requested HTTPS website origin without removing or reordering existing websites. The first origin is the default QR destination; use timely_set_widget with the complete ordered list to change which website is first. Uses generation from timely_get and returns complete widget code and resulting origins.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `generation` | integer | yes | Expected generation |
| `id` | string | yes | Programme id |
| `origin` | string | yes | Exact HTTPS website origin, e.g. https://www.example.org; no path or wildcard |

## `timely_set_widget`

**Timely Set Widget** — writes, closed-world · access: `write`.

PROGRAMME widget websites only (organisation homepage websites are timely_org_add_website). Configure the widget websites and language. Supply the COMPLETE desired origins list (HTTPS only, no wildcards, maximum 20), not just additions. Order matters: the FIRST origin is the default programme QR destination (unless an explicit content.qr_url override is set). Empty origins falls back to the Timely programme page. Existing printed PDFs require re-render and approval to update their QR. Only add websites the owner requested. Returns the full resulting configuration. Uses generation from timely_get. Does not publish.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `generation` | integer | yes | Expected generation |
| `id` | string | yes | Programme id |
| `language` | string | yes | Default widget language |
| `language_selector` | boolean | yes | Allow visitors to choose language |
| `origins` | array | yes | Complete HTTPS website origin list |

## `timely_set_widget_identity`

**Timely Set Widget Identity** — writes, closed-world · access: `write`.

PROGRAMME widget display: choose, for THIS programme and one widget mode, what visitors see. Switches: show_org_info, show_contact, show_logo, show_title, show_addresses, show_links, show_org_line, show_place, show_speaker. Organisation facts come from the organisation record (timely_org_*); this only decides whether they are shown. Layers: mode default, then the organisation's choice (timely_org_set_display), then this programme's choice (this tool). Defaults: full shows everything; programme (also used by next) shows only the programme, with place and speaker. A switched-off item is removed from the page HTML entirely, not hidden with CSS. compact=true defaults this mode to a minimal embedded view (next meeting/date/time/speaker and QR) without projector enlargement; visitors can override compact locally. Supply at least one switch or inherit; omitted switches keep their value; inherit resets named switches (or compact) to follow the organisation again. Requires ownership and generation from timely_get. Applies immediately, is audited, and does not change the PDF or publish a draft.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `compact` | boolean | no | Default to minimal embedded view |
| `generation` | integer | yes | Expected generation |
| `id` | string | yes | Programme id |
| `inherit` | array | no | Switch names to reset so they follow the organisation's choice again, e.g. ["show_place"] |
| `mode` | string | yes | full or programme (programme also covers next) |
| `show_addresses` | boolean | no | Show the Visit and Post addresses at the bottom. Omit to keep the current value. |
| `show_contact` | boolean | no | Show the organisation email address and phone number. Omit to keep the current value. |
| `show_links` | boolean | no | Show the organisation's links (social media, podcast) at the bottom. Omit to keep the current value. |
| `show_logo` | boolean | no | Show the organisation logo in the heading. Omit to keep the current value. |
| `show_org_info` | boolean | no | Show the one-line description and What / Where / When / How with their details. Omit to keep the current value. |
| `show_org_line` | boolean | no | Show the organisation details line at the bottom, e.g. organisation number. Omit to keep the current value. |
| `show_place` | boolean | no | Show each meeting's place. Omit to keep the current value. |
| `show_speaker` | boolean | no | Show each meeting's speaker, including a speaker repeated after a dash in the title. Omit to keep the current value. |
| `show_title` | boolean | no | Show the organisation name (or programme title) and the time zone line in the heading. Omit to keep the current value. |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-22, version 0.1.173. Regenerate rather than edit by hand.*
