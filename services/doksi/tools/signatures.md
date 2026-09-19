# Signatures

**Who still has to sign, and by which link?** 7 Doksi MCP tools, listed with the exact description and
input schema the server itself returns. Endpoint: `https://doksi.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`signature_describe`](#signature-describe) | read | Describe recipients and available named signature slots in a document. Signing is OPTION… |
| [`signature_request_create`](#signature-request-create) | write | Freeze a complete document revision and create optional signing requests for selected na… |
| [`signature_request_get`](#signature-request-get) | read | Get owner-only status for a signing collection: document revision, requester, each signe… |
| [`signature_request_replace`](#signature-request-replace) | write | Request a new signature for ONE person/slot on the same frozen document. Always creates … |
| [`signature_request_revoke`](#signature-request-revoke) | write | Withdraw one signer request or the whole collection and delete its temporary signature m… |
| [`signature_request_render`](#signature-request-render) | write | Explicitly render and issue the completed document after ALL selected signing slots are … |
| [`signature_request_email`](#signature-request-email) | write | Explicitly email ONE named signer's pending link through Pubmail's transactional lane. A… |

---

## `signature_describe`

**Signature Describe** — read-only, idempotent, closed-world · access: `read`.

Describe recipients and available named signature slots in a document. Signing is OPTIONAL: recipients are not automatically signers. Returns slot IDs, roles and placement without image data. Use doc_requirements for the full schema, then explicitly select slots for signature_request_create.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | Complete Doksi document |

## `signature_request_create`

**Signature Request Create** — writes, closed-world · access: `write`.

Freeze a complete document revision and create optional signing requests for selected named signature slots. Returns a private overview_url with every selected signer, individual copy links and QRs. Each signer gets a unique single-use UUID, signing_url and qr_page_url (same request, two views). Links expire after 25 minutes; captured ink is private for at most 45 minutes after submission. No email is sent. Creator can show the QR page on a phone; signer may scan it or choose Sign on this phone. Existing signature assets are refused so previews never expose another person's signature. Call signature_request_get for status; replace one slot with signature_request_replace. No signature image download is provided.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | Complete document with named, unfilled signature slots |
| `slot_ids` | array | yes | Exactly the signature slot IDs to request; other slots remain untouched |

## `signature_request_get`

**Signature Request Get** — read-only, idempotent, closed-world · access: `read`.

Get owner-only status for a signing collection: document revision, requester, each signer/slot, status, deadlines and pending signing/QR URLs. No signature image, reusable asset reference or signed preview is returned. REST status endpoints are available per UUID for webpages.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Signing collection ID |

## `signature_request_replace`

**Signature Request Replace** — writes, closed-world · access: `write`.

Request a new signature for ONE person/slot on the same frozen document. Always creates a new UUID and 25-minute deadline, revokes the old request and deletes its captured ink. Other signers are unchanged. No email is sent automatically.

| Parameter | Type | Required | Description |
|---|---|---|---|
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

Explicitly render and issue the completed document after ALL selected signing slots are completed and their ink is unexpired. Returns a document URL, never raw signature downloads. This keeps an issued PDF containing the signatures; temporary signature capture still expires after 45 minutes. May re-render during retention. Does not send email. finalize:true deletes captured ink immediately after successful issue, preventing subsequent re-rendering.

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

*Generated from the service's own tool registry on the source serving production on
2026-09-20, version 0.1.54. Regenerate rather than edit by hand.*
