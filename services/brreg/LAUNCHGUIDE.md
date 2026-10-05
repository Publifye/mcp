# Brreg

## Tagline
Norway's company register (Enhetsregisteret) for AI: lookup, search, name resolution, key financials

## Description
Brreg gives an AI assistant Brønnøysundregistrene's Enhetsregisteret as structured data. Look an organisation up by organisasjonsnummer, turn a name into candidates without a silent pick, search with filters, regular expressions or a point and a radius, and see how organisations belong together. Key financials from Regnskapsregisteret, and an industry benchmark from Statistics Norway, are fetched when you ask for them.

It is a hosted server with a Streamable HTTP endpoint at https://brreg.publifye.com/mcp, so there is nothing to install. A number is exact and a name is not: `entity_lookup` checks the checksum and is never fuzzy, while `entity_resolve` returns candidates and states whether the match is unique, ambiguous or unresolved. No language model is involved in answering a call, and every result names the register edition it came from.

It is for analysts, sales and compliance teams, journalists and developers who need grounded Norwegian company data. It is not the authoritative register; use https://virksomhet.brreg.no for anything legally binding.

## Setup Requirements
No setup required — sign in with OAuth in the browser on first use.

## Category
Business Tools

## Use Cases
Company lookup by organisasjonsnummer, name resolution, supplier research, sales prospecting, due diligence, finding companies near a place, industry benchmarking, annual accounts key figures, corporate structure mapping

## Features
- Exact lookup by organisasjonsnummer with checksum validation
- Name resolution that returns candidates with `resolution` set to unique, ambiguous or unresolved, never a silent pick
- Ranked search over current and historical names, addresses and websites, with filters taken from `code_list`
- Regular-expression matching over activity, address, city, email, name, phone or website
- Radius search around a point or a company, nearest first, at most 10 km on its own or 50 km with another filter
- Straight-line distance from one place to up to 50 others
- Parent and child structure of an organisation
- Key figures and filed years from Regnskapsregisteret, fetched only when asked
- Industry benchmark from Statistics Norway for the industry and size band
- Filed annual accounts as an expiring private link (a scanned image, not structured data)
- Register edition of 2026-09-29: 1,175,793 main units and 866,095 sub-units, rebuilt weekly
- Every result carries the NLOD attribution and a snapshot id that can be pinned for a session
- All nine tools are read-only
- Sole proprietorships are held back: no e-mail, phone, map point or search listing without a name
- No roles or persons, no bulk export

## Getting Started
- "Look up this organisasjonsnummer and tell me the company's industry and registered address"
- "Find the organisation called Equinor and tell me if the match is unique"
- "Which organisations are registered within 1 km of the company with this organisasjonsnummer?"
- "How far apart are these two companies, and which of my suppliers is closest to our office?"
- "Show the key figures and filed years for this company, and compare with its industry"
- Tool: entity_lookup — exact lookup by organisasjonsnummer, optionally with subunits, financials or location
- Tool: entity_resolve — turn a name into organisation candidates, never an implicit pick
- Tool: entity_search — ranked, filtered search by name, address, website, regular expression or radius
- Tool: entity_nearby — organisations registered near a place or a company, nearest first
- Tool: entity_distance — straight-line distance between registered addresses
- Tool: entity_financials — key figures, filed years, industry benchmark and the filed document

## Tags
norway, company-register, enhetsregisteret, brreg, business-data, organisation-number, financials, due-diligence, geospatial, open-data, nlod, supplier-check, sales, lookup, search

## Documentation URL
https://github.com/Publifye/mcp/tree/main/services/brreg

## Health Check URL
https://brreg.publifye.com/health
