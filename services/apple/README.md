# Apple Books Delivery — deliver your Junifye book to Apple Books from Claude, Cursor and any MCP client

**Apple Books Delivery sends a book you own in [Junifye](../junifye) to Apple Books on your own
App Store Connect provider account. You keep the account, the imprint and the royalties, and Apple
pays you directly. It is self-serve: you supply your own App Store Connect API key, and your
assistant drives the delivery over MCP. It runs as a hosted MCP server over HTTPS.**

| | |
|---|---|
| Endpoint | `https://apple.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open |
| Registry | not yet published |
| Product site | <https://apple.publifye.com> |
| Tool schemas | not yet captured into this repository |

## Connect

```jsonc
{ "mcpServers": { "apple": { "type": "http", "url": "https://apple.publifye.com/mcp" } } }
```

Claude Code: `claude mcp add --transport http apple https://apple.publifye.com/mcp`, then `/mcp`
to sign in with a Publifye account. The discovery chain is the same as for the other servers:
**[../../docs/connect.md](../../docs/connect.md)**.

## The tools a customer uses

- `operator_guide` — walks the sequence; read it first.
- `apple_credential_set` — registers your App Store Connect key id, issuer and provider. The
  private key itself is uploaded over HTTPS for each delivery, never through MCP or chat.
- `apple_delivery_begin` — opens a delivery job for a book. `request_type=verify` is a dry run
  that validates the whole package against Apple and sends nothing; `upload` publishes.
- `review_list` and `review_get` — show the review an upload waits on; `review_approve` approves
  exactly those bytes. A live upload is refused until its review is approved.
- `apple_deliver` — submits the job.
- `apple_delivery_status` and `apple_delivery_log` — follow it.
- `apple_cancel` — stops it.
- `apple_allowance` — what is left of your allowance.

A `book_id` is a book you own in Junifye. The Apple account a delivery goes to is derived from
that book's owner and cannot be chosen by the caller.

## What it guards

Every file is validated with EPUBCheck before upload, and the ISBN inside the EPUB must be the ISBN
being published, or nothing is sent. The App Store Connect private key is not stored: it is
uploaded per delivery, destroyed with it, and identified afterwards only by a SHA-256 fingerprint.
Deliveries are serialised and recorded permanently.

## Plans

The free plan is **five completed deliveries a year** with a Publifye account, renewing every
1 January. Only a completed delivery counts against it: a dry run, a failed delivery, checking status
and reading logs do not (dry runs have a separate daily limit). There is no self-serve paid plan; larger volumes are arranged via
<https://publifye.org/contact>. The current terms are on <https://apple.publifye.com>, and where
this page and the site differ, the site is right.
