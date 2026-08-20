#!/usr/bin/env python3
"""Submit URLs to the IndexNow API (Bing, Yandex, Naver, Seznam, and other
participating search engines) so they crawl new or changed pages immediately
instead of waiting for their next scheduled crawl.

Usage:
    python3 indexnow_submit.py --host example.com --key YOUR_KEY \
        https://example.com/page-1/ https://example.com/page-2/

    # or read URLs from a file, one per line
    python3 indexnow_submit.py --host example.com --key YOUR_KEY --file urls.txt

The key must match a verification file publicly reachable at
https://<host>/<key>.txt containing the key itself. See
https://www.indexnow.org/documentation for details.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
MAX_URLS_PER_REQUEST = 10000


def submit(host: str, key: str, urls: list[str], key_location: str | None = None) -> int:
    """Submit a batch of URLs to IndexNow. Returns the HTTP status code."""
    if not urls:
        raise ValueError("no URLs to submit")
    if len(urls) > MAX_URLS_PER_REQUEST:
        raise ValueError(f"IndexNow accepts at most {MAX_URLS_PER_REQUEST} URLs per request")

    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location or f"https://{host}/{key}.txt",
        "urlList": urls,
    }
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        print(f"IndexNow returned {e.code}: {e.read().decode()}", file=sys.stderr)
        return e.code


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("urls", nargs="*", help="URLs to submit")
    parser.add_argument("--host", required=True, help="Your site's host, e.g. example.com")
    parser.add_argument("--key", required=True, help="Your IndexNow key")
    parser.add_argument("--key-location", help="Override the default key file URL")
    parser.add_argument("--file", help="Read URLs from a file, one per line")
    args = parser.parse_args()

    urls = list(args.urls)
    if args.file:
        with open(args.file) as f:
            urls += [line.strip() for line in f if line.strip()]

    if not urls:
        parser.error("provide URLs as arguments or with --file")

    status = submit(args.host, args.key, urls, args.key_location)
    if status == 200:
        print(f"Submitted {len(urls)} URL(s) successfully.")
    elif status == 202:
        print(f"Submitted {len(urls)} URL(s), accepted for processing.")
    else:
        print(f"Submission finished with status {status}.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
