# Audio Bible

## Tagline
Two Bibles read aloud for AI: World English Bible and NB2026, with listening links and downloads

## Description
Audio Bible gives an AI assistant a Bible as text and as sound: every verse of a chapter, numbered; a listening link that starts at a given verse with its timing in seconds; a recording made on demand when a chapter has not been read aloud yet; and a personal download link for the result.

It is a hosted server with a Streamable HTTP endpoint at https://audiobible.publifye.com/mcp, so there is nothing to install. Sign in once in the browser. Two Bibles are offered, the World English Bible (English) and Bibelen Anno 2026 (NB2026, Norwegian Bokmål), and every capability tool takes a `bible` argument to choose between them. The assistant is told to quote verses exactly as returned, not paraphrase them as scripture.

It is for readers, listeners, pastors and teachers. There is no commentary: text and audio only. For the Hebrew and Greek, other translations and lexicons, see Darash.

## Setup Requirements
No setup required — sign in with OAuth in the browser on first use.

## Category
Content & Media

## Use Cases
Listening to Bible chapters, reading a chapter verse by verse, audio Bible downloads, Norwegian Bible audio, English Bible audio, jumping to a verse in audio, Bible listening for study groups

## Features
- Two Bibles: the World English Bible and NB2026 (Bibelen Anno 2026, Norwegian Bokmål)
- Every capability tool takes an optional `bible` argument; the World English Bible is the default
- Exact verse text, numbered, with whether the chapter's audio is recorded
- Listening links: the public reading page with the verse highlighted and the direct stream with the verse's start and end in seconds
- On-demand recording of a chapter that has not been read aloud, through the same queue as the website's Read button
- Progress check for a recording without starting anything
- Personal, expiring download links: one chapter as `.opus`, several as a ZIP on the annual plan
- Allowance check for the rolling 24 hours before promising a download
- Coverage reporting per Bible of how much has been recorded
- Book list and chapter search matching the website's own search
- The World English Bible is public domain
- Public chapter pages are plain server-rendered HTML anyone can read
- Text and audio only, with no commentary or interpretation

## Getting Started
- "Read me Psalm 23 from the World English Bible, verse by verse"
- "Give me a link to listen to John 3 starting at verse 16"
- "Have Ruth 2 read aloud if it is not recorded yet, and tell me when it is ready"
- "How much of the Bible has been recorded in NB2026?"
- "How many downloads do I have left today?"
- Tool: get_chapter — exact numbered verse text of a chapter and whether its audio is recorded
- Tool: listen_link — reading page and audio stream links, optionally from a given verse
- Tool: prepare_chapter — have a chapter read aloud if it is not yet recorded
- Tool: chapter_progress — how far a chapter's recording has got
- Tool: download_link — personal expiring download link for recorded chapters
- Tool: my_allowance — plan, download allowance left and chapter preparations left today

## Tags
bible, audio-bible, audiobook, scripture, listening, world-english-bible, nb2026, norwegian, bible-reading, download, opus, christian, media, english

## Documentation URL
https://github.com/Publifye/mcp/tree/main/services/audiobible

## Health Check URL
https://audiobible.publifye.com/health
