#!/usr/bin/env python3
"""
Substack → VentureOracle articles.ts sync script

Purpose
-------
Ethan's ventureoracle.kr Next.js site stores articles as a TypeScript
`Article[]` array in `app/data/articles.ts` (NOT as MDX files). This script:

1. Fetches posts from ethancho12.substack.com (RSS)
2. Reads the current app/data/articles.ts to find existing articles
3. Matches substack posts to existing articles by fuzzy title
4. Emits a TypeScript patch:
   - For existing matches: suggested canonical URL updates (root → per-post)
   - For new posts: full `Article` object ready to append to the array

The script does NOT write to the live Next.js repo. It stages output in
`content-drafts/substack-mirror/` for human review before porting.

Why a separate script from substack_to_ventureoracle.py:
The original script emits MDX files which is the wrong format for this
codebase. VentureOracle is content-as-code, not markdown-first. This script
respects that architecture.

Usage
-----
  # Typical usage — reads the live articles.ts, emits TS patch
  ~/Content_VentureOracle/.venv/bin/python pilot/scripts/substack_to_articles_ts.py

  # Specify a different articles.ts source
  python pilot/scripts/substack_to_articles_ts.py \\
      --articles-source /path/to/app/data/articles.ts

  # Dry run — show what would be generated without writing anything
  python pilot/scripts/substack_to_articles_ts.py --dry-run

Requires: feedparser, markdownify, python-dateutil
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

try:
    import feedparser
    from markdownify import markdownify as md
except ImportError as e:
    sys.exit(
        f"Missing dependency: {e.name}. Install with:\n"
        f"  ~/Content_VentureOracle/.venv/bin/pip install feedparser markdownify python-dateutil"
    )

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_ARTICLES_SOURCE = Path("/Users/yeojooncho/clawd/ventureoracle-site/app/data/articles.ts")
DEFAULT_OUTPUT_DIR = REPO_ROOT / "content-drafts" / "substack-mirror"

SUBSTACK_FEED = "https://ethancho12.substack.com/feed"

# Hand-curated overrides for posts where the auto-generator falls short.
# Keyed by substack post URL path (the slug substack gave us), NOT our
# generated slug. Lets us:
#   - give Korean-only titles a proper English title + SEO slug
#   - hand-polish excerpts that the first-paragraph extractor mangled
#   - force categories when the inferrer guesses wrong
# Everything here is editorial; revisit when substack adds/removes posts.
#
# Integration rule: a substack URL ending in /p/<TAIL> matches OVERRIDES[TAIL].
OVERRIDES: dict[str, dict[str, str]] = {
    # 신화가 도착하면 죽는 것들 (2026-04-08)
    "43f": {
        "title": "When the Myth Arrives, Something Dies",
        "slug": "when-myth-arrives-something-dies",
        "category": "Hot Takes",
    },
    # 카카오의 "선택과 집중"은 다각화 실패를 예쁘게 쓴 말이다 (2026-04-02)
    "5ab": {
        "title": "Kakao's 'Focus and Choice' Is a Polite Name for Diversification Failure",
        "slug": "kakao-focus-diversification-failure",
        "category": "Market Analysis",
    },
    # 우리 코드는 안전한데 우리는 불안전해요 (2026-04-01)
    "dae": {
        "title": "The Code Is Safe. We Are Not.",
        "slug": "code-safe-we-are-not",
        "category": "AI Investing",
    },
    # 한국이 AI를 가장 잘 쓰고도 결국 패배할 수도 있는 이유 (2026-03-26)
    "ai-d53": {
        "title": "Why Korea May Lose the AI Race Even While Using AI Best",
        "slug": "why-korea-may-lose-ai-race-while-using-ai-best",
        "category": "Korea VC",
    },
    # Google이 꿈꾸는 세계 (2026-03-14)
    "google": {
        "title": "The World Google Is Dreaming Of",
        "slug": "world-google-is-dreaming-of",
        "category": "AI Investing",
    },
    # 사장님이 이 글을 싫어합니다 (2026-02-20)
    "0fe": {
        "title": "Your Boss Will Hate This Post",
        "slug": "your-boss-will-hate-this-post",
        "category": "Operator Insights",
    },
    # 분노는 공짜가 아니다 (2026-02-18)
    "dfe": {
        "title": "Anger Is Not Free",
        "slug": "anger-is-not-free",
        "category": "Operator Insights",
    },
    # 20와트의 천재, 1000와트의 바보 (2026-02-16)
    "20-1000": {
        "title": "The 20-Watt Genius and the 1000-Watt Fool",
        "slug": "20-watt-genius-1000-watt-fool",
        "category": "Decision Frameworks",
    },
    # 쇠사슬, 부채, 알고리즘 (2026-02-15)
    "b0d": {
        "title": "Chains, Debt, Algorithms",
        "slug": "chains-debt-algorithms",
        "category": "Market Analysis",
    },
    # 루센트블록이 진짜 보여준 것 (2026-02-13)
    "a6b": {
        "title": "What Lucent Block Actually Revealed",
        "slug": "what-lucent-block-actually-revealed",
        "category": "Market Analysis",
    },
    # /p/167 is "[애당초 너두] 투자 피치덱 검토하는 웹사이트 만들기"
    # — the Korean version of the existing AI Native VC Pitch Deck article.
    # Matched by exact canonical URL, so this override is only used if
    # the existing article ever gets removed. Keep a sensible title anyway.
    "167": {
        "title": "Building an AI Pitch Deck Review Website (Korean Original)",
        "slug": "ai-pitch-deck-review-korean-original",
        "category": "Building",
    },
    # VentureOracle #001: 한국의 석유 상황 (2026-04-12)
    # First issue of the VentureOracle prediction series (oil / Hormuz lag).
    "ventureoracle-001": {
        "title": "VentureOracle #001: The Hormuz Oil Lag",
        "slug": "ventureoracle-001-hormuz-oil-lag",
        "category": "Predictions",
    },
    # 호르무즈에서 가장 겁에 질린 두 사람은 테헤란에 없다 (2026-04-12/13)
    # Follow-up to VentureOracle #001 — Hormuz crisis geopolitical analysis.
    "5de": {
        "title": "The Two Most Frightened People at Hormuz Are Not in Tehran",
        "slug": "hormuz-frightened-not-in-tehran",
        "category": "Predictions",
    },
}

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "should", "could", "may", "might", "must", "shall", "can",
    "need", "dare", "ought", "used", "to", "of", "in", "for", "on", "with",
    "as", "at", "by", "from", "up", "about", "into", "through", "during",
    "before", "after", "above", "below", "between", "under", "over", "this",
    "that", "these", "those", "your", "you", "our", "we", "what", "which",
    "who", "whom", "whose", "why", "how", "it", "its", "they", "them",
    "there", "here",
}


@dataclass
class ExistingArticle:
    slug: str
    title: str
    title_ko: str = ""
    canonical_url: str = ""
    word_count: int = 0
    raw_block: str = ""  # for reference/debugging


@dataclass
class SubstackPost:
    title: str
    url: str
    published: datetime
    html: str
    markdown: str = ""
    word_count: int = 0
    language: str = "en"
    excerpt: str = ""
    slug: str = ""
    matched_existing: ExistingArticle | None = None
    match_reason: str = ""


# ---------- articles.ts parsing ----------

# Match individual article objects: `{` at indent 2, then fields, up to matching `}`
ARTICLE_BLOCK_RE = re.compile(
    r"(?ms)^  \{\n(?P<body>.*?)^  \},?\n",
    re.MULTILINE,
)
FIELD_RE = re.compile(r'^\s*(\w+):\s*(.+?)(?:,|$)', re.MULTILINE)


def parse_articles_ts(path: Path) -> list[ExistingArticle]:
    """Best-effort parser for the existing articles.ts. Extracts slug, title,
    titleKo, canonicalUrl, wordCount from each article object.
    """
    if not path.exists():
        return []
    source = path.read_text(encoding="utf-8")

    # Strip interface block
    after_array = source.find("export const articles")
    if after_array == -1:
        return []
    source = source[after_array:]

    articles: list[ExistingArticle] = []
    for match in ARTICLE_BLOCK_RE.finditer(source):
        body = match.group("body")
        article = ExistingArticle(slug="", title="", raw_block=body)
        for field_match in FIELD_RE.finditer(body):
            key = field_match.group(1)
            raw_value = field_match.group(2).rstrip(",").strip()
            # Strip surrounding quotes (single or double)
            if (raw_value.startswith('"') and raw_value.endswith('"')) or (
                raw_value.startswith("'") and raw_value.endswith("'")
            ):
                raw_value = raw_value[1:-1]
            if key == "slug":
                article.slug = raw_value
            elif key == "title":
                article.title = raw_value
            elif key == "titleKo":
                article.title_ko = raw_value
            elif key in ("canonicalUrl", "substackUrl"):
                # Schema has renamed this field back and forth between origin
                # and work-in-progress branches. Treat both field names as the
                # same semantic "per-post substack URL" signal.
                article.canonical_url = raw_value
            elif key == "wordCount":
                try:
                    article.word_count = int(raw_value)
                except ValueError:
                    pass
        if article.slug:  # only keep blocks that have a real slug
            articles.append(article)
    return articles


# ---------- title matching ----------

def tokenize(text: str) -> set[str]:
    """Lowercased content words, dropping stopwords and anything <3 chars."""
    if not text:
        return set()
    words = re.findall(r"[\w']+", text.lower())
    return {w for w in words if len(w) >= 3 and w not in STOPWORDS}


def match_score(substack_title: str, existing: ExistingArticle) -> float:
    """Jaccard overlap between substack post title and the existing article's
    title (or titleKo). Max over both."""
    sub_tokens = tokenize(substack_title)
    if not sub_tokens:
        return 0.0
    scores = []
    for candidate in (existing.title, existing.title_ko):
        cand_tokens = tokenize(candidate)
        if not cand_tokens:
            continue
        union = sub_tokens | cand_tokens
        if not union:
            continue
        scores.append(len(sub_tokens & cand_tokens) / len(union))
    return max(scores, default=0.0)


def find_best_match(post: SubstackPost, existing: list[ExistingArticle]) -> tuple[ExistingArticle | None, float, str]:
    """Match a substack post to an existing article. Returns
    (article, score, match_reason) where score is either 1.0 for an exact
    canonical URL match or a Jaccard score for a fuzzy title match.
    """
    # Exact canonical URL match first — if any existing article already has
    # this post's URL as its canonical, it IS this post. No fuzzy fallback
    # needed, no risk of duplicate.
    for art in existing:
        if art.canonical_url and art.canonical_url == post.url:
            return art, 1.0, "exact canonical URL match"

    # Fuzzy title match fallback
    best: ExistingArticle | None = None
    best_score = 0.0
    for art in existing:
        score = match_score(post.title, art)
        if score > best_score:
            best = art
            best_score = score
    return best, best_score, f"fuzzy title match ({best_score:.2f})"


def is_substack_canonical(url: str) -> bool:
    """Does this canonical URL point at substack? (Root or per-post)"""
    return "substack.com" in url


# ---------- substack fetch + transform ----------

def detect_language(text: str) -> str:
    """Crude Korean vs English detector: if > 20% Hangul code points, call it Korean."""
    if not text:
        return "en"
    total = 0
    hangul = 0
    for ch in text:
        if ch.isalpha() or 0xAC00 <= ord(ch) <= 0xD7A3:
            total += 1
            if 0xAC00 <= ord(ch) <= 0xD7A3:
                hangul += 1
    if total == 0:
        return "en"
    return "ko" if hangul / total > 0.2 else "en"


def clean_slug(text: str, fallback: str) -> str:
    """Generate an SEO-friendly slug from title. Falls back to the substack
    URL tail for non-romanizable titles (Korean, Chinese, etc.)."""
    if not text:
        return fallback
    slug = text.lower()
    # Keep ONLY ASCII word chars + spaces + hyphens. This drops Hangul,
    # Hanzi, emoji, quotes, etc. — producing an ASCII slug or nothing.
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    # Require at least 4 chars AND at least one letter to be a valid slug.
    # Otherwise (Korean-only title, or numeric-only), use the substack URL tail.
    if len(slug) < 4 or not re.search(r"[a-z]", slug):
        return fallback
    return slug[:60]


def compute_excerpt(markdown: str, min_length: int = 80, max_length: int = 250) -> str:
    """Extract a clean excerpt from markdown content, skipping images,
    blockquotes, headings, and other formatting. Takes enough paragraphs
    to reach min_length, truncates at max_length on a word boundary."""
    text = markdown
    # Strip markdown images (including linked images and empty-alt images)
    text = re.sub(r"\[!\[.*?\]\(.*?\)\]\(.*?\)", "", text)  # linked images
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)  # regular images
    text = re.sub(r"\[\]\([^)]+\)", "", text)  # empty-alt images
    # Strip blockquote markers
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
    # Strip headings
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    # Strip bold/italic/code markers
    text = re.sub(r"[*_`]+", "", text)
    # Strip links but keep text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Strip horizontal rules
    text = re.sub(r"^---+$", "", text, flags=re.MULTILINE)
    # Collapse whitespace
    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"  +", " ", text)
    # Find substantive paragraphs (>15 chars, not just whitespace)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip() and len(p.strip()) > 15]
    if not paragraphs:
        return ""
    # Take paragraphs until we reach min_length
    result = ""
    for p in paragraphs[:4]:
        if len(result) >= min_length:
            break
        if result:
            result += " "
        result += p
    # Truncate at word boundary if too long
    if len(result) > max_length:
        result = result[:max_length].rsplit(" ", 1)[0] + "…"
    # Clean up any remaining formatting artifacts
    result = result.replace("\\n", " ")
    result = re.sub(r"\s+", " ", result).strip()
    return result


def format_date(dt: datetime) -> str:
    """Match the existing articles.ts format: 'Feb 19, 2026'"""
    return dt.strftime("%b %d, %Y").replace(" 0", " ")


def word_count(markdown: str) -> int:
    text = re.sub(r"[^\w\s]", " ", markdown)
    return len([w for w in text.split() if w])


def read_time(wc: int) -> str:
    minutes = max(1, round(wc / 200))
    return f"{minutes} min"


def fetch_substack_posts(feed_url: str) -> list[SubstackPost]:
    parsed = feedparser.parse(feed_url)
    posts: list[SubstackPost] = []
    for entry in parsed.entries:
        title = entry.get("title", "").strip()
        url = entry.get("link", "").strip()
        published_raw = entry.get("published_parsed") or entry.get("updated_parsed")
        if published_raw:
            published = datetime(*published_raw[:6])
        else:
            published = datetime.now()
        # Prefer content:encoded over summary
        html = ""
        if "content" in entry and entry.content:
            html = entry.content[0].get("value", "")
        if not html:
            html = entry.get("summary", "")
        markdown_body = md(html, heading_style="ATX", strip=["script", "style"]).strip()
        # Strip Substack CDN image transformation tokens ($s_!XXXX!,) that
        # break when served from a non-substack domain. The URLs work fine
        # without these tokens — they're optimization hints for the substack
        # delivery context only.
        markdown_body = re.sub(r'\$s_![^,]*!,', '', markdown_body)
        lang = detect_language(title + " " + markdown_body[:500])
        url_tail = urlparse(url).path.strip("/").split("/")[-1] or "post"

        # Apply OVERRIDES for hand-curated Korean titles + slugs
        override = OVERRIDES.get(url_tail, {})
        if override.get("title"):
            # Force Korean language so titleKo preserves the original
            lang = "ko"
            display_title = override["title"]
            slug = override.get("slug") or clean_slug(display_title, url_tail)
        else:
            display_title = title
            slug = clean_slug(title, url_tail)

        post = SubstackPost(
            title=display_title,
            url=url,
            published=published,
            html=html,
            markdown=markdown_body,
            word_count=word_count(markdown_body),
            language=lang,
            excerpt=compute_excerpt(markdown_body),
            slug=slug,
        )
        # Stash the original title on a dynamic attribute so emitters can use
        # it for titleKo without needing a new dataclass field.
        post_original_title = title  # noqa: F841 — captured in closure below
        post._original_title = title  # type: ignore[attr-defined]
        post._override_category = override.get("category", "")  # type: ignore[attr-defined]
        posts.append(post)
    posts.sort(key=lambda p: p.published, reverse=True)
    return posts


# ---------- TypeScript emission ----------

def ts_string(s: str) -> str:
    """Escape a string for TypeScript double-quoted literal."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def ts_template_string(s: str) -> str:
    """Escape a string for TypeScript backtick template literal."""
    return "`" + s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${") + "`"


def ts_string_array(items: list[str]) -> str:
    inside = ", ".join(ts_string(i) for i in items)
    return f"[{inside}]"


def default_keywords(post: SubstackPost) -> list[str]:
    """Baseline keywords every new article should include."""
    base = ["Ethan Cho", "TheVentures", "ventureoracle"]
    title_tokens = [t for t in tokenize(post.title) if len(t) > 4]
    merged = base + title_tokens[:8]
    # Dedup preserving order
    seen = set()
    result = []
    for kw in merged:
        if kw not in seen:
            seen.add(kw)
            result.append(kw)
    return result[:12]


def infer_category(post: SubstackPost) -> str:
    """Map title/body keywords to one of the existing categories."""
    text = (post.title + " " + post.markdown[:500]).lower()
    rules = [
        (["korea", "korean", "seoul", "한국"], "Korea VC"),
        (["ai", "llm", "gpt", "claude"], "AI Investing"),
        (["optimism", "tax", "framework"], "Decision Frameworks"),
        (["predict", "prediction"], "Predictions"),
        (["build", "building", "operator"], "Operator Insights"),
        (["market", "valuation", "bond", "credit"], "Market Analysis"),
        (["hot", "rant", "controversial"], "Hot Takes"),
    ]
    for keywords, category in rules:
        if any(k in text for k in keywords):
            return category
    return "Insights"


def emit_article_object(post: SubstackPost, indent: str = "  ") -> str:
    """Emit a TypeScript Article object for a new substack post."""
    lines = [indent + "{"]
    original = getattr(post, "_original_title", post.title)
    override_cat = getattr(post, "_override_category", "")

    title = post.title
    title_ko = ""
    # Only treat as Korean-titled if the ORIGINAL title actually contains
    # Hangul characters. Posts with an English-language title but Korean
    # body shouldn't get the `[Korean]` prefix or a duplicate titleKo.
    has_hangul = any(0xAC00 <= ord(ch) <= 0xD7A3 for ch in original)
    if post.language == "ko" and has_hangul:
        # titleKo holds the original Korean title; title holds either the
        # hand-curated English title (from OVERRIDES) or a [Korean] prefixed
        # fallback for the card grid.
        title_ko = original
        if title == original:  # no override applied
            title = f"[Korean] {original}"

    category = override_cat or infer_category(post)

    lines.append(f'{indent}  title: {ts_string(title)},')
    if title_ko:
        lines.append(f'{indent}  titleKo: {ts_string(title_ko)},')
    lines.append(f'{indent}  excerpt: {ts_string(post.excerpt)},')
    lines.append(f'{indent}  date: {ts_string(format_date(post.published))},')
    lines.append(f'{indent}  category: {ts_string(category)},')
    lines.append(f'{indent}  readTime: {ts_string(read_time(post.word_count))},')
    # Field name on origin/main's Article interface is `substackUrl?` (optional).
    # Some forks rename this to `canonicalUrl: string` — if that's live when you run
    # this, post-process with `sed 's/substackUrl:/canonicalUrl:/g'`.
    lines.append(f'{indent}  substackUrl: {ts_string(post.url)},')
    lines.append(f'{indent}  slug: {ts_string(post.slug)},')
    lines.append(f'{indent}  keywords: {ts_string_array(default_keywords(post))},')
    lines.append(f'{indent}  wordCount: {post.word_count},')
    lines.append(f'{indent}  rating: 3,')
    lines.append(f'{indent}  content: {ts_template_string(post.markdown)},')
    lines.append(indent + "},")
    return "\n".join(lines)


# ---------- output artifacts ----------

def write_outputs(
    output_dir: Path,
    posts: list[SubstackPost],
    new_posts: list[SubstackPost],
    canonical_updates: list[tuple[SubstackPost, ExistingArticle]],
    articles_source: Path,
    existing: list[ExistingArticle],
    already_correct: list[tuple[SubstackPost, ExistingArticle]],
    alt_language_siblings: list[tuple[SubstackPost, ExistingArticle]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. new-articles.ts — just the new Article objects
    new_articles_path = output_dir / "new-articles.ts"
    lines = [
        "// Generated by pilot/scripts/substack_to_articles_ts.py",
        f"// Source: {SUBSTACK_FEED}",
        f"// Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"// New articles: {len(new_posts)} (not yet present in articles.ts)",
        "//",
        "// HOW TO USE:",
        "// 1. Review each object below — titles, slugs, categories, excerpts",
        "// 2. For Korean posts, swap the [Korean] title prefix for a real",
        "//    English title (so cards display well in the /insights grid)",
        "// 3. Copy the entire array contents into the `articles: Article[]`",
        "//    declaration in app/data/articles.ts (append to the end)",
        "// 4. Run `npm run build` to verify no TS errors",
        "// 5. Spot-check /insights and /insights/<slug> in dev",
        "//",
        "",
        "import { Article } from '@/app/data/articles';",
        "",
        "export const newArticlesFromSubstack: Article[] = [",
    ]
    for post in new_posts:
        lines.append(emit_article_object(post))
        lines.append("")
    lines.append("];")
    lines.append("")
    new_articles_path.write_text("\n".join(lines), encoding="utf-8")

    # 2. canonical-url-updates.md — human-readable patch plan for existing articles
    updates_path = output_dir / "canonical-url-updates.md"

    # Categorize existing articles by canonical URL state
    substack_root = [a for a in existing if a.canonical_url == "https://ethancho12.substack.com"]
    per_post_substack = [
        a for a in existing
        if is_substack_canonical(a.canonical_url) and a.canonical_url != "https://ethancho12.substack.com"
    ]
    self_canonical = [a for a in existing if a.canonical_url.startswith("https://ventureoracle.kr")]
    other = [a for a in existing if a not in substack_root + per_post_substack + self_canonical]

    lines = [
        "# Canonical URL health check for existing articles",
        "",
        f"Source feed: {SUBSTACK_FEED}",
        f"Existing articles.ts: {articles_source}",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Current state of canonical URLs across 17 articles",
        "",
        f"- **{len(substack_root)} articles** use the substack ROOT (`https://ethancho12.substack.com`).",
        "  This is the SEO bug: every one of these claims the substack homepage as canonical,",
        "  which dilutes the signal. These need per-post canonical URLs.",
        f"- **{len(per_post_substack)} articles** already use correct per-post substack canonicals.",
        "  Nothing to do for these.",
        f"- **{len(self_canonical)} articles** are self-canonical (point at `ventureoracle.kr/insights/<slug>`).",
        "  These are ventureoracle.kr-native content, never cross-posted on substack.",
        "  Leave them alone.",
    ]
    if other:
        lines.append(f"- **{len(other)} articles** have non-standard canonical URLs. Review manually.")
    lines.append("")
    lines.append("## Articles that need a canonical URL fix")
    lines.append("")
    if not canonical_updates:
        lines.append("_No fixable matches found — either the matcher missed them or the_")
        lines.append("_6 substack-root articles don't have recent substack counterparts._")
    else:
        lines.append(f"**{len(canonical_updates)} articles have confident substack post matches**")
        lines.append("and currently use the wrong canonical URL. Update each one below:")
        lines.append("")
        lines.append("| Slug | Existing title | Match reason | Change from | Change to |")
        lines.append("|---|---|---|---|---|")
        for post, art in canonical_updates:
            existing_title = (art.title or art.title_ko).replace("|", r"\|")[:60]
            lines.append(
                f"| `{art.slug}` | {existing_title}… | {post.match_reason} | "
                f"`{art.canonical_url}` | `{post.url}` |"
            )
    lines.append("")
    lines.append("## Articles already with correct canonical URLs")
    lines.append("")
    if already_correct:
        lines.append(f"**{len(already_correct)} articles are already correct** (exact URL match).")
        lines.append("No action required.")
        lines.append("")
        for post, art in already_correct:
            lines.append(f"- `{art.slug}` → `{art.canonical_url}`")
    else:
        lines.append("_None._")
    lines.append("")
    lines.append("## Alt-language siblings (Korean/English pairs)")
    lines.append("")
    if alt_language_siblings:
        lines.append(f"**{len(alt_language_siblings)} substack posts** fuzzy-matched to existing articles")
        lines.append("that already have a correct per-post substack canonical for the OTHER")
        lines.append("language version. These are effectively translated siblings. Three options:")
        lines.append("")
        lines.append("1. **Add as separate article** — creates a bilingual duplicate pair under")
        lines.append("   a new slug like `<existing-slug>-ko` or `<existing-slug>-en`.")
        lines.append("2. **Embed inside existing article** — populate the `titleKo` field on the")
        lines.append("   existing article with the sibling's title. No new slug created.")
        lines.append("3. **Leave alone** — accept that only one language surfaces on ventureoracle.kr.")
        lines.append("")
        lines.append("| Sibling post URL | Paired with article | Pair existing URL |")
        lines.append("|---|---|---|")
        for post, art in alt_language_siblings:
            lines.append(f"| `{post.url}` | `{art.slug}` | `{art.canonical_url}` |")
    else:
        lines.append("_None._")
    lines.append("")
    lines.append("## Substack-root articles without a detected match")
    lines.append("")
    matched_slugs = {art.slug for _, art in canonical_updates} | {art.slug for _, art in already_correct}
    orphan_substack_root = [a for a in substack_root if a.slug not in matched_slugs]
    if orphan_substack_root:
        lines.append(f"**{len(orphan_substack_root)} articles** use the substack root canonical but")
        lines.append("the matcher couldn't find a corresponding substack post. Two possibilities:")
        lines.append("")
        lines.append("1. The post WAS on substack but is no longer in the RSS feed")
        lines.append("   (substack's public feed returns ~20 most recent posts).")
        lines.append("2. The post was never actually on substack and the root canonical is a leftover placeholder.")
        lines.append("")
        lines.append("For each, either (a) search substack manually for the actual post URL and")
        lines.append("apply it, or (b) change the canonical to `https://ventureoracle.kr/insights/<slug>`")
        lines.append("(self-canonical) if it's a ventureoracle-native article.")
        lines.append("")
        for art in orphan_substack_root:
            lines.append(f"- `{art.slug}` — {(art.title or art.title_ko)[:80]}")
    else:
        lines.append("_None._")
    lines.append("")
    lines.append("## VentureOracle-native content (leave alone)")
    lines.append("")
    for art in self_canonical:
        lines.append(f"- `{art.slug}` → `{art.canonical_url}`")
    lines.append("")
    updates_path.write_text("\n".join(lines), encoding="utf-8")

    # 3. manifest.md — high-level summary
    manifest_path = output_dir / "MANIFEST.md"
    lines = [
        "# Substack → VentureOracle articles.ts sync",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Source feed: {SUBSTACK_FEED}",
        f"Existing articles.ts: {articles_source}",
        "",
        "## Summary",
        "",
        f"- **Substack posts fetched**: {len(posts)}",
        f"- **Existing articles in articles.ts**: {len(existing)}",
        f"- **Substack posts already correctly linked**: {len(already_correct)}",
        f"- **Substack posts needing canonical URL fix on existing articles**: {len(canonical_updates)}",
        f"- **Alt-language siblings (manual decision required)**: {len(alt_language_siblings)}",
        f"- **New substack posts (not yet in articles.ts)**: {len(new_posts)}",
        "",
        "## Output files",
        "",
        "- `new-articles.ts` — TypeScript `Article[]` fragment with the new posts.",
        "  Review, adjust Korean titles if needed, then append to articles.ts.",
        "- `canonical-url-updates.md` — Health check of canonical URLs across",
        "  the existing articles. Identifies substack-root canonicals (SEO bug),",
        "  already-correct ones, alt-language siblings, and ventureoracle-native",
        "  content that should be left alone.",
        "",
        "## Integration steps",
        "",
        "1. Read `canonical-url-updates.md` and apply the per-post URL updates to",
        "   `app/data/articles.ts` in the ventureoracle-site Next.js repo.",
        "2. Read `new-articles.ts`, review each new article's:",
        "   - `title` (for Korean posts, replace `[Korean] ...` with a real English",
        "     title so `/insights` cards display in English)",
        "   - `slug` (ensure it's stable and SEO-friendly)",
        "   - `category` (inferred automatically, check for correctness)",
        "   - `excerpt` (first paragraph; may need hand-polish)",
        "3. Append the new article objects into the existing `articles: Article[]`",
        "   array in `app/data/articles.ts`.",
        "4. Run `npm run build` to verify no TypeScript errors and check that the",
        "   static params include the new slugs.",
        "5. Commit + push. Vercel auto-deploys.",
        "",
        "## New posts at a glance",
        "",
        "| Date | Language | Words | Title | Slug |",
        "|---|---|---|---|---|",
    ]
    for post in new_posts:
        title_preview = post.title.replace("|", r"\|")[:60]
        lines.append(
            f"| {post.published.strftime('%Y-%m-%d')} | {post.language} | "
            f"{post.word_count} | {title_preview} | `{post.slug}` |"
        )
    lines.append("")
    manifest_path.write_text("\n".join(lines), encoding="utf-8")


