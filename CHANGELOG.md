# Changelog

Dates are the date the change was made, not the date it was written up.

## 2026-09-25

- **Marriage covenants** at [marriage.publifye.com](https://marriage.publifye.com) are described in
  the Doksi section and in `services/doksi`: a couple's own vows, a Bible verse and one of nine
  designs, typeset by Doksi as a one-page PDF to sign and frame. It uses the Doksi server; there is
  no new server.

## 2026-09-24

- **Vitae joins the index**, the tenth server: your CV as a document you own, 42 tools, generated
  from the service's own registry. Published to the MCP registry as `pro.publifye/vitae`.
- **The index opening is rewritten in plain language.**

## 2026-09-23

- **All nine servers are in the official MCP registry.** Published: `pro.publifye/brreg`,
  `lexar`, `doksi`, `timely` and `audiobible` at 1.0.0, and `currency` republished at 1.0.2 — the
  1.0.1 record advertised `currency.publifye.pro` and carried no `repository`. Every record now names
  a `.com` endpoint and points back to its folder here. Verified against
  `registry.modelcontextprotocol.io` after publishing.
- **Descriptions fit the registry's 100-character limit.** Doksi, Timely, Audio Bible and Currency
  were longer and the registry refused them with a 422; `server.json` and the server cards now
  carry the shorter text.

## 2026-09-22

- **Timely: the publishing narrative is corrected** — the Timely page and the index said
  `draft_approve` refuses every MCP caller. It does not: an assistant can publish, but only with
  `user_confirmed: true` and the `revision`, `content_hash` and `pdf_hash` of the exact preview the
  user was shown, after asking; the tool's description says a request to edit is not consent.
  Both pages now say so.
- **Timely's surface regenerated at 31 tools** — from the registry of source `354ee8b`, version
  0.1.190. That surface is live in production as 0.1.198 (`9ce28e3`, 2026-09-23). New in the customer surface:
  `timely_edit_history`, `timely_request_edit` and `timely_set_pdf_layout`; several descriptions
  are shorter. Fourteen `admin_*` tools and ten log tools stay excluded, listed by name in
  `tools.json`.

## 2026-09-18

- **Brreg search near a point** — `entity_search` takes `lat`, `lon` and `radius_km` (all three or
  none) and lists the organisations whose registered address falls inside the circle, nearest first,
  each with `distance_km` and the address point it was measured from. At most 10 km on its own, or
  50 km together with another filter. A name query keeps relevance order and uses the radius as a
  filter.
- **Brreg lookups can carry the address point, the parcel and the buildings** — `location`, `unit`
  and `buildings`, from Kartverket's Matrikkelen, for the *registered* address. Not a statement
  about property owned or occupied, and never for a sole proprietorship.
- **A second licence, recorded** — Kartverket's data is CC BY 4.0, so a result carrying a coordinate
  or a distance carries the Kartverket attribution beside the NLOD one, and a result carrying a
  parcel or buildings carries the utleveringsforskriften § 5 (10) private-register notice. The
  § 5 (3) ban on using cadastre data for marketing is recorded in
  [DATA-HANDLING.md](services/brreg/DATA-HANDLING.md), because it binds the caller too.
- **Brreg filed annual accounts** — `fields` takes `filings` for the years an organisation has
  actually filed, which also answers for banks and insurers whose key figures Regnskapsregisteret
  does not serve. `document_year` returns that year's filing as a private, expiring link: a scanned
  image, not structured figures, and never inlined in a response.
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
