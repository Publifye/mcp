#!/usr/bin/env python3
"""Check, and regenerate, the per-service tool reference pages.

The source of truth is services/<name>/tools.json, captured from the live
server (procedure: docs/maintaining.md). Each page services/<name>/tools/*.md
has three parts:

  head     title, the question the page answers, intro line   (hand-written)
  body     summary table and one section per tool             (generated)
  footer   the capture note                                   (hand-written)

Usage:
  render_reference.py           rewrite every page that differs from tools.json
  render_reference.py --check   write nothing; exit 1 if anything is stale

Which tools sit on which page, and in what order, is read from each page's own
summary table. The "What it does" cell of a row that already exists is kept as
written; every section (description, annotations, parameter table) is rebuilt
from tools.json. A tool that is in tools.json but on no page, or on a page but
not in tools.json, fails the run -- unless NEW_PAGES below says which new page
should take it. Pages are never split: the longest are reported if they pass
MAX_LINES, which only means the page should be divided by hand.
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAX_LINES = 800
SUMMARY_WIDTH = 90

# Pages that do not exist yet. Created from tools.json on the first run; after
# that they are ordinary pages (head and footer are kept, the body regenerated).
NEW_PAGES = {
    ('darash', 'session'): {
        'title': 'Session, figures and health',
        'question': 'How do I check the service, send feedback, and manage the figures I have stored?',
        'select': lambda tool: tool.get('kind') == 'plumbing',
        'connect': 'to get a key',
    },
}


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def ptype(prop):
    typ = prop.get('type', 'see schema')
    if isinstance(typ, list):
        return str(typ)
    items = prop.get('items')
    if typ == 'array' and isinstance(items, dict) and isinstance(items.get('type'), str):
        return 'array of ' + items['type']
    return typ


def flags(tool):
    a = tool.get('annotations') or {}
    out = ['read-only' if a.get('readOnlyHint') else 'writes']
    if a.get('destructiveHint') and not a.get('readOnlyHint'):
        out.append('destructive')
    if a.get('idempotentHint'):
        out.append('idempotent')
    out.append('closed-world' if a.get('openWorldHint') is False else 'open-world')
    return ', '.join(out)


def section(tool):
    schema = tool.get('inputSchema') or {}
    props = schema.get('properties') or {}
    required = schema.get('required') or []
    head = f"**{tool.get('title') or tool['name']}** — {flags(tool)}"
    if tool.get('access'):
        head += f" · access: `{tool['access']}`"
    lines = [f"## `{tool['name']}`", '', head + '.', '', tool['description'].rstrip(), '']
    if not props:
        lines += ['*No parameters.*', '']
    else:
        lines += ['| Parameter | Type | Required | Description |', '|---|---|---|---|']
        for name, prop in props.items():
            lines.append(f"| `{name}` | {cell(ptype(prop))} | {'yes' if name in required else 'no'} | "
                         f"{cell(prop.get('description', ''))} |")
        lines.append('')
    return lines


def summary(tool):
    text = re.sub(r'\s*\[END\]\s*$', '', tool['description'].strip()).splitlines()[0]
    match = re.match(r'(.*?[.!?])(?:\s|$)', text)
    text = (match.group(1) if match else text).rstrip('.')
    if len(text) > SUMMARY_WIDTH:
        text = text[:SUMMARY_WIDTH - 1].rstrip() + '…'
    return cell(text)


ROW = re.compile(r'^\| \[`([^`]+)`\]\(#[^)]*\) \|(?: (\w+) \|)? (.*) \|$')


def split_page(text):
    """-> head, [(name, access, cell)], footer. Raises ValueError on a shape we do not know."""
    lines = text.split('\n')
    start = next((i for i, l in enumerate(lines) if l.startswith('| Tool |')), None)
    if start is None:
        raise ValueError('no summary table')
    end = start + 2
    rows = []
    while end < len(lines) and lines[end].startswith('|'):
        line, broken = lines[end], False
        while not line.endswith(' |') and end + 1 < len(lines):  # a cell that swallowed a line break
            end += 1
            line, broken = line + ' ' + lines[end], True
        m = ROW.match(line)
        if not m:
            raise ValueError(f'unreadable table row: {line[:60]}')
        name, access, what = m.groups()
        rows.append((name, access, None if broken else what))  # a broken cell is rewritten
        end += 1
    rules = [i for i, l in enumerate(lines) if l == '---' and i >= end]
    if not rules:
        raise ValueError('no rule after the summary table')
    tail = '\n'.join(lines[rules[-1] + 1:])
    footer = None if '\n## `' in '\n' + tail else tail  # some pages end after the last tool, with no footer
    return '\n'.join(lines[:start]), rows, footer


def build(head, tools, old_cells, with_access, footer):
    out = [head.rstrip('\n'), '']
    out.append('| Tool | Access | What it does |' if with_access else '| Tool | What it does |')
    out.append('|---|---|---|' if with_access else '|---|---|')
    for t in tools:
        what = old_cells.get(t['name'], summary(t))
        row = f"| [`{t['name']}`](#{t['name']}) |"
        out.append(row + (f" {t.get('access', '')} | " if with_access else ' ') + what + ' |')
    out += ['', '---', '']
    for t in tools:
        out += section(t)
    if footer is None:
        return '\n'.join(out[:-1]).rstrip('\n') + '\n'
    return '\n'.join(out + ['---']) + '\n' + footer


def set_count(head, n):
    return re.sub(r'\b\d+( [\w ]+? MCP tools)', lambda m: f'{n}{m.group(1)}', head, count=1)


def load(service_dir):
    data = json.loads((service_dir / 'tools.json').read_text())
    tools = {}
    for t in data['tools']:
        if t['name'] in tools:
            raise ValueError(f"{service_dir.name}: duplicate tool {t['name']}")
        if not t.get('description') or not isinstance(t.get('inputSchema'), dict):
            raise ValueError(f"{service_dir.name}: {t['name']} lacks description or inputSchema")
        tools[t['name']] = t
    counts = data['counts']
    problems = []
    if counts.get('capability_tools') != sum(t.get('kind') == 'capability' for t in tools.values()):
        problems.append('counts.capability_tools')
    if counts.get('session_and_cache_plumbing') != sum(t.get('kind') == 'plumbing' for t in tools.values()):
        problems.append('counts.session_and_cache_plumbing')
    listed = [n for v in data['excluded'].values() if isinstance(v, list) for n in v]
    if len(listed) != len(set(listed)) or set(listed) & set(tools):
        problems.append('excluded names overlap each other or documented tools')
    manifest = json.loads((service_dir / 'server.json').read_text())
    if not any(r.get('url') == data['endpoint'] for r in manifest.get('remotes', [])):
        problems.append('endpoint is not in server.json remotes')
    if problems:
        raise ValueError(f'{service_dir.name}: ' + '; '.join(problems))
    return data, tools


def new_page_head(data, spec, count):
    name = data['service'].capitalize()
    return (f"# {spec['title']}\n\n**{spec['question']}** {count} {name} MCP tools, listed below with the exact\n"
            f"description and input schema the server itself returns. Endpoint: `{data['endpoint']}`.\n"
            f"See [connect](../../../docs/connect.md) {spec['connect']}.\n")


def new_page_footer(data):
    version = re.search(r'version ([\d.]+)', data['how_this_was_made'])
    where = f", version {version.group(1)}," if version else ''
    return (f"\n*Generated by `scripts/render_reference.py` from the live `tools/list`{where} captured "
            f"{data['captured']} (see [tools.json](../tools.json)). Regenerate rather than edit by hand.*\n")


def render_service(service_dir):
    data, tools = load(service_dir)
    name = service_dir.name
    out, seen = {}, {}
    tool_dir = service_dir / 'tools'
    for path in sorted(tool_dir.glob('*.md')):
        head, rows, footer = split_page(path.read_text())
        names = [r[0] for r in rows]
        unknown = [n for n in names if n not in tools]
        if unknown:
            raise ValueError(f'{path.relative_to(ROOT)}: not in tools.json: {unknown}')
        for n in names:
            if n in seen:
                raise ValueError(f'{path.relative_to(ROOT)}: {n} is also on {seen[n]}')
            seen[n] = path.name
        with_access = any(r[1] for r in rows)
        ordered = [tools[n] for n in names]
        text = build(set_count(head, len(ordered)), ordered, {r[0]: r[2] for r in rows if r[2] is not None}, with_access, footer)
        out[path] = text
    for (svc, slug), spec in NEW_PAGES.items():
        if svc != name:
            continue
        path = tool_dir / f'{slug}.md'
        picked = [t for t in tools.values() if spec['select'](t) and t['name'] not in seen]
        if path in out or not picked:
            continue
        for t in picked:
            seen[t['name']] = path.name
        out[path] = build(new_page_head(data, spec, len(picked)), picked, {}, False, new_page_footer(data))
    missing = [n for n in tools if n not in seen]
    if missing:
        raise ValueError(f'{name}: in tools.json but on no page: {missing}')
    return out, len(tools)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--check', action='store_true', help='write nothing; exit 1 if stale')
    args = parser.parse_args()
    expected, total = {}, 0
    services = sorted(p.parent for p in (ROOT / 'services').glob('*/tools.json'))
    for service in services:
        files, count = render_service(service)
        expected.update(files)
        total += count
    stale = []
    for path, content in expected.items():
        if not path.exists() or path.read_text() != content:
            stale.append(str(path.relative_to(ROOT)))
            if not args.check:
                path.write_text(content)
    long_pages = [f'{p.relative_to(ROOT)} ({len(c.splitlines())} lines)' for p, c in expected.items()
                  if len(c.splitlines()) > MAX_LINES]
    print(f'{len(services)} services, {total} tools, {len(expected)} pages; {len(stale)} stale')
    if long_pages:
        print('over MAX_LINES, divide by hand: ' + ', '.join(long_pages))
    if stale:
        print('\n'.join(('stale: ' if args.check else 'rewritten: ') + s for s in stale))
    return 1 if (args.check and stale) or long_pages else 0


if __name__ == '__main__':
    sys.exit(main())
