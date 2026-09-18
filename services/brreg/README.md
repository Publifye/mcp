# Brreg — Norwegian company register MCP server for Claude, Cursor and any MCP client

**Brreg gives an AI assistant Brønnøysundregistrene's Enhetsregisteret as structured data: look an
organisation up by organisasjonsnummer, turn a name into candidates without a silent pick, search
with filters, regular expressions or a point and a radius, and see how organisations belong
together — with key financials from Regnskapsregisteret when you ask for them. It runs as a hosted
MCP server over HTTPS.**

| | |
|---|---|
| Endpoint | `https://brreg.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open · no API keys |
| Registry | `pro.publifye/brreg` ([server.json](server.json); not yet published to the registry) |
| Product site | <https://brreg.publifye.com> |
| What it solves | <https://publifye.com/brreg> |
| Capability tools | **6** ([full schemas](tools.json)) |

## Connect

```jsonc
{ "mcpServers": { "brreg": { "type": "http", "url": "https://brreg.publifye.com/mcp" } } }
```

Claude Code: `claude mcp add --transport http brreg https://brreg.publifye.com/mcp`, then `/mcp` to
sign in.

The OAuth flow runs in the browser on first use, with a Publifye account. Access is granted through
that sign-in only; there is no API key to create, copy or rotate. The discovery chain is the same as
for the other servers: **[../../docs/connect.md](../../docs/connect.md)**.

## The register

The edition the live service was serving on **2026-09-15**, acquired that morning from
Brønnøysundregistrene's bulk files:

| | |
|---|---|
| Main units (enheter) | 1,174,268 |
| Sub-units (underenheter) | 863,374 |
| Sole proprietorships (ENK), among the main units | 462,855 |

The register is rebuilt from the full files every week. An entry Brønnøysundregistrene removes from
open data is dropped within 24 hours. `snapshot_status` returns the age and counts of whichever
edition is current, and every successful result names the edition it came from.

## A number is exact; a name is not

`entity_lookup` takes an organisasjonsnummer, checks its checksum, and is never fuzzy.

`entity_resolve` takes a name and returns **candidates**, with `resolution` set to `unique`,
`ambiguous` or `unresolved` and the order of the candidates stated. It never claims the first
candidate is the organisation. Norwegian spellings are compared through one documented key — æ, ø
and å folded, legal forms such as AS and ASA stripped, former names matched — so the comparison can
be checked rather than trusted.

No language model is involved in answering a call. Every successful result carries the licence
attribution and names the edition it came from, so an answer can be traced back to its source.

## What the tools do

Every tool is documented with its exact description, annotations and input schema —
6 in all, generated from the service's own `tools/list`, never written by hand.

| Area | The question it answers | Tools |
|---|---|---|
| **[Lookup and name resolution](tools/lookup.md)** | You have a number or a name — which organisation is it? | 2 |
| **[Search and structure](tools/search.md)** | Which organisations match, and how do they belong together? | 2 |
| **[Codes and freshness](tools/reference.md)** | Which filter values exist, and which edition of the register is this? | 2 |

Machine-readable: **[tools.json](tools.json)** carries all 6 callable tools (6 capability, 0 session/cache) with full JSON Schema, plus every excluded bucket listed by name so the count is auditable.

All six are read-only. `entity_lookup` is the one marked open-world: with `live=true` it checks the
entry against data.brreg.no, and when `fields` includes `financials` or `filings` it goes to
Regnskapsregisteret.

### Four ways to narrow a search

`entity_search` takes at least one of `query`, `address`, `website`, `match` or a filter, and
everything you give is AND'ed together.

**Filters.** `kind`, `org_form`, `municipality`, `postcode`, `city`, `nace`, `sector`, `status`,
`public_body`, `vat_registered`, `parent_orgnr`, `employees_min`/`max`, `registered_from`/`to`. The
values come from `code_list`, so a filter is a code you looked up, not a guess.

**Regular expressions.** `match` takes 1 to 4 `{field, pattern}` terms over **activity, address,
city, email, name, phone or website**. A pattern is RE2, at most 200 bytes, matched
case-insensitively against the normalised field value — NFC, lower-cased, whitespace-collapsed and
truncated to 256 bytes, so a pattern anchored deep into a long activity text may find nothing — and
**you anchor it yourself**: `^post` matches at the start, an unanchored pattern matches anywhere,
and `.` tests that the field is present at all. One pattern per field; an invalid, over-long,
over-complex or empty-string-matching pattern rejects the whole call with `invalid_filter` before
any work is done. `snapshot_status` lists the fields the installed edition can match, in
`match_fields`.

```jsonc
// generic company inboxes in a given industry
{ "nace": "94.91", "match": [ { "field": "email", "pattern": "^(post|info|kontakt|firmapost)[.0-9]*@" } ] }
```

**A point and a radius.** `lat`, `lon` and `radius_km` — all three or none — list the organisations
whose **registered address** falls inside the circle, nearest first, each with `distance_km` and the
address point it was measured from. Give a name query as well and the order stays relevance, with
the radius acting as a filter. The radius is at most **10 km on its own, or 50 km together with
another filter**, and the centre must fall within latitude 57.5 to 81.5 and longitude 4 to 32.

