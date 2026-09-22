# Publifye MCP Servers — Scripture research, book authoring, dictionaries, Norwegian company data, Norwegian law, exchange rates, documents, meeting programmes and an audio Bible, for AI clients

**Publifye AS runs nine hosted [Model Context Protocol](https://modelcontextprotocol.io) servers.
Point Claude, Cursor, VS Code or any MCP client at them and your assistant can read the Hebrew and
Greek text of Scripture, write and typeset a book, build a dictionary, look up Norwegian
organisations in Enhetsregisteret, read the current text of Norwegian law, convert a currency at a
published central-bank rate, render a document to PDF, build a meeting programme, or listen to the World English Bible read aloud — over an
authenticated HTTPS endpoint, with no local install.**

## Quickstart — connect in under a minute

Paste this into your MCP client's config and restart it. Sign-in happens in the browser on first
use: OAuth 2.1 with PKCE and open Dynamic Client Registration, so there is no key to create first
and nothing to install.

```jsonc
{
  "mcpServers": {
    "darash":  { "type": "http", "url": "https://darash-api.publifye.com/mcp" },
    "junifye": { "type": "http", "url": "https://junifye.publifye.com/mcp" },
    "lexifye": { "type": "http", "url": "https://lexifye.publifye.com/mcp" },
    "brreg":   { "type": "http", "url": "https://brreg.publifye.com/mcp" },
    "lexar":   { "type": "http", "url": "https://lexar-api.publifye.com/mcp" },
    "currency":{ "type": "http", "url": "https://currency.publifye.com/mcp" },
    "doksi":   { "type": "http", "url": "https://doksi.publifye.com/mcp" },
    "timely":  { "type": "http", "url": "https://timely.publifye.com/mcp" },
    "audiobible": { "type": "http", "url": "https://audiobible.publifye.com/mcp" }
  }
}
```

Take only the lines you want — each server stands alone.

- **Claude Desktop** — `claude_desktop_config.json`, or add each URL under Settings → Connectors.
- **Claude Code** — `claude mcp add --transport http darash https://darash-api.publifye.com/mcp`
- **Cursor / VS Code** — the same `mcpServers` block in the client's MCP settings file.

Prefer a key to a browser flow? Every endpoint also takes `X-API-Key`. Both routes, and the full
OAuth discovery chain, are in **[docs/connect.md](docs/connect.md)**.

This repository is the canonical public reference for those servers: their endpoints, their complete
tool schemas, and the provenance of every dataset behind them. It contains no server code — the
services are hosted and commercial. What it contains is everything you need to evaluate them before
you pay for anything.

| Server | What it does | Endpoint | Tools | Registry | Reference |
|---|---|---|---|---|---|
| **Darash** | Bible research | `https://darash-api.publifye.com/mcp` | 34 | [`pro.publifye/darash`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | [services/darash](services/darash) |
| **Junifye** | Book & study authoring | `https://junifye.publifye.com/mcp` | 151 | [`pro.publifye/junifye`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | [services/junifye](services/junifye) |
| **Lexifye** | Dictionary building | `https://lexifye.publifye.com/mcp` | 63 | [`pro.publifye/lexifye`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | [services/lexifye](services/lexifye) |
| **Brreg** | Norwegian company register | `https://brreg.publifye.com/mcp` | 6 | [`pro.publifye/brreg`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | [services/brreg](services/brreg) |
| **Lexar** | Norwegian law | `https://lexar-api.publifye.com/mcp` | 7 | [`pro.publifye/lexar`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | [services/lexar](services/lexar) |
| **Currency** | Exchange rates & buying power | `https://currency.publifye.com/mcp` | 7 | [`pro.publifye/currency`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | [services/currency](services/currency) |
| **Doksi** | Documents & PDFs | `https://doksi.publifye.com/mcp` | 22 | [`pro.publifye/doksi`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | [services/doksi](services/doksi) |
| **Timely** | Meeting programmes | `https://timely.publifye.com/mcp` | 31 | [`pro.publifye/timely`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | [services/timely](services/timely) |
| **Audio Bible** | The World English Bible, read aloud | `https://audiobible.publifye.com/mcp` | 10 | [`pro.publifye/audiobible`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | [services/audiobible](services/audiobible) |

Transport is Streamable HTTP throughout. Authentication is OAuth 2.1 with PKCE (S256) and Dynamic
Client Registration, or a personal API key — except Brreg, which is OAuth only. See
**[docs/connect.md](docs/connect.md)**.

---

## Darash — the Hebrew and Greek text, as data

Most Bible tools give a model an English verse. Darash gives it the underlying data: which Hebrew
stem a verb is in, which Strong's numbers actually occur in a given verse, what a 19th-century
lexicon says about a lemma and which print edition that lexicon came from.

Measured on the live service, **2026-09-13**:

| | |
|---|---|
| Translations | 59, across 36 languages |
| Verses indexed | 2,142,531 |
| Cross-references | 446,544 |
| Hebrew lexicon entries | 8,674 |
| Greek lexicon entries | 5,523 |
| Dictionary entries | 217,352, across 13 dictionaries |
| Morphologically parsed verses | 31,167 |
| Koren Torah letters (ELS corpus) | 304,805 |

Every one of those figures comes from the service's own `get_health`, not from a brochure.
Regenerate them yourself once you have a key.

**Why a translation is not enough.** A Greek verb in the active voice can be rendered perfectly
naturally in the passive in English. An argument about who is acting on whom, built on that English
passive, is an argument about the translator. `get_morphology` returns the voice, person and stem
the text actually carries, and `strongs_in_verse` proves a lemma is really in the verse rather than
merely nearby in a concordance.

→ **[services/darash](services/darash)** · [tool schemas](services/darash/tools.json) ·
**[PROVENANCE.md](services/darash/PROVENANCE.md)** — read this one first if you are evaluating the data

## Junifye — write the book, then publish it

Chapter-structured authoring over MCP: blocks, headings, Scripture quotations that resolve against a
real Bible rather than the model's memory, tables, figures, footnote-free typesetting. Output is a
print-ready PDF with the correct binding gutter, screen-reading PDFs, a valid EPUB3 and a web
reader. Right-to-left scripts are supported end to end, and editions can be linked as translations
of one another.

→ **[services/junifye](services/junifye)** · [tool schemas](services/junifye/tools.json)

## Lexifye — dictionaries with versions and sources

Entries, senses, per-definition sources, revision history and restore. Built for terminology work
that has to be defensible later: every definition can carry where it came from, and every change is
recoverable.

→ **[services/lexifye](services/lexifye)** · [tool schemas](services/lexifye/tools.json)

## Brreg — Norwegian organisations, by number or by name

Lookup by organisasjonsnummer, filtered search, and organisational structure over
Brønnøysundregistrene's Enhetsregisteret, with key financials from Regnskapsregisteret fetched only
when a call asks for them. A name returns candidates, never a silent pick. Open data under NLOD 2.0,
attributed in every successful result; not the authoritative register, no roles or persons, no bulk export.

→ **[services/brreg](services/brreg)** · [tool schemas](services/brreg/tools.json) ·
[PROVENANCE.md](services/brreg/PROVENANCE.md) · [DATA-HANDLING.md](services/brreg/DATA-HANDLING.md)

## Lexar — the current text of Norwegian law

6,859 documents from Lovdata: 759 consolidated statutes, 5,112 central regulations and the current
year's Norsk Lovtidend announcements, with the citation and source URL attached to every passage.
Seven tools, and the number is fixed by specification rather than by what got built — richer
capability goes into typed results, not more tools. `resolve` returns candidates and never picks a
statute silently.

It is equally explicit about what it does not hold: no court decisions, no preparatory works, no
local regulations, no historical consolidated versions. **A search returning nothing does not mean
there is no law.** Open data under NLOD 2.0. Source text and navigation, not legal advice.

→ **[services/lexar](services/lexar)** · [tool schemas](services/lexar/tools.json) ·
[PROVENANCE.md](services/lexar/PROVENANCE.md) — including the measured cross-reference miss rate

---

## Currency — a published rate, or nothing

Norges Bank's daily reference rates: 38 currencies against NOK, back to about 1980, plus conversion
and a daily series for charting. The discipline is in what it refuses to do — it never computes,
estimates or interpolates a rate. Norges Bank publishes once per business day, so weekends and
holidays have no rate, and those days come back **as published** rather than carried forward. A
model that wants a number for a Sunday has to decide that for itself, which is where the decision
belongs.

Two further tools price one USD list price into many markets from World Bank GNI per capita (PPP),
and they return two numbers on purpose: `factor`, the recommended multiplier, never above 1.0; and
`raw_factor`, the uncapped measurement, which exceeds 1.0 for countries richer than the United
States. Norway measures about 1.10 — so applying the raw number to a Norwegian price charges above
list, which is exactly what the cap exists to prevent.

→ **[services/currency](services/currency)** · [tool schemas](services/currency/tools.json)

---

## Doksi — ask what a kind requires, then write it

Letters, notices, agreements, ceremonial covenants, checklists, meeting agendas and schedules, each
rendered to a professional PDF. Four of its twenty-two tools exist only so an agent can find out what
is expected **before** it composes anything — which kinds exist, which blocks a body may hold, and
what one specific kind demands. An agent that can ask produces far fewer refusals than one that
learns by being refused.

Signing is a request with a lifecycle, not a flag on a document: create, describe, replace, revoke,
render, mail. A signer gets an individual link or a QR code, and a revoked link stops working.

→ **[services/doksi](services/doksi)** · [tool schemas](services/doksi/tools.json)

---

## Timely — publishing takes the user's explicit yes

A meeting programme for a fixed number of meetings or a calendar period, with every revision kept
immutably and the approved one rendered through Doksi.

An assistant can create, edit, restyle, preview — and publish, with `draft_approve`. The tool
publishes only when `user_confirmed` is `true` and `revision`, `content_hash` and `pdf_hash` name
the exact preview the user was shown; its description tells the assistant to ask first and says a
request to edit is not consent. `user_confirmed` is the assistant's word that the user said yes (the
server records it but cannot see the conversation); the hashes make that yes apply to one revision
and one PDF only, and the stored PDF is published without re-rendering.

Edits apply against a `base_hash` and are refused rather than merged if the programme moved, so two
assistants — or an assistant and a person — cannot quietly overwrite each other.

→ **[services/timely](services/timely)** · [tool schemas](services/timely/tools.json)

---

## Audio Bible — quoted, heard, kept

The World English Bible as text and sound. `get_chapter` returns every verse numbered and tells the
assistant to quote it as returned rather than paraphrase it as scripture; `listen_link` starts the
audio at a given verse with its timing in seconds; `prepare_chapter` has a chapter read aloud on
demand when it is not yet recorded; `download_link` mints a personal, expiring file, and
`my_allowance` says what is left before an assistant promises one. Listening is free.

→ **[services/audiobible](services/audiobible)** · [tool schemas](services/audiobible/tools.json)

---

## Three ways in

**You study the biblical languages.** Darash is the one that matters. Start with `word_study`,
`get_morphology` and `strongs_in_verse`, and read the provenance table before you trust a gloss.

**You want it run privately.** Darash ships as a single self-contained binary of roughly 205 MB,
carrying CLI, HTTP API and MCP server together. It needs no network at all. That is offline
Scripture research infrastructure, not a reading app with an export button — and for institutions
whose data cannot leave the building it is usually the only workable shape. Licensed by quote.

**You are embedding Scripture data in your own product.** The complete input schemas, output shapes
and tool annotations are in this repository, so you can design against them before you hold a
credential. Every Darash tool carries `readOnlyHint`, `destructiveHint`, `idempotentHint` and
`openWorldHint`, derived from its access level rather than hand-written, so a client can plan
parallel reads safely.

## What this repository does not contain

No server source, no corpus, no lexicon text. Darash's data is roughly 21.5 GiB and the engine is a
commercial product; publishing it is a business decision and it has been decided against. What is
published here is the *description* — schemas, provenance, endpoints — which is the part you need
to evaluate the service and the part we are willing to be held to.

## The products these servers belong to

Each server has a site of its own — what it is for, what it costs, and how to get access:

| Server | The product site | What problem it solves |
|---|---|---|
| Darash | [darash.publifye.com](https://darash.publifye.com) · [docs](https://darash.publifye.com/docs) | [publifye.com/darash](https://publifye.com/darash) |
| Junifye | [junifye.publifye.com](https://junifye.publifye.com) | [publifye.com/junifye](https://publifye.com/junifye) |
| Lexifye | [lexifye.publifye.com](https://lexifye.publifye.com) · [docs](https://lexifye.publifye.com/docs) | [publifye.com/lexifye](https://publifye.com/lexifye) |
| Brreg | [brreg.publifye.com](https://brreg.publifye.com) | [publifye.com/brreg](https://publifye.com/brreg) |
| Lexar | [lexar.publifye.com](https://lexar.publifye.com) | [publifye.com/lexar](https://publifye.com/lexar) |
| Currency | [currency.publifye.com](https://currency.publifye.com) | [publifye.com/currency](https://publifye.com/currency) |
| Doksi | [doksi.publifye.com](https://doksi.publifye.com) | — |
| Timely | [timely.publifye.com](https://timely.publifye.com) | — |
| Audio Bible | [audiobible.publifye.com](https://audiobible.publifye.com) | — |

The left column sells the product and gates access. The right column is one
page on the company site saying what the server is for and when one of the
others is the better answer — written for someone deciding between them.

How the work is done, in English, Norwegian, Spanish, Chinese and Korean:
**[blog.publifye.com](https://blog.publifye.com)**.

## Publifye AS

Norwegian publishing house, Oslo. Organisation number **826774622**
([Enhetsregisteret](https://data.brreg.no/enhetsregisteret/api/enheter/826774622) ·
[Wikidata Q141436507](https://www.wikidata.org/wiki/Q141436507)).
Company site **[publifye.com](https://publifye.com)** ·
[Privacy](https://publifye.com/privacy.html) · [Terms](https://publifye.com/terms.html)

Licence for this repository: **[CC BY 4.0](LICENSE)**. It covers the documentation and metadata
here — **not** the datasets the servers serve, which are separate works under their own terms,
recorded per source in each service's `PROVENANCE.md`. See [NOTICE](NOTICE).

## Written about this work

- [Thayer's Greek Lexicon, rebuilt from the 1889 page scans](https://blog.publifye.com/p/rebuilding-thayer-s-greek-lexicon-entry-by-entry-against-the-1889-page)
- [Darash vs Logos, Accordance and Blue Letter Bible — an honest comparison](https://blog.publifye.com/p/darash-vs-logos-accordance-and-blue-letter-bible-an-honest-comparison)
- [How to connect Claude, ChatGPT or Cursor — MCP and DCR explained](https://blog.publifye.com/p/how-your-ai-connects-to-darash-junifye-and-lexifye-mcp-and-dcr)
- [Deuteronomy 4:29 says "seek" twice. The Hebrew does not.](https://blog.publifye.com/p/deuteronomy-4-29-says-seek-twice-the-hebrew-does-not)
- [Two arks, one word](https://blog.publifye.com/p/two-arks-one-word)

Each is published in English, Norwegian, Spanish, Chinese and Korean at
**[blog.publifye.com](https://blog.publifye.com)**.
