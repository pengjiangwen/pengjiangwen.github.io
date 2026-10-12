#!/usr/bin/env python3
"""Article generator with auto-replenishing keyword pool."""
import json, os, re, random
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
from pathlib import Path
from openai import OpenAI

from taxonomy import tags_for

LLM_API_KEY = os.environ["LLM_API_KEY"]
LLM_BASE_URL = os.environ.get("LLM_BASE_URL") or "https://api.deepseek.com/v1"
LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek-chat")
SITE_NAME = "TechLife Guide"
BASE_URL = os.environ.get("SITE_BASE_URL", "https://pengjiangwen.github.io").rstrip("/")
CATEGORIES = ["tech", "lifestyle", "home", "health"]
CONTENT_DIR = Path("content")
KW_PATH = Path("config/keywords.json")
ARTICLES_PER_RUN = 2
REPLENISH_THRESHOLD = 10
REPLENISH_COUNT = 20
RELATED_COUNT = 3
RELATED_MAX_LINKS = 5


def load_keywords():
    return json.loads(KW_PATH.read_text(encoding="utf-8"))


def save_keywords(data):
    KW_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def get_unused(data):
    existing_slugs = {p.stem for p in CONTENT_DIR.rglob("*.md")}
    candidates = []
    for cat in CATEGORIES:
        entry = data[cat]
        for kw in entry["pool"]:
            if kw in entry["used"]:
                continue
            kw_slug = slugify(kw)
            if any(kw_slug in s for s in existing_slugs):
                continue
            candidates.append((kw, cat))
    random.shuffle(candidates)
    return candidates[:ARTICLES_PER_RUN]


def need_replenish(data):
    for cat in CATEGORIES:
        pending = [kw for kw in data[cat]["pool"] if kw not in data[cat]["used"]]
        if len(pending) < REPLENISH_THRESHOLD:
            return cat
    return None


SAFETY_BLOCKLIST = [
    "porn", "sex", "nude", "erotic", "adult content", "xxx", "hentai",
    "gambling", "casino", "betting", "crack", "hack", "cheat code",
    "drug", "weed", "cocaine", "weed", " marijuana", "illegal",
    "weapon", "gun", "ammo", "dark web", "deep web",
    "escort", "dating", "hookup", "casual encounter",
    "weight loss pill", "diet pill", "fat burner",
    "get rich quick", "make money fast", "forex",
    "spy", "hacker", "cracked", "warez",
]

def is_safe(text):
    text_lower = text.lower()
    for word in SAFETY_BLOCKLIST:
        if re.search(r"\b" + re.escape(word) + r"\b", text_lower):
            return False
    return True


def replenish_keywords(data, category):
    client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
    prompt = f"""Generate {REPLENISH_COUNT} SEO-friendly blog post topics for the "{category}" category on "{SITE_NAME}".
Each topic: a common search phrase people type into Google (2-8 words).
ONLY generate safe, family-friendly, legal topics. NO adult, gambling, drug, weapon, or illegal content.
Return a JSON array of strings ONLY. Example: {{"keywords": ["topic 1", "topic 2", ...]}}"""
    resp = client.chat.completions.create(model=LLM_MODEL, messages=[
        {"role": "system", "content": "You are an SEO keyword researcher. Return ONLY valid JSON. Never suggest unsafe or illegal topics."},
        {"role": "user", "content": prompt},
    ], temperature=0.8, max_tokens=4096)
    text = resp.choices[0].message.content.strip()
    m = re.search(r"\[.*?\]", text, re.DOTALL)
    if m:
        try:
            new_kws = json.loads(m.group(0))
        except json.JSONDecodeError:
            new_kws = []
    else:
        new_kws = []
    existing = set(data[category]["pool"])
    added = [kw for kw in new_kws if isinstance(kw, str) and kw.strip() and is_safe(kw) and kw not in existing]
    data[category]["pool"].extend(added)
    print(f"  Replenished {category}: +{len(added)} keywords (filtered {len(new_kws) - len(added)} unsafe)")
    return added


def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text.lower().strip())
    return re.sub(r"-+", "-", re.sub(r"[\s_]+", "-", text)).strip("-")


def yaml_str(text):
    """Quote a string safely for YAML front matter (escape backslashes, quotes, newlines)."""
    text = " ".join(str(text).split())
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def article_url(category, slug):
    return f"{BASE_URL}/{category}/{slug}/"


def load_existing_articles():
    """Read every published article's title/tags/category for internal linking."""
    arts = []
    for f in CONTENT_DIR.rglob("*.md"):
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        if not m:
            continue
        front = m.group(1)
        tm = re.search(r'^title:\s*"(.*)"\s*$', front, re.MULTILINE)
        gm = re.search(r"^tags:\s*\[(.*)\]", front, re.MULTILINE)
        title = (tm.group(1).replace('\\"', '"') if tm else f.stem.replace("-", " ")).strip()
        tags = {t.strip().strip('"') for t in gm.group(1).split(",") if t.strip()} if gm else set()
        arts.append({"path": f, "title": title, "cat": f.parent.name, "slug": f.stem, "tags": tags})
    return arts


