#!/usr/bin/env python3
"""
list_feed_entries.py – List every entry of a given Miniflux feed.

Usage:
    python scripts/list_feed_entries.py <feed_id> [--limit N]

* ``feed_id`` – numeric ID of the feed you want to query.
* ``--limit`` – maximum number of entries to return (default: 100, max ≈ 10 000).
"""

import argparse
from _wrapper import WrapperClient


def main() -> None:
    parser = argparse.ArgumentParser(description="List all entries of a Miniflux feed.")
    parser.add_argument("feed_id", type=int, help="Feed ID to query")
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of entries to return (default: 100).",
    )
    args = parser.parse_args()

    client = WrapperClient()

    result = client.get_feed_entries(args.feed_id, limit=args.limit)
    entries = result.get("entries", [])
    total = result.get("total", len(entries))

    print(f"Feed #{args.feed_id} – showing {len(entries)} of {total} entries:\n")

    for entry in entries:
        eid = entry.get("id", "?")
        title = entry.get("title", "(no title)")
        url = entry.get("url", "")
        pub = entry.get("published_at", "")
        print(f"  {eid:>5} | {title[:60]:60} | {pub} | {url}")
        print()


if __name__ == "__main__":
    main()
