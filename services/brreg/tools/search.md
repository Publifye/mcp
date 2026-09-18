# Search and structure

**Which organisations match, and how do they belong together?** 2 Brreg MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://brreg.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | What it does |
|---|---|
| [`entity_search`](#entity_search) | Ranked, filtered search over current and historical names, addresses and websites |
| [`entity_structure`](#entity_structure) | Organisational structure of one orgnr: items with relation parent (overordnet chain to the… |

---

## `entity_search`

**Entity Search** — read-only, idempotent, closed-world.

Ranked, filtered search over current and historical names, addresses and websites. Give at least one of query, address, website, match or a filter. Filters: kind, org_form (code_list codes), municipality (number or name), postcode, city, nace or sector prefix, status (active by default; any for all), public_body, vat_registered, parent_orgnr, employees_min/max, registered_from/to. sort: relevance, name, registered_desc. match: 1-4 RE2 filters [{field, pattern}] (fields in the schema), AND'ed with the rest; case-insensitive, you anchor them, "." = present. Anchor when you can: ^post narrows the scan to a range, an unanchored pattern reads the field's whole dictionary once (tens of ms) and is then cached. lat+lon+radius_km: registered-address points (Kartverket), nearest first without query; items add distance_km and location. Items are summaries (orgnr, kind, name, org_form, municipality, city, address, nace1, status, public_body, email, parent_orgnr, matched, score); entity_lookup gives the record. Diagnostics: mode, terms, filters_applied, empty_reason with next_action. Customer searches without a name query, radius searches and match never return personal-data records (ENK and their establishments). Follow cursor to the end: paging has no depth limit. Example: entity_search query="tilsyn" public_body=true. Next: entity_lookup orgnr=<item orgnr>. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | string | no | Street or address-line text. |
| `city` | string | no | Postal city name. |
| `compact` | boolean | no | One-line text summary, not duplicated JSON. |
| `cursor` | string | no | Next-page token; send it alone (+max_bytes, compact). |
| `employees_max` | integer | no | Maximum employees. |
| `employees_min` | integer | no | Minimum employees. |
| `fields` | array | no | Item fields to return (orgnr kept). |
| `kind` | string | no | Default all. |
| `lat` | number | no | Radius centre latitude; needs lon and radius_km. |
| `limit` | integer | no | Items per page (1-100, default 20). |
| `lon` | number | no | Radius centre longitude. |
| `match` | array | no | Regex filters, AND'ed with the rest: [{"field":"email","pattern":"^post"}]. |
| `max_bytes` | integer | no | Response byte budget (default 24576). |
| `municipality` | string | no | Municipality number or name. |
| `nace` | string | no | NACE code prefix, e.g. 84 or 84.110. |
| `offset` | integer | no | Skip results (first call only, max 10000). |
| `org_form` | array | no | Org form codes, e.g. AS, ENK (see code_list). |
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

Organisational structure of one orgnr: items with relation parent (overordnet chain to the root, depth 1 = direct parent, at most 20), child (enheter whose parent is this orgnr) and subunit (underenheter). section: all (default), children or subunits. A ministry lists its agencies as children; a company its establishments as subunits. Diagnostics carry the root summary. Example: entity_structure orgnr=983887457 section=children. Next: entity_lookup orgnr=<item orgnr>. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `compact` | boolean | no | One-line text summary, not duplicated JSON. |
| `cursor` | string | no | Next-page token; send it alone (+max_bytes, compact). |
| `fields` | array | no | Item fields to return (orgnr kept). |
| `limit` | integer | no | Items per page (1-100, default 50). |
| `max_bytes` | integer | no | Response byte budget (default 24576). |
| `orgnr` | string | yes | The organisasjonsnummer whose structure to read. |
| `section` | string | no | Default all (parents, children, subunits). |
| `snapshot_id` | string | no | Pin a snapshot (else snapshot_expired). |

---

*Generated from the customer-plane `tools/list` of the release serving production on 2026-09-18. Regenerate rather than edit by hand.*
