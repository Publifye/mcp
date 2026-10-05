# Junifye

## Tagline
Write books, studies & commentaries with your AI — EPUB, print-ready PDF, web reader, ISBN, RTL

## Description
Junifye lets an AI assistant write a structured book with you: chapters, blocks, headings, Scripture quotations, tables and figures. The same source is then published as a print-ready PDF, an EPUB 3, a web reader and more.

It is a hosted server with a Streamable HTTP endpoint at https://junifye.publifye.com/mcp, so there is nothing to install. Sign in once in the browser. The assistant never touches JSON or LaTeX: it edits through block and span tools against a plain-text source grammar, and the system owns the typesetting. Bible-quote blocks resolve against Darash, so a misquotation or a wrong Strong's number is rejected at write time rather than discovered in print.

It is for authors, pastors, teachers and small publishers who want to draft and revise a book with an assistant and produce files a printer or an e-reader will accept.

## Setup Requirements
- `X-API-Key` (optional): Personal API key sent as a header, an alternative to the OAuth browser sign-in. https://github.com/Publifye/mcp/blob/main/docs/connect.md

## Category
Content & Media

## Use Cases
Writing a book with AI, Bible study guides, commentaries, EPUB publishing, print-on-demand preparation, ISBN assignment, translating and linking language editions, right-to-left Hebrew and Arabic books, collaborative editing

## Features
- Structured authoring through block and span tools: paragraphs, headings, quotations, lists, tables, stat blocks, figures and inline markup
- Scripture quotation blocks verified against Darash, with wrong quotes and Strong's numbers rejected at write time
- One source, many outputs: reader PDFs in light and dark, a press-ready print interior, a full wrap cover, EPUB 3, TXT, TeX, an HTML reader and a JSON bundle
- Print setup with printer presets, spine formula, gutter ladder, bleed, PDF/X and a low-DPI press report
- Real ISBN-13 assignment from an allocated registrant pool, not a placeholder
- Right-to-left typesetting for Hebrew, Arabic, Persian and Urdu with an explicit LTR-island span
- Chapter versioning with word-level diff and revert
- Linked language editions of the same book
- Round-trippable plain-text source: read a chapter out, edit it and write it back
- Book and chapter outline tools that plan a read before pulling any content
- Covers, logos, figures and image uploads
- Groups, guests and private working notes for sharing a book with an editor
- Book export as an editable bundle
- Trash and restore for books and chapters
- Documented guarantees for recovering, exporting and deleting your work (DATA-HANDLING.md)

## Getting Started
- "Create a new book called 'Walking in Grace' with three chapters and add an introduction"
- "Add a Bible quotation block for John 3:16 to chapter 2"
- "Show me an outline of my book before you read any chapters"
- "What changed in chapter 4 in my last edit?"
- "Set up my book for print and tell me whether the interior is press-ready"
- Tool: house_style — the editorial ruleset; read once before writing or vetting a book
- Tool: source_syntax — the plain-text block grammar used to read and write chapters
- Tool: book_create — create a new book and get its id
- Tool: chapter_create — add a chapter to a book
- Tool: block_add_bible_quote — add a verified scripture quotation block
- Tool: print_set — configure a book for print-on-demand and render a press-ready interior PDF

## Tags
books, authoring, writing, epub, pdf, publishing, print-on-demand, isbn, typesetting, rtl, bible-study, commentary, ebook, self-publishing, collaboration

## Documentation URL
https://github.com/Publifye/mcp/tree/main/services/junifye

## Health Check URL
https://junifye.publifye.com/health
