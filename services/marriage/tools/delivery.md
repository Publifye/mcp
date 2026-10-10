# Links and email

**How does someone else get the covenant, and how do I take the link back?** 4 Marriage Covenant MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://marriage.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`covenant_share`](#covenant_share) | write | Make a temporary, private download link for a kept covenant to paste into a chat or an em… |
| [`covenant_link_rotate`](#covenant_link_rotate) | write | Replace a covenant's link with a new one; the old link stops working at once |
| [`covenant_link_revoke`](#covenant_link_revoke) | write | Withdraw a covenant's link with no replacement |
| [`covenant_mail_to_me`](#covenant_mail_to_me) | write | Email a kept covenant (PDF attached, link in the body) to the customer's OWN verified add… |

---

## `covenant_share`

**Covenant Share** — writes, closed-world · access: `write`.

Make a temporary, private download link for a kept covenant to paste into a chat or an email: one hour by default, at most 7 days. Deleting the covenant kills it at once.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The covenant id |
| `ttl_seconds` | integer | no | How long the link works: 300 to 604800 seconds (default 3600) |

## `covenant_link_rotate`

**Covenant Link Rotate** — writes, closed-world · access: `write`.

Replace a covenant's link with a new one; the old link stops working at once. Use it when a link went further than intended. It also reinstates a withdrawn link.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The covenant id (from covenant_compose or covenant_list) |

## `covenant_link_revoke`

**Covenant Link Revoke** — writes, closed-world · access: `write`.

Withdraw a covenant's link with no replacement. The covenant is kept (covenant_link_rotate gives it a new link later); to remove it, use covenant_delete.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The covenant id (from covenant_compose or covenant_list) |

## `covenant_mail_to_me`

**Covenant Mail To Me** — writes, closed-world · access: `write`.

Email a kept covenant (PDF attached, link in the body) to the customer's OWN verified address — the Publifye account they connected with. It cannot go to anyone else and there is no recipient to set; to give it to someone, share the link (covenant_share). Reports 'queued', not delivered. No extra charge.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The covenant id (from covenant_compose or covenant_list) |

---

*Generated from the live `tools/list` of the release serving production (0.1.38) on 2026-10-10.
Regenerate rather than edit by hand.*
