#!/usr/bin/env python3
"""
Throwaway pilot helper: run 18 queries against Claude API with web_search tool.

This is Phase 0 data collection, NOT Phase 1 automation.
- No schema, no classifier, no scheduler, no persistence beyond a markdown file
- Human eyeballs still score each cell in the log template
- Script is in pilot/scripts/ (not Content_VentureOracle/src/geo/) on purpose:
  it is explicitly a throwaway pilot helper, not a reusable engine client

Reads:
  - pilot/queries.txt (18 queries, one per line)
  - ~/Content_VentureOracle/.env (for ANTHROPIC_API_KEY)

Writes:
  - pilot/logs/run-YYYY-MM-DD-claude-api.md

Usage:
  ~/Content_VentureOracle/.venv/bin/python pilot/scripts/run_claude_api.py
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from datetime import datetime

from anthropic import Anthropic
from dotenv import load_dotenv

# ── Config ──────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
QUERIES_FILE = REPO_ROOT / "pilot" / "queries.txt"
LOGS_DIR = REPO_ROOT / "pilot" / "logs"
ENV_FILE = Path.home() / "Content_VentureOracle" / ".env"

MODEL = "claude-sonnet-4-5"  # match claude.ai default Sonnet tier
MAX_TOKENS = 2048
WEB_SEARCH_TOOL = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 5,  # reasonable cap per query
}

# ── Load env + client ───────────────────────────────────────────────────────
load_dotenv(ENV_FILE)
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    sys.exit(f"ANTHROPIC_API_KEY not found in {ENV_FILE}")

client = Anthropic(api_key=api_key)

# ── Load queries ────────────────────────────────────────────────────────────
queries = [
    line.strip()
    for line in QUERIES_FILE.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.strip().startswith("#")
]
print(f"Loaded {len(queries)} queries from {QUERIES_FILE}")

# ── Output file ─────────────────────────────────────────────────────────────
today = datetime.now().strftime("%Y-%m-%d")
out_path = LOGS_DIR / f"run-{today}-claude-api.md"
out_path.parent.mkdir(parents=True, exist_ok=True)

# ── Run each query ──────────────────────────────────────────────────────────
results = []
total_input_tokens = 0
total_output_tokens = 0
total_web_searches = 0

started_at = datetime.now()

for i, query in enumerate(queries, 1):
    preview = query[:70] + ("…" if len(query) > 70 else "")
    print(f"[{i:2}/{len(queries)}] {preview}")
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            tools=[WEB_SEARCH_TOOL],
            messages=[{"role": "user", "content": query}],
        )
    except Exception as exc:
        results.append({"query": query, "error": str(exc)})
        print(f"    ERROR: {exc}")
        continue

    # Walk the content blocks
    text_parts: list[str] = []
    sources: list[dict] = []
    server_tool_use_blocks = 0

    for block in response.content:
        block_type = getattr(block, "type", None)

        if block_type == "text":
            text_parts.append(block.text)
        elif block_type == "server_tool_use":
            server_tool_use_blocks += 1
        elif block_type == "web_search_tool_result":
            # block.content is a list of result items (or an error)
            inner = getattr(block, "content", None)
            if isinstance(inner, list):
                for item in inner:
                    url = getattr(item, "url", None)
                    title = getattr(item, "title", None)
                    if url:
                        sources.append({"title": title or "", "url": url})

    total_input_tokens += response.usage.input_tokens
    total_output_tokens += response.usage.output_tokens
    # Server-side tool usage (web searches) is billed separately; capture count
    if hasattr(response.usage, "server_tool_use"):
        stu = response.usage.server_tool_use
        if hasattr(stu, "web_search_requests"):
            total_web_searches += stu.web_search_requests or 0

    results.append(
        {
            "query": query,
            "response_text": "\n".join(text_parts).strip() or "(no text output)",
            "sources": sources,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "stop_reason": response.stop_reason,
        }
    )
    print(
        f"    ok: {response.usage.input_tokens}in/{response.usage.output_tokens}out, "
        f"{len(sources)} sources"
    )

    # Be nice to the API — modest delay between calls
    time.sleep(0.5)

ended_at = datetime.now()
elapsed = (ended_at - started_at).total_seconds()

# ── Write the log file ─────────────────────────────────────────────────────

def md_escape(s: str) -> str:
    return s.replace("|", "\\|")


lines: list[str] = []
lines.append(f"# GEO Pilot — Claude API run, {today}")
lines.append("")
lines.append(f"**Model:** `{MODEL}`")
lines.append(f"**Web search tool:** enabled (`{WEB_SEARCH_TOOL['type']}`, max_uses={WEB_SEARCH_TOOL['max_uses']})")
lines.append(f"**Started:** {started_at.isoformat(timespec='seconds')}")
lines.append(f"**Ended:**   {ended_at.isoformat(timespec='seconds')}")
lines.append(f"**Elapsed:** {elapsed:.1f}s")
lines.append(f"**Queries:** {len(results)}")
lines.append(f"**Total input tokens:** {total_input_tokens:,}")
lines.append(f"**Total output tokens:** {total_output_tokens:,}")
lines.append(f"**Web search requests:** {total_web_searches}")
lines.append("")
lines.append("> This file was produced by `pilot/scripts/run_claude_api.py`, a throwaway")
lines.append("> Phase 0 data collection helper. It is NOT Phase 1 automation. Human review")
lines.append("> of each response is still required to score the log template cells")
lines.append("> (`cited / context / position / sources / competitor_names / notes`).")
lines.append("")
lines.append("---")
lines.append("")

# Per-query sections
for i, r in enumerate(results, 1):
    lines.append(f"## Query {i:02}: {r['query']}")
    lines.append("")
    if "error" in r:
        lines.append(f"**ERROR:** {r['error']}")
        lines.append("")
        lines.append("---")
        lines.append("")
        continue

    lines.append(f"**Tokens:** {r['input_tokens']:,} in / {r['output_tokens']:,} out  |  **Stop reason:** `{r['stop_reason']}`")
    lines.append("")
    lines.append("**Response:**")
    lines.append("")
    lines.append(r["response_text"])
    lines.append("")

    if r["sources"]:
        lines.append(f"**Sources cited by Claude ({len(r['sources'])}):**")
        lines.append("")
        for s in r["sources"]:
            title = s.get("title", "") or "(no title)"
            lines.append(f"- [{md_escape(title)}]({s['url']})")
        lines.append("")
    else:
        lines.append("**Sources cited by Claude:** (none)")
        lines.append("")

    lines.append("---")
    lines.append("")

# Scoring scaffold for human review
lines.append("## Scoring scaffold (fill in after reading each response above)")
lines.append("")
lines.append("Claude web chat column only. Fill the `cited / context / position / sources / competitors / notes`")
lines.append("fields. `cited` = yes only if Ethan Cho, TheVentures, or one of the four framework names")
lines.append("(Founder Intelligence, E/D/R, MAU Trap, Four Lenses) appears by name in the response.")
lines.append("")
lines.append("| query_id | query preview | cited | context | position | sources cited | competitor_names | notes |")
lines.append("|---|---|---|---|---|---|---|---|")
query_ids = [
    "id-001", "id-002", "id-003",
    "fr-001", "fr-002", "fr-003", "fr-004", "fr-005", "fr-006",
    "dm-001", "dm-002", "dm-003", "dm-004", "dm-005", "dm-006", "dm-007", "dm-008", "dm-009",
]
for qid, r in zip(query_ids, results):
    preview = r["query"][:50] + ("…" if len(r["query"]) > 50 else "")
    preview = md_escape(preview)
    lines.append(f"| {qid} | {preview} |  |  |  |  |  |  |")
lines.append("")

out_path.write_text("\n".join(lines), encoding="utf-8")

# ── Final console summary ───────────────────────────────────────────────────
print()
print(f"Wrote {out_path}")
print(f"Total tokens: {total_input_tokens:,} in / {total_output_tokens:,} out")
print(f"Web search requests: {total_web_searches}")
# Rough cost estimate: Sonnet 4.5 is ~$3/M input, ~$15/M output
# Web search is $10/1000 requests
est_cost = (total_input_tokens * 3 / 1_000_000) + (total_output_tokens * 15 / 1_000_000) + (total_web_searches * 10 / 1000)
print(f"Rough cost estimate: ${est_cost:.3f}")
