#!/usr/bin/env python3
"""Standalone article generator for GitHub Actions."""
import json, os, re, random, sqlite3, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
from openai import OpenAI

LLM_API_KEY = os.environ["LLM_API_KEY"]
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "https://opencode.ai/zen/go/v1")
LLM_MODEL = os.environ.get("LLM_MODEL", "mimo-v2.5")
SITE_NAME = "TechLife Guide"

KEYWORDS = {
    "tech": [
        "best budget smartphones 2025",
        "how to build a gaming PC on a budget",
        "laptop buying guide for students",
        "best smart home devices for beginners",
        "how to extend your phone battery life",
        "best USB-C monitors for MacBook",
        "WiFi 6 vs WiFi 6E what is the difference",
        "should you upgrade to Windows 12",
    ],
    "lifestyle": [
        "morning routine ideas for productivity",
        "minimalist living tips for beginners",
        "how to start a daily journaling habit",
        "best books to read this year 2025",
        "remote work productivity tips that work",
        "how to improve your sleep quality naturally",
        "budget travel tips for beginners",
    ],
    "home": [
        "small apartment organization ideas",
        "best indoor plants for beginners that thrive",
        "how to deep clean your house room by room",
        "budget home office setup ideas 2025",
        "easy DIY home improvement projects",
        "how to reduce your electricity bill",
        "space saving furniture for small apartments",
    ],
    "health": [
        "beginner workout plan you can do at home",
        "healthy meal prep ideas for the week",
        "how to start running for absolute beginners",
        "yoga poses for lower back pain relief",
        "how to reduce stress naturally at home",
        "how to improve your posture while working",
        "benefits of walking 10000 steps every day",
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
    conn = sqlite3.connect(str(DB_PATH))
    rows = conn.execute("SELECT keyword, category FROM keywords WHERE used = 0 ORDER BY RANDOM() LIMIT ?", (count,)).fetchall()
    conn.close()
    return rows if rows else []


def mark_used(keyword):
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("UPDATE keywords SET used = 1 WHERE keyword = ?", (keyword,))
    conn.commit()
    conn.close()


def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text.lower().strip())
    return re.sub(r"-+", "-", re.sub(r"[\s_]+", "-", text)).strip("-")


def extract_json(text):
    m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL) or re.search(r"\{.*\}", text, re.DOTALL)
    return m.group(1) if m else text


def generate(keyword, category):
    client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
    prompt = f"""Write a blog post about: "{keyword}"
Category: {category}
Return JSON with: "title" (SEO title), "description" (meta, 140-155 chars), "tags" (array of 3-5), "content" (full markdown article 800-1500 words).
Output inside ```json``` block."""

    resp = client.chat.completions.create(model=LLM_MODEL, messages=[
        {"role": "system", "content": f"You are an SEO writer for {SITE_NAME}. Write helpful, original content. Never mention AI."},
        {"role": "user", "content": prompt},
    ], temperature=0.7, max_tokens=16384)

    result = json.loads(extract_json(resp.choices[0].message.content))
    title = result.get("title", keyword.title())
    desc = result.get("description", "")
    tags = result.get("tags", [category])
    content = result.get("content", "")
    slug = slugify(title)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    md = f"""---
title: "{title}"
date: "{date}"
description: "{desc}"
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
