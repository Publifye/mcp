# Tringine — build your own Bible edition from Claude, Cursor and any MCP client

**Tringine builds a Bible edition of your own: choose the translation — or two or three, aligned
verse for verse — the scope (the whole Bible, the Old or New Testament, or any range of books) and
the trim, and get a print-ready PDF, light and dark reading PDFs and an EPUB 3. Editions are
private: for personal and in-organisation use, never for resale, and without an ISBN. It runs as a
hosted MCP server over HTTPS.**

| | |
|---|---|
| Endpoint | `https://tringine.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open |
| Registry | not yet published |
| Product site | <https://tringine.publifye.com> |
| Tool schemas | not yet captured into this repository |

## Connect

```jsonc
{ "mcpServers": { "tringine": { "type": "http", "url": "https://tringine.publifye.com/mcp" } } }
```

Claude Code: `claude mcp add --transport http tringine https://tringine.publifye.com/mcp`, then
`/mcp` to sign in. The discovery chain is the same as for the other servers:
**[../../docs/connect.md](../../docs/connect.md)**.

There is **no free MCP tier**: a token is issued only to an entitled account, and the entitlement
comes from claiming the free first build credit or buying credits.

## The tools a customer uses

- `validate_spec` — dry-runs a build spec and returns the normalised spec or a typed rejection.
- `list_translations` — what can be built.
- `list_builds` and `get_build` — your builds, their state and credit outcome; `get_build` carries
  signed download links once a build is done.
- `get_artifacts` — a build's file inventory.
- `credits_get` — your credit balance.
- `queue_status` — the build pipeline.
- `module_list` and `module_get` — the free Bible-app modules.

Builds themselves are started in the website wizard at <https://tringine.publifye.com/build>.
Scripture text comes from the [Darash](../darash) corpus, with the source and licence credited per
edition.

## Plans

The first build credit is free, once per account. A Personal pack is **$12 for 6 credits**; the
**Congregation** plan is **$280 a year for up to 140 builds**. A New Testament build spends one
credit; the Old Testament or the whole Bible spends two. The current plans are always on
<https://tringine.publifye.com/store>, and where this page and the site differ, the site is right.
