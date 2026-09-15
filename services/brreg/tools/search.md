# Search and structure

**Which organisations match, and how do they belong together?** 2 Brreg MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://brreg.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | What it does |
|---|---|
| [`entity_search`](#entity-search) | Ranked, filtered search over current and historical names, addresses and websites |
| [`entity_structure`](#entity-structure) | Organisational structure of one orgnr as a stream of items with relation parent (overordnet… |

---

## `entity_search`

**Entity Search** — read-only, idempotent, closed-world.

Ranked, filtered search over current and historical names, addresses and websites. Give at least one of query, address, website or a filter. Filters: kind, org_form (codes from code_list), municipality (number or name), postcode, city, nace or sector prefix, status (active by default; any for all), public_body, vat_registered, parent_orgnr, employees_min/max, registered_from/to. sort: relevance, name or registered_desc. Items are summaries (orgnr, kind, name, org_form, municipality, city, address, nace1, status, public_body, parent_orgnr, matched, score); entity_lookup gives the full record. Diagnostics state mode, ranking_version, searched/matched/dropped terms, filters_applied and empty_reason (no_query_term_in_snapshot, filters_excluded_all_matches, offset_beyond_results) with a next_action, and prefix_truncated when a short prefix matched too many terms. Customer searches without a name query never return personal-data records (sole proprietorships and their establishments); diagnostics say so. Follow cursor; paging stops at 10000 results (depth_limit_reached) except for services. Example: entity_search query="tilsyn" public_body=true. Next: entity_lookup orgnr=<item orgnr>. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | string | no | Street or address-line text. |
| `city` | string | no | Postal city name. |
| `compact` | boolean | no | One-line text summary instead of duplicated JSON. |
| `cursor` | string | no | Next-page token; send it alone (max_bytes, compact allowed). |
| `employees_max` | integer | no | Maximum employees. |
| `employees_min` | integer | no | Minimum employees. |
| `fields` | array | no | Top-level item fields to return (orgnr kept). |
| `kind` | string | no | enhet, underenhet or all (default all). |
| `limit` | integer | no | Items per page (1-100, default 20). |
| `max_bytes` | integer | no | Response byte budget (default 24576; above 49152 services with compact only). |
| `municipality` | string | no | Municipality number or name. |
| `nace` | string | no | NACE code prefix, e.g. 84 or 84.110. |
| `offset` | integer | no | Skip results (first call only, max 10000). |
| `org_form` | array | no | Org form codes, e.g. AS, ENK (see code_list). |
| `parent_orgnr` | string | no | Only direct children of this orgnr. |
| `postcode` | string | no | Four-digit postcode. |
| `public_body` | boolean | no | Public bodies only (true) or none (false). |
| `query` | string | no | Name text (current and historical); orgnr digits also match. |
| `registered_from` | string | no | Registered on or after (YYYY-MM-DD). |
| `registered_to` | string | no | Registered on or before (YYYY-MM-DD). |
| `sector` | string | no | Institutional sector code prefix. |
| `snapshot_id` | string | no | Pin a snapshot (else snapshot_expired). |
| `sort` | string | no | relevance (default), name or registered_desc. |
| `status` | string | no | active (default), bankrupt, dissolving, deleted or any. |
| `vat_registered` | boolean | no | VAT-registered (true) or not (false). |
| `website` | string | no | Domain or URL fragment. |

## `entity_structure`

**Entity Structure** — read-only, idempotent, closed-world.

Organisational structure of one orgnr as a stream of items with relation parent (overordnet chain to the root, depth 1 = direct parent, at most 20), child (enheter whose parent is this orgnr) and subunit (underenheter). section: all (default), children or subunits. A ministry lists its agencies as children; a company lists its establishments as subunits. Diagnostics carry the root summary. Example: entity_structure orgnr=983887457 section=children. Next: entity_lookup orgnr=<item orgnr>. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `compact` | boolean | no | One-line text summary instead of duplicated JSON. |
| `cursor` | string | no | Next-page token; send it alone (max_bytes, compact allowed). |
| `fields` | array | no | Top-level item fields to return (orgnr kept). |
| `limit` | integer | no | Items per page (1-100, default 50). |
| `max_bytes` | integer | no | Response byte budget (default 24576; above 49152 services with compact only). |
| `orgnr` | string | yes | The organisasjonsnummer whose structure to read. |
| `section` | string | no | all (parents, children, subunits), children or subunits. |
| `snapshot_id` | string | no | Pin a snapshot (else snapshot_expired). |

---

*Generated from the customer-plane `tools/list` of the release serving production on 2026-09-15. Regenerate rather than edit by hand.*
