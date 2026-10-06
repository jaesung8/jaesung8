#!/usr/bin/env python3
"""Refresh only the marked README section from recent public GitHub events."""

import argparse
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

START = "<!--START_SECTION:activity-->"
END = "<!--END_SECTION:activity-->"
EMPTY = "No recent public PR, review, release, or code activity in GitHub's event window."


def markdown_text(value):
    """Keep API text on one line and prevent Markdown/HTML injection."""
    text = " ".join(str(value).split())[:120]
    text = html.escape(text, quote=True)
    return re.sub(r"([\\`*_{}\[\]()#+.!|>~-])", r"\\\1", text)


def public_link(value, repo):
    """Accept only GitHub links to the event's public repository."""
    if not isinstance(value, str):
        return None
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or parsed.netloc != "github.com"
            or not parsed.path.startswith(f"/{repo}/")):
        return None
    return quote(value, safe="/:#?=&%")


def render_activity(events, username, limit=5):
    excluded = {f"{username}/{username}".lower(), f"{username}/{username}.github.io".lower()}
    rows, seen = [], set()
    for event in events:
        if event.get("public") is False:
            continue
        repo = event.get("repo", {}).get("name", "")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) or repo.lower() in excluded:
            continue
        try:
            timestamp = datetime.fromisoformat(event["created_at"].replace("Z", "+00:00"))
            if timestamp.tzinfo is None:
                continue
            date = timestamp.astimezone(timezone.utc).date().isoformat()
        except (KeyError, TypeError, ValueError):
            continue
        payload = event.get("payload", {})
        kind = event.get("type")
        url, label = None, None
        if kind in {"PullRequestEvent", "PullRequestReviewEvent"}:
            pr = payload.get("pull_request", {})
            number = pr.get("number", payload.get("number"))
            if not isinstance(number, int) or isinstance(number, bool) or number < 1:
                continue
            url = f"https://github.com/{repo}/pull/{number}"
            if kind == "PullRequestReviewEvent" and payload.get("action") == "submitted":
                verb = "Reviewed"
                url = public_link(payload.get("review", {}).get("html_url"), repo) or url
            elif kind == "PullRequestEvent" and payload.get("action") in {"opened", "closed"}:
                verb = "Opened" if payload["action"] == "opened" else ("Merged" if pr.get("merged") else "Closed")
            else:
                continue
            title = f" — {markdown_text(pr['title'])}" if pr.get("title") else ""
            label = f"{verb} PR [{markdown_text(repo)} #{number}]({url}){title}"
        elif kind == "ReleaseEvent" and payload.get("action") == "published":
            release = payload.get("release", {})
            url = public_link(release.get("html_url"), repo)
            if url:
                name = release.get("name") or release.get("tag_name")
                suffix = f" — {markdown_text(name)}" if name else ""
                label = f"Published a release in [{markdown_text(repo)}]({url}){suffix}"
        elif kind == "PushEvent":
            head = payload.get("head", "")
            if isinstance(head, str) and re.fullmatch(r"[0-9a-fA-F]{40}", head):
                url = f"https://github.com/{repo}/commit/{head}"
            else:
                url = f"https://github.com/{repo}/commits"
            label = f"Pushed code to [{markdown_text(repo)}]({url})"
        if label and url not in seen:
            rows.append(f"- {date} (UTC) · {label}")
            seen.add(url)
            if len(rows) == limit:
                break
    return "\n".join(rows) if rows else EMPTY, len(rows)


def update_section(readme, content):
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain exactly one activity marker pair")
    start = readme.index(START) + len(START)
    end = readme.index(END)
    if start > end:
        raise ValueError("README activity markers are reversed")
    return readme[:start] + "\n" + content + "\n" + readme[end:]


def fetch_events(username):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-public-activity",
               "X-GitHub-Api-Version": "2022-11-28"}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/users/{username}/events/public?per_page=100", headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="jaesung8")
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    parser.add_argument("--events-file", type=Path, help="Read an offline public-event JSON fixture")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", args.username):
        parser.error("Invalid GitHub username")
    try:
        # Validate markers before making a request; preserve original newline bytes.
        original = args.readme.read_bytes().decode("utf-8")
        update_section(original, "")
        events = json.loads(args.events_file.read_text()) if args.events_file else fetch_events(args.username)
        if not isinstance(events, list) or not all(isinstance(event, dict) for event in events):
            raise ValueError("Expected a public-event JSON array")
        content, count = render_activity(events, args.username)
        updated = update_section(original, content)
        if updated != original:
            args.readme.write_bytes(updated.encode("utf-8"))
        print(f"Updated public activity: {count} events")
    except HTTPError as error:
        print(f"Public activity request failed (HTTP {error.code}); README unchanged", file=sys.stderr)
        return 1
    except URLError:
        print("Public activity request failed; README unchanged", file=sys.stderr)
        return 1
    except (OSError, ValueError) as error:
        print(f"Activity update failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
