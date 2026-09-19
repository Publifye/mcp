# Issue, share and deliver

**How does someone else get at it, and how do I take it back?** 6 Doksi MCP tools, listed with the exact description and
input schema the server itself returns. Endpoint: `https://doksi.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`doc_issue`](#doc-issue) | write | Typeset a document, KEEP it, and return a permanent link that opens it — no login, no ac… |
| [`doc_share`](#doc-share) | write | Typeset a document and hand back a TEMPORARY download link a person can open — no login,… |
| [`doc_share_revoke`](#doc-share-revoke) | write | Kill a temporary link now, before it expires. Use it the moment a document went to the w… |
| [`doc_link_rotate`](#doc-link-rotate) | write | Replace a document's link with a new one. The old link stops working immediately, the do… |
| [`doc_link_revoke`](#doc-link-revoke) | write | Kill a document's link with no replacement. Anyone opening it afterwards is told the lin… |
| [`doc_mail_to_me`](#doc-mail-to-me) | write | Email an issued document to the address you are signed in as. The document is attached a… |

---

## `doc_issue`

**Doc Issue** — writes, closed-world · access: `write`.

Typeset a document, KEEP it, and return a permanent link that opens it — no login, no account, no expiry. This is the normal way to deliver a document: give the person the link.

The link is the credential, so treat it like one: it is not indexed anywhere and it is not guessable, but anyone holding it can open the document. If it reaches the wrong person, doc_link_rotate replaces it and doc_link_revoke kills it — which is exactly what an emailed attachment can never do.

The stored bytes never change afterwards. A template fix or a font change does not alter a document somebody already received.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | The whole document object |
| `filename` | string | no | What the person sees when saving, e.g. oppsigelse.pdf |

## `doc_share`

**Doc Share** — writes, closed-world · access: `write`.

Typeset a document and hand back a TEMPORARY download link a person can open — no login, no account, and it expires. Use this when somebody needs the document itself rather than the bytes: paste the link into a chat or an email and they click it.

The link is private and short-lived by design. It is not published anywhere, it never reaches the open web, and it can be killed early with doc_share_revoke. Validation runs first: an incomplete document produces the same problem list doc_validate returns and nothing is uploaded.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | The whole document object |
| `filename` | string | no | What the person sees when saving, e.g. oppsigelse.pdf |
| `title` | string | no | What the document IS, in human words |
| `ttl_seconds` | integer | no | How long the link works. Default 3600 (one hour), minimum 60, maximum 604800 (one week). The value actually granted is returned — it is clamped, and reporting what was asked for rather than what was allowed is how a person gets told the wrong expiry. |

## `doc_share_revoke`

**Doc Share Revoke** — writes, closed-world · access: `write`.

Kill a temporary link now, before it expires. Use it the moment a document went to the wrong person: the link stops working immediately and the bytes are dropped. Revoking an already-dead link is not an error — it is the outcome you wanted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | string | yes | The id returned by doc_share |

## `doc_link_rotate`

**Doc Link Rotate** — writes, closed-world · access: `write`.

Replace a document's link with a new one. The old link stops working immediately, the document is untouched, and you get a fresh link to send. Use this when a link was forwarded further than intended.

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

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The document id from doc_issue |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-20, version 0.1.54. Regenerate rather than edit by hand.*
