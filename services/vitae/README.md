# Vitae — CV MCP server for Claude, Cursor and any MCP client

**Vitae keeps your CV as a document you own. Your AI assistant edits it with you, keeps the
different language versions in step, and turns it into a typeset PDF. Nobody sees it until you
publish it.**

| | |
|---|---|
| Endpoint | `https://vitae.publifye.com/mcp` |
| Transport | Streamable HTTP |
| Auth | OAuth 2.1 + PKCE (S256), DCR open |
| Registry | `pro.publifye/vitae` ([server.json](server.json)) |
| Product site | <https://vitae.publifye.com> |
| Capability tools | **42** ([full schemas](tools.json)) |

## Connect

```jsonc
{ "mcpServers": { "vitae": { "type": "http", "url": "https://vitae.publifye.com/mcp" } } }
```

Claude Code: `claude mcp add --transport http vitae https://vitae.publifye.com/mcp`, then `/mcp` to
sign in. The first time, you sign in from your browser with a Publifye account. The full discovery
chain is in **[../../docs/connect.md](../../docs/connect.md)**.

## How it works

Your CV is stored in the open [JSON Resume](https://jsonresume.org) format, so you can take it with
you at any time with `cv_export`. You can keep it in more than one language, and `parity_check`
shows where two versions no longer match, for example a job that is in the English version but
missing from the Norwegian one.

Every change is kept. `cv_history` lists the last 365 edits of each language version, `cv_diff`
shows what changed, and `cv_revert` takes you back.

A new CV always starts unpublished. Publishing is a separate step you take with `visibility_set`.
A published CV can be read by anyone who has its address, but it is never added to search engines,
and `link_rotate` gives it a new address if you want to take the old one back. The PDF comes in
two versions: a complete one for you, and a public one with private details removed.

## What the tools do

Every tool is documented with its exact description, annotations and input schema, 42 in all,
generated from the service's own registry.

| Area | The question it answers | Tools |
|---|---|---|
| **[Your CVs](tools/cvs.md)** | Which CVs do you have, and how do you bring one in or take it out? | 9 |
| **[Editing a CV](tools/editing.md)** | How do you change what the CV says? | 12 |
| **[Languages and history](tools/languages-and-history.md)** | Do the language versions agree, and what changed? | 9 |
| **[Publishing and sharing](tools/publishing.md)** | Who can see the CV, and where do they find the PDF? | 8 |
| **[Photo](tools/photo.md)** | Which photo goes on the CV, and who sees it? | 4 |

Machine-readable: **[tools.json](tools.json)** has all 42 with full JSON Schema. Staff-only tools
and the logging tools are listed by name there too, but they are not part of what a customer can use.

## What it does not do

- It does not write your CV for you. Your assistant helps, but what the CV says is your decision.
- It does not list CVs anywhere. There is no directory and no search.
- It does not apply for jobs or send your CV to anyone.

## Plans

Free with a Publifye account: 60 assistant calls a day, no card needed. Vitae Access costs $24 a
year. Prices can change, and **the current ones are always on <https://vitae.publifye.com>**. If
this page and the site disagree, the site is right.
