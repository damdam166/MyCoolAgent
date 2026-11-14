#!/home/node/.pi/agent/skills/rss-feed/.venv/bin/python3
"""
fetch_article.py – Fetch a specific Miniflux entry using the official Python client.

Requires: pip install miniflux

Usage:
    python fetch_article.py ENTRY_ID [--feed-id FEED_ID] [--save FILE]

Retrieves entry metadata (title, author, URL, published date) and prints the
full HTML content.
"""

import argparse
import sys
from _wrapper import WrapperClient

try:
    import miniflux
except ImportError:
    sys.exit("Missing dependency: miniflux\nInstall with: pip install miniflux")


def find_entry(client, entry_id: int) -> dict | None:
    """Locate an entry by id."""
    try:
        entry = client.get_entry(entry_id)
        return entry
    except miniflux.ClientError:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch a Miniflux article.")
    parser.add_argument("entry_id", type=int, help="Entry id to retrieve.")
    parser.add_argument(
        "--save", default=None, help="Save article body to FILE instead of printing."
    )
    args = parser.parse_args()

    client = WrapperClient()

    entry = find_entry(client, args.entry_id)
    if entry is None:
        sys.exit(f"Entry {args.entry_id} not found.")

    output = (
        f"Title: {entry.get('title', 'Untitled')}\n"
        f"Author: {entry.get('author', 'Unknown author')}\n"
        f"Published: {entry.get('published_at', '')}\n"
        f"URL: {entry.get('url', '')}\n\n"
        f"{entry.get('content', '')}\n"
    )

    if args.save:
        with open(args.save, "w", encoding="utf-8") as fh:
            fh.write(output)
        print(f"Saved article to {args.save}")
    else:
        print(output)


if __name__ == "__main__":
    main()
