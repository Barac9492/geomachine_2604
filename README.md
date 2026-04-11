# GEO Tracker (GEOMachine)

**Owner:** Ethan Cho, CIO, TheVentures
**Status:** **Phase 0 — Manual Pilot** cleared to start Mon 2026-04-13 (Phase -1 resolved same-day)
**Started:** 2026-04-11

---

## What this is

A personal instrument for measuring whether the AI engines (ChatGPT, Claude, Perplexity, Gemini) cite Ethan, TheVentures, or the proprietary frameworks on a fixed schedule, and tracking the results as a time series.

Not a product. Not a platform. The instrument that makes the GEO strategy measurable, the content credible, and the eventual SaaS (if it ever ships) defensible.

## Phase -1 — indexing fix (CLEARED 2026-04-11)

An earlier version of this README described a critical indexing problem based on GSC's non-www property showing 5 of 6 pages not indexed. **That turned out to be a GSC property-mismatch artifact.** The site lives at `www.ventureoracle.kr` (www). The verified GSC property was `ventureoracle.kr` (non-www URL-prefix). The sitemap listed non-www URLs. Google followed the 301 from non-www to www successfully — pages served fine — but the non-www property couldn't see them because the URLs redirected out of its namespace.

**Fix landed at the source:** `sitemap.ts` and `robots.ts` in the Next.js project were updated to reference `https://www.ventureoracle.kr`. All 40 sitemap URLs now point directly to the www hostname. Committed to main, auto-deployed by Vercel. GSC re-indexing requested, validation started 2026-04-11.

**Confirmation via DuckDuckGo diagnostic (2026-04-11):**
- `site:www.ventureoracle.kr` → 8+ indexed pages including `/`, `/predictions`, `/about/ethan-cho`, `/speaking`, `/tools`, `/concepts/mau-trap`, `/concepts/private-credit-ai`, and the Key Concepts landing
- `site:ventureoracle.kr -site:www.ventureoracle.kr` → zero results (nothing stranded under non-www)
- DuckDuckGo draws from Bing, which powers web retrieval for Perplexity, ChatGPT browsing, and Bing Chat. Site IS retrievable by those engines.

**Outstanding post-Phase-1 housekeeping (not blocking anything):**
- Fix the 1 remaining 404 page (1 URL of 40, low priority)
- Optionally add a Domain property via DNS verification for cleaner GSC tracking going forward
- Wait for Google's GSC view to catch up over the coming 1-28 days as Googlebot recrawls

Full record in `docs/designs/ceo-plan-2026-04-11.md` → "Phase -1 — Fix Indexing" block.

## Phase 0 manual pilot — cleared to start

- **Week 1:** Monday **2026-04-13**, ~20 minutes
- **Week 2:** Monday **2026-04-20**, ~20 minutes
- **Go/no-go decision:** Monday **2026-04-27**

18 queries locked in `pilot/queries.yaml`. 9 Ethan-authored (identity + framework) + 9 demand-seeded (from Naver DataLab, Bing autocomplete, and the Korean VC corpus). Run them manually each Monday, log to a new `pilot/logs/run-YYYY-MM-DD.md` using `pilot/pilot_log_template.md`, then the week-2 assessment triggers the GO / NO-GO / PIVOT decision on whether to build automation.

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
