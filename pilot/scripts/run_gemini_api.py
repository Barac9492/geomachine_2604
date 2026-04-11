#!/usr/bin/env python3
"""
Throwaway pilot helper: run 18 queries against Google Gemini API
(gemini-2.5-pro with Google Search grounding).

Phase 0 data collection helper, NOT Phase 1 automation. Sibling of the other
run_*_api.py scripts.

Uses the `google-genai` SDK (new unified SDK, not the legacy
`google-generativeai`). Grounding tool enables Google Search retrieval,
equivalent to Gemini's web-grounded chat UI default.

Reads:
  - pilot/queries.txt
  - ~/Content_VentureOracle/.env (GOOGLE_API_KEY or GEMINI_API_KEY)
Writes:
  - pilot/logs/run-YYYY-MM-DD-gemini-api.md
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from datetime import datetime

from google import genai
from google.genai import types
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
QUERIES_FILE = REPO_ROOT / "pilot" / "queries.txt"
LOGS_DIR = REPO_ROOT / "pilot" / "logs"
ENV_FILE = Path.home() / "Content_VentureOracle" / ".env"

MODEL = "gemini-2.5-pro"
MAX_TOKENS = 2048

load_dotenv(ENV_FILE)
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    sys.exit(f"GOOGLE_API_KEY or GEMINI_API_KEY not found in {ENV_FILE}")

client = genai.Client(api_key=api_key)

queries = [
    line.strip()
    for line in QUERIES_FILE.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.strip().startswith("#")
]
print(f"Loaded {len(queries)} queries from {QUERIES_FILE}")

today = datetime.now().strftime("%Y-%m-%d")
out_path = LOGS_DIR / f"run-{today}-gemini-api.md"
out_path.parent.mkdir(parents=True, exist_ok=True)

# Configure Google Search grounding
config = types.GenerateContentConfig(
    tools=[types.Tool(google_search=types.GoogleSearch())],
    max_output_tokens=MAX_TOKENS,
)

results = []
total_input_tokens = 0
total_output_tokens = 0

started_at = datetime.now()

for i, query in enumerate(queries, 1):
    preview = query[:70] + ("…" if len(query) > 70 else "")
    print(f"[{i:2}/{len(queries)}] {preview}")
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=query,
            config=config,
        )
    except Exception as exc:
        results.append({"query": query, "error": str(exc)})
        print(f"    ERROR: {exc}")
        continue

    # Extract text
    text = ""
    try:
        text = response.text or ""
    except Exception:
        # Fallback to candidate parts
        parts = []
        for cand in getattr(response, "candidates", []) or []:
            for part in getattr(cand.content, "parts", []) or []:
                if getattr(part, "text", None):
                    parts.append(part.text)
        text = "\n".join(parts)

    # Extract grounding sources from grounding_metadata
    sources: list[dict] = []
    for cand in getattr(response, "candidates", []) or []:
        gm = getattr(cand, "grounding_metadata", None)
        if not gm:
            continue
        chunks = getattr(gm, "grounding_chunks", []) or []
        for chunk in chunks:
            web = getattr(chunk, "web", None)
            if web:
                sources.append(
                    {
                        "title": getattr(web, "title", "") or "",
                        "url": getattr(web, "uri", "") or "",
                    }
                )

    usage = getattr(response, "usage_metadata", None)
    in_tokens = getattr(usage, "prompt_token_count", 0) if usage else 0
    out_tokens = getattr(usage, "candidates_token_count", 0) if usage else 0

    total_input_tokens += in_tokens
    total_output_tokens += out_tokens

    finish_reason = "unknown"
    for cand in getattr(response, "candidates", []) or []:
        finish_reason = str(getattr(cand, "finish_reason", "unknown"))
        break

    results.append(
        {
            "query": query,
            "response_text": text.strip() or "(no text output)",
            "sources": sources,
            "input_tokens": in_tokens,
            "output_tokens": out_tokens,
            "finish_reason": finish_reason,
        }
    )
    print(f"    ok: {in_tokens}in/{out_tokens}out, {len(sources)} sources")
    time.sleep(0.5)

ended_at = datetime.now()
elapsed = (ended_at - started_at).total_seconds()

# ── Write the log ───────────────────────────────────────────────────────────

def md_escape(s: str) -> str:
    return s.replace("|", "\\|")


lines: list[str] = []
lines.append(f"# GEO Pilot — Gemini 2.5 Pro API run, {today}")
lines.append("")
lines.append(f"**Model:** `{MODEL}`")
lines.append(f"**Tool:** `GoogleSearch` grounding (server-side web retrieval)")
lines.append(f"**SDK:** `google-genai` (unified SDK, not legacy google-generativeai)")
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
    lines.append(f"**Tokens:** {r['input_tokens']:,} in / {r['output_tokens']:,} out  |  **Finish:** `{r['finish_reason']}`")
    lines.append("")
    lines.append("**Response:**")
    lines.append("")
    lines.append(r["response_text"])
    lines.append("")
    if r["sources"]:
        lines.append(f"**Grounding sources cited by Gemini ({len(r['sources'])}):**")
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
        lines.append("**Grounding sources cited by Gemini:** (none)")
        lines.append("")
    lines.append("---")
    lines.append("")

out_path.write_text("\n".join(lines), encoding="utf-8")

print()
print(f"Wrote {out_path}")
print(f"Total tokens: {total_input_tokens:,} in / {total_output_tokens:,} out")
# gemini-2.5-pro: ~$1.25/M input, ~$10/M output + grounding ~$35/1000 calls (tier dependent)
est_cost = (total_input_tokens * 1.25 / 1_000_000) + (total_output_tokens * 10 / 1_000_000) + (len(results) * 0.01)
print(f"Rough cost estimate: ${est_cost:.3f}")
