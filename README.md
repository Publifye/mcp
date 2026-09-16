# Publifye MCP Servers — Scripture research, book authoring, dictionaries, Norwegian company data and Norwegian law, for AI clients

**Publifye AS runs five hosted [Model Context Protocol](https://modelcontextprotocol.io) servers.
Point Claude, Cursor, VS Code or any MCP client at them and your assistant can read the Hebrew and
Greek text of Scripture, write and typeset a book, build a dictionary, look up Norwegian
organisations in Enhetsregisteret, or read the current text of Norwegian law — over an
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
    "lexar":   { "type": "http", "url": "https://lexar-api.publifye.pro/mcp" }
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

| | Darash | Junifye | Lexifye | Brreg | Lexar |
|---|---|---|---|---|---|
| What it does | Bible research | Book & study authoring | Dictionary building | Norwegian company register | Norwegian law |
| Endpoint | `https://darash-api.publifye.com/mcp` | `https://junifye.publifye.com/mcp` | `https://lexifye.publifye.com/mcp` | `https://brreg.publifye.com/mcp` | `https://lexar-api.publifye.pro/mcp` |
| Capability tools | 35 | 151 | 63 | 6 | 7 |
| Registry | [`pro.publifye/darash`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | [`pro.publifye/junifye`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | [`pro.publifye/lexifye`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) | `pro.publifye/brreg` (not yet published) | `pro.publifye/lexar` (not yet published) |
| Reference | [services/darash](services/darash) | [services/junifye](services/junifye) | [services/lexifye](services/lexifye) | [services/brreg](services/brreg) | [services/lexar](services/lexar) |

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

| | |
|---|---|
| [darash.publifye.com](https://darash.publifye.com) | Darash — Scripture research. [Documentation](https://darash.publifye.com/docs) |
| [junifye.publifye.com](https://junifye.publifye.com) | Junifye — write and publish a book with your AI |
| [lexifye.publifye.com](https://lexifye.publifye.com) | Lexifye — build and publish a dictionary. [Documentation](https://lexifye.publifye.com/docs) |
| [brreg.publifye.com](https://brreg.publifye.com) | Brreg — the Norwegian company register |
| [lexar.publifye.com](https://lexar.publifye.com) | Lexar — Norwegian law |
| [blog.publifye.com](https://blog.publifye.com) | How this work is done, in English, Norwegian, Spanish, Chinese and Korean |

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
