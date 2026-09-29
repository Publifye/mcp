# Issue, share and deliver

**How does someone else get at it, and how do I take it back?** 6 Doksi MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://doksi.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`doc_issue`](#doc_issue) | write | Typeset a document, KEEP it, and return a permanent link that opens it — no login, no… |
| [`doc_share`](#doc_share) | write | Typeset a document and hand back a TEMPORARY download link a person can open — no login,… |
| [`doc_share_revoke`](#doc_share_revoke) | write | Kill a temporary link now, before it expires. Use it the moment a document went to the w… |
| [`doc_link_rotate`](#doc_link_rotate) | write | Replace a document's link with a new one |
| [`doc_link_revoke`](#doc_link_revoke) | write | Kill a document's link with no replacement. Anyone opening it afterwards is told the lin… |
| [`doc_mail_to_me`](#doc_mail_to_me) | write | Email an issued document to the address you are signed in as |

---

## `doc_issue`

**Doc Issue** — writes, closed-world · access: `write`.

Typeset a document, KEEP it, and return a permanent link that opens it — no login, no account, no expiry. This is the normal way to deliver a document: give the person the link.

The link is the credential, so treat it like one: it is not indexed anywhere and it is not guessable, but anyone holding it can open the document. If it reaches the wrong person, doc_link_rotate replaces it and doc_link_revoke kills it — which is exactly what an emailed attachment can never do.

The stored bytes never change afterwards. A template fix or a font change does not alter a document somebody already received.

A COVENANT (kind covenant, any occasion) is refused here on a free account: the print-ready covenant uses one credit (doc_compose_credit, with issue:true for a link), a marriage pass or a Doksi plan.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | The whole document object |
| `filename` | string | no | What the person sees when saving, e.g. oppsigelse.pdf |
| `name` | string | no | Your private name for the kept document (1-80 characters; never printed) |

## `doc_share`

**Doc Share** — writes, closed-world · access: `write`.

Typeset a document and hand back a TEMPORARY download link a person can open — no login, no account, and it expires. Use this when somebody needs the document itself rather than the bytes: paste the link into a chat or an email and they click it.

The link is private and short-lived by design. It is not published anywhere, it never reaches the open web, and it can be killed early with doc_share_revoke. Validation runs first: an incomplete document produces the same problem list doc_validate returns and nothing is uploaded. A COVENANT (kind covenant, any occasion) is refused here on a free account: the print-ready covenant uses one credit (doc_compose_credit), a marriage pass or a Doksi plan. A covenant YOU paid for with doc_compose_credit(issue:true) is yours: pass its id instead of document and the issued PDF is shared at no further charge; so is its signed copy (the id signature_request_render returns). A document whose link was withdrawn (doc_link_revoke) is not shared until doc_link_rotate reinstates it.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | no | The whole document object (or give id instead) |
| `filename` | string | no | What the person sees when saving, e.g. oppsigelse.pdf |
| `id` | string | no | Instead of document: the id of a document already issued (e.g. by doc_compose_credit with issue:true); its stored PDF is shared unchanged |
| `title` | string | no | What the document IS, in human words |
| `ttl_seconds` | integer | no | How long the link works. Default 3600 (one hour), minimum 60, maximum 604800 (one week). The value actually granted is returned — it is clamped, and reporting … |

## `doc_share_revoke`

**Doc Share Revoke** — writes, closed-world · access: `write`.

Kill a temporary link now, before it expires. Use it the moment a document went to the wrong person: the link stops working immediately and the bytes are dropped. Revoking an already-dead link is not an error — it is the outcome you wanted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | string | yes | The id returned by doc_share |

## `doc_link_rotate`

**Doc Link Rotate** — writes, closed-world · access: `write`.

Replace a document's link with a new one. The old link stops working immediately, the document is untouched, and you get a fresh link to send. Use this when a link was forwarded further than intended.

On a document whose link was withdrawn with doc_link_revoke, rotating REINSTATES it: the new link is public again (anyone holding it can open the document), and doc_share, doc_mail_to_me and signature_request_create accept the document by id again.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The document id from doc_issue |

## `doc_link_revoke`

**Doc Link Revoke** — writes, closed-world · access: `write`.

Kill a document's link with no replacement. Anyone opening it afterwards is told the link was withdrawn. The DOCUMENT IS KEPT — revoking decides who may fetch it, and is not a way to erase a record somebody may already hold a copy of.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The document id from doc_issue |

## `doc_mail_to_me`

**Doc Mail To Me** — writes, closed-world · access: `write`.

Email an issued document to the address you are signed in as. The document is attached and the link is in the body.

IT GOES ONLY TO YOU. doksi does not email documents to anyone else, and there is no argument that changes that: sending a person's correspondence onward would put our sending reputation behind somebody else's letter. To reach a recipient, send them the document's link yourself — from your own address, under your own name.

Reports the document as QUEUED, never as delivered: pubmail accepts it for sending and reports failures separately, so 'sent' would be a claim this service cannot make.

A COVENANT (any occasion) is refused here on a free account: the print-ready covenant uses one credit (doc_compose_credit), a marriage pass or a Doksi plan. A covenant you paid for with doc_compose_credit(issue:true) is yours to mail by its id, at no further charge.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The document id from doc_issue |

---

*Generated from the live `tools/list` of the release serving production (0.1.85) on 2026-09-29.
Regenerate rather than edit by hand.*
