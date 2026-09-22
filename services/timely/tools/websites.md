# Websites and widgets

**Where may the programme appear, and how does it look there?** 3 Timely MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://timely.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`timely_add_website`](#timely_add_website) | write | Append one owner-requested HTTPS website origin without removing or reordering existing … |
| [`timely_set_widget`](#timely_set_widget) | write | PROGRAMME widget websites and language (homepage websites: timely_org_add_website). orig… |
| [`timely_set_widget_identity`](#timely_set_widget_identity) | write | What visitors see of THIS programme in one mode; wins over timely_org_set_display. compa… |

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

PROGRAMME widget websites and language (homepage websites: timely_org_add_website). origins is the COMPLETE list (https, no wildcards, ≤20) of sites the owner asked for; the FIRST is the default PDF QR destination (a printed PDF changes only after re-render and approval). Generation from timely_get. Never publishes.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `generation` | integer | yes | Expected generation |
| `id` | string | yes | Programme id |
| `language` | string | yes | Default widget language |
| `language_selector` | boolean | yes | Allow visitors to choose language |
| `origins` | array of string | yes | Complete HTTPS website origin list |

## `timely_set_widget_identity`

**Timely Set Widget Identity** — writes, closed-world · access: `write`.

What visitors see of THIS programme in one mode; wins over timely_org_set_display. compact:true = minimal embed. A hidden item is removed from the page HTML. Omitted switches keep their value; inherit follows the organisation again. Generation from timely_get. Immediate, never changes the PDF or publishes. operator_guide topic widget.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `compact` | boolean | no | Default to minimal embedded view |
| `generation` | integer | yes | Expected generation |
| `id` | string | yes | Programme id |
| `inherit` | array of string | no | Switch names to reset so they follow the organisation's choice again, e.g. ["show_place"] |
| `mode` | string | yes | full or programme (programme also covers next) |
| `show_addresses` | boolean | no |  |
| `show_contact` | boolean | no |  |
| `show_links` | boolean | no |  |
| `show_logo` | boolean | no |  |
| `show_org_info` | boolean | no |  |
| `show_org_line` | boolean | no |  |
| `show_place` | boolean | no |  |
| `show_speaker` | boolean | no |  |
| `show_title` | boolean | no |  |
