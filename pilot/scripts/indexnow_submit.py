"""Submit ventureoracle.kr sitemap URLs to IndexNow.

Pings Bing, Yandex, Seznam, and Brave crawlers to re-index changes.
Run on demand after major content pushes or when discoverability is stalling.
"""
from __future__ import annotations

import json
import sys
import urllib.request
import xml.etree.ElementTree as ET

HOST = "www.ventureoracle.kr"
KEY = "7f90e7115e5c45e4bc09ddfd48f937df"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
SITEMAP_URL = f"https://{HOST}/sitemap.xml"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"


def fetch_sitemap_urls() -> list[str]:
    with urllib.request.urlopen(SITEMAP_URL, timeout=30) as resp:
        xml = resp.read()
    root = ET.fromstring(xml)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text.strip() for loc in root.findall(".//sm:loc", ns) if loc.text]


def submit(urls: list[str]) -> tuple[int, str]:
    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }).encode()
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, resp.read().decode("utf-8", "replace")


def main() -> int:
    urls = fetch_sitemap_urls()
    print(f"Sitemap URLs: {len(urls)}")
    for u in urls[:5]:
        print(f"  {u}")
    if len(urls) > 5:
        print(f"  … ({len(urls) - 5} more)")

    # IndexNow accepts up to 10,000 URLs per call.
    status, body = submit(urls)
    print(f"IndexNow response: HTTP {status}")
    if body:
        print(body)
    # 200 = accepted, 202 = accepted, 422 = URLs mismatch host key
    return 0 if status in (200, 202) else 1


if __name__ == "__main__":
    sys.exit(main())
