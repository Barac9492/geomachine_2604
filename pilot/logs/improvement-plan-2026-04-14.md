# GEO Improvement Plan — 2026-04-14

Based on the 72-cell re-measurement run vs. 2026-04-11 baseline.

## What the re-run tells us

| Signal | Baseline | Now | Read |
|---|---|---|---|
| ventureoracle.kr cells cited | 2 | 3 | Marginal +1 (Perplexity fr-004, Gemini fr-004/fr-006) |
| Framework queries with any hit | 2/6 | 2/6 | Stuck below floor |
| E/D/R hallucinating engines | 2/4 | 0/4 | **Fixed** — the new `/concepts/edr-framework` page displaced the wrong expansions |
| Aggregate citation rate | 50% | 50% | Flat |

**The headline:** one real win (E/D/R hallucination eliminated), one cosmetic win (+1 cell), and four framework queries (fr-001, fr-002, fr-003, fr-005) where no engine cites anyone — including us — because "Founder Intelligence", "E/D/R", and "MAU Trap" are our proprietary terms with no external corpus to draw from yet.

## The actual blocker

**Claude and OpenAI web search find zero ventureoracle.kr content across all 18 queries.** Only Perplexity (Brave/internal) and Gemini (Google grounding) surface the site. This is the ceiling on aggregate rate — until Claude's web search (Brave) and OpenAI's web search (Bing) index the site, two of four engines are structurally locked out.

Corroborating evidence: Perplexity's fr-001 result cites `infounderswords.substack.com/p/founder-intelligence-your-always` — a competing term with the same name — rather than our canonical page. We built the page; crawlers just haven't found it.

## Three-week improvement plan

### P0 — Fix the indexing gap for Claude + OpenAI (week of 2026-04-14)

The root cause is discoverability, not citability. The pages are well-structured; nothing external points at them.

1. **Submit ventureoracle.kr to Bing Webmaster Tools.** OpenAI web search uses Bing. Currently the site is not verified there. Expected lift: unlocks the OpenAI engine entirely. Effort: 15 min.
2. **Submit sitemap to IndexNow** (pings Bing + Yandex + Seznam). One POST per URL. Claude's Brave index ingests IndexNow signals. Expected lift: unlocks Claude. Effort: 30 min script.
3. **Build 6-10 outbound links from Ethan's Substack posts → concept pages.** Every framework mentioned in a Substack post should link to `/concepts/<slug>`. Substack is already in the crawl corpus of all four engines. Expected lift: each link is a discovery path. Effort: 1 hour.
4. **Cross-link concepts from the about/bio page.** The author page at `/about/ethan-cho` should list the 10 concepts as "Frameworks developed" with links. Effort: 30 min template change.

### P1 — Displace competing "Founder Intelligence" content (week of 2026-04-21)

fr-001 / fr-005 return the infounderswords.substack.com entry, not ours. Even if Claude/OpenAI index our page, we need to *outrank* the collision.

1. **Add a disambiguation block to `/concepts/founder-intelligence`** — one paragraph that explicitly states "Not to be confused with the Substack publication of the same name" + the Ethan-authored framework definition repeated verbatim. Disambiguators are extraction signals for AI systems.
2. **Publish one Substack essay titled "Founder Intelligence is not test scores"** with a canonical link back to the concept page. This doubles the corpus surface area under our control.
3. **Add three citations of external authorities** (Kahneman, Thiel, etc.) inside the concept page. Research shows quoted-authority content gets cited 115% more often.

### P2 — Statistical density pass on all 10 concept pages (week of 2026-04-28)

Citability audits on founder-intelligence (55/100) and edr-framework (52/100) both flagged low statistical density. AI engines prefer fact-dense pages.

1. **Add 3-5 verifiable statistics per concept page** from Ethan's 20-year data (IRRs, fund sizes, success rates where publishable). Expected +10 points citability.
2. **Add a comparison table to each concept** ("X vs. traditional VC approach"). Tables extract at 2-3x accuracy.
3. **Re-run citability audit** on all 10 pages to confirm lift.

## Re-measurement gate

Next full 72-cell run: **2026-05-03** (already calendared in `pilot/NEXT_RUN.md`).

Pass criteria for Phase 1 GO:
- ventureoracle.kr cited in ≥4 cells (currently 3)
- Framework queries hitting ≥3 engines (currently 2)
- At least 1 Claude or OpenAI citation of ventureoracle.kr (currently 0/36 cells from those two engines)
- E/D/R hallucination stays at 0/4

If P0 (Bing + IndexNow + Substack backlinks) lands before 2026-05-03, the Claude/OpenAI zero should break. That's the single most important variable.

## What NOT to do

- Don't add more concept pages yet. 10 is enough; we need the existing 10 to actually get indexed.
- Don't rewrite concept page copy further. Current citability audits show the pages are already in the 50s/100 range — good enough if they get crawled. The bottleneck is discovery, not quality.
- Don't run another full 72-cell pilot before 2026-05-03. Cost was ~$3.20 this run; re-running without letting crawlers catch up wastes money and signal.

## Cost this run

- Claude: $2.41
- OpenAI: $0.26
- Perplexity: $0.20
- Gemini: $0.32
- **Total: ~$3.19**

Month-to-date LLM spend on pilot: ~$6.30. Well under the $40 circuit breaker.
