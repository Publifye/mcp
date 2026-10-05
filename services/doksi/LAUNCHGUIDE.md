# Doksi

## Tagline
Professional PDFs for AI: letters, agreements, agendas, checklists — signatures by link or QR

## Description
Doksi turns a structured document into a professional PDF: personal and official letters, notices, agreements, ceremonial covenants, checklists, meeting agendas and schedules. It can also collect signatures by individual link or QR code.

It is a hosted server with a Streamable HTTP endpoint at https://doksi.publifye.com/mcp, so there is nothing to install. Sign in once in the browser. Doksi is built so an assistant can ask what a kind of document requires before writing it: `kind_list`, `purpose_list`, `block_types` and `doc_requirements` exist for that, and `doc_validate` reports every problem at once without rendering.

It is for individuals, congregations, clubs and small organisations who want an assistant to produce a correct, typeset document and take it through signing. Doksi is not a word processor and not a legal service.

## Setup Requirements
No setup required — sign in with OAuth in the browser on first use.

## Category
Productivity

## Use Cases
Formal letters, agreements, meeting agendas, checklists, notices, marriage covenants, collecting signatures, QR code signing, document PDFs, ceremonial documents

## Features
- Eight document kinds, each with its own layout and stated requirements
- Requirements lookup per kind, with required, optional and forbidden fields
- Validation that reports every problem at once, with the JSON path to each
- Compose and typeset in one call: validate, render, return the PDF
- Signature requests with their own lifecycle: create, describe, fetch, replace, revoke, render and e-mail
- Individual signing links and QR codes for each signer, with optional expiry
- Revoked links stop working; rotating a link does not invalidate its document
- Share links, link rotation and revocation for issued documents
- E-mail an issued document to the account holder only
- Logo and mark upload for use in documents
- Kept documents with private names, a trash and restore within 7 days, then an announced purge
- Credits and access status tell you before composing whether a covenant will be print-ready or a watermarked preview
- Marriage covenants site, marriage.publifye.com, built on the same server
- A document that does not meet its kind's requirements is refused rather than rendered with gaps filled in

## Getting Started
- "Which kinds of document can Doksi make, and what does a formal letter require?"
- "Write a letter of notice to my landlord and give me the PDF"
- "Validate this meeting agenda before you render it"
- "Create a signing request for this agreement with a link for each signer"
- "Show me the documents I have kept and email the latest to me"
- Tool: kind_list — the document kinds Doksi makes and what each is for
- Tool: doc_requirements — the exact field requirements for one kind
- Tool: doc_validate — check a document against its kind and report every problem
- Tool: doc_compose — validate, typeset and return the PDF in one call
- Tool: signature_request_create — freeze a revision and create signing requests with links and QR codes
- Tool: doc_mail_to_me — e-mail an issued document to the signed-in account only
## Tags
pdf, documents, letters, agreements, signatures, qr-code, agenda, checklist, covenant, typesetting, e-signature, forms, templates, productivity, document-generation

## Documentation URL
https://github.com/Publifye/mcp/tree/main/services/doksi

## Health Check URL
https://doksi.publifye.com/health
