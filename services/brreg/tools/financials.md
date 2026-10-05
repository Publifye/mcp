# Key financials

**What has it filed, and what do the figures say?** 1 Brreg MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://brreg.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | What it does |
|---|---|
| [`entity_financials`](#entity_financials) | Money for an organisation: key figures, the years actually filed, the industry benchmark… |

---

## `entity_financials`

**Entity Financials** — read-only, idempotent, open-world.

Money for an organisation: key figures, the years actually filed, the industry benchmark and the filed document. The one tool that reaches upstream for figures.
ARGS: orgnr (one) or orgnrs (a batch, answered in input order). include selects blocks: key_figures (the default), filings, sector_benchmark. document_year asks for that year's filed document (one orgnr only).
FETCHING: figures come from Regnskapsregisteret, fetched only when this tool is called, then stored. One orgnr waits up to 3 s; a batch answers stored, fetching or queue_full — ask again shortly. Over the caller's budget the answer is rate_limited with financials_retry_after_seconds. A year already held is never refetched.
FILINGS: which accounting years an enhet has FILED. It answers for banks and insurers, whose key figures are not_supported.
BENCHMARK: sector_benchmark judges the figures against Statistics Norway's industry-and-size statistics (CC BY 4.0, its own attribution block). It is per industry, never per company, and it names the level that answered rather than silently widening.
DOCUMENT: document_year hands over an expiring private link. It is a SCANNED IMAGE with no text layer: give the link to the user, never fetch it to read — the figures, if any, are in key_figures.
UNDERENHET: an underenhet is answered, not refused — it files nothing of its own, so the answer is found=true with no financials block; ask its parent enhet.
REFUSALS: an ENK's accounts are personal data: customers get them through a single orgnr, never in a batch.
Example: entity_financials orgnr="983 887 457" include=["key_figures","filings"]. Next: entity_lookup orgnr=<orgnr>. [END]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `compact` | boolean | no | One-line text summary, not duplicated JSON. |
| `cursor` | string | no | Next-page token; send it alone (+max_bytes, compact). |
| `document_year` | integer | no | That year's filed accounts as an expiring link (single orgnr). A scanned image: no text to extract. |
| `include` | array of string | no | key_figures (default), filings (years actually filed), sector_benchmark (SSB industry comparison). |
| `max_bytes` | integer | no | Response byte budget (default 24576). |
| `orgnr` | string | no | One organisasjonsnummer; spaces and dots tolerated (983 887 457). |
| `orgnrs` | array of string | no | Several organisasjonsnummer, answers in input order. |
| `snapshot_id` | string | no | Pin a snapshot (else snapshot_expired). |

---

*Generated from the live `tools/list` of the release serving production (0.3.32) on 2026-09-29. Regenerate rather than edit by hand.*
