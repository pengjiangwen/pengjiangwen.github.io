#!/usr/bin/env python3
"""Remove duplicate / near-duplicate keywords from the pool.

Two kinds of duplicates are removed (only keywords that are NOT yet used):
  1. an unused keyword whose slug matches an already-published article
  2. an unused keyword that is a near-duplicate of another unused keyword
     (including across categories)
"""
import json
import re
from itertools import combinations
from pathlib import Path

KW = Path("config/keywords.json")
CATS = ["tech", "lifestyle", "home", "health"]
STOP = {
    "best", "top", "how", "to", "a", "an", "the", "your", "you", "guide", "guides",
    "ideas", "tips", "for", "of", "and", "in", "on", "with", "2024", "2025", "2026",
    "beginners", "beginner", "review", "reviews",
}


def slugify(t):
    t = re.sub(r"[^\w\s-]", "", t.lower().strip())
    return re.sub(r"-+", "-", re.sub(r"[\s_]+", "-", t)).strip("-")


def toks(k):
    return {t for t in re.findall(r"[a-z0-9]+", k.lower()) if t not in STOP}


def sim(a, b):
    A, B = toks(a), toks(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def main():
    data = json.loads(KW.read_text(encoding="utf-8"))
    slugs = {p.stem for p in Path("content").rglob("*.md")}
    removed = []

    # 1) drop unused keywords that duplicate a published article
    for cat in CATS:
        used = set(data[cat]["used"])
        kept = []
        for k in data[cat]["pool"]:
            if k in used:
                kept.append(k)
                continue
            s = slugify(k)
            if any(s in existing for existing in slugs):
                removed.append((cat, k, "duplicate of a published article"))
                continue
            kept.append(k)
        data[cat]["pool"] = kept

    # 2) drop near-duplicate unused keywords (across categories)
    items = []
    for cat in CATS:
        used = set(data[cat]["used"])
        items.extend((cat, k) for k in data[cat]["pool"] if k not in used)

    drop = set()
    for (c1, k1), (c2, k2) in combinations(items, 2):
        if (c1, k1) in drop or (c2, k2) in drop:
            continue
        if sim(k1, k2) >= 0.55:
            drop.add((c2, k2))
            removed.append((c2, k2, f"near-duplicate of ({c1}) {k1}"))

    for cat in CATS:
        used = set(data[cat]["used"])
        data[cat]["pool"] = [k for k in data[cat]["pool"] if k in used or (cat, k) not in drop]

    KW.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Removed {len(removed)} keywords:")
    for cat, k, why in removed:
        print(f"  [{cat}] {k}  <- {why}")


if __name__ == "__main__":
    main()