def pick_related(articles, category, tags, exclude_path, count=RELATED_COUNT):
    """Same-category articles ranked by tag overlap (ties broken randomly)."""
    pool = [a for a in articles if a["cat"] == category and a["path"] != exclude_path]
    random.shuffle(pool)
    pool.sort(key=lambda a: len(a["tags"] & tags), reverse=True)
    return pool[:count]


def upsert_related(path, new_link, max_links=RELATED_MAX_LINKS):
    """Add/refresh a backlink in an older article's 'Related Reading' section."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return
    marker = "## Related Reading"
    if marker in text:
        head, _, tail = text.partition(marker)
        items = [ln.strip() for ln in tail.split("\n") if ln.strip().startswith("- ")]
        items = [new_link] + [i for i in items if i != new_link]
        items = items[:max_links]
        new_text = head.rstrip() + "\n\n" + marker + "\n\n" + "\n".join(items) + "\n"
    else:
        new_text = text.rstrip() + "\n\n" + marker + "\n\n" + new_link + "\n"
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")


def parse_response(text):
    title = ""
    description = ""
    tags = []
    content = ""
    m = re.search(r"TITLE:\s*(.+?)(?:\n|$)", text)
    if m: title = m.group(1).strip().strip('"')
    m = re.search(r"DESCRIPTION:\s*(.+?)(?:\n|$)", text)
    if m: description = m.group(1).strip().strip('"')
    m = re.search(r"TAGS:\s*(.+?)(?:\n|$)", text)
    if m: tags = [t.strip().lower() for t in m.group(1).split(",") if t.strip()]
    m = re.search(r"CONTENT:\s*(.+)", text, re.DOTALL)
    if m: content = m.group(1).strip()
    return title, description, tags, content


def generate(keyword, category, articles):
    client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
    prompt = f"""Write a deeply useful, original blog post about: "{keyword}"
Category: {category}

Requirements:
- 1200-1800 words of genuinely useful content (depth over breadth)
- Open with a concrete, specific hook: a real scenario, a number, or a sharp question. NO generic intros.
- Well-structured with H2/H3 subheadings. Include specific, actionable details: numbers, steps, examples, common mistakes to avoid.
- Write like an experienced human specialist. Vary sentence length. Be direct and specific.
- Include at least one practical checklist or step-by-step section.
- BANNED phrases (never use): "in today's fast-paced world", "in conclusion", "delve", "landscape", "game-changer", "unlock", "elevate", "it's important to note", "when it comes to", "in the realm of".
- 100% original, family-safe content. Do NOT include: adult, gambling, drugs, violence, illegal topics
- Format EXACTLY:

TITLE: SEO title (under 60 chars)
DESCRIPTION: Meta description (140-155 chars)
CONTENT:
## Introduction
...body with subheadings and practical value..."""
    resp = client.chat.completions.create(model=LLM_MODEL, messages=[
        {"role": "user", "content": prompt},
    ], temperature=0.7, max_tokens=16384)
    title, description, tags, content = parse_response(resp.choices[0].message.content)
    if not title: title = keyword.title()
    if not content: content = resp.choices[0].message.content
    if not is_safe(title + " " + description + " " + content):
        print(f"  SKIP (unsafe content detected)")
        return None
    # Ensure content is substantial (not just front matter)
    body_words = len(content.split())
    if body_words < 50:
        print(f"  SKIP (content too short: {body_words} words)")
        return None
    slug = slugify(title)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Controlled tags (title-first), so we never create thousands of thin tag pages.
    tags = tags_for(title, content, category)

    # Internal links: point the new article at related older posts, and add a
    # backlink from the most relevant older post so crawlers discover the new page.
    related = pick_related(articles, category, set(tags), exclude_path=CONTENT_DIR / category / f"{slug}.md")
    if related:
        lines = [f"- [{a['title']}]({article_url(a['cat'], a['slug'])})" for a in related]
        content = content.rstrip() + "\n\n## Related Reading\n\n" + "\n".join(lines) + "\n"

    md = f"""---
title: {yaml_str(title)}
date: "{date}"
description: {yaml_str(description)}
tags: {json.dumps(tags)}
categories: ["{category}"]
draft: false
---
{content}
"""
    cat_dir = CONTENT_DIR / category
    cat_dir.mkdir(parents=True, exist_ok=True)
    article_path = cat_dir / f"{slug}.md"
    article_path.write_text(md, encoding="utf-8")

    if related:
        upsert_related(related[0]["path"], f"- [{title}]({article_url(category, slug)})")

    return title, slug


def main():
    data = load_keywords()
    cat = need_replenish(data)
    if cat:
        print(f"Replenishing keywords for [{cat}]...")
        replenish_keywords(data, cat)
        save_keywords(data)
    keywords = get_unused(data)
    if not keywords:
        print("No unused keywords left across all categories!")
        return
    articles = load_existing_articles()
    for kw, cat in keywords:
        print(f"Generating: [{cat}] {kw}")
        try:
            result = generate(kw, cat, articles)
            if result is None:
                print(f"  SKIPPED (safety filter)")
                continue
            title, slug = result
            data[cat]["used"].append(kw)
            articles.append({"path": CONTENT_DIR / cat / f"{slug}.md", "title": title, "cat": cat, "slug": slug, "tags": set()})
            print(f"  OK: {title}")
        except Exception as e:
            print(f"  FAIL: {e}")
    save_keywords(data)


if __name__ == "__main__":
    main()
