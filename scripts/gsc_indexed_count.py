#!/usr/bin/env python3
"""Count how many article pages Google has indexed, using the
Google Search Console URL Inspection API.

Requires a service account (JSON key) that has been added as a user of the
Search Console property. The key is read from GSC_SERVICE_ACCOUNT_JSON.

Writes INDEXED_COUNT=<n> to $GITHUB_ENV (or prints it when run locally).
Silently skips (exit 0) if credentials are missing.
"""
import json
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASE_URL = os.environ.get("SITE_BASE_URL", "https://pengjiangwen.github.io").rstrip("/")
SITE_URL = os.environ.get("GSC_SITE_URL", BASE_URL + "/").strip()
CREDS_JSON = os.environ.get("GSC_SERVICE_ACCOUNT_JSON", "").strip()
MAX_WORKERS = int(os.environ.get("GSC_WORKERS", "10"))
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

_local = threading.local()
_CREDS = None


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


def is_indexed(url):
    try:
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
    except Exception:
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

    if "GITHUB_ENV" in os.environ:
        with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as fh:
            fh.write(f"INDEXED_COUNT={indexed}\n")
    else:
        print(f"INDEXED_COUNT={indexed}")


if __name__ == "__main__":
    main()
