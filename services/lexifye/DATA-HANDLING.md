# Lexifye — what happens to your work

You are about to put a dictionary you may build over years inside someone else's service. This page says what the service
guarantees about getting it back, and links to the documents that govern the rest. Every tool named
here is in [tools.json](tools.json) with its full input schema.

## Ownership

From the [Terms](https://publifye.com/terms.html):

> What you write, upload or build in our services stays yours. We do not claim ownership of it.

## Deletion is soft, and recoverable

Deleting is a reversible state, not an erasure. The recovery surface, all callable by you:

| Tool | What it does |
|---|---|
| `trash_list` | shows what is deleted but still recoverable |
| `dict_restore` | brings back a deleted dictionary |
| `entry_restore` | brings back a deleted entry |
| `definition_restore` | brings back a deleted definition |
| `definition_revert` | returns a definition to an earlier version |
| `definition_history` · `definition_diff` | read and compare earlier versions |
| `dict_freeze` · `dict_unfreeze` | make a dictionary read-only so nothing can change it |

Version history is per definition, so a single sense can be rolled back without touching the entry
around it.

## Getting it out

One source renders to a light PDF, a dark PDF, a 6×9″ print interior, EPUB 3, an HTML reader and
JSON. `definition_get_source` returns the round-trippable markup — the grammar satisfies
`parse(render(x)) == x`, so what you read out is what you can write back.

Dictionary artifacts are credentialled: there is no public shareable reader URL, by design.

## Closing the account

From the [Privacy Policy](https://publifye.com/privacy.html):

> Closing an account removes it from use immediately and keeps a restorable copy for 30 days, after
> which it is erased.

Procedure: <https://publifye.com/data-deletion.html>. GDPR rights, including portability — "the data
you gave us, in a machine-readable form" — are set out in the same policy.

## AI training

**Publifye does not use your content to train AI models.** Not your book, not your dictionary, not
your notes — no part of what you write here is used as training data for any model, ours or anyone
else's.

What does happen, and the [Privacy Policy](https://publifye.com/privacy.html) says so: when you ask
the assistant to do something — a translation, a draft, a check — the content needed for that
request is sent to a third-party AI provider to perform it. That is inference, not training: the
provider answers the request and the exchange is over. It is how the assistant works at all, and
nothing reaches a provider except in service of something you asked for.

We state the limits of that honestly. We control what we send and why. We do not control, and
therefore do not speak for, what any third-party provider does under its own terms — so read this
as our commitment about our own handling, which is the part we can stand behind.

## What governs what

This page describes **mechanics**, and everything in it is checkable against
[tools.json](tools.json) and the live service. The binding commitments are in the
[Terms](https://publifye.com/terms.html) and the [Privacy Policy](https://publifye.com/privacy.html).
Where the two disagree, those documents win, not this one.
