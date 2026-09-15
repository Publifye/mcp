# Brreg — Norwegian company register MCP server for Claude, Cursor and any MCP client

**Brreg gives an AI assistant Brønnøysundregistrene's Enhetsregisteret as structured data: look an
organisation up by organisasjonsnummer, turn a name into candidates without a silent pick, search
with filters, and see how organisations belong together — with key financials from
Regnskapsregisteret when you ask for them. It runs as a hosted MCP server over HTTPS.**

| | |
|---|---|
| Endpoint | `https://brreg.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open · no API keys |
| Registry | `pro.publifye/brreg` ([server.json](server.json); not yet published to the registry) |
| Product site | <https://brreg.publifye.com> |
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
open data is dropped within 24 hours. `snapshot_status` returns the id, age and counts of whichever
edition is current, and every successful result names the edition it came from.

## A number is exact; a name is not

`entity_lookup` takes an organisasjonsnummer, checks its checksum, and is never fuzzy.

`entity_resolve` takes a name and returns **candidates**, with `resolution` set to `unique`,
`ambiguous` or `unresolved` and the order of the candidates stated. It never claims the first
candidate is the organisation. Norwegian spellings are compared through one documented key — æ, ø
and å folded, legal forms such as AS and ASA stripped, former names matched — so the comparison can
be checked rather than trusted.

No language model is involved in answering a call. Every successful result carries the snapshot id
and the licence attribution, so an answer can be traced to the edition it came from.

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
entry against data.brreg.no, and when `fields` includes `financials` it fetches key figures from
Regnskapsregisteret.

## What it does not do

- **No roles or persons** — no board members, managing directors or owners.
- **Not the authoritative register.** Brreg is operated by Publifye AS and is not affiliated with
  Brønnøysundregistrene. For anything legally binding, use the official record at
  <https://virksomhet.brreg.no>.
- **No bulk export.** A search pages through at most 10,000 results.
- **Sole proprietorships are held back.** E-mail and phone numbers, former names and activity text
  are not shown, and a search without a name never lists them.
- **No full annual accounts**, notes or auditor's reports — key figures only.

## Data and licence

**[PROVENANCE.md](PROVENANCE.md)** records each dataset, how it reaches the service, how fresh it
is, and what is withheld. The data is open data from Brønnøysundregistrene under the Norwegian
Licence for Open Government Data (NLOD 2.0), and every successful result carries the attribution
the licence asks for:

> Inneholder data under Norsk lisens for offentlige data (NLOD) tilgjengeliggjort av Brønnøysundregistrene.

## Your questions

See **[DATA-HANDLING.md](DATA-HANDLING.md)** for what is logged about a call — never its arguments —
and what leaves the service on your behalf.

## Limits

| | |
|---|---|
| Daily calls | a per-account allowance set by the plan, reset at midnight UTC |
| Key financials | up to 30 fresh fetches from Regnskapsregisteret per minute per account; beyond that, figures already fetched or a note saying when to retry |
| Response size | about 24 KiB by default, adjustable from 4 to 48 KiB; longer results continue with a cursor valid for 15 minutes |
| Search depth | 10,000 results per query; narrow with filters to reach the rest |

## Plans

Access needs a Brreg plan on a Publifye account. The current plans:

| Plan | Price | Daily tool calls |
|---|---|---|
| Personal | NOK 49/month or NOK 490/year, incl. VAT | up to 200 |
| Business | NOK 480/month or NOK 4,800/year, excl. VAT (NOK 600 / NOK 6,000 incl. 25% VAT) | up to 2,500 |
| Self-hosted | by arrangement — [contact us](https://publifye.com/support.html) | |

Payment is by card at checkout, through Stripe. Plans and prices can change; **the current ones are
always on <https://brreg.publifye.com>**, and where this page and the site differ, the site is right.
