# Lexifye

## Tagline
Build dictionaries & glossaries with AI: entries, senses, versions, print PDF, EPUB, web reader

## Description
Lexifye keeps the words you study, with your senses, your references and the Hebrew and Greek behind them, as a real dictionary with revision history. The same entries are turned into a print-ready book.

It is a hosted server with a Streamable HTTP endpoint at https://lexifye.publifye.com/mcp, so there is nothing to install. Sign in once in the browser. A dictionary has three levels: dictionary, entry (lemma) and definition (sense). The definition markup is round-trippable, so an assistant can read a definition out, edit it and write it back without drift.

It is for translators, lexicographers, teachers and Bible students who want an assistant to help build and maintain a glossary or dictionary.

## Setup Requirements
- `X-API-Key` (optional): Personal API key sent as a header, an alternative to the OAuth browser sign-in. https://github.com/Publifye/mcp/blob/main/docs/connect.md

## Category
Education & Research

## Use Cases
Building a dictionary, translation glossaries, Bible word lists, lexicography, term bases for translators, publishing a dictionary as a book, collaborative glossary editing, multilingual vocabulary

## Features
- Three-level model: dictionary, entry (lemma) and definition (sense)
- Round-trippable markup satisfying `parse(render(x)) == x`, so definitions can be read, edited and written back
- Strong's enrichment from Darash: cite `[H2617]` in a definition and the lemma, SBL transliteration and gloss are written in
- Six formats from one source: light PDF, dark PDF, a 6x9 inch print interior, EPUB 3, an HTML reader and JSON
- Sixteen typesettable scripts, three of them right-to-left (Hebrew, Arabic, Persian)
- A glyph gate that fails loudly rather than shipping missing characters
- Version history, diff and revert for every definition, with history never destroyed
- Entry search by text fragment within a dictionary
- Guest editors with instant revoke
- Groups for sharing a dictionary, plus private working notes
- Trash list and restore for deleted entries and definitions
- Dictionary artifacts are credentialled: there is no public shareable reader URL, by design

## Getting Started
- "Create a Hebrew-English glossary called 'Covenant Terms' and add an entry for hesed"
- "Add a definition to the entry 'hesed' and cite Strong's [H2617]"
- "Find entries in my dictionary that contain 'kiste'"
- "Show what changed in the definition of 'logos' and revert to version 2"
- "Enrich my dictionary with Strong's data from Darash"
- Tool: dict_create — create a new dictionary
- Tool: entry_add — add a term entry to a dictionary
- Tool: definition_add — add a definition (sense) to an entry
- Tool: dict_enrich — run Darash Strong's enrichment over a dictionary's definitions
- Tool: definition_diff — compare two versions of a definition
- Tool: definition_revert — restore a definition to a past version, recorded as a new version

## Tags
dictionary, glossary, lexicography, terminology, translation, bible, strongs, epub, pdf, hebrew, greek, publishing, rtl, versioning, vocabulary

## Documentation URL
https://github.com/Publifye/mcp/tree/main/services/lexifye

## Health Check URL
https://lexifye.publifye.com/health
