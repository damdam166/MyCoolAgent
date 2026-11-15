#!/usr/bin/env python3
"""
list_feeds.py – List feeds from a Miniflux instance using the official Python client.

Requires: pip install miniflux

Usage:
    python list_feeds.py [--entries FEED_ID]

Without arguments, prints all feeds (id + title).
With --entries <feed_id>, prints the latest entries for that feed.
"""

import argparse
from _wrapper import WrapperClient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--entries",
        type=int,
        metavar="FEED_ID",
        help="Show latest entries for this feed id",
    )
    parser.add_argument(
        "--limit", type=int, default=10, help="Max entries to show (default: 10)"
    )
    args = parser.parse_args()

    client = WrapperClient()

    if args.entries is not None:
        entries = client.get_feed_entries(
            args.entries,
            direction="desc",
            order="published_at",
            limit=args.limit,
        )
        for entry in entries["entries"]:
            print(f"{entry['id']}\t{entry['title']}")
            print(f"  {entry['url']}\n")
        return

    feeds = client.get_feeds()
    for feed in feeds:
        print(f"{feed['id']}\t{feed['title']}")


if __name__ == "__main__":
    main()
