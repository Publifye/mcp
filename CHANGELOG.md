# Changelog

Dates are the date the change was made, not the date it was written up.

## 2026-09-15

- Brreg added: lookup, search and name resolution over Brønnøysundregistrene's Enhetsregisteret,
  with key financials from Regnskapsregisteret on request. Endpoint `https://brreg.publifye.com/mcp`,
  OAuth only. See [services/brreg](services/brreg).
- Tool schemas generated from the customer-plane `tools/list` of the release serving production —
  6 capability tools, with the 25 tools hidden from customers listed by name.
- Plans on sale: Personal and Business, paid by card. Current prices are on
  <https://brreg.publifye.com>.
- Data sources, licence and what is withheld recorded in
  [services/brreg/PROVENANCE.md](services/brreg/PROVENANCE.md); what is logged about a call in
  [services/brreg/DATA-HANDLING.md](services/brreg/DATA-HANDLING.md).
- `pro.publifye/brreg` registry record prepared in `server.json`; not yet published to the registry.

## 2026-09-13

- Repository created. Public reference for the Darash, Junifye and Lexifye MCP servers:
  endpoints, complete tool schemas and dataset provenance.
- Tool schemas captured from each live service's own `tools/list`
  — Darash 35 capability tools, Junifye 151, Lexifye 63.
- Provenance recorded for all 13 Darash dictionaries and both Strong's lexicons, including the
  fields that are **not** established. See [services/darash/PROVENANCE.md](services/darash/PROVENANCE.md).
- Endpoints documented on `publifye.com`. The `publifye.pro` hostnames still resolve and redirect.
