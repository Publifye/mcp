# Publishing and sharing

**Who can see the CV, and where do they find the PDF?** 8 Vitae MCP tools, listed with the exact description and input
schema the server itself returns. Endpoint: `https://vitae.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to sign in.

| Tool | Access | What it does |
|---|---|---|
| [`visibility_set`](#visibility_set) | write | Publish or unpublish a CV: {cv_id, visibility: "published"\|"unpublished", ttl?}.   TWO S… |
| [`link_rotate`](#link_rotate) | write | REVOKE the current share link and issue a new one: {cv_id}. Everyone holding the old add… |
| [`pdf_uuid_rotate`](#pdf_uuid_rotate) | write | Rotate the direct-file token: {cv_id}. The previous /pdf/<uuid> link dies immediately.  … |
| [`relay_set`](#relay_set) | write | Record whether you would like this CV's email to go through a per-CV forwarding relay, o… |
| [`contact_sync`](#contact_sync) | write | Copy account contact details into the CV's basics: {cv_id, contact:{name?, label?, email… |
| [`cv_render`](#cv_render) | write | Render a CV edition to a typeset PDF: {cv_id, lang?, audience?, force?}.   TWO VARIANTS … |
| [`cv_pdf_link`](#cv_pdf_link) | read | Where the PDFs of a CV can be fetched: {cv_id, lang?}.   Two URLs per edition, because t… |
| [`render_status`](#render_status) | read | What has been rendered, and whether it is still the current document: {cv_id, lang?}.   … |

---

## `visibility_set`

**Visibility Set** — writes, closed-world · access: `write`.

Publish or unpublish a CV: {cv_id, visibility: "published"|"unpublished", ttl?}.
  TWO STATES, because a CV is public by definition (owner ruling 2026-09-23: "a cv is public by definition. So no cv no details — no cv at all"). published = anyone with the CV's address reads it, with the owner's email, phone and city — there is no per-field contact switch; the street address and postcode are never shown. A published CV is NEVER offered to search engines (noindex, and absent from robots and the sitemap). unpublished = NO CV for anyone but the owner — the page in every language, the PDF, every direct-file PDF link and the photo answer the same 404 as an address nobody ever took, immediately (published copies are served private, no-store, so no cache keeps one). Publishing again restores every address; to kill links already handed out, also call link_rotate / pdf_uuid_rotate.
  OLD VALUES ARE ACCEPTED AS ALIASES so existing agents keep working: link and public mean published; private and password mean unpublished. There is no password gate and no indexing switch any more — the old `indexable` argument is ignored if sent. The answer always reports the two-state word.
  ttl UNPUBLISHES AT A DATE: a number and a unit — 7d, 24h, 4w, 3M, 1y. 0 or omitted = published until you unpublish. When the time passes the CV is refused to everyone but the owner exactly as if unpublished; it is refused on read, so the guarantee needs no sweeper. Only meaningful with published; refused with unpublished.
  Written to the durable record and the audit trail BEFORE the index learns about it, so a crash leaves the more restrictive value in force.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `ttl` | string | no | unpublish automatically after this long, e.g. 7d, 24h, 4w, 3M, 1y. 0 or omitted = until you unpublish. Only with published. |
| `visibility` | string | yes | published or unpublished. link/public (= published) and private/password (= unpublished) are accepted aliases. |

## `link_rotate`

**Link Rotate** — writes, closed-world · access: `write`.

REVOKE the current share link and issue a new one: {cv_id}. Everyone holding the old address loses access the moment this returns.
  The address IS the share link: a fresh unguessable slug is minted and the previous one is released, with no redirect (spec §4). There is no window in which both work.
  REFUSED unless the CV is published. An unpublished CV shares nothing, so rotating would be theatre.
  A CUSTOM SLUG IS LOST when you rotate: the new one is 32 random hex characters, because a memorable share link is a guessable one. Set a new memorable slug with cv_set afterwards if you meant to keep it (and accept that it is then guessable).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |

## `pdf_uuid_rotate`

**PDF Uuid Rotate** — writes, closed-world · access: `write`.

Rotate the direct-file token: {cv_id}. The previous /pdf/<uuid> link dies immediately.
  Revocable INDEPENDENTLY of the share link (spec §6.1): rotating this leaves /<slug> alone, and link_rotate leaves this alone. That separation is the point — a PDF handed to one recruiter can be revoked without disturbing everyone else's link.
  THE TOKEN IS NOT AN EXEMPTION FROM THE ACCESS RULES. It resolves to the REDACTED variant, never the owner's complete PDF, and it is refused outright while the CV is unpublished. A bearer URL that bypassed visibility would make every other control here decorative.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |

## `relay_set`

**Relay Set** — writes, closed-world · access: `write`.

Record whether you would like this CV's email to go through a per-CV forwarding relay, once one exists: {cv_id, enabled}.
  THE RELAY IS NOT BUILT, and this is a PREFERENCE ONLY. Today a published CV shows your REAL email address, together with your phone and city, on the page and in the PDF — a CV is public by definition, and a CV a reader cannot answer is not doing its job. Calling this changes nothing a reader sees. If you do not want your email seen, do not publish the CV (visibility_set unpublished): there is no per-field contact switch.
  The street address and postal code are never published under any setting.
  If the relay is ever built it would be plus-addressing on one mailbox (cv+<token>@publifye.com), forwarded from our own domain with Reply-To set so SPF/DKIM stay aligned, rate-limited per CV and disableable here — and would replace the real address only for owners who enabled it.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `enabled` | boolean | yes | true records a preference for a relayed address once a relay exists, false for none. Neither changes what is shown today: a published CV shows the real email. |

## `contact_sync`

**Contact Sync** — writes, closed-world · access: `write`.

Copy account contact details into the CV's basics: {cv_id, contact:{name?, label?, email?, url?}, langs?}.
  A COPY TAKEN AT THIS MOMENT, NEVER A LIVE LINK (spec §7). Changing your billing email later does not rewrite a published CV, and this call is the only thing that ever updates it. The two identities are deliberately separate: the account email is for login and invoices and is never rendered.
  Applied to EVERY language edition by default, because the editions must name the same person — a contact that differs between languages is the parity defect this service exists to catch.
  REFUSES phone and location. They are not account contact details, and a copy of the account is not the door they come in through — set them deliberately with basics_set. Note what a published CV shows: email, phone and city; never the street address or postal code.
  Phase 1 has no Lighthouse account to read, so contact must be supplied. When the customer plane lands, omitting it will read the account contact.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `contact` | object | yes |  |
| `cv_id` | string | yes |  |
| `langs` | array | no | editions to update; omit for all |

## `cv_render`

**CV Render** — writes, closed-world · access: `write`.

Render a CV edition to a typeset PDF: {cv_id, lang?, audience?, force?}.
  TWO VARIANTS EXIST PER EDITION and they are different documents: `owner` is complete, `redacted` is what everyone else gets (internal/redact.ForPublic — the same redaction the public page uses). Omit `audience` and BOTH are rendered, which is the normal thing to want: the public URL serves one and the owner's download the other.
  Content-addressed by the source document plus the audience, so re-rendering an unchanged edition costs nothing and returns the cached bytes. Pass force:true only when the TEMPLATE changed rather than the document.
  Returns metadata, not the file: {renders:[{lang, audience, filename, etag, bytes, cached, source_hash}]}. Fetch the bytes from the URL cv_pdf_link gives you — the same access rules apply there as to the page, and a PDF is never a way around them.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `audience` | string | no | omit for BOTH variants |
| `cv_id` | string | yes |  |
| `force` | boolean | no | re-render even when the cached PDF matches the document. For a template change, not a content change. |
| `lang` | string | no | one edition; omit for every edition this CV has |

## `cv_pdf_link`

**CV PDF Link** — read-only, idempotent, closed-world · access: `read`.

Where the PDFs of a CV can be fetched: {cv_id, lang?}.
  Two URLs per edition, because there are two documents. `owner_url` needs your session and serves the COMPLETE PDF; `public_url` serves the REDACTED one under exactly the rules the page obeys — an unpublished CV answers the same 404 a slug nobody has taken answers.
  `uuid_url` is the DIRECT FILE LINK, present only once pdf_uuid_rotate has minted a token. It reaches the same redacted file without putting the slug in the address, and it is NOT an exemption from anything: refused while the CV is unpublished, never the owner variant, and dead the instant the token is rotated. Treat it as a credential — it is never search-indexed and never cached by anything shared.
  `public_resolves` tells you whether that public URL works for a stranger RIGHT NOW. It is derived from the visibility, never from whether a file has been rendered: a link that exists and a link that opens are different facts, and an owner pasting one into an application needs the second.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `lang` | string | no | one edition; omit for every edition |

## `render_status`

**Render Status** — read-only, idempotent, closed-world · access: `read`.

What has been rendered, and whether it is still the current document: {cv_id, lang?}.
  Per edition and per audience: {cached, current, bytes, rendered_at, state}. `current` compares the hash the PDF was rendered from against the document as it stands NOW, so a stale PDF is a fact this tool reports rather than something you infer from timestamps.
  IT RENDERS NOTHING. A status call that quietly repaired what it reports on could not be used to find out whether the repair was needed — and it would be the call that costs thirty seconds of tectonic.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cv_id` | string | yes |  |
| `lang` | string | no | one edition; omit for every edition |

---

*Generated from the service's own tool registry on the source serving production on
2026-09-24, version 0.2.63. Regenerate rather than edit by hand.*
