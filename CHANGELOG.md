# Changelog

Dates are the date the change was made, not the date it was written up.

## 2026-09-18

- **Brreg `entity_search` takes `match`** — 1 to 4 `{field, pattern}` regex terms over activity,
  address, city, email, name, phone or website, AND'ed with each other and with every other filter.
  RE2, at most 200 bytes, matched case-insensitively against the normalised field value and anchored
  by the caller. Personal-data records — sole proprietorships and their establishments — carry no
  field values, so a `match` term never returns one.
- **Search items carry `email`** — the address registered in Enhetsregisteret, absent for
  personal-data records.
- **The 10,000-result paging depth is gone** — a cursor pages to the end of the result set on every
  plane, and `depth_limit_reached` is no longer part of the envelope. `offset` is unchanged: a
  first-call convenience, at most 10,000.

## 2026-09-16

- **Lexar added** — the current text of Norwegian law from Lovdata: 6,859 documents, 7 research
  tools, full schemas, and a provenance record that publishes the cross-reference miss rate rather
  than only the resolved count.
- **Quickstart** at the top of the README — a copy-pasteable `mcpServers` block for all five
  servers, plus the Claude Code one-liner. Everything here served evaluation; nothing served first
  contact.
- **Live product sites linked** — darash, junifye, lexifye, brreg, lexar and the blog.
- **LICENSE is now the canonical CC BY 4.0 text**, so the licence is detected rather than reported
  as NOASSERTION. The scope caveat it used to carry moved to NOTICE, where it is not competing with
  licence detection: the repository is CC BY 4.0, the datasets are not.

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
