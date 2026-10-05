# Lexar

## Tagline
Norwegian law for AI: current statutes and central regulations from Lovdata, with source citations

## Description
Lexar puts the current text of Norwegian law in front of an AI assistant: consolidated statutes and central regulations from Lovdata, with the citation and the source URL attached to every passage it returns. It is a research surface, not legal advice. It hands you the wording and tells you what it does not cover.

It is a hosted server with a Streamable HTTP endpoint at https://lexar-api.publifye.com/mcp, so there is nothing to install. There are seven tools: find the law, read the provision, follow its connections, and check coverage. `resolve` never picks silently; a law name or ambiguous citation returns candidates.

It is for lawyers, students, compliance staff and developers who need an assistant to quote Norwegian law exactly. Court decisions, local regulations, English translations and historical consolidated versions are not in the corpus, so no hit does not mean no law.

## Setup Requirements
No setup required — sign in with OAuth in the browser on first use.

## Category
Education & Research

## Use Cases
Norwegian legal research, quoting statutes exactly, finding the right law by name or abbreviation, reading regulations, tracing cross-references between provisions, finding preparatory works, legal compliance research, law students

## Features
- Current consolidated law from Lovdata: 759 statutes and 5,112 central regulations (measured 2026-09-16)
- 988 Norsk Lovtidend avd. I announcements for 2026
- Preparatory works (forarbeider): 23,965 from Stortinget and 5,662 from Nasjonalbiblioteket, under NLOD 2.0
- Source text with citation and source URL on every passage
- `resolve` returns candidates for a law name, short title or abbreviation instead of guessing
- In-force status on hits, reported as true, false or unknown with its basis
- Cross-references extracted between provisions (290,805 measured 2026-09-16)
- Outline tool for the table of contents of a document or unit
- `terms` browses the statutory word forms, to find the law's own wording for a plain-language word
- Source acquired 2026-09-12 from the Lovdata publicData API, with a source snapshot id
- Read-only research surface that provides source text and navigation, not legal advice
- Explicit statement of what is not covered: court decisions, local regulations, English translations, historical versions

## Getting Started
- "What does the Working Environment Act say about notice of dismissal? Quote the provision with its citation"
- "Resolve 'ferieloven' to the exact law and show me its outline"
- "Read aml § 15-7 and list the provisions it refers to"
- "Is this law in force, and where does that come from?"
- "Find preparatory works that discuss this provision"
- Tool: search — plain-language question search over provisions; the usual starting point
- Tool: resolve — map a law name, abbreviation or citation to candidate documents
- Tool: read — read exact legal wording by citation or id; quote only this
- Tool: outline — table of contents for a document or unit
- Tool: connections — follow cross-references and preparatory-works pointers after reading
- Tool: status — coverage, freshness and legal-effect uncertainty for the corpus or a document

## Tags
norwegian-law, legal, lovdata, statutes, regulations, norway, legal-research, citations, nlod, compliance, forarbeider, lovtidend, law, norwegian, research

## Documentation URL
https://github.com/Publifye/mcp/tree/main/services/lexar

## Health Check URL
https://lexar-api.publifye.com/health
