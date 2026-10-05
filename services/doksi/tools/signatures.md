# Signatures

**Who still has to sign, and by which link?** 7 Doksi MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://doksi.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`signature_describe`](#signature_describe) | read | Describe recipients and available named signature slots in a document. Signing is OPTION… |
| [`signature_request_create`](#signature_request_create) | write | Freeze a complete document revision and create optional signing requests for selected… |
| [`signature_request_get`](#signature_request_get) | read | Get owner-only status for a signing collection: document revision, requester, each… |
| [`signature_request_replace`](#signature_request_replace) | write | Request a new signature for ONE person/slot on the same frozen document |
| [`signature_request_revoke`](#signature_request_revoke) | write | Withdraw one signer request or the whole collection and delete its temporary signature m… |
| [`signature_request_render`](#signature_request_render) | write | Explicitly render and issue the completed document after ALL selected signing slots are… |
| [`signature_request_email`](#signature_request_email) | write | Explicitly email ONE named signer's pending link through Pubmail's transactional lane. A… |

---

## `signature_describe`

**Signature Describe** — read-only, idempotent, closed-world · access: `read`.

Describe recipients and available named signature slots in a document. Signing is OPTIONAL: recipients are not automatically signers. Returns slot IDs, roles and placement without image data. Use doc_requirements for the full schema, then explicitly select slots for signature_request_create.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | Complete Doksi document |

## `signature_request_create`

**Signature Request Create** — writes, closed-world · access: `write`.

Freeze a complete document revision and create optional signing requests for selected named signature slots. Returns a private overview_url with every selected signer, individual copy links and QRs. Each signer gets a unique single-use UUID, signing_url and qr_page_url (same request, two views). Links expire after expires_in_minutes (default 25, min 5, max 1440; anything else is refused); each request's expires_at is in the response. Captured ink is private until the later of the link deadline and 45 minutes after submission, unless finalized, replaced or revoked earlier. Each submitted request reports retain_until. After drawing, the signer sees the FINAL document with their signature placed exactly as it will be issued and chooses Approve or Sign again (Sign again discards the ink). When every selected slot is approved, doksi issues the signed PDF itself (as signature_request_render with finalize:true), deletes the ink and records issued_document_id/issued_document_url on the collection; the signer gets a link to the final PDF and the link is closed for good. The signing page is Norwegian when the document lang is nb, English otherwise. No email is sent. Creator can show the QR page on a phone; signer may scan it or choose Sign on this phone. Existing signature assets are refused so previews never expose another person's signature. A COVENANT (any occasion) is refused on a free account (it needs one credit, a marriage pass or a Doksi plan); a covenant you paid for with doc_compose_credit(issue:true) is yours: pass its id instead of document. Call signature_request_get for status; replace one slot with signature_request_replace. No signature image download is provided.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | no | Complete document with named, unfilled signature slots (or give id instead) |
| `expires_in_minutes` | integer | no | Signing link lifetime in minutes (default 25, min 5, max 1440) |
| `id` | string | no | Instead of document: the id of an issued document whose source was retained (e.g. from doc_compose_credit with issue:true) |
| `slot_ids` | array of string | yes | Exactly the signature slot IDs to request; other slots remain untouched |

## `signature_request_get`

**Signature Request Get** — read-only, idempotent, closed-world · access: `read`.

Get owner-only status for a signing collection: document revision, requester, each signer/slot, status (pending, processing, completed = drawn and awaiting the signer's approval, approved, finalized, expired, revoked, failed), link lifetime (expires_in_minutes) and each link's expires_at, pending signing/QR URLs, and issued_document_id/issued_document_url once the signers' approval issued the final PDF (issue_error if that failed; render manually then). No signature image, reusable asset reference or signed preview is returned. REST status endpoints are available per UUID for webpages.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Signing collection ID |

## `signature_request_replace`

**Signature Request Replace** — writes, closed-world · access: `write`.

Request a new signature for ONE person/slot on the same frozen document. Always creates a new UUID with its own lifetime (expires_in_minutes, default 25, min 5, max 1440), revokes the old request and deletes its captured ink. Other signers are unchanged. Refused once the collection has been issued by approval. No email is sent automatically.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `expires_in_minutes` | integer | no | Lifetime of the new link in minutes (default 25, min 5, max 1440) |
| `id` | string | yes | Signing collection ID |
| `slot_id` | string | yes | Exact signer slot to replace |

## `signature_request_revoke`

**Signature Request Revoke** — writes, closed-world · access: `write`.

Withdraw one signer request or the whole collection and delete its temporary signature material. Existing issued PDFs are not changed.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Signing collection ID |
| `slot_id` | string | no | One slot, or omit to revoke all |

## `signature_request_render`

**Signature Request Render** — writes, closed-world · access: `write`.

Explicitly render and issue the completed document after ALL selected signing slots are completed (or approved) and their ink is unexpired. Usually unnecessary: when every signer approves their preview, doksi issues the document itself and signature_request_get shows issued_document_url. Returns a document URL, never raw signature downloads. This keeps an issued PDF containing the signatures; temporary signature capture expires at each request's retain_until (the later of the link deadline and 45 minutes after submission). Manual rendering is refused while approval is issuing the document. May re-render during retention. Refused while the stored document a collection was created from by id has its link withdrawn (doc_link_revoke): call doc_link_rotate on that document first. Does not send email. finalize:true deletes captured ink immediately after successful issue, preventing subsequent re-rendering.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `finalize` | boolean | no | Delete temporary signature ink after successful issue |
| `id` | string | yes | Signing collection ID |

## `signature_request_email`

**Signature Request Email** — writes, closed-world · access: `write`.

Explicitly email ONE named signer's pending link through Pubmail's transactional lane. Alternative to showing qr_page_url; never automatically do both. Requires an authenticated creator account with an email address; a bare service identity cannot send invitations. Request has a fixed recipient after first send. Returns queued, sending, pending_review, failed or unknown, never claims inbox delivery. Duplicate calls do not send again. Limits: 20 invitations per creator/hour and 3 per recipient/hour. A refused or expired request needs a new UUID for that slot. No document or signature image is attached.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Signing collection ID |
| `slot_id` | string | yes | Specific named signer slot |
| `to` | string | yes | This signer's email address |

---

*Generated from the live `tools/list` of the release serving production (0.1.85) on 2026-09-29.
Regenerate rather than edit by hand.*
