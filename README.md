# indexnow-submit

A small, dependency-free Python script for submitting URLs to the
[IndexNow](https://www.indexnow.org/) API — the protocol Bing, Yandex,
Naver, Seznam.cz and other search engines use to crawl new or changed
pages within minutes instead of waiting for their next scheduled crawl.

We built this to push new pages on [fanpino.com](https://fanpino.com)
the moment they publish, and pulled it out as a standalone tool since
there wasn't a minimal, no-dependency version we could find.

## Usage

```bash
python3 indexnow_submit.py --host example.com --key YOUR_KEY \
    https://example.com/page-1/ https://example.com/page-2/

# or read URLs from a file, one per line
python3 indexnow_submit.py --host example.com --key YOUR_KEY --file urls.txt
```

Requires only the Python standard library — no `pip install` needed.

## Before you use it

1. Generate a key (any hex string works, e.g. `openssl rand -hex 16`).
2. Publish it at `https://<your-host>/<key>.txt`, containing just the key.
3. Run the script with that key.

See the [IndexNow documentation](https://www.indexnow.org/documentation)
for the full protocol spec.

## Why this matters

A sitemap tells a crawler what exists, but it still has to come back and
check it on its own schedule. IndexNow pushes a URL the moment it
changes. This matters more than it sounds — for example, ChatGPT's web
search runs on Bing's index, not Google's, so a page Bing hasn't seen
yet can't show up in a ChatGPT answer no matter how well it ranks on
Google.

## License

MIT — see [LICENSE](LICENSE).
