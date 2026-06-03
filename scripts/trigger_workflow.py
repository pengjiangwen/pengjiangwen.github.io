#!/usr/bin/env python3
"""Trigger Auto Generate Articles workflow via GitHub API."""
import json, os, subprocess, sys, urllib.request

REPO = "pengjiangwen/pengjiangwen.github.io"
WORKFLOW = "auto-articles.yml"


def get_token():
    token = os.environ.get("GH_TOKEN")
    if token:
        return token
    proc = subprocess.run(
        ["git", "credential-osxkeychain", "get"],
        input="protocol=https\nhost=github.com\n", capture_output=True, text=True, timeout=10,
    )
    for line in proc.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1]
    raise SystemExit("No GitHub token found")


def trigger():
    token = get_token()
    url = f"https://api.github.com/repos/{REPO}/actions/workflows/{WORKFLOW}/dispatches"
    data = json.dumps({"ref": "main"}).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"Triggered! Status: {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"Failed: {e.code} {e.read().decode()}")
        sys.exit(1)


if __name__ == "__main__":
    trigger()
