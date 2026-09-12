# Print, ISBN and store — Junifye MCP tools

**Press-ready output, real ISBN-13 assignment, and retail publishing.** 9 tools, listed below with the exact description and input
schema the server itself returns. Endpoint: `https://junifye.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`isbn_record_acceptance`](#isbn-record-acceptance) | ADMIN |
| [`isbn_status`](#isbn-status) | Read your ISBN standing — the fast way to see whether book_isbn_assign will work for you |
| [`print_get`](#print-get) | Read a book's PHYSICAL-PRINT status — does NOT change anything or render |
| [`print_set`](#print-set) | Configure a book for PHYSICAL PRINT (print-on-demand) and render a press-ready interior PDF |
| [`publish_request`](#publish-request) | Request that a book be PUBLISHED (made publicly listed) |
| [`retail_record_acceptance`](#retail-record-acceptance) | ADMIN |
| [`retail_status`](#retail-status) | Whether an author is approved to sell books on a live retail shelf, and what the remaining… |
| [`retail_terms`](#retail-terms) | The retail terms an AUTHOR accepts before a book goes on sale, plus the version string the… |
| [`store_readiness`](#store-readiness) | Everything standing between this book and a live retail shelf, in one call: the deterministic… |

---

## `isbn_record_acceptance`

**ISBN Record Acceptance** — writes, closed-world.

ADMIN. Record that a book's OWNER has accepted the ISBN publisher terms, where they gave that acceptance OUT OF BAND — by email, or a signed message — rather than by ticking the box on their book page. This exists because the acceptance can only ever be the author's own: no tool lets an AI or an operator DECIDE it, and this one does not either. It writes down a 'yes' that was actually given, and it is labelled as operator-recorded (channel=operator, with your identity and your note of where the consent came from) so nobody can later mistake it for the author clicking. USE IT ONLY with the author's actual words in front of you, for the CURRENT terms version, and quote where they came from in `evidence`. The consent is attributed to the book's owner, never to you. Returns {book_id, by, channel, terms_version}.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the book whose OWNER gave the acceptance. |
| `evidence` | string | yes | Where the acceptance came from, in enough detail to find it again: e.g. "email from anna@example.com, 2026-08-09, subject 'ISBN terms — yes'". Required: an ope… |

## `isbn_status`

**ISBN Status** — read-only, idempotent, closed-world.

Read your ISBN standing — the fast way to see whether book_isbn_assign will work for you. There is NO separate ISBN allowance to be granted: your paid plan includes one ISBN per book, so what this reports is how many of your books already carry one and how many books your plan allows. Without user_id: returns YOUR OWN standing plus whether the feature is enabled on this deployment and whether you pass the paid-plan gate. With user_id: returns that user's counts (ADMIN only; plan and cap are read from the CALLER's key, so they are reported for yourself only). Returns {user_id, books, isbns_assigned, feature_enabled, and for yourself book_cap, isbns_remaining, plan, plan_ok}.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `user_id` | string | no | Optional pubhub user id (idu…) to inspect. Omit for your own standing. Inspecting another user requires admin. |

## `print_get`

**Print Get** — read-only, idempotent, closed-world.

Read a book's PHYSICAL-PRINT status — does NOT change anything or render. Returns: whether it's configured for print, the resolved printer + trim + bleed, the print_url, cover_print_url + spine_mm + spine_source (the full-wrap cover, once rendered) — or cover_print_unavailable explaining why this printer can never produce one, the last render's press-ready report (pages, even-page count, page-count bounds, grayscale, PDF/X, fonts, low-DPI images), and a plain next_step.

THE FULL PROFILE, in two halves. `available_printers` is the MENU: every field of every preset — trim, interior bleed, cover bleed, the spine formula (spine_per_page_mm + spine_constant_mm), the page-count→gutter ladder, min/max pages, spine_text_min_pages, crop_marks, barcode_keep_out and the printer's notes. `effective` is the ORDER: what THIS book will actually be built to, each value labelled `*_from` with the layer that decided it — "preset", "book" (an override set via print_set) or "stated" (a width the printer simply gave you). Nothing settable is hidden from either half.

`spine_warning` is the one to read first: it fires when a PRINTER-STATED spine (spine_mm) was quoted for a different page count than the book now renders — a cover bound to the wrong spine looks perfect on screen and is scrap on the press. Per-printer `targets` each carry `stale` plus, when stale, a `stale_reason`: "content" = the book was EDITED since that render, so the page count (and any wrap cover's spine) is suspect — do not send it to a press; "build" = the book is untouched and only the service redeployed, which marks every artifact stale and re-renders to the same book. Use this first to learn state, then print_set to configure/render.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (or the public UUID). |

## `print_set`

**Print Set** — writes, closed-world.

Configure a book for PHYSICAL PRINT (print-on-demand) and render a press-ready interior PDF. This is the one tool to set up printing — it ACTIVELY changes the book's print settings and PERSISTS them, so afterwards regenerating the print is a single bare call: print_set(book_id).

Pick a PRINTER (you never touch millimetres):
  printer = drukatava_170x240 | drukatava_a5 | ingramspark_6x9 | kdp_5.5x8.5 | kdp_5x8 | kdp_6x9 | kdp_6x9_cream | lulu_5.5x8.5 | lulu_5x8 | lulu_6x9
  e.g. print_set(book_id, printer="lulu_6x9")  → Lulu 6×9 US trade paperback
       print_set(book_id, printer="drukatava_170x240") → Drukātava 170×240 mm (their recommended larger-A5 Scandinavian trade size, 5 mm bleed)

The chosen printer is PERSISTED as the book's print geometry: bleed (kdp_6x9 = EXACT trim, NO bleed — KDP's requirement for text interiors; Lulu/IngramSpark = exact 0.125in), the printer's own gutter ladder, and page-count bounds (validated in the report).

Or a CUSTOM trim for a printer junifye has no preset for: page_size (e.g. "6x9", "5.5x8.5", "148x210mm", "170x240mm", or A5) + optional bleed_mm (0=3 mm default; 5=Drukātava/EU; for a strict NO-bleed interior use printer="kdp_6x9"). Optional: margins_preset (narrow|normal|wide), body_font_size (10..16).

A CUSTOM TRIM CAN ALSO PRODUCE A FULL WRAP COVER — you do not need a preset, and you do not need junifye changed. Ask your printer for three numbers and pass them: spine_per_page_mm (their paper bulk per PAGE — they quote it per LEAF, so halve it), spine_constant_mm (the cover-board addend, often 0), cover_bleed_mm (the wrap's own bleed, 3.175 US / 5 EU). They persist on the book, they override the preset, and the spine then recomputes from the real page count on every render — so it can never go stale.
  e.g. print_set(book_id, page_size="170x240mm", bleed_mm=5, spine_per_page_mm=0.052222, spine_constant_mm=0.8111, cover_bleed_mm=5)

OR — SIMPLER, AND WHAT PRINTERS ACTUALLY DO — just set the spine THEY STATED. A printer rarely hands you a caliper to derive from; they say "for this book, the spine width will be 17 mm". Pass exactly that: spine_mm=17 together with spine_mm_for_pages=<the page count they quoted it at>. The stated width OVERRIDES every formula, and the page count is what keeps it honest: if the book later renders a different number of pages, every render, report and file listing carries a LOUD spine_warning naming both counts, because a cover bound to a spine quoted for a different book length looks perfect on screen and is scrap on the press. spine_mm=0 clears it and returns the book to the formula.
  e.g. print_set(book_id, printer="drukatava_170x240", spine_mm=17, spine_mm_for_pages=310)

CROP MARKS are per printer and settable per book: crop_marks="on"|"off"|"auto" (auto = follow the preset). Lulu and IngramSpark FORBID trim marks; Drukātava asked in writing for files WITHOUT them, so no shipped preset adds them — use "on" only when your printer asks.

Call with NO printer/size when the book is ALREADY configured → just re-renders the held settings. Call with NO printer/size when NOT configured → returns the printer menu so you know what to pick.

Returns the interior's print_url + a press-ready report (trim size, pages, even-page count, page-count bounds, grayscale/DeviceGray, PDF/X output intent, fonts embedded, any sub-300-DPI images) AND — for the presets that carry spine math (drukatava_170x240, drukatava_a5, ingramspark_6x9, kdp_5.5x8.5, kdp_5x8, kdp_6x9, kdp_6x9_cream, lulu_5.5x8.5, lulu_5x8, lulu_6x9) — cover_print_url: a FULL-WRAP cover PDF (back + spine + front) with the spine width computed from the real page count, the uploaded cover art (or a typeset front when the art has no title), the description on the back, and the barcode zone: when the book carries a valid PRINT ISBN (book_set key=print_isbn — the print edition's own number, always the author's, which Publifye does not issue), the wrap prints that EAN-13; without one, KDP presets reserve the white keep-out for KDP's auto-barcode. The colophon's ISBN line is a different number — the DIGITAL edition's `isbn`, which book_isbn_assign allocates — so a book can legitimately show one, both, or neither. Both files together are the complete KDP/Lulu upload.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `bleed_mm` | number | no | Bleed added to every edge (0 = 3 mm Lulu/KDP, 5 = Drukātava/EU; 0..10). |
| `body_font_size` | integer | no | 10..16 |
| `book_id` | string | yes | The 'idb...' id from book_create.id (or the public UUID). |
| `cover_bleed_mm` | number | no | The WRAP COVER's own bleed, which is NOT the interior's: 3.175 = US POD, 5 = Drukātava/EU. Getting this wrong prints a white sliver at the trimmed edge on ever… |
| `crop_marks` | string | no | Trim marks around the WRAP COVER, per printer. "auto" (default) follows the printer preset; "on" forces them; "off" suppresses them even when the preset asks f… |
| `margins_preset` | string | no |  |
| `page_size` | string | no | Custom trim: WxH inches (6x9, 5.5x8.5), millimetres (148x210mm), or a named size (A5). Sets print_ready automatically. |
| `printer` | string | no | Printer preset — expands to the right trim + bleed. Omit to set a custom page_size, or to re-render an already-configured book. |
| `spine_constant_mm` | number | no | Fixed addend on the spine, independent of page count — the cover boards the block is glued between (e.g. 0.576 = 2×0.288 mm). Most US formulas fold this into t… |
| `spine_mm` | number | no | THE SPINE WIDTH YOUR PRINTER STATED for this job, in millimetres — e.g. 17 for "for this book, the spine width will be 17 mm". This BEATS every formula (spine_… |
| `spine_mm_for_pages` | integer | no | The PAGE COUNT the printer quoted spine_mm at (e.g. 310). This is what keeps a fixed spine honest: every render compares the interior's real page count against… |
| `spine_per_page_mm` | number | no | YOUR PRINTER'S paper bulk in mm per PAGE — the one number that unlocks a wrap cover on a custom trim. A printer quotes caliper per LEAF (a sheet, = 2 pages), s… |

## `publish_request`

**Publish Request** — writes, closed-world.

Request that a book be PUBLISHED (made publicly listed). This is HOW you publish. For an ordinary author it does NOT go public immediately: the book is submitted for review and a reviewer must approve it first — vet_state becomes 'pending', listed stays false, and the book joins the review queue (vet_list) until someone decides it. ALWAYS read the response's listed + reviewed_by fields instead of assuming; they state which of the two things actually happened. reviewed_by is one of: 'human' (QUEUED — automated vetting is switched OFF on this deployment and an admin reads the book personally); 'agent' (QUEUED — an automated vetting session reads it first); 'admin_self' (NOT queued — you hold admin publication authority and own this book, so it was PUBLISHED IMMEDIATELY and the decision recorded as a self-approval against your user id, meaning nobody else reviewed it); 'admin_override' (NOT queued — an admin published a book they do not own). The admin paths skip the queue, never the guards: an origin=transcript book is still refused, for an admin too. Use vet_status to check progress; if it is rejected you'll see the reason there and can fix the issue and call publish_request again. Calling it again is also how you requeue a book stuck in vet_state='stalled' (a PAST automated vetting round failed repeatedly and gave up): a fresh request clears the failed attempt count and puts the book back in the review queue. (The book's URL was already reachable by anyone holding the UUID; publishing makes it DISCOVERABLE in the public library + search once approved.) A book under an EDITORIAL FREEZE cannot be published by ANY route — not by an author, not by an admin, not by vet_decide: lock_reason=admin is a canonical freeze (an admin lifts it) and lock_reason=auto is the 30-day inactivity lock (its OWNER or an admin lifts it). Publishing does NOT lift a freeze; book_unfreeze must, first. For a book you do NOT own, the route is: its owner submits it here, and an admin settles it with vet_decide(decision:'approve'). 

PUBLISHING IS PERMANENT — read before you submit. Once approved, the book is PERMANENT: you cannot delete it and it remains publicly available. Its text FREEZES as canonical (you get up to 10 self-service revision windows via book_revision_open / book_revision_close; beyond that an operator must intervene). And any ISBN assigned to it is FINAL. Submit only work you're ready to stand behind permanently. Owner-only.

--- IDENTIFIERS ---
A book has TWO distinct identifiers, NEVER interchange them:
  • id   = 'idb...' string. Use for EVERY MCP call (chapter_create, book_set_*, etc.).
  • uuid = standard 8-4-4-4-12 UUID. ONLY appears in the public PDF URL (https://junifye.publifye.com/<uuid>-light.pdf).
Chapter id is 'idc...', block id is 'blk...', dict entry is its term string. Always pass the type-matching id.

--- RENDERING ---
There is no explicit render tool. Every mutation auto-bumps book.version; the next fetch of
https://junifye.publifye.com/<uuid>-light.pdf (or -dark.pdf) lazily re-renders if drifted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the uuid that appears in public PDF URLs). |

## `retail_record_acceptance`

**Retail Record Acceptance** — writes, closed-world.

ADMIN. Record that a book's OWNER has accepted the retail terms, where they gave that acceptance OUT OF BAND — by email, or a signed message — rather than by ticking the box on their book page. This exists because the acceptance can only ever be the author's own: no tool lets an AI or an operator DECIDE it, and this one does not either. It writes down a 'yes' that was actually given, and it is labelled as operator-recorded (channel=operator, with your identity and your note of where the consent came from) so nobody can later mistake it for the author clicking.

USE IT ONLY with the author's actual words in front of you, for the CURRENT terms version, and quote where they came from in `evidence`. The consent is attributed to the book's owner, never to you.

The acceptance covers the book's CONTENT VERSION AS IT IS NOW. If the book is edited afterwards the acceptance stops counting and the author must be asked again — that is the point of it, not a defect.

Returns {book_id, by, channel, terms_version, book_version}.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id of the book whose OWNER gave the acceptance. |
| `evidence` | string | yes | Where the acceptance came from, in enough detail to find it again: e.g. "email from anna@example.com, 2026-08-29, subject 'yes, put it on sale'". Required: an … |

## `retail_status`

**Retail Status** — read-only, idempotent, closed-world.

Whether an author is approved to sell books on a live retail shelf, and what the remaining gates are. Answers 'can this author put a book on sale?' without needing an admin. Omit owner_id for yourself.

Approval is only the FIRST gate: each book also needs its readiness checklist clear (store_readiness) and the author's own acceptance of the retail terms. Returns {owner_id, retail_approved, next}.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `owner_id` | string | no | The author's user id ('idu...'). Omit to ask about yourself. |

## `retail_terms`

**Retail Terms** — read-only, idempotent, closed-world.

The retail terms an AUTHOR accepts before a book goes on sale, plus the version string the acceptance is recorded against. Render these verbatim to the author — the record stores the version, never the words, so the two must match.

YOU CANNOT ACCEPT THESE FOR SOMEONE. There is no tool that lets an assistant agree on an author's behalf at any access level. The author accepts on their own book page in the junifye web UI. If they gave their agreement out of band (an email, a signed message), an operator writes it down with retail_record_acceptance and it is labelled as operator-recorded.

Returns {version, terms}.

## `store_readiness`

**Store Readiness** — read-only, idempotent, closed-world.

Everything standing between this book and a live retail shelf, in one call: the deterministic checklist, whether the author is approved to sell, and whether the author has accepted the retail terms for THIS version of the text.

Each step carries done + a detail saying exactly how to clear it. `ready` is true only when every required step is done AND the author's acceptance is on file for the current book version.

NOTE the acceptance is not something you can supply — see retail_terms. Returns {book_id, ready, steps, blockers, author_approved, accepted, book_version}.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `book_id` | string | yes | The 'idb...' id from book_create.id (NOT the public uuid). |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
