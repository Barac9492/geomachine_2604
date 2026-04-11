#!/usr/bin/env python3
"""
GEO audit — one-command P0.0 inventory of ventureoracle.kr and related surfaces.

Fetches the framework pages, author page, and substack surfaces, extracts
title/H1/meta/schema.org/word-count/internal-links/disambiguation-phrase-hits,
and emits a markdown report that can be pasted into
`docs/designs/geo-improvement-plan-2026-04-11.md` → "Page inventory" section.

This is the automation that eliminates the P0.0 manual task entirely. Run it
once from a machine with working egress, paste the output, done.

Reads:
  - (nothing — URLs are configured inline below)
Writes:
  - pilot/logs/audit-YYYY-MM-DD.md
  - stdout: compact per-URL status

Dependencies:
  - requests
  - beautifulsoup4
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit(
        "Install dependencies first: pip install requests beautifulsoup4"
    )

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = REPO_ROOT / "pilot" / "logs"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
TIMEOUT = 20

# URLs to audit, grouped by role. Edit this list when pages are added/removed.
AUDIT_TARGETS: list[dict] = [
    # Framework pages — the critical ones for the improvement plan
    {"url": "https://www.ventureoracle.kr/concepts/four-lenses-framework", "role": "framework", "query_id": "fr-004", "framework": "Four Lenses"},
    {"url": "https://www.ventureoracle.kr/concepts/mau-trap", "role": "framework", "query_id": "fr-003", "framework": "MAU Trap"},
    {"url": "https://www.ventureoracle.kr/concepts/founder-intelligence", "role": "framework", "query_id": "fr-001", "framework": "Founder Intelligence"},
    {"url": "https://www.ventureoracle.kr/concepts/edr-ai-framework", "role": "framework", "query_id": "fr-002", "framework": "E/D/R"},
    {"url": "https://www.ventureoracle.kr/concepts/negative-sequence", "role": "framework", "query_id": "fr-007 (new)", "framework": "Negative Sequence"},
    # Hub + author + track record
    {"url": "https://www.ventureoracle.kr/concepts", "role": "hub", "query_id": None, "framework": None},
    {"url": "https://www.ventureoracle.kr/about/ethan-cho", "role": "author", "query_id": "id-001/dm-008", "framework": None},
    {"url": "https://www.ventureoracle.kr/predictions", "role": "predictions-hub", "query_id": None, "framework": None},
    {"url": "https://www.ventureoracle.kr/", "role": "home", "query_id": None, "framework": None},
    # Substacks — both, so Ethan can compare the working one to the invisible one
    {"url": "https://ethancho12.substack.com/", "role": "substack-personal", "query_id": None, "framework": None},
    {"url": "https://theventures.substack.com/", "role": "substack-firm", "query_id": None, "framework": None},
]

# Disambiguation phrases the plan says should appear on each framework page.
# Keyed by framework name.
REQUIRED_PHRASES: dict[str, list[str]] = {
    "Four Lenses": ["Ethan Cho", "VentureOracle"],
    "MAU Trap": ["MAU Trap framework by Ethan Cho", "Ethan Cho"],
    "Founder Intelligence": ["Ethan Cho", "not", "Accenture"],
    "E/D/R": ["Ethan Cho", "not", "Endpoint Detection"],
    "Negative Sequence": ["Ethan Cho", "죽음의 순서"],
}


@dataclass
class PageAudit:
    url: str
    role: str
    query_id: str | None
    framework: str | None
    status_code: int | None = None
    error: str | None = None
    title: str | None = None
    h1: str | None = None
    meta_description: str | None = None
    canonical: str | None = None
    lang: str | None = None
    word_count: int = 0
    jsonld_blocks: list[dict] = field(default_factory=list)
    jsonld_types: list[str] = field(default_factory=list)
    internal_links: list[str] = field(default_factory=list)
    external_links: list[str] = field(default_factory=list)
    hreflang_alternates: list[str] = field(default_factory=list)
    has_author_person_schema: bool = False
    has_defined_term_schema: bool = False
    phrase_hits: dict[str, bool] = field(default_factory=dict)
    first_paragraph: str = ""


def fetch(url: str) -> tuple[int | None, str | None, str | None]:
    """Return (status_code, html_or_none, error_or_none)."""
    try:
        r = requests.get(
            url,
            headers={"User-Agent": USER_AGENT, "Accept-Language": "en,ko;q=0.9"},
            timeout=TIMEOUT,
            allow_redirects=True,
        )
        return r.status_code, r.text if r.status_code == 200 else None, None
    except Exception as exc:
        return None, None, str(exc)


def audit_one(target: dict) -> PageAudit:
    a = PageAudit(
        url=target["url"],
        role=target["role"],
        query_id=target.get("query_id"),
        framework=target.get("framework"),
    )
    status, html, err = fetch(a.url)
    a.status_code = status
    if err:
        a.error = err
        return a
    if status != 200 or html is None:
        a.error = f"HTTP {status}"
        return a

    soup = BeautifulSoup(html, "html.parser")

    # Basic metadata
    if soup.title and soup.title.string:
        a.title = soup.title.string.strip()
    h1 = soup.find("h1")
    if h1:
        a.h1 = h1.get_text(strip=True)
    md = soup.find("meta", attrs={"name": "description"})
    if md and md.get("content"):
        a.meta_description = md["content"].strip()
    canonical = soup.find("link", rel="canonical")
    if canonical and canonical.get("href"):
        a.canonical = canonical["href"].strip()
    html_tag = soup.find("html")
    if html_tag and html_tag.get("lang"):
        a.lang = html_tag["lang"]

    # hreflang alternates
    for alt in soup.find_all("link", rel="alternate"):
        if alt.get("hreflang") and alt.get("href"):
            a.hreflang_alternates.append(f"{alt['hreflang']} → {alt['href']}")

    # JSON-LD blocks
    for script in soup.find_all("script", type="application/ld+json"):
        raw = script.string or script.get_text() or ""
        if not raw.strip():
            continue
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            a.jsonld_types.append("(unparseable)")
            continue
        a.jsonld_blocks.append(parsed)
        # @type can be a string or list; parsed can be object or list
        items = parsed if isinstance(parsed, list) else [parsed]
        for item in items:
            if isinstance(item, dict):
                t = item.get("@type")
                if isinstance(t, list):
                    a.jsonld_types.extend(str(x) for x in t)
                elif t:
                    a.jsonld_types.append(str(t))

    a.has_author_person_schema = any(
        t in ("Person",) for t in a.jsonld_types
    )
    a.has_defined_term_schema = any(
        t in ("DefinedTerm", "DefinedTermSet") for t in a.jsonld_types
    )

    # Body text + first paragraph + word count
    body = soup.find("body")
    if body:
        # Remove script/style/nav/footer noise
        for bad in body.find_all(["script", "style", "nav", "footer", "header"]):
            bad.decompose()
        text = body.get_text(" ", strip=True)
        a.word_count = len(re.findall(r"\w+", text))
        first_p = body.find("p")
        if first_p:
            a.first_paragraph = first_p.get_text(" ", strip=True)[:500]

        # Phrase hits against the full body text, case-insensitive
        body_lower = text.lower()
        if a.framework and a.framework in REQUIRED_PHRASES:
            for phrase in REQUIRED_PHRASES[a.framework]:
                a.phrase_hits[phrase] = phrase.lower() in body_lower

    # Links
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/") or "ventureoracle.kr" in href:
            a.internal_links.append(href)
        elif href.startswith("http"):
            a.external_links.append(href)

    return a


def render_report(audits: list[PageAudit], today: str) -> str:
    lines: list[str] = []
    lines.append(f"# GEO audit — {today}")
    lines.append("")
    lines.append(
        "Automated inventory of ventureoracle.kr framework pages, the author "
        "page, and related substack surfaces. Generated by "
        "`pilot/scripts/geo_audit.py`. Paste the table below into "
        "`docs/designs/geo-improvement-plan-2026-04-11.md` → "
        "\"Page inventory — 2026-04-11\" section."
    )
    lines.append("")

    # Summary counters
    reached = sum(1 for a in audits if a.status_code == 200)
    missing = sum(1 for a in audits if a.status_code and a.status_code != 200)
    errored = sum(1 for a in audits if a.error and not a.status_code)
    lines.append(
        f"**Reached:** {reached} / {len(audits)} · **Missing (404/3xx):** {missing} · **Errored:** {errored}"
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Inventory table
    lines.append("## Inventory table")
    lines.append("")
    lines.append(
        "| Role | URL | HTTP | Words | JSON-LD types | Author schema | DefinedTerm schema | hreflang | Phrase hits |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for a in audits:
        url_short = a.url.replace("https://www.ventureoracle.kr", "vo").replace(
            "https://ethancho12.substack.com", "substack-personal"
        ).replace("https://theventures.substack.com", "substack-firm")
        http = str(a.status_code) if a.status_code else (a.error or "?")
        jsonld = ", ".join(sorted(set(a.jsonld_types))) or "—"
        author = "✅" if a.has_author_person_schema else "❌"
        defterm = "✅" if a.has_defined_term_schema else "❌"
        hl = ", ".join(a.hreflang_alternates) or "—"
        if a.phrase_hits:
            phrases = " · ".join(
                f"{p}:{'✅' if hit else '❌'}" for p, hit in a.phrase_hits.items()
            )
        else:
            phrases = "—"
        lines.append(
            f"| {a.role} | {url_short} | {http} | {a.word_count} | {jsonld} | {author} | {defterm} | {hl} | {phrases} |"
        )
    lines.append("")

    # Per-page detail
    lines.append("## Per-page detail")
    lines.append("")
    for a in audits:
        lines.append(f"### {a.role} — {a.url}")
        lines.append("")
        if a.error or a.status_code != 200:
            lines.append(f"**HTTP {a.status_code or 'error'}:** {a.error or 'non-200'}")
            lines.append("")
            lines.append("---")
            lines.append("")
            continue
        lines.append(f"- **Title:** `{a.title or '—'}`")
        lines.append(f"- **H1:** `{a.h1 or '—'}`")
        lines.append(f"- **Meta description:** `{a.meta_description or '—'}`")
        lines.append(f"- **Canonical:** `{a.canonical or '—'}`")
        lines.append(f"- **lang:** `{a.lang or '—'}`")
        lines.append(f"- **Word count:** {a.word_count}")
        lines.append(f"- **JSON-LD types present:** {', '.join(sorted(set(a.jsonld_types))) or '(none)'}")
        if a.hreflang_alternates:
            lines.append(f"- **hreflang alternates:** {', '.join(a.hreflang_alternates)}")
        if a.phrase_hits:
            lines.append(
                "- **Required phrases:** "
                + " · ".join(
                    f"`{p}` {'✅ present' if hit else '❌ MISSING'}"
                    for p, hit in a.phrase_hits.items()
                )
            )
        if a.first_paragraph:
            snippet = a.first_paragraph.replace("|", "\\|")
            lines.append(f"- **First paragraph:** {snippet}")
        if a.jsonld_blocks:
            lines.append("")
            lines.append("<details><summary>Raw JSON-LD blocks</summary>")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(a.jsonld_blocks, indent=2, ensure_ascii=False)[:4000])
            lines.append("```")
            lines.append("</details>")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Actionable diagnosis
    lines.append("## Actionable diagnosis")
    lines.append("")
    lines.append("Framework pages that need attention, ordered by impact:")
    lines.append("")
    for a in audits:
        if a.role != "framework":
            continue
        problems: list[str] = []
        if a.status_code != 200:
            problems.append(f"page missing or errored ({a.status_code or a.error})")
        else:
            if not a.has_defined_term_schema:
                problems.append("no `DefinedTerm` schema.org JSON-LD")
            if not a.has_author_person_schema:
                problems.append("no `Person` schema on this page")
            if a.framework and a.framework in REQUIRED_PHRASES:
                missing_phrases = [p for p, hit in a.phrase_hits.items() if not hit]
                if missing_phrases:
                    problems.append(f"missing disambiguation phrases: {', '.join(missing_phrases)}")
            if not a.hreflang_alternates:
                problems.append("no hreflang alternates — Korean version may not be linked")
            if a.word_count < 800:
                problems.append(f"only {a.word_count} words — likely below corpus-mass threshold to displace generic content")
        if problems:
            lines.append(f"### {a.framework} ({a.url})")
            for p in problems:
                lines.append(f"- ❌ {p}")
            lines.append("")

    return "\n".join(lines)


def main() -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Auditing {len(AUDIT_TARGETS)} URLs…")
    audits: list[PageAudit] = []
    for target in AUDIT_TARGETS:
        print(f"  {target['url']}")
        a = audit_one(target)
        if a.error:
            print(f"    ERROR: {a.error}")
        else:
            print(
                f"    {a.status_code}  words={a.word_count}  jsonld={','.join(set(a.jsonld_types)) or '—'}"
            )
        audits.append(a)

    report = render_report(audits, today)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = LOGS_DIR / f"audit-{today}.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
