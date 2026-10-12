#!/usr/bin/env python3
"""Send a DingTalk group-robot notification when a workflow step fails.

Reads DINGTALK_WEBHOOK and DINGTALK_SECRET from the environment.
Uses urllib (stdlib) so no extra dependencies are needed.
Silently skips (exit 0) if the webhook is not configured.
"""
import base64
import hashlib
import hmac
import json
import os
import time
import urllib.parse
import urllib.request

WEBHOOK = os.environ.get("DINGTALK_WEBHOOK", "").strip()
SECRET = os.environ.get("DINGTALK_SECRET", "").strip()
REPO = os.environ.get("GITHUB_REPOSITORY", "unknown/repo")
RUN_ID = os.environ.get("GITHUB_RUN_ID", "")
RUN_URL = f"https://github.com/{REPO}/actions/runs/{RUN_ID}"


def signed_url(webhook: str, secret: str) -> str:
    if not secret:
        return webhook
    timestamp = str(round(time.time() * 1000))
    string_to_sign = f"{timestamp}\n{secret}"
    digest = hmac.new(secret.encode("utf-8"), string_to_sign.encode("utf-8"), hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(digest))
    sep = "&" if "?" in webhook else "?"
    return f"{webhook}{sep}timestamp={timestamp}&sign={sign}"


def main() -> None:
    if not WEBHOOK:
        print("DINGTALK_WEBHOOK not set, skipping notification.")
        return
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "博客定时任务失败",
            "text": (
                "### ⚠️ 博客定时任务失败\n\n"
                "文章生成或网站部署出错，**网站可能未更新**。\n\n"
                f"[查看运行日志]({RUN_URL})"
            ),
        },
    }
    req = urllib.request.Request(
        signed_url(WEBHOOK, SECRET),
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            print("DingTalk response:", resp.read().decode("utf-8"))
    except Exception as exc:  # never fail the job because of a notification
        print(f"Failed to send DingTalk notification: {exc}")


if __name__ == "__main__":
    main()