The point is the Kartverket address point of the registered address — the business address for a
main unit, the location address for a sub-unit. It is **not** a building footprint and not
necessarily where the work is done. Sharing a point is the norm rather than the exception — an
accountant's office, a shared business park — so each result says how many records share its point.
Addresses given as c/o, post boxes, foreign addresses and addresses that do not match the address
register get no point and never appear in a radius search.

**Cursor.** Paging has no depth limit: follow the cursor to the end of the result set. `offset` is a
first-call convenience only, capped at 10,000.

### What a lookup can add

`entity_lookup` returns the register entry. Ask for more in `fields`:

| `fields` value | What you get |
|---|---|
| `financials` | Key figures from the latest filed annual accounts, with the year they belong to |
| `filings` | The years actually filed — which also answers for banks and insurers, whose key figures Regnskapsregisteret does not serve |
| `location` | The Kartverket address point of the registered address, or `null` with a reason |
| `unit` | The matrikkel parcel at that address — matrikkelnummer, grunnkrets, parish and tettsted |
| `buildings` | The existing buildings at that address, when one of them is not a home |

`document_year` returns that year's filed annual accounts as an **expiring private link** — a
scanned image with no text layer, not structured figures, and not a second route to them. The
filing itself never travels in an MCP response: what comes back is a link, a size, a checksum and
an expiry.

`unit` and `buildings` describe the parcel and the buildings **at the registered address**. They are
not a statement about property the organisation owns or occupies, and there is no owner data
anywhere in the service.

## What it does not do

- **No roles or persons** — no board members, managing directors or owners.
- **Not the authoritative register.** Brreg is operated by Publifye AS and is not affiliated with
  Brønnøysundregistrene. For anything legally binding, use the official record at
  <https://virksomhet.brreg.no>.
- **Not a reidentification tool.** It is a register of organisations and cannot be used to look
  people up; there are no address-only lookups of individuals.
- **No bulk export.** A search answers a page at a time, followed by cursor; there is no download of
  the register.
- **Sole proprietorships are held back.** E-mail and phone numbers, former names and activity text
  are not shown; they get no map point, no parcel and no buildings; and a search without a name
  never lists them. A `match` term cannot reach one either — personal-data records contribute no
  values to the fields `match` reads.
- **No structured annual accounts.** Key figures and the list of filed years are structured data;
  the accounts themselves are not. A filed year can be handed over as a scanned copy on request, and
  a scan is where it ends — there are no machine-readable notes, line items or auditor's reports.
- **No property ownership.** Nothing from grunnboken; the parcel is the one at the registered
  address.

## Data and licence

**[PROVENANCE.md](PROVENANCE.md)** records each dataset, how it reaches the service, how fresh it
is, and what is withheld. Two licences apply, and a result carries the ones its own content needs.

**Enhetsregisteret and Regnskapsregisteret** are open data from Brønnøysundregistrene under the
Norwegian Licence for Open Government Data (NLOD 2.0). Every successful result carries the
attribution the licence asks for:

> Inneholder data under Norsk lisens for offentlige data (NLOD) tilgjengeliggjort av Brønnøysundregistrene.

**Address points, parcels and buildings** come from Kartverket's Matrikkelen under
[Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). A
result that carries a coordinate or a distance carries the Kartverket attribution too, and says what
Publifye changed — the points were matched to each organisation's registered address and do not show
where a business physically operates. A result that carries a parcel or buildings also carries the
private-register notice that
[utleveringsforskriften](https://lovdata.no/forskrift/2013-12-18-1599) § 5 tenth paragraph requires:

> Opplysningene utleveres fra et privat register (utleveringsforskriften § 5 tiende ledd).

The same regulation's third paragraph forbids using information from grunnboken and matrikkelen for
advertising or marketing without the consent of the party it concerns. That applies to you as a
caller, not only to us.

## Your questions

See **[DATA-HANDLING.md](DATA-HANDLING.md)** for what is logged about a call — never its arguments —
and what leaves the service on your behalf.

## Limits

| | |
|---|---|
| Daily calls | a per-account allowance set by the plan, reset at midnight UTC |
| Key financials | up to 30 fresh fetches from Regnskapsregisteret per minute per account; beyond that, figures already fetched or a note saying when to retry |
| Filed documents | up to 3 fresh document fetches per minute per account; a link lives 15 minutes, and a filing over 40 MiB is not relayed — the answer names the open source URL instead |
| Response size | about 24 KiB by default, adjustable from 4 to 48 KiB; longer results continue with a cursor valid for 15 minutes |
| Radius | at most 10 km on its own, 50 km together with another filter |
| Search depth | none — a cursor pages to the end of the result set; `offset` skips at most 10,000 on the first call |

## Plans

Access needs a Brreg plan on a Publifye account. The current plans:

| Plan | Price | Daily tool calls |
|---|---|---|
| Personal | NOK 49/month or NOK 490/year, incl. VAT | up to 200 |
| Business | NOK 480/month or NOK 4,800/year, excl. VAT (NOK 600 / NOK 6,000 incl. 25% VAT) | up to 2,500 |
| Self-hosted | in development, by quote — [request one](https://brreg.publifye.com/en/store) | no daily quota |

Payment is by card at checkout, through Stripe. Plans and prices can change; **the current ones are
always on <https://brreg.publifye.com>**, and where this page and the site differ, the site is right.
