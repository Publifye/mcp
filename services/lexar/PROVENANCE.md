# Lexar — source provenance

**Where the text comes from, under what licence, how much of it there is, and — the part that
decides whether Lexar can answer your question — what it does not hold.**

Figures measured on the live service via `status`, 2026-09-16. Call `status` yourself and you get
the same record.

## Source

| | |
|---|---|
| Publisher | Lovdata |
| Route | the free `publicData` API — no registration, no API key |
| Datasets | `gjeldende-lover`, `gjeldende-sentrale-forskrifter`, `lovtidend-avd1-2026` |
| Acquired | 2026-09-12 |
| Source snapshot | `82cff3294c90969e6fc78393d5d24c842e5555ac323593904b104afe1c5e4f11` |
| Licence | [NLOD 2.0](https://data.norge.no/nlod/no/2.0) |

The website is never scraped to fill a coverage gap. Only filenames obtained from the published
catalogue are fetched, one at a time, honouring the rate-limit headers the API returns.

## Licence and attribution

> Inneholder data fra Lovdata under Norsk lisens for offentlige data (NLOD) 2.0.

NLOD 2.0 permits commercial reuse, adaptation and redistribution, subject to its own conditions:
attribution, no misleading presentation, no implied endorsement, and identification of changes. It
does not grant rights the licensor cannot license, and it does not displace privacy or third-party
requirements.

**What is sold is the service, not the corpus** — hosted access, indexing, availability and
operation. The underlying open legal data stays open, and nothing here restricts a right NLOD
already grants you. Lexar's formatting, indexes and derived classifications are identified
separately from the source text, and a reformatted excerpt is never presented as an unmodified
official publication.

## What is in the corpus

| | |
|---|---|
| Documents | **6,859** |
| — current consolidated law | 5,871 |
| — of which statutes | 759 |
| — of which central regulations | 5,112 |
| — announcements (Norsk Lovtidend avd. I, 2026) | 988 |
| Indexed blocks | 457,743 |
| Distinct word forms | 301,140 |
| Document aliases | 5,054 keys · 1,566 conventional forms · 333 ambiguous |

By language: 4,275 `no`, 2,429 `nb`, 154 `nn`, 1 unrecognised.

Announcements are a separate expression collection from consolidated law and are counted
separately. Conflating the two would inflate any claim about how much current law is held.

## What is NOT in the corpus

This is the part worth reading twice, because **a search returning nothing does not mean there is
no law** — it may mean the answer lives where Lexar does not look.

- **Court decisions.** Excluded deliberately, on a legal assessment of their status, not for want
  of effort.
- **Preparatory works** (*forarbeider*) — often exactly what settles how a provision is read.
- **Local regulations.** Central regulations only.
- **English translations.** Norwegian source wording only.
- **Historical consolidated versions.** The current consolidation, not the law as it stood on a
  past date. There is no point-in-time `as_of` API and none is simulated.

## The measured gap in cross-references

Lexar extracts **290,805** references from `href` attributes in the source bodies. Of those:

| | |
|---|---|
| Resolved to a document in the corpus | 120,552 |
| Ambiguous | 1,320 |
| Unresolved | 166,579 |
| — pointing outside the corpus | 155,679 |
| — of which to laws or regulations not loaded | 108,562 |
| — of which to EU legal acts | 41,946 |
| — of which to other Lovdata collections | 5,108 |
| — target document is in the corpus but the link did not resolve | 10,900 |

**Roughly 57% of the references in the source text point somewhere Lexar does not hold**, and most
of that is the coverage boundary above rather than a defect. It is published because a connection
graph quoted without its miss rate invites the reader to believe it is complete.

The 10,900 that *should* have resolved and did not are the genuine defect in that table, and they
are counted rather than rounded away.

## Uncertainty the tools carry rather than hide

- **A document being present is not proof that every provision in it is in force.** Publication,
  consolidation and legal commencement are three separate facts.
- `legal_effect` is reported as unknown unless an explicit source fact supports something narrower.
- Filtering by role — body text, amendment notes — is *structural*, not a legal opinion.
- A source link establishes where wording sits. It does not establish an interpretation.
- A valid corpus can be served while Lovdata itself is unreachable; `status` carries the
  acquisition and source-modification dates so staleness is visible rather than assumed.

## Quoting it correctly

Quote only the exact wording `read` returns, concatenating consecutive segments in `start_byte`
order, and cite the citation and `source_url`. Norwegian source wording is preserved; rendered
whitespace may normalise layout, but any textual omission is explicit.

**Lexar provides source text and navigation. It does not generate legal advice.**
