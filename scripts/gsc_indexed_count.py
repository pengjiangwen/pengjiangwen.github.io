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
import sys
import time
from pathlib import Path

BASE_URL = os.environ.get("SITE_BASE_URL", "https://pengjiangwen.github.io").rstrip("/")
SITE_URL = os.environ.get("GSC_SITE_URL", BASE_URL + "/").strip()
CREDS_JSON = os.environ.get("GSC_SERVICE_ACCOUNT_JSON", "").strip()

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


def article_urls():
    urls = []
    for f in sorted(Path("content").rglob("*.md")):
        urls.append(f"{BASE_URL}/{f.parent.name}/{f.stem}/")
    return urls


def main() -> None:
    if not CREDS_JSON:
        print("GSC_SERVICE_ACCOUNT_JSON not set, skipping index check.")
        return

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError as exc:
        print(f"GSC libraries not installed ({exc}), skipping index check.")
        return

    creds = service_account.Credentials.from_service_account_info(
        json.loads(CREDS_JSON), scopes=SCOPES
    )
    service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)

    urls = article_urls()
    indexed = 0
    checked = 0
    for url in urls:
        try:
            resp = (
                service.urlInspection()
                .index()
                .inspect(body={"inspectionUrl": url, "siteUrl": SITE_URL})
                .execute()
            )
            state = (
                resp.get("inspectionResult", {})
                .get("indexStatusResult", {})
                .get("coverageState", "")
            )
            checked += 1
            if "indexed" in state.lower() and "not indexed" not in state.lower():
                indexed += 1
        except Exception as exc:  # keep going; a few failures shouldn't abort
            print(f"  inspect failed for {url}: {exc}")
        time.sleep(0.12)  # stay well under the 600/min quota

    print(f"Checked {checked}/{len(urls)} pages, indexed: {indexed}")
    if "GITHUB_ENV" in os.environ:
        with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as fh:
            fh.write(f"INDEXED_COUNT={indexed}\n")
    else:
        print(f"INDEXED_COUNT={indexed}")


if __name__ == "__main__":
    main()
