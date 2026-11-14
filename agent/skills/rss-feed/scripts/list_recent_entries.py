#!/home/node/.pi/agent/skills/rss-feed/.venv/bin/python3
"""
list_recent_entries.py – List Miniflux entries newer than a specified period.

Usage:
    python scripts/list_recent_entries.py --hours N

* ``--hours`` – consider only entries published in the last *N* hours (default: 24).
"""

import argparse

from _wrapper import WrapperClient

def main() -> None:
    parser = argparse.ArgumentParser(
        description="List entries newer than a given number of hours."
    )
    parser.add_argument("--hours", type=int, help="N hours since now", required=False, default=24)
    args = parser.parse_args()

    client = WrapperClient()

    # Pull a generous batch (max 100 per request – increase if needed).
    result = client.get_entries(limit=args.hours, direction="desc")
    entries = result.get("entries", [])

    print(
        f"Entries from the last {args.hours} hour(s):\n"
    )

    for entry in entries:
        eid = entry.get("id", "?")
        title = entry.get("title", "(no title)")
        url = entry.get("url", "")
        pub = entry.get("published_at", "")
        print(f"  {eid:>5} | {title[:60]:60} | {pub} | {url}")
        print()


if __name__ == "__main__":
    main()
