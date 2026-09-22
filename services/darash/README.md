# Darash — Bible research MCP server for Claude, Cursor and any MCP client

**Darash gives an AI assistant the Hebrew and Greek text of Scripture as structured data: which
stem a verb is in, which Strong's numbers actually occur in a verse, what a named 19th-century
lexicon says about a lemma, and which printed edition that lexicon came from. It runs as a hosted
MCP server over HTTPS — there is nothing to install.**

| | |
|---|---|
| Endpoint | `https://darash-api.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open · or `X-API-Key` |
| Registry | [`pro.publifye/darash`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) ([server.json](server.json)) |
| Product site | <https://darash.publifye.com> |
| What it solves | <https://publifye.com/darash> |
| Capability tools | **34** ([full schemas](tools.json)) |

## Connect

```jsonc
{ "mcpServers": { "darash": { "type": "http", "url": "https://darash-api.publifye.com/mcp" } } }
```

The OAuth flow runs in the browser on first use. Full detail, including the API-key route and the
discovery chain: **[../../docs/connect.md](../../docs/connect.md)**.

## The corpus

Measured on the live service, **2026-09-13**, via `get_health`:

| | |
|---|---|
| Translations | 59, across 36 languages |
| Verses indexed | 2,142,531 |
| Cross-references | 446,544 |
| Hebrew lexicon entries | 8,674 |
| Greek lexicon entries | 5,523 |
| Dictionary entries | 217,352, across 13 dictionaries |
| Morphologically parsed verses | 31,167 |
| Koren Torah letters | 304,805 |

Included among the 59: the **Leningrad Codex** (`wlc`) and the **Byzantine Majority** Greek text.
Strong's is augmented with the full **Abbott-Smith**, **LSJ** and **BDB**.

## Why a translation is not enough

A Greek verb in the active voice can be rendered perfectly naturally in the passive in English. An
argument about who is acting on whom, built on that English passive, is an argument about the
translator rather than about the text.

`get_morphology` returns the voice, person and stem the text actually carries. `strongs_in_verse`
proves a lemma is genuinely in a verse rather than merely adjacent to it in a concordance. That
distinction is the whole reason this server exists.

## What the tools do

Every tool is documented with its exact description, annotations and input schema —
34 in all, generated from the service's own `tools/list`, never written by hand.

| Area | The question it answers | Tools |
|---|---|---|
| **[Reading the text](tools/text.md)** | Which verse, chapter or book does the text actually contain, and how do translations differ? | 11 |
| **[Hebrew and Greek](tools/original-language.md)** | What is this word, grammatically and lexically — voice, person, stem, lemma, and what the lexicons say? | 9 |
| **[Study and cross-reference](tools/study.md)** | What else does Scripture say about this, and which words move together? | 6 |
| **[Dictionaries](tools/dictionaries.md)** | What do the reference works say, and which work is it? | 4 |
| **[Search](tools/search.md)** | Find it by wording, by meaning, or by how rare it is. | 4 |

Machine-readable: **[tools.json](tools.json)** carries all 42 callable tools (34 capability, 8 session/cache) with full JSON Schema, plus every excluded bucket listed by name so the count is auditable.


## Provenance — read this before you trust a gloss

**[PROVENANCE.md](PROVENANCE.md)** records, for every dictionary and both Strong's lexicons: the
printed work, the edition, how the text reached us, the licence, and what is **not** established.

One dictionary is marked `verified` — collated against the printed edition it claims to be. The
rest are marked `conventional`, meaning the title and author are as distributed and have not been
collated. Most vendors in this space ship the same public-domain texts and do not draw that
distinction. We draw it because a reader deciding how much weight a gloss can carry needs it.

The file also carries a corrections section. In September 2026 we found that a dictionary served
under the key `thayer` was not Thayer; it was archived with a digest and replaced with a
transcription of the 1889 Corrected Edition read from page images — 716 body pages, two independent
passes collated at 98.91% agreement over 856,793 tokens, with ambiguous headwords **refusing to
resolve rather than guessing**. The provenance work is what found the error. That is the argument
for publishing it.

## Self-hosting

Darash also ships as a single self-contained binary of roughly 205 MB, carrying CLI, HTTP API and
MCP server together, running fully offline with no network call at any point. For institutions
whose material cannot leave the building, that is usually the only workable shape. Licensed by
quote — see the product site.

The ELS / Torah-code research tools are part of the self-hosted Engine only. They are not in the
hosted plans, are not listed in [tools.json](tools.json), and are enforced server-side rather than
merely hidden.

## Plans

Three ways in — a personal key for any MCP client, an always-on agent, and a self-hosted or managed
licence by quote. There is a free trial. **Current plans and prices are on
<https://darash.publifye.com>**, which is the only place they are authoritative; they are
deliberately not duplicated here, because a price in a repository is a price that goes stale.

## Written about this work

Published, each also in Norwegian, Spanish, Chinese and Korean:

- [Thayer's Greek Lexicon, rebuilt from the 1889 page scans](https://blog.publifye.com/p/rebuilding-thayer-s-greek-lexicon-entry-by-entry-against-the-1889-page)
  — 716 pages, four transcription routes, five rounds of adversarial review, and why every open
  digital Thayer we could find is lossy.
- [Darash vs Logos, Accordance and Blue Letter Bible (2026) — an honest comparison](https://blog.publifye.com/p/darash-vs-logos-accordance-and-blue-letter-bible-an-honest-comparison)
  — including where the big platforms win.
- [Deuteronomy 4:29 says "seek" twice. The Hebrew does not.](https://blog.publifye.com/p/deuteronomy-4-29-says-seek-twice-the-hebrew-does-not)
  — a worked example, including the searches that prove nothing.
- [Why do AI models hallucinate — and does grounding them in real sources fix it?](https://blog.publifye.com/p/why-do-ai-models-hallucinate-and-does-grounding-them-in-real-sources)
- [Best Bible study tools in order: what to use first, and when Hebrew and Greek pay off](https://blog.publifye.com/p/best-bible-study-tools-for-deeper-reading)
- [Bibelen Anno 2026 — a Norwegian translation built with AI, eight verse gates and a human veto](https://blog.publifye.com/p/bibelen-anno-2026-a-new-norwegian-bible-translation-built-with-ai-and-a)
