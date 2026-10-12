#!/usr/bin/env python3
"""Rewrite the tags of every article to the controlled vocabulary.

Run locally / in CI once to collapse hundreds of one-off tag pages into a
small, meaningful set of topic pages.
"""
import re
from pathlib import Path

from taxonomy import tags_for

CONTENT_DIR = Path("content")


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return None
    front, body = m.group(1), m.group(2)
    tm = re.search(r'^title:\s*"(.*)"\s*$', front, re.MULTILINE)
    title = tm.group(1).replace('\\"', '"') if tm else path.stem.replace("-", " ")
    return text, front, body, title


def main():
    changed = 0
    for f in sorted(CONTENT_DIR.rglob("*.md")):
        parsed = parse(f)
        if not parsed:
            continue
        text, front, body, title = parsed
        category = f.parent.name
        tags = tags_for(title, body, category)
        new_line = "tags: " + str(tags).replace("'", '"')
        new_front, n = re.subn(r"^tags:.*$", new_line, front, count=1, flags=re.MULTILINE)
        if n and new_front != front:
            f.write_text(f"---\n{new_front}\n---\n{body}", encoding="utf-8")
            changed += 1
    print(f"Normalized tags in {changed} files")


if __name__ == "__main__":
    main()
