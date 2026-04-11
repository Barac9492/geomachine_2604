#!/usr/bin/env python3
"""
Throwaway pilot helper: run 18 queries against Perplexity API (sonar-pro).

Phase 0 data collection helper, NOT Phase 1 automation. Sibling of
run_claude_api.py and run_openai_api.py.

Perplexity's API is OpenAI-compatible but ALWAYS does web retrieval — there's
no separate tool to enable. Citations come back in the response root's
`citations` array, not inside the message content. We extract both.

Reads:
  - pilot/queries.txt
  - ~/Content_VentureOracle/.env (PERPLEXITY_API_KEY)
Writes:
  - pilot/logs/run-YYYY-MM-DD-perplexity-api.md
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
QUERIES_FILE = REPO_ROOT / "pilot" / "queries.txt"
LOGS_DIR = REPO_ROOT / "pilot" / "logs"
ENV_FILE = Path.home() / "Content_VentureOracle" / ".env"

MODEL = "sonar-pro"
MAX_TOKENS = 2048

load_dotenv(ENV_FILE)
api_key = os.getenv("PERPLEXITY_API_KEY")
if not api_key:
    sys.exit(f"PERPLEXITY_API_KEY not found in {ENV_FILE}")

client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

queries = [
    line.strip()
    for line in QUERIES_FILE.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.strip().startswith("#")
]
print(f"Loaded {len(queries)} queries from {QUERIES_FILE}")

today = datetime.now().strftime("%Y-%m-%d")
out_path = LOGS_DIR / f"run-{today}-perplexity-api.md"
out_path.parent.mkdir(parents=True, exist_ok=True)

results = []
total_input_tokens = 0
total_output_tokens = 0
total_citations = 0

started_at = datetime.now()

for i, query in enumerate(queries, 1):
    preview = query[:70] + ("…" if len(query) > 70 else "")
    print(f"[{i:2}/{len(queries)}] {preview}")
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": query}],
            max_tokens=MAX_TOKENS,
        )
    except Exception as exc:
        results.append({"query": query, "error": str(exc)})
        print(f"    ERROR: {exc}")
        continue

    text = response.choices[0].message.content or ""
    # Perplexity returns citations on the response root (via additional fields)
    # The openai SDK surfaces these through model_extra or raw dict
    raw = response.model_dump() if hasattr(response, "model_dump") else {}
    citations = raw.get("citations") or raw.get("search_results") or []
    # Normalize — some versions return strings, some return dicts
    sources: list[dict] = []
    for c in citations:
        if isinstance(c, str):
            sources.append({"title": "", "url": c})
        elif isinstance(c, dict):
            sources.append(
                {
                    "title": c.get("title", "") or "",
                    "url": c.get("url") or c.get("link") or "",
                }
            )

    usage = response.usage
    total_input_tokens += usage.prompt_tokens
    total_output_tokens += usage.completion_tokens
    total_citations += len(sources)

    results.append(
        {
            "query": query,
            "response_text": text.strip() or "(no text output)",
            "sources": sources,
            "input_tokens": usage.prompt_tokens,
            "output_tokens": usage.completion_tokens,
            "finish_reason": response.choices[0].finish_reason,
        }
    )
    print(f"    ok: {usage.prompt_tokens}in/{usage.completion_tokens}out, {len(sources)} sources")
    time.sleep(0.5)

ended_at = datetime.now()
elapsed = (ended_at - started_at).total_seconds()

# ── Write the log ───────────────────────────────────────────────────────────

def md_escape(s: str) -> str:
    return s.replace("|", "\\|")


lines: list[str] = []
lines.append(f"# GEO Pilot — Perplexity (sonar-pro) API run, {today}")
lines.append("")
lines.append(f"**Model:** `{MODEL}`")
lines.append(f"**Endpoint:** `https://api.perplexity.ai` (OpenAI-compatible)")
lines.append(f"**Web retrieval:** always on (Perplexity default, not an opt-in tool)")
lines.append(f"**Started:** {started_at.isoformat(timespec='seconds')}")
lines.append(f"**Ended:**   {ended_at.isoformat(timespec='seconds')}")
lines.append(f"**Elapsed:** {elapsed:.1f}s")
lines.append(f"**Queries:** {len(results)}")
lines.append(f"**Total input tokens:** {total_input_tokens:,}")
lines.append(f"**Total output tokens:** {total_output_tokens:,}")
lines.append(f"**Total citations captured:** {total_citations}")
lines.append("")
lines.append("> Phase 0 data collection helper, NOT Phase 1 automation.")
lines.append("> Human review still required to score the cells below.")
lines.append("")
lines.append("---")
lines.append("")

for i, r in enumerate(results, 1):
    lines.append(f"## Query {i:02}: {r['query']}")
    lines.append("")
    if "error" in r:
        lines.append(f"**ERROR:** {r['error']}")
        lines.append("")
        lines.append("---")
        lines.append("")
        continue
    lines.append(f"**Tokens:** {r['input_tokens']:,} in / {r['output_tokens']:,} out  |  **Finish:** `{r['finish_reason']}`")
    lines.append("")
    lines.append("**Response:**")
    lines.append("")
    lines.append(r["response_text"])
    lines.append("")
    if r["sources"]:
        lines.append(f"**Sources cited by Perplexity ({len(r['sources'])}):**")
        lines.append("")
        seen = set()
        for s in r["sources"]:
            key = s["url"]
            if not key or key in seen:
                continue
            seen.add(key)
            title = s.get("title", "") or "(no title)"
            lines.append(f"- [{md_escape(title)}]({s['url']})")
        lines.append("")
    else:
        lines.append("**Sources cited by Perplexity:** (none)")
        lines.append("")
    lines.append("---")
    lines.append("")

out_path.write_text("\n".join(lines), encoding="utf-8")

print()
print(f"Wrote {out_path}")
print(f"Total tokens: {total_input_tokens:,} in / {total_output_tokens:,} out")
print(f"Total citations: {total_citations}")
# sonar-pro pricing: $3/M input, $15/M output + per-request fee
est_cost = (total_input_tokens * 3 / 1_000_000) + (total_output_tokens * 15 / 1_000_000) + (len(results) * 0.005)
print(f"Rough cost estimate: ${est_cost:.3f}")
