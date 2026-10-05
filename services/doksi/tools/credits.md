# Access and credits

**Will it print clean, and what does it cost?** 3 Doksi MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://doksi.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`doc_access_status`](#doc_access_status) | read | What YOUR account gets for a covenant right now: print_ready true (a Doksi plan, a live… |
| [`doc_credit_balance`](#doc_credit_balance) | read | Read your remaining compilation credits, reserved credits, and each pack's expiry |
| [`doc_compose_credit`](#doc_compose_credit) | write | Compile one PDF using ONE purchased credit |

---

## `doc_access_status`

**Doc Access Status** — read-only, idempotent, closed-world · access: `read`.

What YOUR account gets for a covenant right now: print_ready true (a Doksi plan, a live marriage pass) or false (watermarked previews; one credit per print-ready covenant with doc_compose_credit), and where to buy. Read it before composing so the answer is no surprise. Requires a customer login.

*No parameters.*

## `doc_credit_balance`

**Doc Credit Balance** — read-only, idempotent, closed-world · access: `read`.

Read your remaining compilation credits, reserved credits, and each pack's expiry. Only your authenticated customer account can be read.

*No parameters.*

## `doc_compose_credit`

**Doc Compose Credit** — writes, closed-world · access: `write`.

Compile one PDF using ONE purchased credit. Optional alternative to the allowance/subscription: doc_compose is unchanged. Validate first with doc_validate (no credit). Requires a customer login and a stable request_id: after a network error reuse exactly the same request_id and arguments; the retry returns the saved result without a second charge. A refused document is never charged and a failed compilation returns its reserved credit. Packs expire independently; read doc_credit_balance before spending. RECOMMENDED FOR A COVENANT: issue:true. One credit then gives the clean PDF AND an id and link, and that covenant is the buyer's: doc_mail_to_me(id), doc_share(id) and signature_request_create(id) serve it at no further charge, to the paying account only. Without issue:true you get the PDF bytes and nothing is kept. This is how a free account gets a print-ready COVENANT (any occasion): one credit, a clean PDF with no watermark (doc_compose on the free tier returns only a watermarked preview of one; a marriage pass or a Doksi plan composes it clean with doc_compose).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | Complete document object |
| `include` | array of string | no | pdf and/or json; defaults to pdf |
| `issue` | boolean | no | Also keep the PDF and create a shareable URL |
| `name` | string | no | With issue:true: your private name for the kept document (1-80 characters; never printed). Default: the names and date |
| `request_id` | string | yes | Unique id for this compilation (1..128 letters, digits, dots, hyphens, underscores); reuse on retries |

---

*Generated from the live `tools/list` of the release serving production (0.1.85) on 2026-09-29.
Regenerate rather than edit by hand.*
