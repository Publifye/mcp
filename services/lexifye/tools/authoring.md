# Markup and recovery

**The round-trippable source grammar, house style, and the trash.** 3 Lexifye MCP tools, listed below with the exact
description and input schema the server itself returns. Endpoint: `https://lexifye.publifye.com/mcp`.
See [connect](../../../docs/connect.md) to get a key.

| Tool | What it does |
|---|---|
| [`house_style`](#house-style) | THE one-stop authoring guide — read this ONCE before writing a dictionary and you have… |
| [`source_syntax`](#source-syntax) | Return the grammar of the round-trippable definition markup used by definition_get_source… |
| [`trash_list`](#trash-list) | The dict's TRASH BIN: everything soft-deleted and still recoverable, oldest first |

---

## `house_style`

**House Style** — read-only, idempotent, closed-world.

THE one-stop authoring guide — read this ONCE before writing a dictionary and you have everything: lexifye's conventions (the translit-always rule, Darash Strong's enrichment + strongs_depth/dict_enrich, universal optimistic locking, definition version history, private notes, and the access model — owner ∪ guest editors ∪ group members, with no public dictionary and nothing to make public) AND the complete markup grammar (the same content as source_syntax, appended). No arguments.

## `source_syntax`

**Source Syntax** — read-only, idempotent, closed-world.

Return the grammar of the round-trippable definition markup used by definition_get_source (read) and definition_set_source / definition_add_source (write): block prefixes (#/##/### headings, - list items, plain paragraphs) and inline spans (*emph*, **bold**, [H1234] Strong's — case- and zero-padding-insensitive on input, canonical on output, [h:hebrew], [g:greek], [ref:John 3:16]). Call this once before authoring so the source you write validates. No arguments.

## `trash_list`

**Trash List** — read-only, idempotent, closed-world.

The dict's TRASH BIN: everything soft-deleted and still recoverable, oldest first. EDITOR-level (write): a soft delete keeps the content, so the bin is visible only to someone who could edit the dict (owner, guest editor, group member). Deleting must not widen who can read what was deleted.
  entries[] — each with deleted_at, days_remaining, how many definitions and private notes come back with it, and term_taken (true when another entry has since claimed the term; the restore still works, see entry_restore).
  definitions[] — each with deleted_at, days_remaining, retained_versions (definition_history and definition_diff still answer for a deleted definition — that is the point of the soft delete) and entry_deleted (true when its entry is in the trash too, in which case entry_restore is the call to make; it brings the definition back with it).
  Restore with entry_restore / definition_restore. After grace_days the background sweep purges the row for good — and, for an entry, promotes its private notes up to dict level so the research is not lost with the lemma.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `dict_id` | string | yes |  |
| `limit` | integer | no | Bounds EACH of the two collections (entries, definitions) independently. |
| `offset` | integer | no |  |

---

*Generated from the live `tools/list` on 2026-09-13. Regenerate rather than edit by hand.*
