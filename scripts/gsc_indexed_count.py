#!/usr/bin/env python3
"""Count how many article pages Google has indexed, using the
Google Search Console URL Inspection API.

The URL Inspection API has a per-property daily quota, so we cannot check every
page on every run. Instead we keep an incrementally-refreshed cache
(config/index_cache.json, committed to the repo): each run inspects only a
limited number of the least-recently-checked pages, and the reported count is
computed from the whole cache.

Writes INDEXED_COUNT / INDEXED_KNOWN / INDEXED_TOTAL / GSC_ERRORS to
$GITHUB_ENV (or prints them locally). Skips silently if credentials are missing.
"""
import json
import os
import socket
import threading
import time
from pathlib import Path

socket.setdefaulttimeout(30)

BASE_URL = os.environ.get("SITE_BASE_URL", "https://pengjiangwen.github.io").rstrip("/")
SITE_URL = os.environ.get("GSC_SITE_URL", BASE_URL + "/").strip()
CREDS_JSON = os.environ.get("GSC_SERVICE_ACCOUNT_JSON", "").strip()
CACHE_PATH = Path(os.environ.get("GSC_CACHE", "config/index_cache.json"))
CHECK_LIMIT = int(os.environ.get("GSC_LIMIT", "150"))  # pages inspected per run
RATE_PER_SEC = float(os.environ.get("GSC_RATE", "8"))  # stay under 10/sec
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

_rate_lock = threading.Lock()
_next_slot = [0.0]


def _throttle():
    interval = 1.0 / RATE_PER_SEC
    with _rate_lock:
        now = time.monotonic()
        wait = _next_slot[0] - now
        if wait > 0:
            time.sleep(wait)
            now = time.monotonic()
        _next_slot[0] = max(now, _next_slot[0]) + interval


def article_urls():
    return [f"{BASE_URL}/{f.parent.name}/{f.stem}/" for f in sorted(Path("content").rglob("*.md"))]


def load_cache():
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache):
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=0, sort_keys=True) + "\n", encoding="utf-8")


def inspect_once(service, url):
    resp = (
        service.urlInspection()
        .index()
        .inspect(body={"inspectionUrl": url, "siteUrl": SITE_URL})
        .execute(num_retries=0)
    )
    state = (
        resp.get("inspectionResult", {})
        .get("indexStatusResult", {})
        .get("coverageState", "")
    )
    low = state.lower()
    return "indexed" in low and "not indexed" not in low


def main() -> None:
    cache = load_cache()

    if not CREDS_JSON:
        print("GSC_SERVICE_ACCOUNT_JSON not set, reporting cached count only.")
        report(cache)
        return

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
    except ImportError as exc:
        print(f"GSC libraries not installed ({exc}).")
        report(cache)
        return

    creds = service_account.Credentials.from_service_account_info(json.loads(CREDS_JSON), scopes=SCOPES)
    service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)

    urls = article_urls()
    today = time.strftime("%Y-%m-%d")
    # Never-checked pages first, then those checked longest ago.
    ordered = sorted(urls, key=lambda u: (cache.get(u, {}).get("d", ""), cache.get(u, {}).get("d") is not None))
    todo = ordered[:CHECK_LIMIT]

    checked = 0
    errors = []
    for url in todo:
        _throttle()
        try:
            indexed = inspect_once(service, url)
            cache[url] = {"i": 1 if indexed else 0, "d": today}
            checked += 1
        except HttpError as exc:
            status = getattr(getattr(exc, "resp", None), "status", None)
            msg = " ".join(str(exc).split())[:180]
            if msg not in errors:
                errors.append(msg)
            if status == 429:
                print("Quota exhausted (429) - stopping this run.")
                break
        except Exception as exc:
            msg = " ".join(str(exc).split())[:180]
            if msg not in errors:
                errors.append(msg)

    # Drop cache entries for pages that no longer exist.
    valid = set(urls)
    cache = {u: e for u, e in cache.items() if u in valid}
    save_cache(cache)

    print(f"Inspected {checked} pages this run | cache size {len(cache)}/{len(urls)}")
    if errors:
        print("Sample errors:", errors[:3])
    report(cache, errors)


def report(cache, errors=None):
    indexed = sum(1 for e in cache.values() if e.get("i") == 1)
    known = len(cache)
    total = len(article_urls())
    print(f"Indexed (from cache): {indexed} of {known} checked")
    if "GITHUB_ENV" in os.environ:
        with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as fh:
            fh.write(f"INDEXED_COUNT={indexed}\n")
            fh.write(f"INDEXED_KNOWN={known}\n")
            fh.write(f"INDEXED_TOTAL={total}\n")
            fh.write(f"GSC_ERRORS={' || '.join((errors or [])[:2])}\n")
    else:
        print(f"INDEXED_COUNT={indexed} INDEXED_KNOWN={known} INDEXED_TOTAL={total}")


if __name__ == "__main__":
    main()
