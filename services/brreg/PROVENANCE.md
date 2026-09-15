# Dataset provenance

**Everything Brreg serves comes from Brønnøysundregistrene's open data, under NLOD 2.0. This page
records which datasets, how each reaches the service, how fresh it is, and what is deliberately
left out.**

## Sources

| Dataset | What Brreg takes from it | How it arrives | Freshness |
|---|---|---|---|
| Enhetsregisteret — enheter | main units | full bulk file from data.brreg.no | rebuilt weekly |
| Enhetsregisteret — underenheter | sub-units | full bulk file from data.brreg.no | rebuilt weekly |
| Enhetsregisteret — updates | removals from open data | the register's updates feed | checked at least daily; applied within 24 hours |
| Regnskapsregisteret | key figures from the latest filed annual accounts | fetched per organisasjonsnummer, only when a call asks for `financials`, then stored | as filed, shown with the year they belong to |
| Codes | organisation forms, municipalities, industry codes (NACE) and institutional sectors, with counts | derived from the current edition | with each edition |

A lookup with `live=true` also checks that one entry against data.brreg.no at the moment of the call.

## The edition this page describes

The edition the live service was serving on 2026-09-15:

| | |
|---|---|
| Snapshot id | `f7e6d0b8f096c189d82477c1f1338184775125bc2381a4f5fb934f16f0c45af0` |
| Acquired | 2026-09-15 06:51 UTC |
| Main units (enheter) | 1,174,268 |
| Sub-units (underenheter) | 863,374 |
| Sole proprietorships (ENK), among the main units | 462,855 |

Call `snapshot_status` for the edition that is current when you read this. It returns the snapshot
id, when it was acquired, its age, the source ETag and Last-Modified of each bulk file, and the
record counts.

## Licence and attribution

The register data is open data from Brønnøysundregistrene under the
[Norwegian Licence for Open Government Data (NLOD 2.0)](https://data.norge.no/nlod/no/2.0). Every
successful result carries an `attribution` object whose text is the sentence the licence asks for,
verbatim:

> Inneholder data under Norsk lisens for offentlige data (NLOD) tilgjengeliggjort av Brønnøysundregistrene.

The same object names the licence, the source (`https://data.brreg.no`) and this notice:

> Fields selected and normalized; not the authoritative register — verify at https://virksomhet.brreg.no

Brreg is operated by Publifye AS. It is not affiliated with Brønnøysundregistrene and is not the
authoritative register. For anything legally binding, use the official record at
<https://virksomhet.brreg.no>.

## What is withheld

**Roles and persons.** The role registers are not acquired. There are no board members, managing
directors or owners anywhere in the service.

**Sole proprietorships.** A sole proprietorship (ENK) is one person's business, so the register
entry is that person's data. For an ENK and its sub-units, e-mail, phone, mobile and register
annotations are removed when the edition is built. Former names and activity text are not shown to
customers, key financials appear only in a lookup of that single number, and a search without a
name never returns them.

**Accounts beyond the key figures.** Full annual accounts, notes and auditor's reports are not
included.

**Bulk copies.** A search pages through at most 10,000 results, and there is no export.

## Removals

When Brønnøysundregistrene removes an entry from open data — seen in the updates feed, or as HTTP
410 on a live check — Brreg suppresses it within 24 hours, and a lookup of that number answers
`found: false` with `reason: removed`; searches leave it out.
