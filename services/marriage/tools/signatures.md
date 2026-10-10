# Signatures

**Who still has to sign, and by which link?** 3 Marriage Covenant MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://marriage.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`covenant_sign_request`](#covenant_sign_request) | write | Collect signatures on a kept covenant |
| [`covenant_sign_status`](#covenant_sign_status) | read | Status of a signing request: each signer, signed or pending, the deadlines and the links… |
| [`covenant_sign_render`](#covenant_sign_render) | write | Once every requested slot is signed, issue the signed covenant as a new kept covenant wit… |

---

## `covenant_sign_request`

**Covenant Sign Request** — writes, closed-world · access: `write`.

Collect signatures on a kept covenant. Name the signature slots to request (their ids are in the covenant's content.signatures: the couple, the witnesses, the officiant). Returns a private overview page and, per signer, a personal signing link and a QR page; links expire after 25 minutes and signers need no account. Nothing is emailed. Then poll covenant_sign_status, and call covenant_sign_render once everyone has signed.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The covenant id |
| `slot_ids` | array of string | yes | The signature slot ids to request |

## `covenant_sign_status`

**Covenant Sign Status** — read-only, idempotent, closed-world · access: `read`.

Status of a signing request: each signer, signed or pending, the deadlines and the links still open.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The signing request id from covenant_sign_request |

## `covenant_sign_render`

**Covenant Sign Render** — writes, closed-world · access: `write`.

Once every requested slot is signed, issue the signed covenant as a new kept covenant with its own link. The signatures are never downloadable separately.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The signing request id |

---

*Generated from the live `tools/list` of the release serving production (0.1.38) on 2026-10-10.
Regenerate rather than edit by hand.*
