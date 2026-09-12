# Junifye — what happens to your work

You are about to put a book you may spend months writing inside someone else's service. This page says what the service
guarantees about getting it back, and links to the documents that govern the rest. Every tool named
here is in [tools.json](tools.json) with its full input schema.

## Ownership

From the [Terms](https://publifye.com/terms.html):

> What you write, upload or build in our services stays yours. We do not claim ownership of it.

## Deletion is soft, and recoverable

Deleting is a reversible state, not an erasure. The recovery surface, all callable by you:

| Tool | What it does |
|---|---|
| `book_restore` | brings back a deleted book |
| `chapter_restore` | brings back a deleted chapter |
| `chapter_revert` | returns a chapter to an earlier version |
| `chapter_version_get` · `chapter_history` | read any earlier version |
| `chapter_diff` | word-level diff between versions |
| `book_cover_restore` · `book_cover_versions` | the same for covers |
| `book_freeze` · `book_unfreeze` | make a book read-only so nothing can change it |

`chapter_diff` is worth knowing about for a different reason: when you and an assistant are both
editing, it tells you what actually changed rather than what either of you believes changed.

## Getting it out

`book_export_begin` produces a checksummed export of the whole book. Import is the same shape in
reverse, with a three-way conflict gate. Published artifacts — EPUB 3, print-ready PDF, reader PDFs,
TXT, TeX, HTML and a JSON bundle — are listed by `book_files`.

There is no format in which your book exists only inside this service.

## Closing the account

From the [Privacy Policy](https://publifye.com/privacy.html):

> Closing an account removes it from use immediately and keeps a restorable copy for 30 days, after
> which it is erased.

Procedure: <https://publifye.com/data-deletion.html>. GDPR rights, including portability — "the data
you gave us, in a machine-readable form" — are set out in the same policy.

## AI providers

The Privacy Policy discloses that some services send the content you give them to a third-party AI
provider in order to perform the operation you asked for — a translation, a draft, a check. That is
what makes the assistant work.

## What governs what

This page describes **mechanics**, and everything in it is checkable against
[tools.json](tools.json) and the live service. The binding commitments are in the
[Terms](https://publifye.com/terms.html) and the [Privacy Policy](https://publifye.com/privacy.html).
Where the two disagree, those documents win, not this one.
