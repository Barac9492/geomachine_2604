#!/usr/bin/env python3
"""
Substack → VentureOracle cross-publisher.

Fetches the public RSS feed of a Substack publication, converts each post
to a Next.js-ready MDX file with proper frontmatter and schema.org JSON-LD,
and emits the files to a staging directory (or any path you specify).

The generated MDX files are designed to slot into the ventureoracle.kr
Next.js project with minimal wiring — YAML frontmatter for any standard
content loader (contentlayer, content-collections, hand-rolled), plus an
inline <script type="application/ld+json"> block with BlogPosting schema
that retrievers can see directly.

Usage:
  # Preview what would be generated without writing files
  python pilot/scripts/substack_to_ventureoracle.py --dry-run

  # Generate into content-drafts/substack-mirror/ (default)
  python pilot/scripts/substack_to_ventureoracle.py

  # Generate directly into your Next.js repo's content directory
  python pilot/scripts/substack_to_ventureoracle.py \\
      --target-dir ~/Content_VentureOracle/src/content/writings

  # Flip the canonical direction so ventureoracle.kr becomes authoritative.
  # WARNING: you must ALSO set the reverse canonical on each Substack post
  # in Substack's settings, otherwise Google sees duplicate content.
  python pilot/scripts/substack_to_ventureoracle.py --canonical=self

  # Regenerate files even if they already exist
  python pilot/scripts/substack_to_ventureoracle.py --force

Dependencies:
  pip install feedparser markdownify python-dateutil

Reads:
  - Substack RSS feed (defaults to https://ethancho12.substack.com/feed)
Writes:
  - <target-dir>/YYYY-MM-DD-slug.mdx  (one per post)
  - <target-dir>/MANIFEST.md          (summary table)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

try:
    import feedparser
    from markdownify import markdownify as html_to_md
    from dateutil import parser as dateparser
except ImportError:
    sys.exit(
        "Missing dependencies. Install first:\n"
        "  pip install feedparser markdownify python-dateutil"
    )

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_FEED = "https://ethancho12.substack.com/feed"
DEFAULT_TARGET = REPO_ROOT / "content-drafts" / "substack-mirror"
VENTUREORACLE_BASE = "https://www.ventureoracle.kr"

# Author metadata — used to build schema.org Person JSON-LD
AUTHOR_NAME = "Ethan Cho"
AUTHOR_KOREAN = "조여준"
AUTHOR_JOB_TITLE = "CIO at TheVentures"
AUTHOR_SAME_AS = [
    "https://www.ventureoracle.kr/about/ethan-cho",
    "https://ethancho12.substack.com/",
    # Add LinkedIn, Twitter/X, etc. here as they become known
]


@dataclass
class Post:
    title: str
    slug: str
    url: str
    date: datetime
    summary: str
    body_html: str
    body_markdown: str
    word_count: int
    language: str  # "en" or "ko"
    author: str


def detect_language(text: str) -> str:
    """Detect Korean vs English by character ratio. Crude but sufficient."""
    if not text:
        return "en"
    korean_chars = len(re.findall(r"[\uac00-\ud7af]", text))
    latin_chars = len(re.findall(r"[A-Za-z]", text))
    if korean_chars > latin_chars:
        return "ko"
    return "en"


def slugify(value: str) -> str:
    """Generate a URL-safe slug from a post title."""
    value = value.lower().strip()
    # Keep Korean chars as-is; they're fine in URLs
    value = re.sub(r"[^\w\s\-\uac00-\ud7af]", "", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")[:80] or "untitled"


def extract_slug_from_url(url: str) -> str:
    """Substack post URLs are https://<pub>.substack.com/p/<slug> — grab slug."""
    path = urlparse(url).path
    m = re.match(r"/p/([^/]+)", path)
    if m:
        return m.group(1)
    return slugify(path)


