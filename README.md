# GEO Tracker (GEOMachine)

**Owner:** Ethan Cho, CIO, TheVentures
**Status:** Phase 0 — Manual Pilot
**Started:** 2026-04-11

---

## What this is

A personal instrument for measuring whether the AI engines (ChatGPT, Claude, Perplexity, Gemini) cite Ethan, TheVentures, or the proprietary frameworks on a fixed schedule, and tracking the results as a time series.

Not a product. Not a platform. The instrument that makes the GEO strategy measurable, the content credible, and the eventual SaaS (if it ever ships) defensible.

## Current phase — Phase 0 manual pilot

Before any automation is built, this project runs **2 weeks of manual collection** to validate that the signal is worth automating.

- **Week 1:** Monday 2026-04-13, ~20 minutes
- **Week 2:** Monday 2026-04-20, ~20 minutes
- **Go/no-go decision:** Monday 2026-04-27

The pilot exists because the multi-section CEO review surfaced that the cheapest version of this tool is Ethan manually pasting 18 queries into 4 chat UIs and logging to a sheet. If 2 weeks of manual checking shows zero variance across the board, the bottleneck is *content*, not *measurement* — and the 4-6 hours of Claude Code build time should go into writing instead.

See `docs/designs/ceo-plan-2026-04-11.md` for the full review record, rationale, and Phase 1 automation scope (applicable only if Phase 0 returns GO or PIVOT).

## How to run a Phase 0 session

1. Open `pilot/queries.yaml` and confirm the 18 queries are final (nine Ethan-authored, nine demand-seeded — see `pilot/query_research_notes.md`)
2. Create a new file `pilot/logs/run-YYYY-MM-DD.md` from `pilot/pilot_log_template.md`
3. For each query × each of the 4 chat UIs (Claude / ChatGPT / Perplexity / Gemini web):
   - Paste the query as-is
   - Read the response
   - Fill the row: engine / cited? / context / position / competitor names / notes
4. Takes roughly 20 minutes total for all 72 cells (18 queries × 4 engines)
5. Commit the log file when done

## How to run the week-2 assessment

On Monday 2026-04-27, after both weekly logs exist:

1. Open both logs side by side
2. Write `pilot/assessment-2026-04-27.md` — 200 words max covering:
   - How many cells changed between weeks 1 and 2 (out of 72)
   - Were any citations ever found? Where, on which engine, for which query?
   - Was anything surprising about the engines' behavior (refusals, language differences, sourcing patterns)?
   - Decision: **GO** (build automation) / **NO-GO** (archive) / **PIVOT** (competitor-first reframe)
3. Commit the assessment
4. If GO or PIVOT: re-invoke `/plan-ceo-review` or `/plan-eng-review` with the assessment attached
5. If NO-GO: archive this repo and redirect the saved build time into content / ventureoracle.kr SEO

## Repository layout

```
.
├── prd.md                              # Original PRD v0.1
├── README.md                           # This file
├── CLAUDE.md                           # Guardrails for Claude Code sessions
├── .gitignore
├── docs/
│   └── designs/
│       └── ceo-plan-2026-04-11.md      # CEO review record + Phase 1 scope
└── pilot/
    ├── queries.yaml                    # 18 queries to run each Monday
    ├── pilot_log_template.md           # Copy → pilot/logs/run-YYYY-MM-DD.md
    ├── query_research_notes.md         # Demand-seeded query research (GSC / Naver / LinkedIn)
    └── logs/                           # Per-run manual logs (created during pilot)
```

## Links

- Original PRD: [prd.md](./prd.md)
- CEO plan: [docs/designs/ceo-plan-2026-04-11.md](./docs/designs/ceo-plan-2026-04-11.md)
- Sibling project (VentureOracle newsletter engine): `~/Content_VentureOracle/`
