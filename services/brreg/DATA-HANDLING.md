# Brreg — what happens to your questions

Brreg only reads. No tool writes to the register or keeps anything you author, so there is no work
of yours to recover or export. What there is to say is what the service records about the calls you
make, and what leaves the service on your behalf. Every tool named here is in
[tools.json](tools.json) with its full input schema.

## What is logged

From the service's own documentation, <https://brreg.publifye.com/en/docs#privacy>:

> What we log: for every tool call on a customer account, the account, the client IP address, the
> tool and the outcome — never the arguments you send. The audit trail is kept for 365 days.

The organisation numbers you look up and the names and search text you send are arguments, so they
are not in that trail. Calls are also counted per account, which is what the daily allowance is
measured against.

## What is kept for a few minutes

A result too long for one response continues with a cursor. To honour it, the service keeps that
call's normalised arguments in memory and, best effort, in Redis for the cursor's lifetime of 15
minutes. The cursor is bound to the caller who received it; another account cannot use it.

## What leaves the service

Only an organisation number, and only when you ask for something that needs Brønnøysundregistrene:

| When | What is sent | To |
|---|---|---|
| `entity_lookup` with `fields` including `financials` | the organisasjonsnummer | Regnskapsregisteret's open API at data.brreg.no |
| `entity_lookup` with `live=true` | the organisasjonsnummer | Enhetsregisteret's open API at data.brreg.no |

Key figures fetched this way are stored against the organisation number and served to later calls;
the store holds the figures, not who asked for them. No language model is involved in answering a
call, so nothing is sent to an AI provider.

## Personal data in the register

Enhetsregisteret is a register of organisations, but a sole proprietorship (ENK) is tied to one
person. Brreg therefore holds back an ENK's e-mail and phone numbers, former names and activity
text, and a search without a name never lists sole proprietorships or their sub-units. There are
no roles or persons in the service, no address-only lookups of individuals and no bulk export. What
is withheld, and how removals are applied, is in [PROVENANCE.md](PROVENANCE.md).

## What governs what

This page describes **mechanics**, and everything in it is checkable against
[tools.json](tools.json) and the live service. The binding commitments are in the
[Terms](https://publifye.com/terms.html) and the [Privacy Policy](https://publifye.com/privacy.html).
Where this page and those documents disagree, those documents win, not this one.
