"""GitHub stats widget — public API, no token required for basic stats."""
from __future__ import annotations
import json
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class GitHubStats:
    username: str
    repos: int
    followers: int
    following: int
    bio: str


def fetch_github(username: str, timeout: int = 5) -> Optional[GitHubStats]:
    """Fetch public GitHub profile stats. No auth needed."""
    if not username:
        return None
    url = f"https://api.github.com/users/{username}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "devdash/0.1",
        "Accept": "application/vnd.github.v3+json",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
    except Exception:
        return None

    return GitHubStats(
        username=data.get("login", username),
        repos=data.get("public_repos", 0),
        followers=data.get("followers", 0),
        following=data.get("following", 0),
        bio=data.get("bio") or "",
    )
