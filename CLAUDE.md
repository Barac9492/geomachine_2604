# CLAUDE.md — GEOMachine project guardrails

Hand-off notes for any Claude Code session working on this repo.

## Project phase

**Phase 0 — Manual Pilot** (starts Monday 2026-04-13). No automation code yet. If you are being asked to write engine clients, classifiers, or launchd scripts *before* `pilot/assessment-2026-04-27.md` exists with a GO or PIVOT verdict, **stop and ask**. The entire point of Phase 0 is to validate the signal before committing to automation.

**Phase -1 — Fix Indexing** was opened and closed on 2026-04-11 within hours. What looked like a critical indexing crisis (1 of 6 pages indexed, 5 "Redirect error") turned out to be a GSC property-mismatch artifact. The site lives at `www.ventureoracle.kr`; the verified GSC property was non-www; the sitemap referenced non-www URLs. Ethan fixed the root cause at the Next.js source (`sitemap.ts` and `robots.ts` baseUrl → www), committed, Vercel auto-deployed. DuckDuckGo `site:` diagnostic confirmed 8+ pages indexed under the www hostname. Google's GSC view will catch up over 1-28 days as Googlebot recrawls. See `docs/designs/ceo-plan-2026-04-11.md` → "Phase -1 — Fix Indexing" for the full record.

## Indexing history (for future sessions — resolved 2026-04-11, keep as context)

**What it looked like:** GSC (non-www property) showed 1 of 6 pages indexed, 4 flagged "Redirect error", 1 flagged 404, 1 click and 42 impressions in 3 months, and the only query surfacing the site was `oracle ventures` (reversed brand name).

**What it actually was:** A property-mismatch artifact. Site lives at `www.ventureoracle.kr`; verified GSC property was non-www URL-prefix; sitemap listed non-www URLs. Google followed the 301 from non-www to www correctly — pages served fine, content was indexed under the www hostname — but the non-www property couldn't see them because the URLs redirected out of its namespace.

**How it was fixed:** Ethan updated `sitemap.ts` and `robots.ts` in the Next.js project so both point at `https://www.ventureoracle.kr` instead of the non-www version. All 40 sitemap URLs now canonical www. Committed to main, Vercel auto-deployed, GSC re-indexing requested, validation started 2026-04-11.

**Confirmed healthy (via DuckDuckGo diagnostic, same day):**
- `site:www.ventureoracle.kr` returns 8+ indexed pages including `/`, `/predictions`, `/about/ethan-cho`, `/speaking`, `/tools`, `/concepts/mau-trap`, `/concepts/private-credit-ai`
- `site:ventureoracle.kr -site:www.ventureoracle.kr` returns zero results (nothing stranded under non-www)
- DuckDuckGo draws from Bing; AI chat engines with Bing-backed web retrieval (Perplexity, ChatGPT browsing, Bing Chat) can already reach the site

**Still open as housekeeping but not blocking:**
- The 1 remaining 404 page (1 URL of 40, low priority)
- Optional Domain property via DNS verification for cleaner GSC tracking
- Google's GSC view will catch up over 1-28 days as Googlebot recrawls the fixed sitemap
- The 2016 TIPS fraud case reputational-indexing risk remains relevant — separate finding, unrelated to this fix

**What to do if a future session is asked "is the site indexed?":** Don't trust the non-www GSC property. Run `site:www.ventureoracle.kr` on Google or DuckDuckGo instead. That's the authoritative view.

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
