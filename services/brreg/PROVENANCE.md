# Dataset provenance

**Brreg serves Brønnøysundregistrene's open data, placed on the map with Kartverket's open address
register. This page records which datasets, how each reaches the service, how fresh it is, and what
is deliberately left out.**

## Sources

| Dataset | What Brreg takes from it | How it arrives | Freshness |
|---|---|---|---|
| Enhetsregisteret — enheter | main units | full bulk file from data.brreg.no | rebuilt weekly |
| Enhetsregisteret — underenheter | sub-units | full bulk file from data.brreg.no | rebuilt weekly |
| Enhetsregisteret — updates | removals from open data | the register's updates feed | checked at least daily; applied within 24 hours |
| Regnskapsregisteret — key figures | key figures from the latest filed annual accounts | fetched per organisasjonsnummer, only when a call asks for `financials`, then stored | as filed, shown with the year they belong to |
| Regnskapsregisteret — filed documents | which years an organisation has filed, and one year's filed document on request | fetched per organisasjonsnummer, only when a call asks for `filings` | as filed |
| Kartverket — Matrikkelen – Adresse | the address point of each registered address | national bulk file from Geonorge | refreshed weekly with the register |
| Kartverket — Matrikkelen – Bygningspunkt | the existing buildings at that address | national bulk file from Geonorge | refreshed weekly with the register |
| Kartverket — Matrikkelen – Adresse Leilighetsnivå | the section number, when the address has exactly one | national bulk file from Geonorge | refreshed weekly with the register |
| Codes | organisation forms, municipalities, industry codes (NACE) and institutional sectors, with counts | derived from the current edition | with each edition |

A lookup with `live=true` also checks that one entry against data.brreg.no at the moment of the call.

## The edition this page describes

The edition the live service was serving on 2026-09-15:

| | |
|---|---|
| Main units (enheter) | 1,174,268 |
| Sub-units (underenheter) | 863,374 |
| Sole proprietorships (ENK), among the main units | 462,855 |
| Public bodies | 4,220 |
| Main units with annual accounts on file | 449,313 |

Call `snapshot_status` for the edition that is current when you read this. It returns when it was
acquired, its age, the source ETag and Last-Modified of each bulk file, the record counts, and the
fields the installed edition can match with `match`.

## Placing an organisation on the map

Enhetsregisteret carries no address key, so an entry cannot simply be joined to Kartverket's address
register. Brreg joins them **by a deterministic text match on the address itself**, and it does so
once a week when the edition is built — never while answering a call. The result is auditable: each
point says at what level it matched, and each missing point says why it is missing.

Which address is used is stated in the answer as `location_basis`: the **business address** for a
main unit, the **location address** for a sub-unit. A postal address is never geocoded.

In the edition above, about **77%** of main units and **82%** of sub-units had a point. The rest did
not, and the reason is always given — a foreign address, a c/o address, a post box, an address line
with no street number, a street the register does not know, an ambiguous match, and so on. Those two
figures count the whole edition; a customer sees fewer, because sole proprietorships are given no
point at all.

**What a point is not.** It is the point of the *registered address*, not of the place where work is
done, and it is rarely unique: an accountant's office address or a shared business park carries many
organisations at one point. Every answer carrying points therefore says how many records share each
one.

`unit` and `buildings` describe the parcel and the buildings **at that same registered address**.
They say nothing about what an organisation owns or occupies. A section number is returned only when
the address has exactly one; otherwise the count of sections is returned and nothing is guessed. Only
buildings that exist are counted — buildings that are merely approved, under construction or
demolished are left out — and building details appear only where at least one existing building is
not a home.

## Licence and attribution

### Brønnøysundregistrene — NLOD 2.0

The register data is open data from Brønnøysundregistrene under the
[Norwegian Licence for Open Government Data (NLOD 2.0)](https://data.norge.no/nlod/no/2.0). Every
successful result carries an `attribution` object whose text is the sentence the licence asks for,
verbatim:

> Inneholder data under Norsk lisens for offentlige data (NLOD) tilgjengeliggjort av Brønnøysundregistrene.

The same object names the licence, the source (`https://data.brreg.no`) and this notice:

> Fields selected and normalized; not the authoritative register — verify at https://virksomhet.brreg.no

### Kartverket — CC BY 4.0

Address points, parcels and buildings come from Kartverket's Matrikkelen, published on Geonorge
under [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/). A result
that carries a coordinate or a distance carries a second attribution block naming Kartverket, the
licence, the link and what was changed:

> Inneholder adressepunkter fra Matrikkelen – Adresse, © Kartverket, lisensiert under CC BY 4.0. Endret: adressepunktene er koblet av Publifye til enhetens registrerte adresse og viser ikke virksomhetens fysiske lokalisering.

A result that carries a parcel or buildings names all three Kartverket datasets instead, and adds
the notice that [utleveringsforskriften](https://lovdata.no/forskrift/2013-12-18-1599) § 5 tenth
paragraph requires of a private register:

> Opplysningene utleveres fra et privat register (utleveringsforskriften § 5 tiende ledd).

Both blocks are carried in English as well. The same regulation's third paragraph forbids using
information from grunnboken and matrikkelen for advertising or marketing without the consent of the
party it concerns; that obligation runs to whoever uses the data, including you.

### Not the authoritative register

Brreg is operated by Publifye AS. It is not affiliated with Brønnøysundregistrene or Kartverket and
is not the authoritative register. For anything legally binding, use the official record at
<https://virksomhet.brreg.no>.

## What is withheld

**Roles and persons.** The role registers are not acquired. There are no board members, managing
directors or owners anywhere in the service.

**Ownership.** Grunnboken is not acquired, and no dataset here says who owns anything. The parcel
and buildings a lookup can return are those at the registered address.

**Sole proprietorships.** A sole proprietorship (ENK) is one person's business, so the register
entry is that person's data. For an ENK and its sub-units, e-mail, phone, mobile and register
annotations are removed when the edition is built. Former names and activity text are not shown to
customers; key financials appear only in a lookup of that single number, and a filed document is
never handed to a customer at all. They are given no map point, no parcel and no buildings, they are
never members of a radius search, they are not counted among the records sharing a point, and a
search without a name never returns them. They also contribute no values to the fields `match`
reads, so no regular expression can reach one.

**Accounts beyond the key figures.** Full annual accounts, notes and auditor's reports are not
included. A filed document can be handed over as an expiring link on request, but it is a scanned
image with no text layer: it is a copy of a filing, not a route to structured figures, and every
answer that lists filed years says so.

**Bulk copies.** A search answers a page at a time, followed by cursor, and there is no export.
Paging has no depth limit, but the per-account allowances, the rate limits and the radius caps all
stand between a caller and a copy of the register.

## Removals

When Brønnøysundregistrene removes an entry from open data — seen in the updates feed, or as HTTP
410 on a live check — Brreg suppresses it within 24 hours, and a lookup of that number answers
`found: false` with `reason: removed`; searches leave it out.
