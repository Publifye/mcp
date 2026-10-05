# Maintaining the reference

The tool schemas in this repository are dated snapshots of what each server returned from
`tools/list`. A deployment or a directory listing does not update them; someone has to capture
again. Each service's `tools.json` is the source of truth, and the tool pages under
`services/<name>/tools/` are checked against it.

## Capture and review

1. **Request fresh schemas** from the live endpoint (listed in [connect.md](connect.md)) with a
   normal authenticated `tools/list` call. Keep raw captures outside this repository, and never
   commit credentials, account data, or the results of real tool calls.
2. **Choose the audience.** `tools.json` documents what a customer can call. Tools that need an
   administrator, operational and logging tools, help and health tools, and integration endpoints
   that refuse every caller but one fleet service are excluded, and each excluded bucket is listed
   by name so the count can be audited. Do not infer a tool's audience from its name.
3. **Update `services/<name>/tools.json`.** Keep each returned description, annotation set and
   input schema verbatim, and record the capture date, how the file was made, the counts and the
   excluded buckets. Every captured tool must be either documented or excluded, never both and
   never neither. `kind` is `capability` for what the product does and `plumbing` for session,
   figure or health tools that are callable but are not the offering.
4. **Describe the evidence honestly.** A capture made with one account shows what that account
   could list. It is not a test of every account's entitlements, and new schemas do not
   re-verify older claims about datasets or licences.

## Regenerate and validate

```sh
python3 scripts/render_reference.py            # rewrite pages that differ from tools.json
python3 scripts/render_reference.py --check    # write nothing; exit 1 if any page is stale
python3 scripts/check_links.py                 # every relative link and anchor in the Markdown
```

A tool page has a hand-written head (title, the question the page answers, an intro line), a
generated body (the summary table and one section per tool) and, usually, a hand-written footer
that records the capture. The renderer rebuilds every section from `tools.json`: description,
annotations (read-only or writes, destructive, idempotent, closed- or open-world), access level
where the capture recorded one, and the parameter table with its types and required flags. It
corrects the tool count in the intro line. It keeps the head, the footer, the order of tools on a
page, and the wording of each "What it does" cell that already exists.

It also fails when the data and the pages disagree about which tools exist, so a stale page cannot
pass quietly:

- a tool in `tools.json` that is on no page, or a page row for a tool that is not in `tools.json`;
- the same tool on two pages, or a duplicate name in `tools.json`;
- `capability_tools` or `session_and_cache_plumbing` that disagree with the tools' `kind`;
- an excluded tool that is also documented, or listed twice;
- an `endpoint` that is not one of the remotes in the service's `server.json`.

To add a tool, put a row for it in the summary table of the page where it belongs (any text will
do for the last cell; it is kept as written) and run the renderer. A tool that fits no page is
the case for a new page: add it to `NEW_PAGES` in the script, which creates the page once, and
add one row for it to the service README's table of areas. `services/darash/tools/session.md`
was made this way. Pages are not split automatically; the script reports any page over
`MAX_LINES` so that it can be divided by hand.

The renderer does not read or change the narrative around the pages. After a recapture also
review, by hand:

- the tool counts in the top-level [README](../README.md) and in each service README;
- [connect.md](connect.md) and the data-handling statements for the service;
- the capture note in each page footer, which says when the page was last checked;
- [CHANGELOG.md](../CHANGELOG.md).

## Verify discovery and registry claims

For each endpoint, check that an anonymous `POST` to `/mcp` answers `401` with a
`WWW-Authenticate` header whose `resource_metadata` points to a document that names the same
resource, and that the authorisation server it names publishes its own discovery document.

Query the Official MCP Registry for `pro.publifye`, follow pagination, and inspect `isLatest`.
Compare the name, version, remote URL and repository with the service's `server.json`. A file in
this repository is not evidence of registry publication, and a registry metadata version is not
the application's version.

Review the diff and run the three checks before pushing. This repository holds documentation and
metadata only; there is nothing to build or deploy from it.
