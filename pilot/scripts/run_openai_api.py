#!/usr/bin/env python3
"""
Throwaway pilot helper: run 18 queries against OpenAI API (GPT-4o with web search).

Phase 0 data collection helper, NOT Phase 1 automation. Sibling of run_claude_api.py.

Uses the Responses API with `web_search_preview` tool (OpenAI's server-side
web search, equivalent to the ChatGPT web UI's search-the-web feature).

Reads:
  - pilot/queries.txt
  - ~/Content_VentureOracle/.env (OPENAI_API_KEY)
Writes:
  - pilot/logs/run-YYYY-MM-DD-openai-api.md
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

MODEL = "gpt-4o"
MAX_OUTPUT_TOKENS = 2048

load_dotenv(ENV_FILE)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    sys.exit(f"OPENAI_API_KEY not found in {ENV_FILE}")

client = OpenAI(api_key=api_key)

queries = [
    line.strip()
    for line in QUERIES_FILE.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.strip().startswith("#")
]
print(f"Loaded {len(queries)} queries from {QUERIES_FILE}")

today = datetime.now().strftime("%Y-%m-%d")
out_path = LOGS_DIR / f"run-{today}-openai-api.md"
out_path.parent.mkdir(parents=True, exist_ok=True)

results = []
total_input_tokens = 0
total_output_tokens = 0

started_at = datetime.now()

for i, query in enumerate(queries, 1):
    preview = query[:70] + ("…" if len(query) > 70 else "")
    print(f"[{i:2}/{len(queries)}] {preview}")
    try:
        response = client.responses.create(
            model=MODEL,
            input=query,
            tools=[{"type": "web_search_preview"}],
            max_output_tokens=MAX_OUTPUT_TOKENS,
        )
    except Exception as exc:
        results.append({"query": query, "error": str(exc)})
        print(f"    ERROR: {exc}")
        continue

    # Extract text + sources from the Responses API output
    text_parts: list[str] = []
    sources: list[dict] = []

    for output_item in response.output:
        item_type = getattr(output_item, "type", None)
        if item_type == "message":
            for content_block in getattr(output_item, "content", []):
                cb_type = getattr(content_block, "type", None)
                if cb_type == "output_text":
                    text_parts.append(content_block.text)
                    # Annotations may carry URL citations
                    for ann in getattr(content_block, "annotations", []) or []:
                        if getattr(ann, "type", None) == "url_citation":
                            sources.append(
                                {
                                    "title": getattr(ann, "title", "") or "",
                                    "url": getattr(ann, "url", "") or "",
                                }
                            )

    usage = response.usage
    total_input_tokens += usage.input_tokens
    total_output_tokens += usage.output_tokens

    results.append(
        {
            "query": query,
            "response_text": "\n".join(text_parts).strip() or "(no text output)",
            "sources": sources,
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "status": response.status,
        }
    )
    print(f"    ok: {usage.input_tokens}in/{usage.output_tokens}out, {len(sources)} sources")
    time.sleep(0.5)

ended_at = datetime.now()
elapsed = (ended_at - started_at).total_seconds()

# ── Write the log ───────────────────────────────────────────────────────────

def md_escape(s: str) -> str:
    return s.replace("|", "\\|")


lines: list[str] = []
lines.append(f"# GEO Pilot — OpenAI (GPT-4o) API run, {today}")
lines.append("")
lines.append(f"**Model:** `{MODEL}`")
lines.append(f"**Tool:** `web_search_preview` (OpenAI Responses API server-side web search)")
lines.append(f"**Started:** {started_at.isoformat(timespec='seconds')}")
lines.append(f"**Ended:**   {ended_at.isoformat(timespec='seconds')}")
lines.append(f"**Elapsed:** {elapsed:.1f}s")
lines.append(f"**Queries:** {len(results)}")
lines.append(f"**Total input tokens:** {total_input_tokens:,}")
lines.append(f"**Total output tokens:** {total_output_tokens:,}")
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
    lines.append(f"**Tokens:** {r['input_tokens']:,} in / {r['output_tokens']:,} out  |  **Status:** `{r['status']}`")
    lines.append("")
    lines.append("**Response:**")
    lines.append("")
    lines.append(r["response_text"])
    lines.append("")
    if r["sources"]:
        lines.append(f"**Sources cited by GPT-4o ({len(r['sources'])}):**")
        lines.append("")
        seen = set()
        for s in r["sources"]:
            key = s["url"]
            if key in seen or not key:
                continue
            seen.add(key)
            title = s.get("title", "") or "(no title)"
            lines.append(f"- [{md_escape(title)}]({s['url']})")
        lines.append("")
    else:
        lines.append("**Sources cited by GPT-4o:** (none)")
        lines.append("")
    lines.append("---")
    lines.append("")

out_path.write_text("\n".join(lines), encoding="utf-8")

print()
print(f"Wrote {out_path}")
print(f"Total tokens: {total_input_tokens:,} in / {total_output_tokens:,} out")
# GPT-4o rough pricing: $2.50/M input, $10/M output (as of late 2025)
# web_search_preview cost varies; estimate $10/1000 calls
est_cost = (total_input_tokens * 2.5 / 1_000_000) + (total_output_tokens * 10 / 1_000_000) + (len(results) * 0.01)
print(f"Rough cost estimate: ${est_cost:.3f}")
