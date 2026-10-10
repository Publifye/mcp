# Marriage Covenant — marriage covenant MCP server for Claude, Cursor and any MCP client

**Marriage Covenant makes a marriage covenant with your AI assistant: both names, the date and
place, each person's own vow, a Bible verse and the witnesses, in one of twelve painted or drawn
designs, typeset by Doksi as a one-page PDF to sign and frame. It is a keepsake, not a civil
marriage certificate. It runs as a hosted MCP server over HTTPS.**

| | |
|---|---|
| Endpoint | `https://marriage.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open |
| Registry | not yet published ([server.json](server.json) is prepared as `pro.publifye/marriage`) |
| Product site | <https://marriage.publifye.com> · [connect your assistant](https://marriage.publifye.com/connector) · [docs](https://marriage.publifye.com/docs) |
| Capability tools | **19** ([full schemas](tools.json)) |

## Connect

```jsonc
{ "mcpServers": { "marriage": { "type": "http", "url": "https://marriage.publifye.com/mcp" } } }
```

Claude Code: `claude mcp add --transport http marriage https://marriage.publifye.com/mcp`, then
`/mcp` to sign in. In Claude or ChatGPT, add a custom connector with the same URL; the first time,
you sign in from your browser with a Publifye account, and no client ID or secret is needed. The
discovery chain is the same as for the other servers: **[../../docs/connect.md](../../docs/connect.md)**.

No assistant? The same covenant can be made in the browser at
<https://marriage.publifye.com/create>.

## Marriage covenants only, typeset by Doksi

This server is the marriage part of [Doksi](../doksi) on its own connector. It renders nothing
itself: every covenant is typeset by Doksi, and what your account may make (a free preview or the
print-ready page) is decided by Doksi for your account. The server holds every call to
`kind: covenant`, `occasion: marriage`; anything else is refused with a pointer to
<https://doksi.publifye.com>, where letters, agreements and the other kinds are made. A Doksi
connection can make the same covenant with `doc_compose`; this one has a shorter, marriage-only
tool list and is simpler for an assistant to follow.

## What a covenant holds

- **The couple's own words.** Both names, the date and place, each person's vow, the officiant if
  there is one, and signature lines for the couple and their witnesses. The 1662 Book of Common
  Prayer vows are there as an example of wording, and `covenant_requirements` returns complete
  examples in English and Norwegian.
- **A Bible verse.** Ecclesiastes 4:12 is printed unless the couple chooses one to three others, or
  none.
- **Twelve designs.** Seven painted in watercolour (Champagne Butterfly, Something Blue, Blush
  Petunias, Bridal Lilies, Garden Roses, Blue Iris, Ivory Magnolia), four drawn (Together in Bloom,
  Butterfly Garden, Hearts Entwined, Olive & Promise), and Star & Blossom, with a Star of David,
  made for a Jewish marriage. There are also a plain and a laurel frame, or your own artwork.
  `covenant_designs` returns each with a preview image and a sample PDF.
- **A4, or A3 for framing.** The covenant is made in English or Norwegian. The site itself is also
  in Spanish, Chinese and Korean.
- **Signed in ink, or by link.** `covenant_sign_request` gives each signer a personal signing link
  and a QR page; signers need no account. Signature capture does not verify identity.

## How an assistant uses it

`covenant_requirements` first, for the fields, the schema and the examples; `covenant_designs` for
the designs. Write the covenant with the couple, `covenant_validate` it (every problem at once, each
with its JSON path), and show a `covenant_preview`. `covenant_access_status` says before composing
whether this account gets a print-ready covenant. `covenant_compose` then makes it and keeps it on
the account; send a `request_id`, and a retry after a network error returns the same covenant
without charging twice.

A kept covenant can be listed, renamed privately, shared by a temporary link, emailed to your own
address, signed, deleted and restored within 7 days. A kept PDF never changes: to change a
covenant, edit its JSON and compose again.

## What the tools do

Every tool is documented with its exact description, annotations and input schema — 19 in all,
generated from the service's own `tools/list`, never written by hand.

| Area | The question it answers | Tools |
|---|---|---|
| **[Start here](tools/start.md)** | What does a covenant need, which designs are there, and what does this account get? | 3 |
| **[Check, preview and make](tools/compose.md)** | Is the covenant right, what will it look like, and how is the print-ready one made? | 3 |
| **[Your covenants](tools/kept.md)** | Which covenants have I kept, and how do I tidy or recover them? | 6 |
| **[Links and email](tools/delivery.md)** | How does someone else get the covenant, and how do I take the link back? | 4 |
| **[Signatures](tools/signatures.md)** | Who still has to sign, and by which link? | 3 |

Machine-readable: **[tools.json](tools.json)** carries all 19 with full JSON Schema, plus every
excluded bucket listed by name so the count is auditable.

## What it does not do

- **Not a marriage certificate.** Every covenant says at its foot that it is not a civil marriage
  certificate. A marriage is registered the way the couple's country requires.
- **Not other documents.** Letters, agreements and every other kind are made with Doksi itself.
- **Not public.** A covenant is emailed only to the verified address of the account that asks for
  it, and its link is never listed or indexed.

## Plans

Designing, checking the wording and a full preview marked PREVIEW are free with a Publifye account,
within a daily call allowance. The print-ready covenant needs a paid path: a 7-day marriage pass
(as many covenants as you like for a week), one Doksi credit per covenant, or a Doksi plan. Prices
can change; **the current ones are always on <https://marriage.publifye.com/store>**, and where this
page and the site differ, the site is right.
