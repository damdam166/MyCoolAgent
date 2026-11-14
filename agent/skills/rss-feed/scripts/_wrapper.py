#!/home/node/.pi/agent/skills/rss-feed/.venv/bin/python3
"""
_wrapper.py – A simple wrapper over `miniflux.Client` that should not
be called directly.
It is not even a good wrapper btw. Don't look there too much.
"""

import json
import os
import sys

try:
    import miniflux
except ImportError:
    sys.exit(
        "Missing dependency: miniflux\n"
        "Install with: $PI_AGENT_DIR/skills/rss-feed/.venv/bin/pip install miniflux"
    )

RSS_FILE = os.path.join(
    os.getenv("PI_AGENT_DIR", os.path.expanduser("~/.pi/agent")),
    "rss.json",
)


def load_from_file(path: str, key: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read().strip()
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            if key in data:
                return data[key]
            else:
                raise ValueError(f"{key} not found in the file {path}")
        if isinstance(data, str):
            return data
    except json.JSONDecodeError:
        pass
    return raw


def WrapperClient() -> miniflux.Client:
    if not os.path.exists(RSS_FILE):
        sys.exit(f"RSS file not found: {RSS_FILE}")

    base_url = load_from_file(RSS_FILE, "url")
    token = load_from_file(RSS_FILE, "token")
    client = miniflux.Client(base_url, api_key=token)

    return client


if __name__ == "__main__":
    client = WrapperClient()
    print(client.get_feeds())
