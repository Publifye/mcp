# Compose and validate

**Is this document well formed, and what does it render to?** 3 Doksi MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://doksi.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`doc_validate`](#doc_validate) | read | Check a document against its kind's requirements and report EVERY problem at once, never… |
| [`doc_compose`](#doc_compose) | write | Compose a document and typeset it in ONE call: validate, render, and return the PDF |
| [`doc_get`](#doc_get) | write | Read the original structured document JSON retained when doc_issue or doc_compose(issue:… |

---

## `doc_validate`

**Doc Validate** — read-only, idempotent, closed-world · access: `read`.

Check a document against its kind's requirements and report EVERY problem at once, never just the first — you cannot see the page, so one problem per call would be a dozen round trips. Each problem carries the exact JSON path to fix, why the field exists, and whether it is missing (you have not filled it in) or malformed (it is filled in wrongly). Returns no PDF; customer API call limits still apply. A watercolor covenant is typeset once to report in notices any painting a long title or name leaves no room for (it would be left out). For such a covenant notices_checked says whether that typeset COMPLETED: false (with notices_reason) means the artwork was NOT checked — an absent notices list then means unknown, not all clear. If the typeset finds the covenant does not fit its one page, doc_compose would refuse it, so the answer is valid:false with a does_not_fit problem and warning naming what to shorten. notices_checked is absent when no typeset applies (other kinds, and designs without paintings).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | The whole document object, as doc_requirements describes it |

## `doc_compose`

**Doc Compose** — writes, closed-world · access: `write`.

Compose a document and typeset it in ONE call: validate, render, and return the PDF. This is the tool to use when you have the content. Get a complete JSON example and schema from doc_requirements first. For formal application letters, including job applications, use kind letter_official with content.purpose.id application; doc_requirements(kind:letter_official, purpose:application) describes the required fields. This creates a PDF; it does not submit an application. On a validation failure nothing is rendered and you get the same problem list doc_validate returns, so a refusal is a result to act on rather than an error to retry. notices lists any painting of the design that was left out because a long title or name left it no room, with what to shorten. COVENANTS (kind covenant, EVERY occasion) need one credit, a marriage pass or a Doksi plan: on a free account this returns a watermarked PREVIEW: a 120 dpi picture of the page with PREVIEW or FORHÅNDSVISNING burned in (preview:true, access:free_preview; no text layer) and issue:true is refused. The print-ready covenant uses one credit (doc_compose_credit), a Doksi plan or a marriage pass; tell the user before composing so the preview is no surprise. Every other kind is unchanged on the free tier. preview:true (covenants) asks for that watermarked preview on ANY account, paid or not: nothing is kept or charged, and it cannot be combined with issue. include:["image"] (covenants) adds page 1 as a 120 dpi JPEG for screens that cannot show a PDF: clean for a caller entitled to the clean covenant, the same watermarked picture on a preview (image.watermarked says which).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `document` | object | yes | The whole document object |
| `include` | array | no | Which representations to return: pdf (base64 bytes), json (canonical document), image (covenants: page 1 as a JPEG, image.bytes_b64). Defaults to pdf. Use issu… |
| `issue` | boolean | no | Also ISSUE the document: keep it and mint a capability link you can hand to somebody. Off by default — composing is cheap and repeatable, issuing keeps a copy. |
| `name` | string | no | With issue:true: your private name for the kept document (1-80 characters; never printed, never in the link). Default for a customer: the names and date |
| `preview` | boolean | no | Covenants only: return the watermarked preview whatever the account holds. Never kept, never charged; refused with issue:true. |

## `doc_get`

**Doc Get** — read-only, idempotent, closed-world · access: `write`.

Read the original structured document JSON retained when doc_issue or doc_compose(issue:true) issued a PDF. Use the returned document to inspect wording, block IDs, image references and fields, then edit and validate it before issuing a NEW document. This does not extract text from the PDF, re-render, or modify the issued document. Older documents may have source_available:false. Requires authenticated write access and the private document id, like document link management. Revoking a public PDF link does not erase this retained record.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | The private document id returned at issuance; not its public PDF token or URL |

---

*Generated from the live `tools/list` of the release serving production (0.1.85) on 2026-09-29.
Regenerate rather than edit by hand.*
