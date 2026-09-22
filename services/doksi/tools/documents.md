# Compose and validate

**Is this document well formed, and what does it render to?** 3 Doksi MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://doksi.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`doc_validate`](#doc_validate) | read | Check a document against its kind's requirements and report EVERY problem at once, never… |
| [`doc_compose`](#doc_compose) | write | Compose a document and typeset it in ONE call: validate, render, and return the PDF. Thi… |
| [`doc_get`](#doc_get) | write | Read the original structured document JSON retained when doc_issue or doc_compose(issue:… |

---

## `doc_validate`

**Doc Validate** — read-only, idempotent, closed-world · access: `read`.

Check a document against its kind's requirements and report EVERY problem at once, never just the first — you cannot see the page, so one problem per call would be a dozen round trips. Each problem carries the exact JSON path to fix, why the field exists, and whether it is missing (you have not filled it in) or malformed (it is filled in wrongly). Does not render a PDF; customer API call limits still apply.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | The whole document object, as doc_requirements describes it |

## `doc_compose`

**Doc Compose** — writes, closed-world · access: `write`.

Compose a document and typeset it in ONE call: validate, render, and return the PDF. This is the tool to use when you have the content. Get a complete JSON example and schema from doc_requirements first. For formal application letters, including job applications, use kind letter_official with content.purpose.id application; doc_requirements(kind:letter_official, purpose:application) describes the required fields. This creates a PDF; it does not submit an application. On a validation failure nothing is rendered and you get the same problem list doc_validate returns, so a refusal is a result to act on rather than an error to retry.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | The whole document object |
| `include` | array | no | Which representations to return: pdf (base64 bytes), json (canonical document). Defaults to pdf. Use issue:true with include:[json] for a shareable PDF URL. |
| `issue` | boolean | no | Also ISSUE the document: keep it and mint a capability link you can hand to somebody. Off by default — composing is cheap and repeatable, issuing keeps a copy. |

## `doc_get`

**Doc Get** — read-only, idempotent, closed-world · access: `write`.

Read the original structured document JSON retained when doc_issue or doc_compose(issue:true) issued a PDF. Use the returned document to inspect wording, block IDs, image references and fields, then edit and validate it before issuing a NEW document. This does not extract text from the PDF, re-render, or modify the issued document. Older documents may have source_available:false. Requires authenticated write access and the private document id, like document link management. Revoking a public PDF link does not erase this retained record.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The private document id returned at issuance; not its public PDF token or URL |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-22, version 0.1.67. Regenerate rather than edit by hand.*
