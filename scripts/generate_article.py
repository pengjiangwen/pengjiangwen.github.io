#!/usr/bin/env python3
"""Standalone article generator for GitHub Actions."""
import json, os, re, random, sqlite3, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
from openai import OpenAI

LLM_API_KEY = os.environ["LLM_API_KEY"]
LLM_BASE_URL = os.environ.get("LLM_BASE_URL") or "https://opencode.ai/zen/go/v1"
LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek-v4-pro")
SITE_NAME = "TechLife Guide"

KEYWORDS = {
    "tech": [
        "best budget smartphones 2025",
        "how to build a gaming PC on a budget",
        "best wireless earbuds review 2025",
        "laptop buying guide for students",
        "best smart home devices for beginners",
        "how to speed up your slow computer",
        "best mechanical keyboards for programming",
        "iPad vs Android tablet which is better",
        "best budget drones for beginners 2025",
        "how to extend your phone battery life",
        "best USB-C monitors for MacBook",
        "WiFi 6 vs WiFi 6E what is the difference",
        "how to set up a home NAS server",
        "best free software alternatives 2025",
        "should you upgrade to Windows 12",
    ],
    "lifestyle": [
        "morning routine ideas for productivity",
        "minimalist living tips for beginners",
        "how to start a daily journaling habit",
        "best books to read this year 2025",
        "remote work productivity tips that work",
        "how to learn a new language fast at home",
        "budget travel tips for beginners",
        "how to improve your sleep quality naturally",
        "declutter your home in one weekend",
        "how to build a capsule wardrobe",
        "best side hustles you can start today",
        "how to stop procrastinating and get things done",
        "digital detox tips for a healthier life",
        "how to create a personal budget that works",
        "best meditation apps for beginners",
        "how to make money online as a student",
        "best online courses for career change 2025",
        "how to save money on groceries each month",
        "best passive income ideas for beginners",
        "how to negotiate a salary raise successfully",
        "best budgeting apps for young adults",
        "how to start a successful Etsy shop",
        "best credit cards for travel rewards",
        "how to pay off debt fast on a low income",
        "time management tips for busy professionals",
        "how to build confidence and overcome fear",
        "best habits for personal growth",
    ],
    "home": [
        "small apartment organization ideas",
        "best indoor plants for beginners that thrive",
        "how to deep clean your house room by room",
        "budget home office setup ideas 2025",
        "easy DIY home improvement projects",
        "how to reduce your electricity bill",
        "best air purifiers for home 2025",
        "how to organize your kitchen cabinets",
        "beginner guide to growing vegetables at home",
        "how to soundproof a room on a budget",
        "best robot vacuums under 500 dollars",
        "how to paint a room like a professional",
        "space saving furniture for small apartments",
        "how to create an energy efficient home",
        "best smart locks for home security",
        "best home security systems compared 2025",
        "how to increase home value on a budget",
        "best smart thermostats for energy savings",
        "how to winterize your home for winter",
        "best solar panels for home 2025",
        "how to choose the right water filter",
        "best garage organization ideas and tips",
        "how to build a deck in your backyard",
        "best patio furniture for small spaces",
        "how to install smart lighting at home",
        "best cordless vacuum cleaners 2025",
    ],
    "health": [
        "beginner workout plan you can do at home",
        "healthy meal prep ideas for the week",
        "how to start running for absolute beginners",
        "best supplements for energy and focus",
        "yoga poses for lower back pain relief",
        "how to reduce stress naturally at home",
        "high protein vegetarian meals for muscle building",
        "how to improve your posture while working",
        "benefits of walking 10000 steps every day",
        "how to stay hydrated throughout the day",
        "best stretching exercises for office workers",
        "how to build a sustainable fitness routine",
        "intermittent fasting guide for beginners",
        "how to read nutrition labels correctly",
        "best home gym equipment for small spaces",
        "how to boost your immune system naturally",
        "best vitamins for energy and brain focus",
        "how to manage anxiety without medication",
        "best sleep tracking devices and apps",
        "how to lower blood pressure with diet",
        "best protein powders for weight loss",
        "how to improve gut health naturally",
        "best exercises for seniors at home",
        "how to quit sugar in 30 days",
        "best anti inflammatory foods to eat daily",
        "how to create a morning routine for mental health",
    ],
}

DB_PATH = Path("data/factory.db")
CONTENT_DIR = Path("content")


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS keywords (keyword TEXT UNIQUE, category TEXT, used INTEGER DEFAULT 0)")
    c.execute("CREATE TABLE IF NOT EXISTS articles (keyword TEXT, title TEXT, category TEXT, slug TEXT, created_at TEXT)")
    for cat, kws in KEYWORDS.items():
        for kw in kws:
            try:
                c.execute("INSERT INTO keywords (keyword, category) VALUES (?, ?)", (kw, cat))
            except sqlite3.IntegrityError:
                pass
    conn.commit()
    conn.close()


def get_unused(count=2):
    existing_slugs = set()
    for p in CONTENT_DIR.rglob("*.md"):
        existing_slugs.add(p.stem)

    conn = sqlite3.connect(str(DB_PATH))
    all_rows = conn.execute("SELECT keyword, category FROM keywords WHERE used = 0").fetchall()
    conn.close()

    random.shuffle(all_rows)
    result = []
    for kw, cat in all_rows:
        slug = slugify(kw)
        if kw not in existing_slugs and slug not in existing_slugs:
            result.append((kw, cat))
            if len(result) >= count:
                break
    return result


def mark_used(keyword):
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("UPDATE keywords SET used = 1 WHERE keyword = ?", (keyword,))
    conn.commit()
    conn.close()


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
    prompt = f"""Write a blog post about: "{keyword}"
Category: {category}
Article: 800-1500 words. Format EXACTLY:

TITLE: Your SEO title here
DESCRIPTION: Meta description here (140-155 chars)
TAGS: tag1, tag2, tag3
CONTENT:
## Introduction
...article body..."""

    resp = client.chat.completions.create(model=LLM_MODEL, messages=[
        {"role": "system", "content": f"You are an SEO writer for {SITE_NAME}. Write helpful, original content."},
        {"role": "user", "content": prompt},
    ], temperature=0.7, max_tokens=16384)

    title, description, tags, content = parse_response(resp.choices[0].message.content)
    if not title: title = keyword.title()
    if not content: content = resp.choices[0].message.content
    if not tags: tags = [category]
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
    fp = cat_dir / f"{slug}.md"
    fp.write_text(md, encoding="utf-8")
    return title, slug


def main():
    init_db()
    keywords = get_unused(2)
    if not keywords:
        print("No unused keywords left!")
        return

    for kw, cat in keywords:
        print(f"Generating: [{cat}] {kw}")
        try:
            title, slug = generate(kw, cat)
            mark_used(kw)
            conn = sqlite3.connect(str(DB_PATH))
            conn.execute("INSERT INTO articles VALUES (?, ?, ?, ?, ?)", (kw, title, cat, slug, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            print(f"  OK: {title}")
        except Exception as e:
            print(f"  FAIL: {e}")

    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", "Auto: generate daily articles"], check=False)
    subprocess.run(["git", "push"], check=False)


if __name__ == "__main__":
    main()
