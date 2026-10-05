# Timely

## Tagline
Meeting programmes for AI: drafted by your assistant, approved by a person, published as PDF and web

## Description
Timely builds a meeting programme, either a fixed number of meetings or everything inside a calendar period, keeps every revision, and renders the approved version to a PDF through Doksi. An assistant may publish only the exact revision and PDF the user has just confirmed.

It is a hosted server with a Streamable HTTP endpoint at https://timely.publifye.com/mcp, so there is nothing to install. Sign in once in the browser. Edits are atomic against a hash: if the programme moved since the assistant last read it, the edit is refused rather than merged. Publishing needs `user_confirmed` plus the revision, content hash and PDF hash of the preview that was shown.

It is for congregations, clubs and organisations that publish a recurring programme. Timely is not a calendar or a booking system: it does not invite anyone, hold availability or send reminders.

## Setup Requirements
No setup required — sign in with OAuth in the browser on first use.

## Category
Productivity

## Use Cases
Meeting programmes, event schedules, church programmes, club calendars, publishing a programme as PDF, programme widgets for websites, organisation homepages, programme backups

## Features
- Create a programme for an exact meeting count or a date period
- Atomic edits against a `base_hash`, refused rather than merged on conflict
- Every commit kept as an immutable revision, with history and the PDF each produced
- Render through Doksi and retain the exact preview PDF a person then approves
- Publish only after explicit user confirmation, tied to one revision and one PDF by hash
- Approved PDF is published as stored, without re-rendering
- Audit trail records the confirmed publication
- Theme and PDF layout settings
- Website and widget tools for where a programme may appear and how it looks
- Shared organisation page, with logo import or upload, and a homepage built from it
- Lossless, schema-versioned JSON export with a SHA-256 over its exact bytes
- Import creates a new programme from a validated file and never overwrites an existing one
- Delete moves a programme to a bin and can be restored until the purge date
- 31 customer tools; staff-only and operations tools are excluded from this surface

## Getting Started
- "Create a programme for the next eight Sunday meetings"
- "Edit the third meeting in my programme, then render a preview PDF for me to check"
- "Show me the revision history of this programme and what each change was"
- "Back up this programme as an export file"
- "What is in the bin, and when will it be purged?"
- Tool: timely_create — create a programme draft for an exact meeting count or a date period
- Tool: timely_edit — apply explicit operations atomically against a base hash
- Tool: timely_render — render the current draft through Doksi and return a download URL
- Tool: draft_approve — publish the exact confirmed revision and PDF, only after the user's explicit yes
- Tool: timely_history — revision headers, newest first, or the audit trail
- Tool: timely_export — lossless backup of one programme with download links

## Tags
meetings, programme, schedule, pdf, church, events, planning, versioning, approval, widgets, organisation, doksi, publishing, productivity, agenda

## Documentation URL
https://github.com/Publifye/mcp/tree/main/services/timely

## Health Check URL
https://timely.publifye.com/health
