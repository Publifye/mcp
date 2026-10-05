# Vitae

## Tagline
Your CV as a document you own, edited by your AI assistant, in several languages, as a typeset PDF

## Description
Vitae keeps your CV as a document you own. Your AI assistant edits it with you, keeps the different language versions in step, and turns it into a typeset PDF. Nobody sees it until you publish it.

It is a hosted server with a Streamable HTTP endpoint at https://vitae.publifye.com/mcp, so there is nothing to install. The first time, you sign in from your browser with a Publifye account. Your CV is stored in the open JSON Resume format, so you can take it with you at any time. Every change is kept, and you can see what changed and go back.

It is for job seekers and professionals who want help writing and maintaining a CV in more than one language. Vitae does not write the CV for you, does not apply for jobs and does not send your CV to anyone.

## Setup Requirements
No setup required — sign in with OAuth in the browser on first use.

## Category
Productivity

## Use Cases
Writing a CV with AI, keeping CVs in several languages, importing an existing CV, exporting a CV as JSON Resume, CV PDF generation, CV version history, publishing a CV online, updating work experience

## Features
- CV stored in the open JSON Resume format, exportable at any time with `cv_export`
- More than one language version of a CV
- `parity_check` shows where two language versions no longer match
- Every change kept: `cv_history` lists the last 365 edits of each language version
- `cv_diff` compares any two points in history, by hash or by time
- `cv_revert` takes a CV back to an earlier point in its history
- Import of an existing CV, staged and confirmed in two steps
- Edit work entries, education entries and basics, section by section
- New CVs always start unpublished; publishing is a separate step with `visibility_set`
- A published CV is readable by anyone with its address, is never added to search engines, and `link_rotate` gives it a new address
- Typeset PDF in two versions: a complete one for the owner and a public one with private details removed
- Photo set, clear and visibility control
- No directory or search of CVs
- 42 customer tools

## Getting Started
- "Create a CV for me and import my existing CV from this JSON Resume file"
- "Add my new role at Acme as a work entry in the English version"
- "Check whether my English and Norwegian CVs match and tell me what is missing"
- "Show me what changed in my CV since yesterday"
- "Render my CV to a PDF and give me the link"
- Tool: cv_create — create a CV; it always starts unpublished
- Tool: entry_add — append a work role to one language version
- Tool: parity_check — compare two language versions and report where they disagree
- Tool: cv_diff — compare any two points in a CV's history
- Tool: visibility_set — publish or unpublish a CV
- Tool: cv_render — render a CV version to a typeset PDF
## Tags
cv, resume, curriculum-vitae, json-resume, pdf, multilingual, career, job-search, versioning, document, typesetting, profile, productivity, editing, norwegian

## Documentation URL
https://github.com/Publifye/mcp/tree/main/services/vitae

## Health Check URL
https://vitae.publifye.com/health