# ---------- main ----------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument(
        "--articles-source",
        default=str(DEFAULT_ARTICLES_SOURCE),
        help="Path to the live app/data/articles.ts (default: %(default)s)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Where to write staged output (default: %(default)s)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse + match but don't write files",
    )
    parser.add_argument(
        "--match-threshold",
        type=float,
        default=0.35,
        help="Jaccard threshold for considering a substack post 'matched' to "
        "an existing article (default: %(default)s)",
    )
    args = parser.parse_args()

    articles_source = Path(args.articles_source).expanduser()
    output_dir = Path(args.output_dir).expanduser()

    print(f"Reading existing articles from {articles_source}")
    existing = parse_articles_ts(articles_source)
    print(f"Parsed {len(existing)} existing articles")

    print(f"Fetching substack feed: {SUBSTACK_FEED}")
    posts = fetch_substack_posts(SUBSTACK_FEED)
    print(f"Fetched {len(posts)} substack posts")

    canonical_updates: list[tuple[SubstackPost, ExistingArticle]] = []
    already_correct: list[tuple[SubstackPost, ExistingArticle]] = []
    alt_language_siblings: list[tuple[SubstackPost, ExistingArticle]] = []
    new_posts: list[SubstackPost] = []
    for post in posts:
        best, score, reason = find_best_match(post, existing)
        if best and score >= args.match_threshold:
            post.matched_existing = best
            post.match_reason = reason
            if best.canonical_url == post.url:
                # Exact canonical URL match — already linked correctly
                already_correct.append((post, best))
            elif is_substack_canonical(best.canonical_url) and best.canonical_url != "https://ethancho12.substack.com":
                # Existing article already has a per-post substack canonical URL
                # (just a different one). This is most likely the opposite-language
                # sibling of this post. Don't suggest replacing the canonical —
                # that would break the existing correct canonical for the other
                # language. Classify as alt-language sibling.
                alt_language_siblings.append((post, best))
            else:
                # Existing article uses substack ROOT or something unclear —
                # proposing a specific post URL is a real improvement.
                canonical_updates.append((post, best))
        else:
            new_posts.append(post)

    print()
    print("=" * 60)
    print(f"  Matched + already has correct canonical URL: {len(already_correct)}")
    for post, art in already_correct:
        print(f"    ✓ {art.slug}  ↔  {post.title[:60]}")
    print()
    print(f"  Matched + needs canonical URL update: {len(canonical_updates)}")
    for post, art in canonical_updates:
        print(f"    → {art.slug}  ↔  {post.title[:60]}  [{post.match_reason}]")
    print()
    print(f"  Alt-language siblings (not adding, not updating canonical): {len(alt_language_siblings)}")
    for post, art in alt_language_siblings:
        print(f"    = {art.slug}  ↔  {post.title[:60]}  [{post.match_reason}]")
    print()
    print(f"  New substack posts to add: {len(new_posts)}")
    for post in new_posts:
        print(f"    {post.published.strftime('%Y-%m-%d')} [{post.language}] "
              f"{post.title[:60]}  →  {post.slug}")
    print("=" * 60)

    if args.dry_run:
        print("\n(dry-run — no files written)")
        return

    write_outputs(
        output_dir,
        posts,
        new_posts,
        canonical_updates,
        articles_source,
        existing,
        already_correct,
        alt_language_siblings,
    )
    print()
    print(f"Wrote:")
    print(f"  {output_dir / 'new-articles.ts'}")
    print(f"  {output_dir / 'canonical-url-updates.md'}")
    print(f"  {output_dir / 'MANIFEST.md'}")


if __name__ == "__main__":
    main()
