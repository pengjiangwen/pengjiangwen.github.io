#!/bin/bash
# Trigger Auto Generate Articles workflow via GitHub API
TOKEN=$(git credential-osxkeychain get <<< "protocol=https
host=github.com" 2>/dev/null | grep "^password=" | sed 's/^password=//')
curl -s -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/pengjiangwen/pengjiangwen.github.io/actions/workflows/auto-articles.yml/dispatches" \
  -d '{"ref":"main"}' && echo "Triggered!"
