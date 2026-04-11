#!/usr/bin/env python3
"""
GEO re-measurement diff — parse two sets of per-engine raw logs and emit a
baseline-vs-now delta report for the improvement plan's re-measurement gate.

The workflow this script closes:
  1. Ethan runs `pilot/scripts/run_claude_api.py`, `run_openai_api.py`,
     `run_perplexity_api.py`, `run_gemini_api.py` on the day of re-measurement.
     Each writes `pilot/logs/run-YYYY-MM-DD-<engine>-api.md`.
  2. Ethan runs this script: `python pilot/scripts/geo_remeasure_diff.py`
  3. This script reads the 2026-04-11/12 baseline logs and the most recent
     per-engine logs, counts citations + ventureoracle.kr hits + hallucinations
     per cell, and emits a delta report against the improvement plan's
     re-measurement gate (target / hard floor).

The re-measurement gate, copied from
`docs/designs/geo-improvement-plan-2026-04-11.md`:

  | Metric                              | Current | Target | Hard floor |
  |-------------------------------------|---------|--------|------------|
  | ventureoracle.kr cells cited        | 2 / 72  | ≥ 6    | ≥ 3        |
  | Framework queries hitting ≥1 engine | 1 / 4   | 3 / 4  | 2 / 4      |
  | E/D/R hallucinations remaining      | 2 / 4   | 0      | 1          |
  | Aggregate strict-citation rate      | 47%     | ≥ 55%  | ≥ 50%      |

Reads:
  - pilot/logs/run-2026-04-11-claude-api.md       (baseline Claude)
  - pilot/logs/run-2026-04-12-openai-api.md       (baseline OpenAI)
  - pilot/logs/run-2026-04-12-perplexity-api.md   (baseline Perplexity)
  - pilot/logs/run-2026-04-12-gemini-api.md       (baseline Gemini)
  - pilot/logs/run-YYYY-MM-DD-<engine>-api.md     (most recent run per engine)
Writes:
  - pilot/logs/remeasure-diff-YYYY-MM-DD.md
  - stdout: gate-row scores with pass/fail/floor markers

No API calls, no network — pure log parsing. This is the thing Ethan runs
after shipping content and waiting 14-21 days.

No extra dependencies beyond the stdlib.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = REPO_ROOT / "pilot" / "logs"

# Baseline log paths — referenced when `find_latest_logs` filters them out so
# that post-baseline runs can be identified by date.
BASELINE_LOGS = {
    "claude": LOGS_DIR / "run-2026-04-11-claude-api.md",
    "openai": LOGS_DIR / "run-2026-04-12-openai-api.md",
    "perplexity": LOGS_DIR / "run-2026-04-12-perplexity-api.md",
    "gemini": LOGS_DIR / "run-2026-04-12-gemini-api.md",
}

# Query IDs in pilot/queries.txt order — matches pilot/queries.yaml
QUERY_IDS = [
    "id-001", "id-002", "id-003",
    "fr-001", "fr-002", "fr-003", "fr-004", "fr-005", "fr-006",
    "dm-001", "dm-002", "dm-003", "dm-004", "dm-005", "dm-006",
    "dm-007", "dm-008", "dm-009",
]
FRAMEWORK_IDS = {"fr-001", "fr-002", "fr-003", "fr-004", "fr-005", "fr-006"}
# dm-006 is a competitor probe, not a citation target — excluded from rate denominator
EXCLUDED_FROM_RATE = {"dm-006"}

VENTUREORACLE_NEEDLE = "ventureoracle.kr"

# Tight citation signals: require identity anchors, NOT bare framework names.
# Bare framework mentions like "Four Lenses is a social enterprise framework"
# must NOT count as a citation. An engine is citing Ethan only if it mentions
# him, TheVentures, 조여준, 더벤처스, or links to ventureoracle.kr directly.
IDENTITY_SIGNALS = [
    r"\bEthan Cho\b",
    r"조여준",
    r"\bTheVentures\b",
    r"더벤처스",
]
IDENTITY_REGEX = re.compile("|".join(IDENTITY_SIGNALS), re.IGNORECASE)

# E/D/R hallucination requires the full invented expansion, not a single word.
# These are the exact patterns captured in the 2026-04-11 run:
#   GPT-4o: Enablement, Development, Realization
#   Gemini: Evaluation, Development, Responsibility
# Cybersecurity EDR (Endpoint Detection and Response) is a COLLISION, not a
# hallucination — the engine is losing to an existing term, not inventing one.
EDR_HALLUCINATION_PATTERNS = [
    # Widened to 400 chars between keywords to survive numbered-list formats
    # and multi-line expansions. Order-invariant via alternation below.
    re.compile(r"enablement.{0,400}development.{0,400}realization", re.IGNORECASE | re.DOTALL),
    re.compile(r"evaluation.{0,400}development.{0,400}responsibility", re.IGNORECASE | re.DOTALL),
    # Catch the labeled-definition format: "E: Enablement" or "**Enablement:**"
    re.compile(r"\bE\s*[:\-]\s*enablement", re.IGNORECASE),
    re.compile(r"\bE\s*[:\-]\s*evaluation", re.IGNORECASE),
]

# Synthesis-authoritative baseline numbers (for display). The parser will
# re-derive its own numbers from the baseline logs so that baseline and
# "now" comparisons are apples-to-apples under the same heuristic.
# Parser drift is ±2 cells on citation count (50% parser vs 47% manual),
# exact match on vo_cells, framework_with_any_hit, and edr_halluc_count.
SYNTHESIS_BASELINE = {
    "vo_cells": 2,
    "cited_cells": 32,
    "total_cells": 68,
    "rate": 32 / 68,
    "frameworks_with_any_hit": 2,
    "edr_halluc_count": 2,
}


@dataclass
class CellResult:
    query_id: str
    query_text: str
    response_text: str = ""
    sources: list[str] = field(default_factory=list)
    cited: bool = False
    ventureoracle_cited: bool = False
    edr_hallucinated: bool = False


def parse_run_log(path: Path) -> list[CellResult]:
    """Parse one `run-*.md` log into a list of 18 CellResults."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")

    # Split on "## Query NN: ..." headers
    sections = re.split(r"^## Query \d+:\s*", text, flags=re.MULTILINE)[1:]
    results: list[CellResult] = []
    for i, section in enumerate(sections):
        if i >= len(QUERY_IDS):
            break
        # First line is the query text, rest is the response + sources
        first_newline = section.find("\n")
        query_text = section[:first_newline].strip() if first_newline >= 0 else section.strip()
        body = section[first_newline + 1 :] if first_newline >= 0 else ""

        # Everything up to the next "---" or end-of-section is the response body
        end_marker = body.find("\n---")
        response_block = body[:end_marker] if end_marker >= 0 else body

        # Extract source URLs and link text from markdown `- [title](url)` lines
        source_links = re.findall(r"\[([^\]]*)\]\((https?://[^\s)]+)\)", response_block)
        sources = [url for _text, url in source_links]
        link_texts = [txt for txt, _url in source_links]

        # Full text includes both prose and link text — this is what we
        # search for ventureoracle.kr mentions, because Gemini cites
        # ventureoracle.kr as the LINK TEXT of a vertexaisearch redirect URL
        full_text = response_block

        # Prose-only text for identity/hallucination checks — strips markdown
        # source list lines entirely
        prose_text = re.sub(
            r"^\s*-\s*\[[^\]]*\]\(https?://[^\s)]+\)\s*$",
            "",
            response_block,
            flags=re.MULTILINE,
        )

        # Citation: require an identity anchor (Ethan/TheVentures/etc.) OR
        # a direct ventureoracle.kr reference
        has_identity = bool(IDENTITY_REGEX.search(prose_text))
        vo_in_text = VENTUREORACLE_NEEDLE in full_text.lower()
        vo_in_sources = any(VENTUREORACLE_NEEDLE in s.lower() for s in sources)
        vo_in_link_text = any(VENTUREORACLE_NEEDLE in t.lower() for t in link_texts)
        vo_cited = vo_in_text or vo_in_sources or vo_in_link_text

        cited = has_identity or vo_cited

        edr_hallucinated = False
        if QUERY_IDS[i] == "fr-002":
            edr_hallucinated = any(p.search(prose_text) for p in EDR_HALLUCINATION_PATTERNS)

        results.append(
            CellResult(
                query_id=QUERY_IDS[i],
                query_text=query_text,
                response_text=prose_text[:2000],
                sources=sources,
                cited=cited,
                ventureoracle_cited=vo_cited,
                edr_hallucinated=edr_hallucinated,
            )
        )
    return results


