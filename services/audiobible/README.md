# Audio Bible — five Bibles, read aloud, for Claude, Cursor and any MCP client

**Audio Bible gives an AI assistant a Bible as text and as sound: every verse of a chapter,
numbered, a listening link that starts at a given verse with its timing in seconds, a recording
made on demand when a chapter has not been read aloud yet, and a personal download link for the
result. Five Bibles are offered — the World English Bible (English), Bibelen Anno 2026 (NB2026,
Norwegian Bokmål), the Old Persian Version (OPV, 1895, Persian), the Reina Valera (RV1909, Spanish)
and the Lutherbibel (1912, German) — and every capability tool takes a `bible` argument to choose
between them. It
runs as a hosted MCP server over HTTPS.**

| | |
|---|---|
| Endpoint | `https://audiobible.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open |
| Registry | [`pro.publifye/audiobible`](https://registry.modelcontextprotocol.io/v0/servers?search=publifye) ([server.json](server.json)) |
| Product site | <https://audiobible.publifye.com> · NB2026 at <https://audiobible.publifye.com/nb/nb2026> |
| YouTube | [Ruth — Audio Bible (World English Bible)](https://www.youtube.com/playlist?list=PLafP-kvSDbS8) on the [Publifye channel](https://www.youtube.com/@publifyeofficial) |
| Capability tools | **10** ([full schemas](tools.json)) |

## Connect

```jsonc
{ "mcpServers": { "audiobible": { "type": "http", "url": "https://audiobible.publifye.com/mcp" } } }
```

Claude Code: `claude mcp add --transport http audiobible https://audiobible.publifye.com/mcp`, then
`/mcp` to sign in. The discovery chain is the same as for the other servers:
**[../../docs/connect.md](../../docs/connect.md)**.

## Five Bibles, one tool surface

Every capability tool accepts an optional `bible` argument — `web`, `nb2026`, `opv`, `rv1909` or
`gerlut1912`; the World English Bible stays the default when it is omitted. Book slugs are each
Bible's own, so take them from `list_books` for that Bible. Each has its own contents page:
[NB2026](https://audiobible.publifye.com/nb/nb2026), [OPV](https://audiobible.publifye.com/fa/opv),
[RV1909](https://audiobible.publifye.com/es/rv1909) and
[Luther 1912](https://audiobible.publifye.com/de/gerlut1912). `coverage` and `chapter_status` report
how far each Bible has been read aloud, per Bible.

The tool schemas in this repository were captured on 2026-09-29, when only `web` and `nb2026` were
offered, so their `bible` parameter still lists those two; the live server accepts all five.

## The text is quoted, not remembered

`get_chapter` returns every verse's exact text, numbered, and its own description tells the
assistant to quote it as returned rather than paraphrase it as scripture. The World English Bible
is public domain; the chapter pages are plain server-rendered HTML that anyone can read.

## Listening is free; keeping is a plan

- **Listen** — `listen_link` returns the public reading page, which plays the audio with the verse
  highlighted, and the direct stream with that verse's start and end in seconds.
- **Record** — `prepare_chapter` has a chapter read aloud if it is not yet recorded, through the same
  idempotent queue as the website's Read button. It takes a minute or two; `chapter_progress` reports
  how far it has got without starting anything.
- **Download** — `download_link` mints a personal, expiring link: one chapter as `.opus`, or several
  as a ZIP on the annual plan. `my_allowance` states what is left in the rolling 24 hours before an
  assistant promises a download it cannot deliver.

## Watch it read aloud on YouTube

The book of Ruth, all four chapters from the World English Bible, is on YouTube as a playlist:
**[Ruth — Audio Bible (World English Bible)](https://www.youtube.com/playlist?list=PLafP-kvSDbS8)**,
on Publifye's channel, **[@publifyeofficial](https://www.youtube.com/@publifyeofficial)**. Each
video is one chapter, read aloud with the text on screen — for example
[Ruth 3](https://www.youtube.com/watch?v=Zq91hS--vDE).

## What the tools do

Every tool is documented with its exact description, annotations and input schema — 10 in all,
generated from the service's own `tools/list`, never written by hand.

| Area | The question it answers | Tools |
|---|---|---|
| **[Listen, prepare and download](tools/listening.md)** | Can the user hear this chapter, and can they keep it? | 6 |
| **[What is recorded](tools/catalogue.md)** | Which books exist, and how much has been read aloud? | 4 |

Machine-readable: **[tools.json](tools.json)** carries all 10 with full JSON Schema, plus every
excluded bucket listed by name so the count is auditable. The staff-only admin tools (recording
runs, voice options, deletion and restore, batch narration, search-engine notification) are excluded from the customer surface.

## What it does not do

- **Five translations, not the originals.** The World English Bible, NB2026, OPV, RV1909 and the
  Lutherbibel 1912, and no other. For
  the Hebrew and Greek, other translations, lexicons and cross-references, see
  **[Darash](../darash)**.
- **No commentary or interpretation.** Text and audio only.
- **Not a crawler endpoint.** Audio, generation, downloads and accounts are for people and their
  assistants; the public chapter pages are what search engines should read.

## Plans

Listening is free. A free registered plan includes a small rolling download allowance; the annual
plan raises it and adds multi-chapter ZIP downloads. Plans and prices can change; **the current ones
are always on <https://audiobible.publifye.com/store>**, and where this page and the site differ,
the site is right.
