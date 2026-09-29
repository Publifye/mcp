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

Exact lookup by organisasjonsnummer in Enhetsregisteret; never fuzzy.
ARGS: orgnr (one) or orgnrs (several, answered in input order); spaces and dots tolerated. include_subunits adds the first 20 underenheter. live=true (one orgnr only) also checks data.brreg.no now. fields projects any top-level record key (name, org_form, nace, business_address, location, ...).
ITEMS: {orgnr, found, record?, reason?}; reason invalid_checksum, not_in_snapshot or removed. record_as_of: the record was read from the update feed after the snapshot.
LIVE: live_status current, changed (with changed_fields), deleted, removed, not_found or unavailable; too many live checks answer rate_limited with retry_after.
PLACE: location, unit and buildings are the point, parcel and buildings at the REGISTERED address (Kartverket), not where the business operates; an unlocated record has location null with a reason and no unit or buildings.
REFUSALS: no roles, owners or persons; not the authoritative record (verify at virksomhet.brreg.no). Customers never see an ENK's former names, activity text, location, parcel or buildings.
SIZE: a full record is about 6 KiB — with a small max_bytes use fields or compact=true.
MONEY: figures, filed years, the industry benchmark and the filed document are entity_financials. This tool still accepts them unchanged: they are fetched only when fields includes "financials" or "filings", and without that nothing is fetched — stored figures, else not_requested.
Example: entity_lookup orgnr="983 887 457". Next: entity_structure orgnr=<orgnr>. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `compact` | boolean | no | One-line text summary, not duplicated JSON. |
| `cursor` | string | no | Next-page token; send it alone (+max_bytes, compact). |
| `document_year` | integer | no | That year's filed accounts as an expiring link (single orgnr, fields filings). A scanned image: no text to extract. |
| `fields` | array | no | Item fields to return (orgnr kept). |
| `include_subunits` | boolean | no | Add the first 20 underenheter of each enhet. |
| `live` | boolean | no | Also check data.brreg.no now (single orgnr only; rate limited). |
| `max_bytes` | integer | no | Response byte budget (default 24576). |
| `orgnr` | string | no | One organisasjonsnummer; spaces and dots tolerated (983 887 457). |
| `orgnrs` | array | no | Several organisasjonsnummer, results in input order. |
| `snapshot_id` | string | no | Pin a snapshot (else snapshot_expired). |

## `entity_resolve`

**Entity Resolve** — read-only, idempotent, closed-world.

Name to organisation candidates, never an implicit pick.
ARGS: name (required), and the filters kind, public_body, municipality, include_deleted.
KEY: one documented comparator — NFC, lowercase, fold æ→ae ø→o å→a (oe and aa also match), & → og, punctuation stripped, trailing legal forms (AS, ASA, ENK, ...) and leading STIFTELSEN/FORENINGEN/SELSKAPET removed.
TIERS, first non-empty wins: exact_name (1.0), normalized_name (0.9), historical_name (0.8); only when all three are empty, prefix and near_miss (max 0.5, unresolved).
RESOLUTION: unique (one strong candidate), ambiguous (several; order active_first_then_enhet_then_public_body_then_orgnr) or unresolved. Only unique is safe to use without review; none found gives one unresolved item with next_action entity_search.
Example: entity_resolve name="Sosialdepartementet". Next: entity_lookup orgnr=<candidate orgnr>. [END]

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

*Generated from the live `tools/list` of the release serving production (0.3.32) on 2026-09-29. Regenerate rather than edit by hand.*
