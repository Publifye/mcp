# Publifye MCP Servers — Scripture research, book authoring and dictionary building for AI clients

**Publifye AS runs three hosted [Model Context Protocol](https://modelcontextprotocol.io) servers.
Point Claude, Cursor, VS Code or any MCP client at them and your assistant can read the Hebrew and
Greek text of Scripture, write and typeset a book, or build a dictionary — over an authenticated
HTTPS endpoint, with no local install.**

This repository is the canonical public reference for those servers: their endpoints, their complete
tool schemas, and the provenance of every dataset behind them. It contains no server code — the
services are hosted and commercial. What it contains is everything you need to evaluate them before
you pay for anything.

| | Darash | Junifye | Lexifye |
|---|---|---|---|
| What it does | Bible research | Book & study authoring | Dictionary building |
| Endpoint | `https://darash-api.publifye.com/mcp` | `https://junifye.publifye.com/mcp` | `https://lexifye.publifye.com/mcp` |
| Capability tools | 35 | 151 | 63 |
| Registry | [`pro.publifye/darash`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | [`pro.publifye/junifye`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | [`pro.publifye/lexifye`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) |
| Reference | [services/darash](services/darash) | [services/junifye](services/junifye) | [services/lexifye](services/lexifye) |

Transport is Streamable HTTP. Authentication is OAuth 2.1 with PKCE (S256) and Dynamic Client
Registration, or a personal API key. See **[docs/connect.md](docs/connect.md)**.

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
credential. Every tool carries `readOnlyHint`, `destructiveHint`, `idempotentHint` and
`openWorldHint`, derived from its access level rather than hand-written, so a client can plan
parallel reads safely.

## What this repository does not contain

No server source, no corpus, no lexicon text. Darash's data is roughly 21.5 GiB and the engine is a
commercial product; publishing it is a business decision and it has been decided against. What is
published here is the *description* — schemas, provenance, endpoints — which is the part you need
to evaluate the service and the part we are willing to be held to.

## Publifye AS

Norwegian publishing house, Oslo. Organisation number **826774622**
([Enhetsregisteret](https://data.brreg.no/enhetsregisteret/api/enheter/826774622) ·
[Wikidata Q141436507](https://www.wikidata.org/wiki/Q141436507)).
Company site **[publifye.com](https://publifye.com)** ·
[Privacy](https://publifye.com/privacy.html) · [Terms](https://publifye.com/terms.html)

Licence for this repository: [CC BY 4.0](LICENSE). The datasets it describes carry their own
licences, recorded per source in each service's `PROVENANCE.md`.
