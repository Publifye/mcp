#!/usr/bin/env python3
"""Check every relative link and #anchor in the repository's Markdown.

Anchors are computed the way GitHub computes heading ids (github-slugger),
verified against GitHub's own rendering of this repository:
lower-case; drop every character that is not a letter, digit, mark,
connector (underscore), space or hyphen; spaces become hyphens; a repeated
heading gets -1, -2, ... So "## `asset_upload_begin`" is #asset_upload_begin
and "## Timely — an AI" is #timely--an-ai. Explicit <a id|name="..."> count too.

Usage: scripts/check_links.py [--fix]   (exit 1 when anything is broken)
--fix rewrites an anchor that differs from a real heading id only in
hyphens versus underscores (the one systematic mistake this has fixed).
"""
import os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FENCE = re.compile(r"^(```|~~~)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LINK = re.compile(r"(?<!!)\[(?:[^\]\\]|\\.)*\]\(\s*<?([^)\s>]*)>?(?:\s+\"[^\"]*\")?\s*\)")


def slug(text):
    text = re.sub(r"<[^>]+>", "", text)          # inline HTML
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links -> text
    text = text.replace("`", "").replace("*", "").strip().lower()
    out = []
    for ch in text:
        cat = unicodedata.category(ch)
        if ch in " -" or cat[0] in "LNM" or cat == "Pc":
            out.append("-" if ch == " " else ch)
    return "".join(out)


def anchors(path, cache={}):
    if path in cache:
        return cache[path]
    ids, seen, fenced = set(), {}, False
    for line in open(path, encoding="utf-8"):
        if FENCE.match(line.strip()):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = HEADING.match(line.rstrip("\n"))
        if m:
            s = slug(m.group(2))
            n = seen.get(s, 0)
            seen[s] = n + 1
            ids.add(s if n == 0 else f"{s}-{n}")
        for a in re.findall(r'<a\s+(?:id|name)="([^"]+)"', line):
            ids.add(a)
    cache[path] = ids
    return ids


def main():
    fix = "--fix" in sys.argv
    broken, fixed, checked = [], 0, 0
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            path = os.path.join(dirpath, f)
            text = open(path, encoding="utf-8").read()
            new = text

            def check(m):
                nonlocal fixed, checked
                target = m.group(1)
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                    return m.group(0)  # http(s), mailto, ...
                file_part, _, frag = target.partition("#")
                dest = os.path.normpath(os.path.join(dirpath, file_part)) if file_part else path
                checked += 1
                rel = os.path.relpath(path, ROOT)
                if not os.path.exists(dest):
                    broken.append(f"{rel}: missing file {target}")
                    return m.group(0)
                if not frag or not dest.endswith(".md"):
                    return m.group(0)
                ids = anchors(dest)
                if frag in ids:
                    return m.group(0)
                cand = [i for i in ids if i.replace("_", "-") == frag.replace("_", "-")]
                if fix and len(cand) == 1:
                    fixed += 1
                    return m.group(0).replace("#" + frag, "#" + cand[0])
                broken.append(f"{rel}: no anchor #{frag} in {os.path.relpath(dest, ROOT)}" + (f" (GitHub id: #{cand[0]})" if cand else ""))
                return m.group(0)

            fenced, lines = False, []
            for line in new.splitlines(keepends=True):
                if FENCE.match(line.strip()):
                    fenced = not fenced
                lines.append(line if fenced else LINK.sub(check, line))
            new = "".join(lines)
            if fix and new != text:
                open(path, "w", encoding="utf-8").write(new)
    print(f"checked {checked} relative links; fixed {fixed}; broken {len(broken)}")
    for b in broken:
        print("  " + b)
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
