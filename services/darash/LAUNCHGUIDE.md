# Darash

## Tagline
Bible research: 59 translations, Hebrew/Greek Strong's, morphology, cross-refs, 13 dictionaries

## Description
Darash gives an AI assistant the Hebrew and Greek text of Scripture as structured data: which stem a verb is in, which Strong's numbers actually occur in a verse, what a named 19th-century lexicon says about a lemma, and which printed edition that lexicon came from.

It is a hosted server with a Streamable HTTP endpoint at https://darash-api.publifye.com/mcp, so there is nothing to install. Sign in once in the browser and your MCP client can call the tools directly. A translation alone can mislead: a Greek active verb is often rendered in the passive in English. Darash returns the voice, person and stem the text actually carries, and proves a lemma is in a verse rather than merely near it in a concordance.

It is for Bible students, pastors, translators and writers who want an assistant that quotes and parses the text instead of recalling it from memory. Every dictionary carries a provenance record that states what is verified and what is only conventional.

## Setup Requirements
- `X-API-Key` (optional): Personal API key sent as a header, an alternative to the OAuth browser sign-in. https://github.com/Publifye/mcp/blob/main/docs/connect.md

## Category
Education & Research

## Use Cases
Hebrew and Greek word studies, Bible verse parsing, Strong's number lookup, comparing Bible translations, cross-reference tracing, sermon preparation, Bible translation checking, biblical dictionary lookup, theological research

## Features
- 59 Bible translations across 36 languages, including the Leningrad Codex (`wlc`) and the Byzantine Majority Greek text (measured on the live service 2026-09-13)
- 2,142,531 verses indexed and 446,544 cross-references (measured 2026-09-13)
- Strong's lexicons augmented with Abbott-Smith, LSJ and BDB: 8,674 Hebrew and 5,523 Greek entries (measured 2026-09-13)
- Word-by-word morphology (voice, person, stem, tense, case) for 31,167 parsed verses (measured 2026-09-13)
- `strongs_in_verse` proves which Hebrew or Greek lemma is really in a verse
- `word_study` returns a complete word study in one call
- `verse_study` combines verse text, Strong's numbers, morphology and cross-references in one call
- 13 Bible dictionaries with 217,352 entries, each response carrying its provenance block (measured 2026-09-13)
- Compare the same verse across several translations in one call
- Full-text search, semantic search, Strong's search and rarity-based word frequency and hapax lists
- Etymology trees, related Strong's numbers and synonyms for a word
- Provenance record for every dictionary and both Strong's lexicons, marking each `verified` or `conventional`
- Read-only reference corpus: a lookup returns the same answer tomorrow
- OAuth 2.1 with PKCE and open Dynamic Client Registration, so a new client can register itself

## Getting Started
- "Do a word study on the Hebrew word translated 'seek' in Deuteronomy 4:29"
- "Which Strong's numbers occur in John 1:1, and what voice is each verb in?"
- "Compare Romans 8:28 across several translations"
- "What does the Bible say about mercy? Show the cross-references for Psalm 136:1"
- "Look up 'logos' in the Bible dictionaries and tell me which work each definition comes from"
- Tool: word_study — complete word study of a Greek or Hebrew word in one call; start here for any word
- Tool: strongs_in_verse — list every Strong's number, lemma and short definition in a verse
- Tool: get_morphology — word-by-word grammatical parsing of a verse, for questions of voice, person and stem
- Tool: verse_study — verse text, Strong's, morphology and cross-references in one call
- Tool: compare_verses — the same verse across several translations
- Tool: lookup_dictionary — search the 13 Bible dictionaries, with provenance

## Tags
bible, hebrew, greek, strongs, lexicon, morphology, concordance, cross-references, theology, translation, bible-dictionary, word-study, scripture, exegesis, research

## Documentation URL
https://github.com/Publifye/mcp/tree/main/services/darash

## Health Check URL
https://darash-api.publifye.com/health
