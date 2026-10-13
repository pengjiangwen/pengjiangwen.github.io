#!/usr/bin/env python3
"""Count how many article pages Google has indexed, using the
Google Search Console URL Inspection API.

Requires a service account (JSON key) added as a user of the Search Console
property. The key is read from GSC_SERVICE_ACCOUNT_JSON.

The URL Inspection API is rate limited (~600 requests/minute), so requests are
paced by a global limiter (default 8/second) regardless of worker count, and
transient failures are retried with backoff.

Writes INDEXED_COUNT / INDEXED_FAILED / GSC_ERRORS to $GITHUB_ENV
(or prints them when run locally). Skips silently if credentials are missing.
"""
import json
import os
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

socket.setdefaulttimeout(30)

BASE_URL = os.environ.get("SITE_BASE_URL", "https://pengjiangwen.github.io").rstrip("/")
SITE_URL = os.environ.get("GSC_SITE_URL", BASE_URL + "/").strip()
CREDS_JSON = os.environ.get("GSC_SERVICE_ACCOUNT_JSON", "").strip()
MAX_WORKERS = int(os.environ.get("GSC_WORKERS", "8"))
RATE_PER_SEC = float(os.environ.get("GSC_RATE", "8"))  # must stay under 10/sec
MAX_RETRIES = int(os.environ.get("GSC_RETRIES", "3"))
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

_local = threading.local()
_CREDS = None
_ERRORS = []

_rate_lock = threading.Lock()
_next_slot = [0.0]


def _throttle():
    """Global limiter: keep at most RATE_PER_SEC request starts per second."""
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


def get_service():
    """One Search Console client per thread (service objects are not thread-safe)."""
    service = getattr(_local, "service", None)
    if service is None:
        from googleapiclient.discovery import build

        service = build("searchconsole", "v1", credentials=_CREDS, cache_discovery=False)
        _local.service = service
    return service


def inspect_once(url):
    resp = (
        get_service()
        .urlInspection()
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


def is_indexed(url):
    last_error = None
    for attempt in range(MAX_RETRIES):
        _throttle()
        try:
            return inspect_once(url)
        except Exception as exc:
            last_error = " ".join(str(exc).split())[:200]
            time.sleep(1.0 * (attempt + 1))
    if last_error and last_error not in _ERRORS and len(_ERRORS) < 5:
        _ERRORS.append(last_error)
    return None


def main() -> None:
    if not CREDS_JSON:
        print("GSC_SERVICE_ACCOUNT_JSON not set, skipping index check.")
        return

    try:
        from google.oauth2 import service_account
    except ImportError as exc:
        print(f"GSC libraries not installed ({exc}), skipping index check.")
        return

    global _CREDS
    _CREDS = service_account.Credentials.from_service_account_info(
        json.loads(CREDS_JSON), scopes=SCOPES
    )

    urls = article_urls()
    start = time.time()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        results = list(pool.map(is_indexed, urls))

    indexed = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is None)
    print(f"Checked {len(urls)} pages in {time.time() - start:.0f}s | indexed: {indexed} | failed: {failed}")
    if _ERRORS:
        print("Sample errors:", _ERRORS)

    if "GITHUB_ENV" in os.environ:
        with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as fh:
            fh.write(f"INDEXED_COUNT={indexed}\n")
            fh.write(f"INDEXED_FAILED={failed}\n")
            fh.write(f"GSC_ERRORS={' || '.join(_ERRORS)}\n")
    else:
        print(f"INDEXED_COUNT={indexed}")
        print(f"INDEXED_FAILED={failed}")


if __name__ == "__main__":
    main()