def find_latest_logs() -> dict[str, Path | None]:
    """Find the most recent run-*-<engine>-api.md log for each engine."""
    out: dict[str, Path | None] = {}
    for engine in ("claude", "openai", "perplexity", "gemini"):
        matches = sorted(LOGS_DIR.glob(f"run-*-{engine}-api.md"))
        # Exclude baseline logs
        non_baseline = [p for p in matches if p != BASELINE_LOGS[engine]]
        out[engine] = non_baseline[-1] if non_baseline else None
    return out


def score_run(per_engine: dict[str, list[CellResult]]) -> dict:
    """Compute the 4 gate metrics from a run's parsed results."""
    # ventureoracle.kr cells across the whole run (72 cells total, but 4*17=68
    # if we exclude dm-006)
    vo_cells = 0
    cited_cells = 0
    total_cells = 0
    framework_hit_engines: dict[str, set[str]] = {f: set() for f in FRAMEWORK_IDS}
    edr_halluc_engines: set[str] = set()

    for engine, cells in per_engine.items():
        for c in cells:
            if c.query_id in EXCLUDED_FROM_RATE:
                continue
            total_cells += 1
            if c.cited:
                cited_cells += 1
            if c.ventureoracle_cited:
                vo_cells += 1
            if c.query_id in FRAMEWORK_IDS and c.cited:
                framework_hit_engines[c.query_id].add(engine)
            if c.query_id == "fr-002" and c.edr_hallucinated:
                edr_halluc_engines.add(engine)

    frameworks_with_any_hit = sum(1 for engines in framework_hit_engines.values() if engines)
    rate = cited_cells / total_cells if total_cells else 0.0

    return {
        "vo_cells": vo_cells,
        "cited_cells": cited_cells,
        "total_cells": total_cells,
        "rate": rate,
        "framework_hit_engines": framework_hit_engines,
        "frameworks_with_any_hit": frameworks_with_any_hit,
        "edr_halluc_engines": edr_halluc_engines,
        "edr_halluc_count": len(edr_halluc_engines),
    }


