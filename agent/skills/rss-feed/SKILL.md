---
name: "rss-feed"
description: "Retrieve RSS feeds from a Miniflux instance using the official Python client (miniflux) or curl/jq. The token is stored in $PI_AGENT_DIR/rss.json. Use to list feeds, get feed details, fetch headlines, or retrieve full article content."
version: 1
created: "2026-11-14"
updated: "2026-11-15"
---
## When to Use
When you need to list available feeds, retrieve feed details, or get headlines from your Miniflux instance. Example queries: \"List my feeds\", \"Show headlines from feed 5\", \"What are the latest items in feed X\".

## Procedure
### List feeds (Python, using official miniflux client)
1. Read the token from $PI_AGENT_DIR/rss.json (JSON or plain string).
Read the url from $PI_AGENT_DIR/rss.json (JSON or plain string).
2. Run the provided script:
   ```bash
   python scripts/list_feeds.py          # list all feeds
   python scripts/list_feeds.py --entries 42   # show latest 10 entries for feed 42
   ```

### Show headlines for a feed (Python)
   The same script with `--entries` prints the latest entries (id, title, URL).

### Fetch full article content (Python)
3. Run:
   ```bash
   python scripts/fetch_article.py 1234           # prints metadata + HTML content
   python scripts/fetch_article.py 1234 --save article.html   # save to file
   ```
   Optionally narrow the search with `--feed-id 42` if you know the feed.

### List all articles of a specific feed (Python)
4. Run:
   ```bash
   python scripts/list_feed_entries.py 42 [--limit 100]
   ```
   * `42` is the numeric feed id.
   * `--limit` (default 100) controls how many entries are fetched.

### List recent articles from a specific time span (Python)
5. Run:
   ```bash
   python scripts/list_recent_entries.py --hours 12
   ```
   * `--hours` (default 24) – only entries newer than *N* hours are shown.

### Fallback: curl / jq
If you prefer the raw API, the $URL variable comes from the `$PI_AGENT_DIR/rss.json` file:
- List feeds:
  `curl -s -H "X-Auth-Token: $TOKEN" https://$URL/v1/feeds | jq -r '.[] | "\(.id)\t\(.title)"'`
- Feed entries:
  `curl -s -H "X-Auth-Token: $TOKEN" https://$URL/v1/feeds/<feed_id>/entries?limit=10&direction=desc&order=published_at | jq -r '.entries[] | "\(.title)\n  \(.url)\n"'`

## Pitfalls
- Token file missing or unreadable
- Network connectivity or API downtime
- Rate limiting by Miniflux
- Changes in API response format breaking jq parsing
- jq not installed on the system
- `python` interpreter missing or `miniflux` package not installed (`pip install miniflux`)

## Verification
1. `python scripts/list_feeds.py` outputs a list of feed IDs and titles.
2. `python scripts/list_feeds.py --entries <feed_id>` prints entries for that feed.
3. `python scripts/fetch_article.py <entry_id>` prints title, author and HTML content.
4. `--save` writes a non‑empty file.
5. `python scripts/list_feed_entries.py <feed_id>` prints all entries for that feed.
6. `python scripts/list_recent_entries.py --hours <N>` prints only entries newer than *N* hours.

## Python scripts
- `scripts/list_feeds.py` – list feeds or show latest entries for a feed (uses `miniflux.Client.get_feeds` / `get_feed_entries`).
- `scripts/fetch_article.py` – fetch a single entry's metadata and full article content (uses `miniflux.Client.get_entries` / `get_feed_entries`).
- `scripts/list_feed_entries.py` – list all entries of a specific feed (uses `miniflux.Client.get_feed_entries`).
- `scripts/list_recent_entries.py` – list entries newer than a given time span (uses `miniflux.Client.get_feed_entries`).

## Requirements
The skill uses a virtual environment located at `$PI_AGENT_DIR/skills/rss-feed/.venv`.
Activate it (or invoke scripts with the shebang) and install the Miniflux client:

```bash
$PI_AGENT_DIR/skills/rss-feed/.venv/bin/pip install miniflux
```
