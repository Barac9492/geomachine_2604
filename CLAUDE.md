# CLAUDE.md — GEOMachine project guardrails

Hand-off notes for any Claude Code session working on this repo.

## Project phase

**Phase 0 — Manual Pilot.** No automation code yet. If you are being asked to write engine clients, classifiers, or launchd scripts *before* `pilot/assessment-2026-04-27.md` exists with a GO or PIVOT verdict, **stop and ask**. The entire point of Phase 0 is to validate the signal before committing to automation.

## Strategic guardrails (from CEO review 2026-04-11)

1. **< 2 hours / month operating budget.** This is the VentureOracle core principle. Every design decision must preserve it. Obsidian is the primary reporting surface. Slack is the alert layer. **No hosted dashboards, no email for v1.**
2. **"No code reading required."** `pilot/queries.yaml` and eventually `config/venture_oracle_pages.yaml` are the only files Ethan should need to edit. Hide everything else behind defaults.
3. **Zero-citation is the 80% case** for the first 3-6 months. Design the weekly digest for "still zero" first, "big spike" second. A boring zero-digest will get ignored and kill the feedback loop.
4. **Local execution over hosted.** The tool reads/writes a local Obsidian vault. Any attempt to push execution to Railway needs to resolve the filesystem mismatch first.
5. **Private competitor data only.** The public quarterly report talks about Ethan — citations, frameworks, trends. Named competitor comparisons stay in the private SQLite file, never published.
6. **GEO module is process-isolated** from the sibling `Content_VentureOracle` codebase when Phase 1 begins. Zero Python-level imports across project boundaries. Copy small utilities, don't import.

## Decision rules for Phase 1 automation (if/when it starts)

- Classifier model: Claude Haiku, dated snapshot pinned. `temperature=0` where supported.
- For Claude and Perplexity (which drift at temp=0), run N=3 calls per query and majority-vote.
- Cross-check 10% of classifier samples weekly with GPT-4o. Alert if disagreement > 15%.
- Replace hard rate thresholds with a one-sided binomial significance test (p < 0.10) before the content feedback loop fires.
- Time-weighted delta math (rate per day since last successful run), not run-to-run.
- Cost circuit breaker: abort any run that projects > $40 month-to-date LLM spend.
- SQLite schema: versioned via a `schema_version` table from day 1. No ad-hoc ALTERs.
- Run lockfile at `data/.geo_run.lock`. Stale after 2h triggers clear + alert.
- launchd wake caveat: accept ≤ 4 missed runs / 90 days OR install `pmset repeat wakeorpoweron` as a sudo one-liner.
- GPT-4o disagreement, classifier drift sample, celebration state (first citation ever), and regression alarm state all surface in the Slack digest, not just in a log file.

## Workflow

- Read `docs/designs/ceo-plan-2026-04-11.md` before modifying scope. Every decision in there has a trail.
- Any scope change requires updating that document's `Scope Decisions` table + re-running `/plan-ceo-review`.
- Pilot logs are authoritative during Phase 0. Do not interpolate or "tidy" them.
- `prd.md` is a historical artifact (v0.1). Updates to scope go in the CEO plan, not the PRD.

## What "done" looks like for Phase 0

A file at `pilot/assessment-2026-04-27.md` with a GO / NO-GO / PIVOT verdict, backed by the 2 weekly logs under `pilot/logs/`.

## What NOT to do

- Do not write Python code for engine clients, classifiers, or any `src/geo/` module before Phase 0 closes.
- Do not push the tracker's execution to Railway; the Obsidian filesystem dilemma was already adjudicated.
- Do not expand the query list beyond 18 during the pilot — the whole point is a fixed baseline.
- Do not skip the manual logs in favor of "I'll just script it really quick." That defeats the pilot.
- Do not commit `geo.db` or any raw API response file if/when Phase 1 begins (see `.gitignore`).
