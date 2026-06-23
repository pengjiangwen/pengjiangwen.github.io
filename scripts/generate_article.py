#!/usr/bin/env python3
"""Article generator with auto-replenishing keyword pool."""
import json, os, re, random, subprocess, sys
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
from pathlib import Path
from openai import OpenAI

LLM_API_KEY = os.environ["LLM_API_KEY"]
LLM_BASE_URL = os.environ.get("LLM_BASE_URL") or "https://opencode.ai/zen/go/v1"
LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek-v4-pro")
SITE_NAME = "TechLife Guide"
CATEGORIES = ["tech", "lifestyle", "home", "health"]
CONTENT_DIR = Path("content")
KW_PATH = Path("config/keywords.json")
ARTICLES_PER_RUN = 2
REPLENISH_THRESHOLD = 10
REPLENISH_COUNT = 20


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


def generate(keyword, category):
    client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
    prompt = f"""Write a high-quality blog post about: "{keyword}"
Category: {category}

Requirements:
- 800-1500 words, well-structured with H2/H3 subheadings
- Start with a strong hook, include real examples or actionable tips
- Write naturally — like a knowledgeable human blogger, NOT like generic AI
- NO fluff, no filler sentences, no clichés
- 100% original, family-safe content. Do NOT include: adult, gambling, drugs, violence, illegal topics
- Format EXACTLY:

TITLE: SEO title (under 60 chars)
DESCRIPTION: Meta description (140-155 chars)
TAGS: tag1, tag2, tag3
CONTENT:
## Introduction
...body with subheadings and practical value..."""
    resp = client.chat.completions.create(model=LLM_MODEL, messages=[
        {"role": "user", "content": prompt},
    ], temperature=0.7, max_tokens=16384)
    title, description, tags, content = parse_response(resp.choices[0].message.content)
    if not title: title = keyword.title()
    if not content: content = resp.choices[0].message.content
    if not tags: tags = [category]
    if not is_safe(title + " " + description + " " + content):
        print(f"  SKIP (unsafe content detected)")
        return None
    slug = slugify(title)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    md = f"""---
title: "{title}"
date: "{date}"
description: "{description}"
tags: {json.dumps(tags)}
categories: ["{category}"]
draft: false
---
{content}
"""
    cat_dir = CONTENT_DIR / category
    cat_dir.mkdir(parents=True, exist_ok=True)
    (cat_dir / f"{slug}.md").write_text(md, encoding="utf-8")
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
        subprocess.run(["git", "add", "-A"], check=True)
        subprocess.run(["git", "commit", "-m", "Auto: replenish keywords"], check=False)
        subprocess.run(["git", "push"], check=False)
        return
    for kw, cat in keywords:
        print(f"Generating: [{cat}] {kw}")
        try:
            result = generate(kw, cat)
            if result is None:
                print(f"  SKIPPED (safety filter)")
                continue
            title, slug = result
            data[cat]["used"].append(kw)
            print(f"  OK: {title}")
        except Exception as e:
            print(f"  FAIL: {e}")
    save_keywords(data)
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", "Auto: generate daily articles"], check=False)
    subprocess.run(["git", "push"], check=False)


if __name__ == "__main__":
    main()
