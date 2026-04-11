#!/usr/bin/env python3
"""
GEO variance check — the ~$0.50 stability test the 2026-04-11 baseline hinges on.

The 2026-04-11 synthesis found exactly 2 cells out of 72 where ventureoracle.kr
was cited directly:
  - fr-004 (English) "Four Lenses VC framework" on Perplexity sonar-pro
  - fr-006 (Korean) "VC가 스타트업을 평가하는 Four Lenses 프레임워크" on Gemini 2.5 Pro

Both were single-call results. CLAUDE.md Phase 1 decision rules prescribe N=3
majority-vote for Claude and Perplexity because they drift at temperature=0.
This script re-runs each of those two load-bearing cells three times, checks
whether ventureoracle.kr still appears in response text or citations each time,
and emits a stability verdict.

If either cell drops to 0/3 on re-test, the baseline is 1/72 (not 2/72), which
moves the re-measurement gate materially.

Reads:
  - ~/Content_VentureOracle/.env (PERPLEXITY_API_KEY, GOOGLE_API_KEY)
Writes:
  - pilot/logs/variance-check-YYYY-MM-DD.md
  - stdout: per-call pass/fail

Dependencies:
  - openai (for Perplexity via OpenAI-compatible endpoint)
  - google-genai
  - python-dotenv
"""
from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
    from openai import OpenAI
    from google import genai
    from google.genai import types
except ImportError:
    sys.exit(
        "Install dependencies first: pip install openai google-genai python-dotenv"
    )

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = REPO_ROOT / "pilot" / "logs"
ENV_FILE = Path.home() / "Content_VentureOracle" / ".env"

# The two cells we're variance-checking — see docstring for why.
PERPLEXITY_CELL = {
    "cell_id": "fr-004",
    "engine": "perplexity",
    "model": "sonar-pro",
    "query": "Four Lenses VC framework",
    "language": "en",
}
GEMINI_CELL = {
    "cell_id": "fr-006",
    "engine": "gemini",
    "model": "gemini-2.5-pro",
    "query": "VC가 스타트업을 평가하는 Four Lenses 프레임워크",
    "language": "ko",
}
N_CALLS = 3
CITATION_NEEDLE = "ventureoracle.kr"

load_dotenv(ENV_FILE)


def cell_cited(text: str, sources: list[str]) -> bool:
    """True if ventureoracle.kr appears in the response body or any source URL."""
    if CITATION_NEEDLE in (text or "").lower():
        return True
    for s in sources:
        if CITATION_NEEDLE in (s or "").lower():
            return True
    return False


def run_perplexity(query: str, n: int) -> list[dict]:
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        return [{"error": f"PERPLEXITY_API_KEY not found in {ENV_FILE}"}] * n
    client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
    out: list[dict] = []
    for i in range(1, n + 1):
        print(f"  perplexity call {i}/{n}…", flush=True)
        try:
            response = client.chat.completions.create(
                model="sonar-pro",
                messages=[{"role": "user", "content": query}],
                max_tokens=2048,
            )
        except Exception as exc:
            out.append({"call": i, "error": str(exc)})
            continue
        text = (response.choices[0].message.content or "").strip()
        raw = response.model_dump() if hasattr(response, "model_dump") else {}
        citations = raw.get("citations") or raw.get("search_results") or []
        urls: list[str] = []
        for c in citations:
            if isinstance(c, str):
                urls.append(c)
            elif isinstance(c, dict):
                urls.append(c.get("url") or c.get("link") or "")
        out.append(
            {
                "call": i,
                "text": text,
                "sources": urls,
                "ventureoracle_cited": cell_cited(text, urls),
            }
        )
    return out


def run_gemini(query: str, n: int) -> list[dict]:
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return [{"error": f"GOOGLE_API_KEY / GEMINI_API_KEY not found in {ENV_FILE}"}] * n
    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        max_output_tokens=2048,
    )
    out: list[dict] = []
    for i in range(1, n + 1):
        print(f"  gemini call {i}/{n}…", flush=True)
        try:
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=query,
                config=config,
            )
        except Exception as exc:
            out.append({"call": i, "error": str(exc)})
            continue
        try:
            text = response.text or ""
        except Exception:
            parts = []
            for cand in getattr(response, "candidates", []) or []:
                for part in getattr(cand.content, "parts", []) or []:
                    if getattr(part, "text", None):
                        parts.append(part.text)
            text = "\n".join(parts)
        urls: list[str] = []
        for cand in getattr(response, "candidates", []) or []:
            gm = getattr(cand, "grounding_metadata", None)
            if not gm:
                continue
            for chunk in getattr(gm, "grounding_chunks", []) or []:
                web = getattr(chunk, "web", None)
                if web:
                    url = getattr(web, "uri", None) or getattr(web, "url", None)
                    if url:
                        urls.append(url)
        out.append(
            {
                "call": i,
                "text": text.strip(),
                "sources": urls,
                "ventureoracle_cited": cell_cited(text, urls),
            }
        )
    return out