def fetch_feed(feed_url: str) -> list[Post]:
    """Fetch and parse the Substack RSS feed into Post objects."""
    print(f"Fetching {feed_url}…")
    parsed = feedparser.parse(feed_url)
    if parsed.bozo and not parsed.entries:
        raise RuntimeError(
            f"Failed to parse feed {feed_url}: {parsed.bozo_exception}"
        )
    if not parsed.entries:
        raise RuntimeError(
            f"Feed {feed_url} returned 0 entries. "
            "Verify the URL in a browser; Substack's feed is at <pub>.substack.com/feed"
        )

    posts: list[Post] = []
    for entry in parsed.entries:
        title = (entry.get("title") or "(untitled)").strip()
        url = entry.get("link") or ""
        slug = extract_slug_from_url(url) if url else slugify(title)

        # Publish date: try published_parsed, then updated_parsed, then string parse
        date: datetime
        if getattr(entry, "published_parsed", None):
            date = datetime(*entry.published_parsed[:6])
        elif getattr(entry, "updated_parsed", None):
            date = datetime(*entry.updated_parsed[:6])
        elif entry.get("published"):
            date = dateparser.parse(entry["published"])
        else:
            date = datetime.now()

        # Body: Substack RSS usually includes full HTML in content:encoded
        body_html = ""
        if entry.get("content"):
            body_html = entry.content[0].value if entry.content else ""
        if not body_html:
            body_html = entry.get("summary", "") or entry.get("description", "") or ""

        body_markdown = html_to_md(body_html, heading_style="ATX").strip() if body_html else ""

        summary = entry.get("summary", "") or ""
        # Strip HTML from summary for frontmatter
        summary_text = re.sub(r"<[^>]+>", "", summary).strip()
        if len(summary_text) > 300:
            summary_text = summary_text[:297] + "…"

        word_count = len(re.findall(r"\w+", body_markdown))
        language = detect_language(title + " " + body_markdown[:500])
        author = (entry.get("author") or AUTHOR_NAME).strip()

        posts.append(
            Post(
                title=title,
                slug=slug,
                url=url,
                date=date,
                summary=summary_text,
                body_html=body_html,
                body_markdown=body_markdown,
                word_count=word_count,
                language=language,
                author=author,
            )
        )

    posts.sort(key=lambda p: p.date, reverse=True)
    return posts


def build_jsonld(post: Post, canonical_url: str) -> dict:
    """Build schema.org BlogPosting JSON-LD for this post."""
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "datePublished": post.date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dateModified": post.date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "inLanguage": post.language,
        "description": post.summary,
        "wordCount": post.word_count,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical_url,
        },
        "author": {
            "@type": "Person",
            "name": AUTHOR_NAME,
            "alternateName": AUTHOR_KOREAN,
            "jobTitle": AUTHOR_JOB_TITLE,
            "url": f"{VENTUREORACLE_BASE}/about/ethan-cho",
            "sameAs": AUTHOR_SAME_AS,
        },
        "publisher": {
            "@type": "Organization",
            "name": "VentureOracle",
            "url": VENTUREORACLE_BASE,
        },
    }


def render_mdx(post: Post, canonical_mode: str) -> str:
    """Render one post as MDX with YAML frontmatter + JSON-LD + body."""
    vo_slug_path = f"/writings/{post.slug}"
    vo_full_url = f"{VENTUREORACLE_BASE}{vo_slug_path}"

    if canonical_mode == "substack":
        canonical_url = post.url
    else:
        canonical_url = vo_full_url

    jsonld = build_jsonld(post, canonical_url)
    jsonld_str = json.dumps(jsonld, ensure_ascii=False, indent=2)

    # YAML frontmatter — keys are common across Next.js content loaders
    description_value = json.dumps(post.summary, ensure_ascii=False) if post.summary else '""'
    fm_lines = [
        "---",
        f'title: {json.dumps(post.title, ensure_ascii=False)}',
        f"slug: {post.slug}",
        f'date: "{post.date.strftime("%Y-%m-%d")}"',
        f'author: "{AUTHOR_NAME}"',
        f"language: {post.language}",
        f"description: {description_value}",
        f'canonical: "{canonical_url}"',
        f"canonical_mode: {canonical_mode}",
        f'original_source: "substack"',
        f'original_url: "{post.url}"',
        f"word_count: {post.word_count}",
        "---",
        "",
    ]

    body_lines = [
        "{/* AUTO-GENERATED from Substack RSS. Do not edit this file directly;",
        "    re-run pilot/scripts/substack_to_ventureoracle.py to refresh. */}",
        "",
        "<script",
        '  type="application/ld+json"',
        "  dangerouslySetInnerHTML={{",
        f"    __html: `{jsonld_str}`",
        "  }}",
        "/>",
        "",
        f"# {post.title}",
        "",
    ]

    if canonical_mode == "substack":
        body_lines.extend(
            [
                f"> **This post was originally published on Substack.** "
                f"The canonical version lives at [{post.url}]({post.url}). "
                "This page mirrors the content for retrieval indexing.",
                "",
            ]
        )
    else:
        body_lines.extend(
            [
                f"> Also published on Substack: [{post.url}]({post.url})",
                "",
            ]
        )

    body_lines.append(post.body_markdown)
    body_lines.append("")

    return "\n".join(fm_lines + body_lines)