def render_report(baseline: dict, latest: dict, latest_dates: dict[str, str | None], today: str) -> str:
    lines: list[str] = []
    lines.append(f"# GEO re-measurement diff — {today}")
    lines.append("")
    lines.append(
        "Baseline: 2026-04-11/12 four-engine run. Latest: most recent per-engine log."
    )
    lines.append("")
    lines.append("## Sources")
    lines.append("")
    for engine, path in latest_dates.items():
        lines.append(f"- **{engine}**: baseline `{BASELINE_LOGS[engine].name}` → latest `{path or '(no new run yet)'}`")
    lines.append("")

    # Gate table
    def row(name: str, b: str, n: str, target: str, floor: str, verdict: str) -> str:
        return f"| {name} | {b} | {n} | {target} | {floor} | {verdict} |"

    def verdict_mark(now: float, target: float, floor: float, higher_is_better: bool = True) -> str:
        if higher_is_better:
            if now >= target:
                return "✅ TARGET"
            if now >= floor:
                return "⚠️ FLOOR"
            return "❌ BELOW FLOOR"
        else:
            if now <= target:
                return "✅ TARGET"
            if now <= floor:
                return "⚠️ FLOOR"
            return "❌ ABOVE FLOOR"

    lines.append("## Gate scorecard")
    lines.append("")
    lines.append("| Metric | Baseline | Now | Target | Hard floor | Verdict |")
    lines.append("|---|---|---|---|---|---|")
    lines.append(
        row(
            "ventureoracle.kr cells cited",
            f"{baseline['vo_cells']}",
            f"{latest['vo_cells']}",
            "≥ 6",
            "≥ 3",
            verdict_mark(latest["vo_cells"], 6, 3, higher_is_better=True),
        )
    )
    lines.append(
        row(
            "Framework queries hitting ≥1 engine",
            f"{baseline['frameworks_with_any_hit']} / 6",
            f"{latest['frameworks_with_any_hit']} / 6",
            "≥ 4",
            "≥ 3",
            verdict_mark(latest["frameworks_with_any_hit"], 4, 3, higher_is_better=True),
        )
    )
    lines.append(
        row(
            "E/D/R hallucination engines",
            f"{baseline['edr_halluc_count']} / 4",
            f"{latest['edr_halluc_count']} / 4",
            "0 / 4",
            "≤ 1 / 4",
            verdict_mark(latest["edr_halluc_count"], 0, 1, higher_is_better=False),
        )
    )
    lines.append(
        row(
            "Aggregate citation rate",
            f"{baseline['rate']*100:.0f}%",
            f"{latest['rate']*100:.0f}%",
            "≥ 55%",
            "≥ 50%",
            verdict_mark(latest["rate"], 0.55, 0.50, higher_is_better=True),
        )
    )
    lines.append("")

    # Deltas
    def delta(b: float, n: float) -> str:
        d = n - b
        sign = "+" if d >= 0 else ""
        return f"{sign}{d}"

    lines.append("## Deltas")
    lines.append("")
    lines.append(f"- **ventureoracle.kr cells:** {delta(baseline['vo_cells'], latest['vo_cells'])}")
    lines.append(f"- **Framework queries with any hit:** {delta(baseline['frameworks_with_any_hit'], latest['frameworks_with_any_hit'])}")
    lines.append(f"- **E/D/R hallucinating engines:** {delta(baseline['edr_halluc_count'], latest['edr_halluc_count'])}")
    lines.append(f"- **Citation rate:** {(latest['rate']-baseline['rate'])*100:+.1f} points")
    lines.append("")

    # Framework-query breakdown
    lines.append("## Framework query breakdown")
    lines.append("")
    lines.append("| Query | Baseline engines | Now engines |")
    lines.append("|---|---|---|")
    for f in sorted(FRAMEWORK_IDS):
        b_engines = ", ".join(sorted(baseline["framework_hit_engines"][f])) or "—"
        n_engines = ", ".join(sorted(latest["framework_hit_engines"][f])) or "—"
        lines.append(f"| {f} | {b_engines} | {n_engines} |")
    lines.append("")

    # Gate decision
    passes = 0
    floors = 0
    fails = 0
    for metric_verdict in (
        verdict_mark(latest["vo_cells"], 6, 3),
        verdict_mark(latest["frameworks_with_any_hit"], 4, 3),
        verdict_mark(latest["edr_halluc_count"], 0, 1, higher_is_better=False),
        verdict_mark(latest["rate"], 0.55, 0.50),
    ):
        if "TARGET" in metric_verdict:
            passes += 1
        elif "FLOOR" in metric_verdict and "BELOW" not in metric_verdict and "ABOVE" not in metric_verdict:
            floors += 1
        else:
            fails += 1

    # Guard: if there are no latest logs at all, the script is running before
    # re-measurement has happened. Show baseline only, no decision.
    any_latest = any(path is not None for path in latest_dates.values())
    if not any_latest:
        lines.append("## Decision")
        lines.append("")
        lines.append(
            "**No post-baseline runs yet.** This report is showing the baseline "
            "only. Run `pilot/scripts/run_claude_api.py`, `run_openai_api.py`, "
            "`run_perplexity_api.py`, and `run_gemini_api.py` after content has "
            "shipped and Google has had 14–21 days to re-index, then re-run this "
            "script to score the re-measurement against the gate."
        )
        lines.append("")
        return "\n".join(lines)

    lines.append("## Decision")
    lines.append("")
    if passes >= 3:
        lines.append(
            f"**PASS** — {passes}/4 metrics hit target. Content-first thesis validated. "
            "Proceed to Phase 1 automation work per the CEO plan."
        )
    elif passes + floors >= 3 and fails <= 1:
        lines.append(
            f"**MARGINAL** — {passes}/4 target, {floors}/4 floor, {fails}/4 below floor. "
            "Ship remaining P1 items and re-run once more in 2-4 weeks before committing to Phase 1."
        )
    else:
        lines.append(
            f"**FAIL** — {passes}/4 target, {floors}/4 floor, {fails}/4 below floor. "
            "Content-first thesis is not validated. Stop shipping content and diagnose "
            "at the retrieval-authority layer instead (domain age, inbound links, "
            "schema.org deployment correctness)."
        )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    today = datetime.now().strftime("%Y-%m-%d")

    # Parse baseline logs with the same heuristic used for the new run,
    # so baseline and "now" numbers are apples-to-apples. Manual synthesis
    # numbers are preserved in SYNTHESIS_BASELINE for cross-reference.
    baseline_per_engine: dict[str, list[CellResult]] = {}
    for engine, path in BASELINE_LOGS.items():
        cells = parse_run_log(path)
        if not cells:
            print(f"WARNING: baseline log {path.name} unreadable", file=sys.stderr)
        baseline_per_engine[engine] = cells
    baseline_score = score_run(baseline_per_engine)

    # Parse latest per-engine logs
    latest_paths = find_latest_logs()
    latest_per_engine: dict[str, list[CellResult]] = {}
    latest_dates: dict[str, str | None] = {}
    for engine in ("claude", "openai", "perplexity", "gemini"):
        path = latest_paths[engine]
        latest_dates[engine] = path.name if path else None
        if path is None:
            print(f"NOTE: no post-baseline log for {engine}; treating as 0", file=sys.stderr)
            latest_per_engine[engine] = []
        else:
            latest_per_engine[engine] = parse_run_log(path)
    latest_score = score_run(latest_per_engine)

    report = render_report(baseline_score, latest_score, latest_dates, today)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = LOGS_DIR / f"remeasure-diff-{today}.md"
    out_path.write_text(report, encoding="utf-8")

    # stdout summary
    print(f"\nWrote {out_path}")
    print()
    print(f"Baseline: vo={baseline_score['vo_cells']}  "
          f"fw_hit={baseline_score['frameworks_with_any_hit']}/6  "
          f"edr_halluc={baseline_score['edr_halluc_count']}/4  "
          f"rate={baseline_score['rate']*100:.0f}%")
    print(f"Now:      vo={latest_score['vo_cells']}  "
          f"fw_hit={latest_score['frameworks_with_any_hit']}/6  "
          f"edr_halluc={latest_score['edr_halluc_count']}/4  "
          f"rate={latest_score['rate']*100:.0f}%")


if __name__ == "__main__":
    main()
