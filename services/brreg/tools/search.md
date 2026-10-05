# Search and structure

**Which organisations match, and how do they belong together?** 2 Brreg MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://brreg.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | What it does |
|---|---|
| [`entity_search`](#entity_search) | Ranked, filtered search over current and historical names, addresses and websites |
| [`entity_structure`](#entity_structure) | Organisational structure of one orgnr |

---

## `entity_search`

**Entity Search** — read-only, idempotent, closed-world.

Ranked, filtered search over current and historical names, addresses and websites. Give at least one of query, address, website, match or a filter.
TEXT: query (name text; orgnr digits also match), address (street or address line), website (domain or URL fragment).
FILTERS: kind, org_form (code_list codes), municipality (number or name), postcode, city, nace or sector prefix, status (active by default; any for all), public_body, vat_registered, parent_orgnr, employees_min/max, registered_from/to. sort: relevance (default), name, registered_desc.
MATCH: 1-4 RE2 filters [{field, pattern}] (fields in the schema), AND'ed with the rest; case-insensitive, you anchor them, "." = the field is present. Anchor when you can: ^post narrows the scan to a range, while an unanchored pattern's first use reads that field's whole dictionary (~114 ms) before it is cached. A rejected pattern is invalid_filter: fix it, do not retry it unchanged.
ITEMS: summaries (orgnr, kind, name, org_form, municipality, city, address, nace1, status, public_body, email, parent_orgnr, matched, score) — entity_lookup gives the record. forced_dissolution=true inside status "dissolving" means tvangsavvikling/tvangsoppløsning, closure compelled by the state; absent, the owner is winding up voluntarily.
REFUSALS: a customer search without a name query, and every match search, returns no personal-data records (ENK and their establishments).
PAGING: follow cursor to the end; there is no depth limit. Diagnostics carry mode, terms, filters_applied and empty_reason with a next_action.
NEARBY: lat+lon+radius_km still work here; entity_nearby is the front door for a coordinate search.
Example: entity_search query="tilsyn" public_body=true. Next: entity_lookup orgnr=<item orgnr>. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | string | no | Street or address-line text. |
| `city` | string | no | Postal city name. |
| `compact` | boolean | no | One-line text summary, not duplicated JSON. |
| `cursor` | string | no | Next-page token; send it alone (+max_bytes, compact). |
| `employees_max` | integer | no | Maximum employees. |
| `employees_min` | integer | no | Minimum employees. |
| `fields` | array of string | no | Item fields to return (orgnr kept). |
| `kind` | string | no | Default all. |
| `lat` | number | no | Radius centre latitude, decimal degrees; needs lon and radius_km. Coordinates only — for a place use municipality, city or postcode. |
| `limit` | integer | no | Items per page (1-100, default 20). |
| `lon` | number | no | Radius centre longitude. |
| `match` | array of object | no | Regex filters, AND'ed with the rest: [{"field":"email","pattern":"^post"}]. |
| `max_bytes` | integer | no | Response byte budget (default 24576). |
| `municipality` | string | no | Municipality number or name. |
| `nace` | string | no | NACE code prefix, e.g. 84 or 84.110. |
| `offset` | integer | no | Skip results (first call only, max 10000). |
| `org_form` | array of string | no | Org form codes, e.g. AS, ENK (see code_list). |
| `parent_orgnr` | string | no | Only direct children of this orgnr. |
| `postcode` | string | no | Four-digit postcode. |
| `public_body` | boolean | no | Public bodies only (true) or none (false). |
| `query` | string | no | Name text (current and historical); orgnr digits also match. |
| `radius_km` | number | no | Km; max 10 alone, 50 with another filter. |
| `registered_from` | string | no | Registered on or after (YYYY-MM-DD). |
| `registered_to` | string | no | Registered on or before (YYYY-MM-DD). |
| `sector` | string | no | Institutional sector code prefix. |
| `snapshot_id` | string | no | Pin a snapshot (else snapshot_expired). |
| `sort` | string | no | Default relevance. |
| `status` | string | no | Default active. |
| `vat_registered` | boolean | no | VAT-registered (true) or not (false). |
| `website` | string | no | Domain or URL fragment. |

## `entity_structure`

**Entity Structure** — read-only, idempotent, closed-world.

Organisational structure of one orgnr.
ARGS: orgnr (required); section all (default), children or subunits.
ITEMS: relation parent (the overordnet chain to the root, depth 1 = direct parent, at most 20), child (enheter whose parent is this orgnr) or subunit (underenheter). A ministry lists its agencies as children; a company its establishments as subunits.
NOTE: every relation comes from the weekly snapshot, whatever the entity's own record_as_of. Diagnostics carry the root summary.
Example: entity_structure orgnr=983887457 section=children. Next: entity_lookup orgnr=<item orgnr>. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `compact` | boolean | no | One-line text summary, not duplicated JSON. |
| `cursor` | string | no | Next-page token; send it alone (+max_bytes, compact). |
| `fields` | array of string | no | Item fields to return (orgnr kept). |
| `limit` | integer | no | Items per page (1-100, default 50). |
| `max_bytes` | integer | no | Response byte budget (default 24576). |
| `orgnr` | string | yes | The organisasjonsnummer whose structure to read. |
| `section` | string | no | Default all (parents, children, subunits). |
| `snapshot_id` | string | no | Pin a snapshot (else snapshot_expired). |

---

*Generated from the live `tools/list` of the release serving production (0.3.32) on 2026-09-29. Regenerate rather than edit by hand.*
