# CLAUDE.md — GEOMachine project guardrails

Hand-off notes for any Claude Code session working on this repo.

## Project phase

**Phase -1 — Fix Indexing.** Added 2026-04-11 after direct GSC inspection revealed only 1 of 6 ventureoracle.kr pages is indexed by Google and the only query surfacing the site in 3 months is `oracle ventures` (reversed brand name, 0 clicks). The citation tracker (Phase 0 pilot) is gated on at least 10 indexed pages in GSC.

Today's baseline (captured 2026-04-11):
- 1 indexed page, 5 not-indexed pages
- 4 pages blocked by redirect errors, 1 by 404
- 1 click and 42 impressions in 3 months
- Core Web Vitals: no data (insufficient traffic)

**Phase 0 — Manual Pilot.** No automation code yet. Gated on Phase -1 clearance. If you are being asked to write engine clients, classifiers, or launchd scripts *before* `pilot/assessment-2026-04-27.md` exists with a GO or PIVOT verdict AND Phase -1 has cleared, **stop and ask**. The entire point of Phase 0 is to validate the signal before committing to automation, and Phase -1 exists to ensure there IS a signal to validate.

## Indexing context (revised 2026-04-11 after deeper GSC investigation)

**Original finding (superseded):** 5 of 6 pages in the GSC `https://ventureoracle.kr/` property were flagged as not-indexed, 4 for "Redirect error" and 1 for 404.

**Sharpened finding:** The 4 "Redirect error" entries are a **GSC property-mismatch artifact**, not a real crawl failure. The site lives at `https://www.ventureoracle.kr/` (www). The existing GSC property is `https://ventureoracle.kr/` (non-www URL-prefix). The sitemap lists non-www URLs. Google correctly follows the 301 from non-www to www, pages serve fine, and the content is almost certainly already indexed under the www hostname — but the non-www property can't see it because the URL "left the property" via redirect.

**The real fix:** Add a **Domain property via DNS verification** in GSC. This single action covers `https://www.*`, `https://*`, `http://*`, and any future subdomains — and makes the sitemap URL form irrelevant. Google's 2022+ guidance recommends Domain properties as the default for production sites. Details in `docs/designs/ceo-plan-2026-04-11.md` → "Phase -1 deliverables (REVISED)".

**The 1 page 404 is still a real issue** and should be fixed separately (restore, redirect, or remove from sitemap) regardless of the property fix.

**When working in this repo:**
- Phase 0 pilot is gated on the **Domain property** showing ≥10 indexed pages, NOT the non-www URL-prefix property
- Prefer actions that unblock indexing over actions that build automation
- Code for the tracker remains premature until the Domain property baseline is captured
- If you're asked "is the site indexed?", the authoritative check is `site:www.ventureoracle.kr` in Google Search, not the non-www GSC property

## Known reputational indexing risk (surfaced 2026-04-11 during demand seeding)

**The 2016 TheVentures TIPS fraud case is still deeply indexed** in the Korean-language web corpus. Timeline: 호창성 CEO indicted April 2016, acquitted October 2016 at trial, Supreme Court confirmed acquittal February 2018. But Bing autocomplete surfaces `더벤처스 사건` as the #2 suggestion for `더벤처스`, meaning AI engines trained on this corpus may default to the indictment story when asked about TheVentures.

This is a load-bearing context item: the tracker's zero-citation baseline is not just about content volume, it's potentially about *negative* old content dominating the indexing. Queries `dm-003` and `dm-004` in `pilot/queries.yaml` are designed to probe this directly. See `pilot/query_research_notes.md` "Strategic alert" section for the detailed interpretation table.

Strategic implication: if the pilot reveals engines leading with 2016 content, the Q2 2026 content priority shifts toward proactively publishing the acquittal story + the 2026 leadership era, regardless of what the framework-query pilot results show.

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
