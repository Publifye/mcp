# Catalogue

**What kinds exist, and what does this one require?** 4 Doksi MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://doksi.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`kind_list`](#kind_list) | read | List the eight document kinds doksi makes, with what each one is for. Read this before d… |
| [`purpose_list`](#purpose_list) | read | List the curated purposes an official letter can have, with the EXTRA fields each one re… |
| [`block_types`](#block_types) | read | List the building blocks a document body is made of, and which kinds accept each one. Th… |
| [`doc_requirements`](#doc_requirements) | read | Return the exact field requirements for one kind, optionally composed with one purpose. … |

---

## `kind_list`

**Kind List** — read-only, idempotent, closed-world · access: `read`.

List the eight document kinds doksi makes, with what each one is for. Read this before doc_compose if you are unsure which kind fits: the kinds differ in LAYOUT, not in wording. An application, request, complaint or resignation is a purpose on letter_official (see purpose_list), not a separate kind. For a formal job, admission, grant or permit application, call doc_requirements(kind:letter_official, purpose:application). letter_personal is for private correspondence.

*No parameters.*

## `purpose_list`

**Purpose List** — read-only, idempotent, closed-world · access: `read`.

List the curated purposes an official letter can have, with the EXTRA fields each one requires. A purpose supplies default subject, salutation and closing wording in Norwegian and English, and may demand fields the kind alone does not — a request needs a response-by date, a termination needs an effective date and a notice period. Applications use application: content.purpose.concerning.what must name the role, programme, grant or permission sought. Purposes are optional on official letters and forbidden on personal letters; do not invent purpose IDs.

*No parameters.*

## `block_types`

**Block Types** — read-only, idempotent, closed-world · access: `read`.

List the building blocks a document body is made of, and which kinds accept each one. The set is CLOSED: an unknown block type is refused naming what the kind does take, because a document that quietly dropped its table is worse than one that refused.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `kind` | string | no | Restrict to the blocks this kind accepts |

## `doc_requirements`

**Doc Requirements** — read-only, idempotent, closed-world · access: `read`.

Return the exact field requirements for one kind, optionally composed with one purpose. Each field is required, optional or forbidden, and a forbidden field is refused by name — reference numbers on a personal letter, for instance. Includes a complete JSON Schema, nested field shapes and a valid document example. Meetings and schedules support qr_url and qr_placement (bottom_center default, top_right, hidden); supplied owner names are printed. Read this before composing. For an application letter pass kind:letter_official and purpose:application. Ask for missing required facts; never invent addresses, qualifications or reference numbers.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `kind` | string | yes | Document kind |
| `purpose` | string | no | Optional purpose id, for letter_official only |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-22, version 0.1.67. Regenerate rather than edit by hand.*