def render_report(
    today: str,
    ppx_cell: dict,
    gem_cell: dict,
    ppx_calls: list[dict],
    gem_calls: list[dict],
) -> str:
    def hit_count(calls: list[dict]) -> int:
        return sum(1 for c in calls if c.get("ventureoracle_cited"))

    ppx_hits = hit_count(ppx_calls)
    gem_hits = hit_count(gem_calls)

    lines: list[str] = []
    lines.append(f"# GEO variance check — {today}")
    lines.append("")
    lines.append(
        "Stability test for the two load-bearing ventureoracle.kr citations "
        "in the 2026-04-11 baseline. Runs each cell 3× and counts how many "
        "of the 3 calls still cite ventureoracle.kr."
    )
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append(
        f"| Cell | Engine | Cited 2026-04-11 | Cited now (N=3) | Stable? |"
    )
    lines.append("|---|---|---|---|---|")
    lines.append(
        f"| {ppx_cell['cell_id']} ({ppx_cell['language']}) | {ppx_cell['engine']} {ppx_cell['model']} | ✅ 1/1 | {ppx_hits}/{N_CALLS} | {'✅' if ppx_hits >= 2 else '⚠️' if ppx_hits == 1 else '❌'} |"
    )
    lines.append(
        f"| {gem_cell['cell_id']} ({gem_cell['language']}) | {gem_cell['engine']} {gem_cell['model']} | ✅ 1/1 | {gem_hits}/{N_CALLS} | {'✅' if gem_hits >= 2 else '⚠️' if gem_hits == 1 else '❌'} |"
    )
    lines.append("")
    total_hits = ppx_hits + gem_hits
    if total_hits >= 4:
        lines.append(
            "**Verdict:** Baseline is stable. Both cells cite ventureoracle.kr ≥2/3 times. "
            "Proceed with the improvement plan's re-measurement gate as written."
        )
    elif total_hits >= 2:
        lines.append(
            "**Verdict:** Baseline is partially stable. At least one cell is unstable "
            "(≤1/3). Re-score the 2026-04-11 synthesis with the confirmed-stable cells "
            "only, and amend the re-measurement gate's hard floor downward accordingly."
        )
    else:
        lines.append(
            "**Verdict:** Baseline is NOT stable. Both ventureoracle.kr cells were "
            "likely noise. The 2026-04-11 baseline should be treated as 0–1 cells, not 2. "
            "The improvement plan's re-measurement gate needs its targets revised before "
            "it can be trusted as an evaluation criterion."
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Detail per engine
    for cell, calls, label in (
        (ppx_cell, ppx_calls, "Perplexity sonar-pro"),
        (gem_cell, gem_calls, "Gemini 2.5 Pro"),
    ):
        lines.append(f"## {label} — {cell['cell_id']} ({cell['language']})")
        lines.append("")
        lines.append(f"Query: `{cell['query']}`")
        lines.append("")
        for c in calls:
            if "error" in c:
                lines.append(f"**Call {c.get('call', '?')}:** ERROR — {c['error']}")
                lines.append("")
                continue
            mark = "✅ CITED" if c["ventureoracle_cited"] else "❌ NOT CITED"
            lines.append(
                f"**Call {c['call']}:** {mark}  ·  {len(c['sources'])} sources"
            )
            lines.append("")
            if c["sources"]:
                lines.append("<details><summary>Sources</summary>")
                lines.append("")
                for s in c["sources"][:12]:
                    lines.append(f"- {s}")
                lines.append("")
                lines.append("</details>")
                lines.append("")
            snippet = (c["text"] or "")[:500].replace("\n", " ")
            lines.append(f"> {snippet}{'…' if len(c['text']) > 500 else ''}")
            lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"Variance check — {today}")
    print(f"Perplexity {PERPLEXITY_CELL['cell_id']}: {PERPLEXITY_CELL['query']}")
    ppx_calls = run_perplexity(PERPLEXITY_CELL["query"], N_CALLS)
    print(f"Gemini {GEMINI_CELL['cell_id']}: {GEMINI_CELL['query']}")
    gem_calls = run_gemini(GEMINI_CELL["query"], N_CALLS)

    report = render_report(today, PERPLEXITY_CELL, GEMINI_CELL, ppx_calls, gem_calls)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = LOGS_DIR / f"variance-check-{today}.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"\nWrote {out_path}")

    # Summary line to stdout
    ppx_hits = sum(1 for c in ppx_calls if c.get("ventureoracle_cited"))
    gem_hits = sum(1 for c in gem_calls if c.get("ventureoracle_cited"))
    print(f"Perplexity fr-004: {ppx_hits}/{N_CALLS} cited")
    print(f"Gemini fr-006:      {gem_hits}/{N_CALLS} cited")


if __name__ == "__main__":
    main()
