#!/usr/bin/env python3
"""Send a DingTalk group-robot notification for the daily publishing run.

Reads from the environment:
  DINGTALK_WEBHOOK, DINGTALK_SECRET  - robot credentials (secret is optional)
  NOTIFY_STATUS                      - "success" or "failure" (default: failure)
  NEW_TITLES                         - newline-separated titles published this run
  TOTAL_ARTICLES                     - total article count on the site
  INDEXED_COUNT                      - Google-indexed page count (optional)
  RUN_URL                            - link to the workflow run

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
RUN_URL = os.environ.get("RUN_URL") or f"https://github.com/{REPO}/actions/runs/{RUN_ID}"


def signed_url(webhook: str, secret: str) -> str:
    if not secret:
        return webhook
    timestamp = str(round(time.time() * 1000))
    string_to_sign = f"{timestamp}\n{secret}"
    digest = hmac.new(secret.encode("utf-8"), string_to_sign.encode("utf-8"), hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(digest))
    sep = "&" if "?" in webhook else "?"
    return f"{webhook}{sep}timestamp={timestamp}&sign={sign}"


def build_message() -> dict:
    status = os.environ.get("NOTIFY_STATUS", "failure").lower()
    now = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time() + 8 * 3600))  # CST
    total = os.environ.get("TOTAL_ARTICLES", "?").strip()
    indexed = os.environ.get("INDEXED_COUNT", "").strip()
    failed = os.environ.get("INDEXED_FAILED", "").strip()
    items = [t.strip() for t in os.environ.get("NEW_ITEMS", "").split("\n") if t.strip()]

    if status == "success":
        lines = [
            "### ✅ 博客发布成功",
            "",
            f"**推送时间**：{now} (CST)",
            "**推送状态**：成功 ✅",
            f"**本次推送篇幅**：{len(items)} 篇",
        ]
        lines.extend(items)
        if not items:
            lines.append("- （本次无新文章）")
        lines.append("")
        lines.append(f"**网站文章总数**：{total} 篇")
        if indexed:
            suffix = f"（另有 {failed} 页查询失败）" if failed not in ("", "0") else ""
            lines.append(f"**Google 已收录**：{indexed} 页{suffix}")
        lines.append("")
        lines.append(f"[查看运行日志]({RUN_URL})")
    else:
        lines = [
            "### ⚠️ 博客定时任务失败",
            "",
            f"**推送时间**：{now} (CST)",
            "**推送状态**：失败 ❌",
            "",
            "文章生成或网站部署出错，**网站可能未更新**。",
            "",
            f"[查看运行日志]({RUN_URL})",
        ]

    reply = "✅ 博客发布成功" if status == "success" else "⚠️ 博客定时任务失败"
    return {
        "msgtype": "markdown",
        "markdown": {"title": reply, "text": "\n".join(lines)},
    }


def main() -> None:
    if not WEBHOOK:
        print("DINGTALK_WEBHOOK not set, skipping notification.")
        return
    req = urllib.request.Request(
        signed_url(WEBHOOK, SECRET),
        data=json.dumps(build_message(), ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            print("DingTalk response:", resp.read().decode("utf-8"))
    except Exception as exc:  # never fail the job because of a notification
        print(f"Failed to send DingTalk notification: {exc}")


if __name__ == "__main__":
    main()
