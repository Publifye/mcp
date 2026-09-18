# Lookup and name resolution

**You have a number or a name — which organisation is it?** 2 Brreg MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://brreg.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | What it does |
|---|---|
| [`entity_lookup`](#entity_lookup) | Exact lookup by organisasjonsnummer in Enhetsregisteret; never fuzzy |
| [`entity_resolve`](#entity_resolve) | Name to organisation candidates, never an implicit pick |

---

## `entity_lookup`

**Entity Lookup** — read-only, idempotent.

Exact lookup by organisasjonsnummer in Enhetsregisteret; never fuzzy. orgnr (one) or orgnrs (several, in input order); spaces and dots tolerated. Items are {orgnr, found, record?, reason?}, reason invalid_checksum, not_in_snapshot or removed. Key financials (Regnskapsregisteret, latest filed accounts) are fetched only when fields includes "financials", then stored: one orgnr waits up to 3 s, a batch answers stored/fetching/queue_full, over budget rate_limited with financials_retry_after_seconds — repeat later. Without it nothing is fetched: stored figures, else not_requested. fields "filings" adds the years actually filed, and answers for banks and insurers whose financials are not_supported; document_year returns that year's filed document as an expiring private link (a scan, not figures). include_subunits adds the first 20 underenheter. live=true (one orgnr) also checks data.brreg.no: live_status current, changed (changed_fields), deleted, removed, not_found or unavailable; rate limited (rate_limited, retry_after). ENK never show former names or activity text to customers, and their financials only in a one-orgnr lookup. A record is about 6 KiB; with a small max_bytes use fields or compact=true. location, unit, buildings: point, parcel and buildings at the registered address (Kartverket); location null with a reason, others omitted. fields: any top-level record key (name, org_form, nace, business_address, ...). Example: entity_lookup orgnr="983 887 457". Next: entity_structure orgnr=<orgnr>. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `compact` | boolean | no | One-line text summary, not duplicated JSON. |
| `cursor` | string | no | Next-page token; send it alone (+max_bytes, compact). |
| `document_year` | integer | no | That year's filed accounts as an expiring link (single orgnr, fields filings). |
| `fields` | array | no | Item fields to return (orgnr kept). |
| `include_subunits` | boolean | no | Add the first 20 underenheter of each enhet. |
| `live` | boolean | no | Also check data.brreg.no now (single orgnr only; rate limited). |
| `max_bytes` | integer | no | Response byte budget (default 24576). |
| `orgnr` | string | no | One organisasjonsnummer; spaces and dots tolerated (983 887 457). |
| `orgnrs` | array | no | Several organisasjonsnummer, results in input order. |
| `snapshot_id` | string | no | Pin a snapshot (else snapshot_expired). |

## `entity_resolve`

**Entity Resolve** — read-only, idempotent, closed-world.

Name to organisation candidates, never an implicit pick. One documented key: NFC, lowercase, fold æ→ae ø→o å→a (oe and aa also match), & → og, punctuation stripped, trailing legal forms (AS, ASA, ENK, DA, ANS, SA, STI, I LIKVIDASJON, ...) and leading STIFTELSEN/FORENINGEN/SELSKAPET removed. Tiers, first non-empty wins: exact_name (1.0), normalized_name (0.9), historical_name (0.8); only when all are empty, prefix and near_miss (max 0.5, unresolved). resolution is unique (one strong candidate), ambiguous (several; order active_first_then_enhet_then_public_body_then_orgnr) or unresolved. None: one unresolved item with next_action entity_search. Filters: kind, public_body, municipality, include_deleted. Example: entity_resolve name="Sosialdepartementet". Next: entity_lookup orgnr=<candidate orgnr>. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `compact` | boolean | no | One-line text summary, not duplicated JSON. |
| `cursor` | string | no | Next-page token; send it alone (+max_bytes, compact). |
| `fields` | array | no | Item fields to return (orgnr kept). |
| `include_deleted` | boolean | no | Include deleted entities (default false). |
| `kind` | string | no | Default all. |
| `limit` | integer | no | Maximum candidates (1-25, default 10). |
| `max_bytes` | integer | no | Response byte budget (default 24576). |
| `municipality` | string | no | Municipality number or name. |
| `name` | string | yes | Name to resolve (current or historical). |
| `public_body` | boolean | no | Public bodies only (true) or none (false). |
| `snapshot_id` | string | no | Pin a snapshot (else snapshot_expired). |

---

*Generated from the customer-plane `tools/list` of the release serving production on 2026-09-18. Regenerate rather than edit by hand.*
