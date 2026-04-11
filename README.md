# GEO Tracker (GEOMachine)

**Owner:** Ethan Cho, CIO, TheVentures
**Status:** **Phase -1 — Fix Indexing** (Phase 0 manual pilot gated on this)
**Started:** 2026-04-11

---

## What this is

A personal instrument for measuring whether the AI engines (ChatGPT, Claude, Perplexity, Gemini) cite Ethan, TheVentures, or the proprietary frameworks on a fixed schedule, and tracking the results as a time series.

Not a product. Not a platform. The instrument that makes the GEO strategy measurable, the content credible, and the eventual SaaS (if it ever ships) defensible.

## Current phase — Phase -1, fix indexing

**Today's state (2026-04-11 GSC baseline):**
- 1 indexed page, 5 not indexed (4 redirect errors + 1 404)
- 1 total click and 42 impressions from Google Search over the last 3 months
- Only one query has ever surfaced ventureoracle.kr in Google: `oracle ventures` (reversed brand name, 0 clicks)
- Core Web Vitals: insufficient traffic to compute

**Why this blocks everything downstream:** AI chat engines with web retrieval (Claude web_search, Perplexity, Gemini grounding, ChatGPT browsing) can only cite pages that exist in Google's index. With 5 of 6 pages rejected, the citation tracker (Phase 0) would measure a site that is essentially invisible to the engines it's designed to query.

**Phase -1 deliverables (before Phase 0 starts):**
1. Fix the 4 redirect errors in GSC → Indexing → Pages
2. Fix the 1 404
3. Click "Validate Fix" on both reason rows
4. Manually request indexing on 3-5 key pages via URL Inspection
5. Submit sitemap.xml
6. Publish content until ≥10 pages are indexed

Full diagnosis, action list, and gating criteria in `docs/designs/ceo-plan-2026-04-11.md` → "Phase -1 — Fix Indexing" block.

## Phase 0 manual pilot — gated on Phase -1 clearance

When Phase -1 clears (≥10 indexed pages), Phase 0 runs as originally scoped: 2 weeks of manual collection against the 18 locked queries in `pilot/queries.yaml`.

- **Week 1:** Monday ~, ~20 minutes (date TBD based on Phase -1 completion)
- **Week 2:** Monday ~, ~20 minutes
- **Go/no-go decision:** Monday ~ (2 weeks after week 1)

The pilot exists because the multi-section CEO review surfaced that the cheapest version of this tool is Ethan manually pasting 18 queries into 4 chat UIs and logging to a sheet. Running it before indexing is fixed would produce predictable zero-signal noise.

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