def render_manifest(posts: list[Post], canonical_mode: str, target_dir: Path) -> str:
    lines: list[str] = []
    lines.append("# Substack mirror manifest")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Source feed: `{DEFAULT_FEED}` (or whatever `--feed-url` was passed)")
    lines.append(f"Target: `{target_dir}`")
    lines.append(f"Canonical mode: **{canonical_mode}**")
    lines.append("")
    if canonical_mode == "substack":
        lines.append(
            "Canonical URL on each generated page points BACK to the Substack "
            "original. Google will treat Substack as authoritative. This is "
            "the safer default; it will not cause duplicate-content penalties."
        )
    else:
        lines.append(
            "⚠️ **Canonical mode is `self` — ventureoracle.kr pages claim "
            "authority.** You MUST also set each Substack post's canonical "
            "URL in Substack's post settings to match the ventureoracle URL "
            "below, or Google will see duplicate content on both surfaces "
            "and penalize both. Substack's canonical field is under Post "
            "Settings → SEO → Canonical URL."
        )
    lines.append("")
    lines.append("## Posts")
    lines.append("")
    lines.append("| Date | Title | Language | Words | Substack URL | VentureOracle slug |")
    lines.append("|---|---|---|---|---|---|")
    for p in posts:
        vo_slug = f"/writings/{p.slug}"
        title_short = p.title if len(p.title) <= 60 else p.title[:57] + "…"
        title_esc = title_short.replace("|", "\\|")
        lines.append(
            f"| {p.date.strftime('%Y-%m-%d')} "
            f"| {title_esc} "
            f"| {p.language} "
            f"| {p.word_count} "
            f"| [link]({p.url}) "
            f"| `{vo_slug}` |"
        )
    lines.append("")
    lines.append(f"**Total posts:** {len(posts)}")
    lines.append(f"**Total words:** {sum(p.word_count for p in posts):,}")
    lines.append("")

    # Integration notes
    lines.append("## Integration steps")
    lines.append("")
    lines.append(
        "1. Copy the generated `.mdx` files into the ventureoracle.kr Next.js "
        "project under `src/content/writings/` (or wherever your content loader "
        "reads from)."
    )
    lines.append(
        "2. Ensure your Next.js route for `/writings/[slug]` exists and renders "
        "the MDX. If you don't have a writings section yet, create:"
    )
    lines.append("")
    lines.append("   - `src/app/writings/page.tsx` — index page listing all posts")
    lines.append("   - `src/app/writings/[slug]/page.tsx` — single-post page")
    lines.append("")
    lines.append(
        "3. The JSON-LD `<script>` block at the top of each MDX is a React "
        "element — it will render into the page `<head>` automatically if your "
        "MDX is rendered inside a `<Head>` component, or inline if not. Either "
        "way Google's crawler picks it up."
    )
    lines.append(
        "4. Commit and push to the Next.js repo. Vercel auto-deploys."
    )
    lines.append(
        "5. After Vercel deploys, verify at least 3 of the generated pages "
        "respond 200 and contain the JSON-LD block. Then re-run "
        "`pilot/scripts/geo_audit.py` to confirm schema.org coverage picked up."
    )
    lines.append(
        "6. Wait 14–21 days for re-indexing, then run "
        "`pilot/scripts/geo_remeasure_diff.py` to score the gate."
    )
    lines.append("")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--feed-url", default=DEFAULT_FEED, help=f"Substack RSS URL (default: {DEFAULT_FEED})")
    p.add_argument("--target-dir", type=Path, default=DEFAULT_TARGET, help=f"Output directory (default: {DEFAULT_TARGET.relative_to(REPO_ROOT)})")
    p.add_argument("--canonical", choices=["substack", "self"], default="substack", help="Which URL claims authority (default: substack, safer)")
    p.add_argument("--force", action="store_true", help="Regenerate files that already exist")
    p.add_argument("--dry-run", action="store_true", help="Fetch + parse but don't write files")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    try:
        posts = fetch_feed(args.feed_url)
    except Exception as exc:
        sys.exit(f"ERROR fetching feed: {exc}")

    print(f"Fetched {len(posts)} posts")
    if not posts:
        sys.exit("No posts found — nothing to do.")

    args.target_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0
    errors = 0

    for p in posts:
        filename = f"{p.date.strftime('%Y-%m-%d')}-{p.slug}.mdx"
        out_path = args.target_dir / filename

        if out_path.exists() and not args.force:
            skipped += 1
            print(f"  skip  {filename}  (already exists, use --force to overwrite)")
            continue

        try:
            mdx = render_mdx(p, args.canonical)
        except Exception as exc:
            errors += 1
            print(f"  ERROR on {p.slug}: {exc}")
            continue

        if args.dry_run:
            print(f"  dry   {filename}  ({p.word_count} words, {p.language})")
        else:
            out_path.write_text(mdx, encoding="utf-8")
            print(f"  write {filename}  ({p.word_count} words, {p.language})")
        written += 1

    # Manifest
    manifest = render_manifest(posts, args.canonical, args.target_dir)
    manifest_path = args.target_dir / "MANIFEST.md"
    if not args.dry_run:
        manifest_path.write_text(manifest, encoding="utf-8")

    print()
    print(f"Written: {written}  Skipped: {skipped}  Errors: {errors}")
    if not args.dry_run:
        print(f"Files in: {args.target_dir}")
        print(f"Manifest: {manifest_path}")
    else:
        print("(dry-run — no files written)")


if __name__ == "__main__":
    main()
