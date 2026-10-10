# Start here

**What does a covenant need, which designs are there, and what does this account get?** 3 Marriage Covenant MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://marriage.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`covenant_requirements`](#covenant_requirements) | read | READ THIS FIRST |
| [`covenant_designs`](#covenant_designs) | read | List the marriage covenant designs: twelve illustrated designs (seven watercolour paintin… |
| [`covenant_access_status`](#covenant_access_status) | read | What the customer gets right now: print_ready true (a live marriage pass — and until when… |

---

## `covenant_requirements`

**Covenant Requirements** — read-only, idempotent, closed-world · access: `read`.

READ THIS FIRST. Everything a marriage covenant needs: the fields, the full JSON schema, guidance (Scripture — a verse is printed by default and can be swapped or switched off —, vows, designs, A4/A3 and text size), complete examples in English and Norwegian including the 1662 Book of Common Prayer vows, and what is free versus paid with live prices. It is a ceremonial keepsake, not a civil marriage certificate. Free.

*No parameters.*

## `covenant_designs`

**Covenant Designs** — read-only, idempotent, closed-world · access: `read`.

List the marriage covenant designs: twelve illustrated designs (seven watercolour paintings, five fine-line drawings, among them Star & Blossom for a Jewish marriage) plus the plain and laurel frames and your own artwork, each with a preview image and a sample PDF, the colour palettes of the drawn designs, and which paintings can be swapped or switched off. Free.

*No parameters.*

## `covenant_access_status`

**Covenant Access Status** — read-only, idempotent, closed-world · access: `read`.

What the customer gets right now: print_ready true (a live marriage pass — and until when — or a Doksi plan) or false (free, watermarked previews), their credits, and the live offers with prices and where to buy (marriage.publifye.com/store). Call it before composing, so the answer is no surprise.

*No parameters.*

---

*Generated from the live `tools/list` of the release serving production (0.1.38) on 2026-10-10.
Regenerate rather than edit by hand.*
