# Audio Bible — World English Bible audio MCP server for Claude, Cursor and any MCP client

**Audio Bible gives an AI assistant the World English Bible as text and as sound: every verse of a
chapter, numbered, a listening link that starts at a given verse with its timing in seconds, a
recording made on demand when a chapter has not been read aloud yet, and a personal download link
for the result. It runs as a hosted MCP server over HTTPS.**

| | |
|---|---|
| Endpoint | `https://audiobible.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open |
| Registry | `pro.publifye/audiobible` ([server.json](server.json); not yet published to the registry) |
| Product site | <https://audiobible.publifye.com> |
| Capability tools | **10** ([full schemas](tools.json)) |

## Connect

```jsonc
{ "mcpServers": { "audiobible": { "type": "http", "url": "https://audiobible.publifye.com/mcp" } } }
```

Claude Code: `claude mcp add --transport http audiobible https://audiobible.publifye.com/mcp`, then
`/mcp` to sign in. The discovery chain is the same as for the other servers:
**[../../docs/connect.md](../../docs/connect.md)**.

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

## What the tools do

Every tool is documented with its exact description, annotations and input schema — 10 in all,
generated from the service's own registry, never written by hand.

| Area | The question it answers | Tools |
|---|---|---|
| **[Listen, prepare and download](tools/listening.md)** | Can the user hear this chapter, and can they keep it? | 6 |
| **[What is recorded](tools/catalogue.md)** | Which books exist, and how much has been read aloud? | 4 |

Machine-readable: **[tools.json](tools.json)** carries all 10 with full JSON Schema, plus every
excluded bucket listed by name so the count is auditable. Three staff-only tools (`admin_jobs`,
`admin_recordings`, `admin_prepare_chapter`) are excluded from the customer surface.

## What it does not do

- **One translation.** The World English Bible, and no other. For the Hebrew and Greek, other
  translations, lexicons and cross-references, see **[Darash](../darash)**.
- **No commentary or interpretation.** Text and audio only.
- **Not a crawler endpoint.** Audio, generation, downloads and accounts are for people and their
  assistants; the public chapter pages are what search engines should read.

## Plans

Listening is free. A free registered plan includes a small rolling download allowance; the annual
plan raises it and adds multi-chapter ZIP downloads. Plans and prices can change; **the current ones
are always on <https://audiobible.publifye.com/store>**, and where this page and the site differ,
the site is right.
