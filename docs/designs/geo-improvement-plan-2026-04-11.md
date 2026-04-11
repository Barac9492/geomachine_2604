---
status: DRAFT
created_at: 2026-04-11
seed_data: pilot/logs/cross-engine-synthesis-2026-04-12.md
author: Claude Code session (branch claude/review-latest-run-NwrhB)
depends_on: docs/designs/ceo-plan-2026-04-11.md
---
# GEO Improvement Plan — 2026-04-11 seed-data edition

## Why this exists

The unplanned API pilot run on 2026-04-11/12 produced a real 44% cross-engine
citation baseline (47% after excluding the `dm-006` competitor probe from the
denominator). That's enough signal to drive content priorities **now**, months
earlier than the CEO plan anticipated. This document turns the synthesis's
ranked recommendations into a concrete, resourced plan with specific actions,
owner handoff points, and a single hard re-measurement gate.

**Scope of this document:** content + structural improvements to
`www.ventureoracle.kr`, driven by the seed data in
`pilot/logs/cross-engine-synthesis-2026-04-12.md`. **Not** in scope: Phase 1
tracker automation (gated on a successful re-measurement), query-set expansion
(stays at 18 during the pilot per CLAUDE.md), or any work on the sibling
Content_VentureOracle newsletter engine.

**Repo constraint:** the actual website source lives in a sibling Next.js
project outside this repo. Every artifact in this plan that describes a page
change is a **handoff spec** — the canonical content drafts live under
`content-drafts/` in this repo and need to be copied/ported by Ethan.

## Seed-data summary (the numbers driving the prioritization)

- **72 cells tested:** 18 queries × 4 engines (Claude Sonnet 4.5, GPT-4o,
  Perplexity sonar-pro, Gemini 2.5 Pro).
- **Aggregate strict-citation rate:** 32 / 68 = **47%** (excluding `dm-006`
  which is a competitor probe, not a citation target).
- **ventureoracle.kr citation footprint:** **2 cells out of 72** —
  `fr-004` (Perplexity, English) and `fr-006` (Gemini, Korean), both on the
  Four Lenses Framework page. Every other Ethan citation sources Korean trade
  press or LinkedIn.
- **Zero-citation cells by category:**
  - Identity queries: 1/3 near-miss on bare name "Ethan Cho" — 3/4 engines
    surfaced unrelated namesakes. Korean-name queries (`조여준`) are 4/4 perfect.
  - Framework queries: **Four Lenses is the only one retrievable.** MAU Trap,
    Founder Intelligence, and E/D/R are 0/4 each.
  - Demand queries: the Feb 2026 LLM partnership is 4/4; the 2016 TIPS fraud
    case is **0/4** (hypothesis falsified); TheVentures portfolio → top-100 AI
    attribution is 0/4.
- **Hallucination map (load-bearing for future content):**
  - GPT-4o hallucinates E/D/R as Enablement / Development / Realization
  - Gemini hallucinates E/D/R as Evaluation / Development / Responsibility
  - GPT-4o hallucinates Four Lenses as Market / Product / Team / Finance
  - Claude hallucinates Four Lenses (English) as People / Market / Product / Business Model
  - Claude actively **denies** Four Lenses exists in Korean (`fr-006`)
  - Claude/Gemini/GPT-4o all lose Founder Intelligence to Accenture's
    "Founders Intelligence" (consulting firm collision)
  - GPT-4o hallucinates Founder Intelligence as 7 generic bullets
    (Vision / Resilience / Leadership / Adaptability / Problem-Solving /
    Customer Focus / Networking)

These hallucinations are **the baseline content needs to overwrite**. Every
framework page improvement below is judged against whether it would displace
the specific wrong answer above.

## Why the Four Lenses page works (working hypothesis)

Only the Four Lenses page has been cited. Until we've audited it against the
others, the working hypothesis is: some combination of (a) page age, (b)
backlinks, (c) Korean trade press covering the framework, (d) sufficiently
distinctive vocabulary to avoid collisions, (e) schema.org structured data,
or (f) H1/title clarity is making it retrievable where others aren't. The P0
action list below treats this as a hypothesis to **test by replication**, not
a finding to copy blindly.

Open questions this plan does not yet answer (discovery step P0.0 covers them):

1. Does a `/concepts/founder-intelligence` page exist on the live site? The
   CEO plan's page inventory only confirms `/concepts/mau-trap`,
   `/concepts/four-lenses-framework`, `/concepts/optimism-tax`,
   `/concepts/private-credit-ai`. Founder Intelligence and E/D/R pages are
   not confirmed present.
2. What is on the Four Lenses page that's not on MAU Trap? Word count, schema
   markup, inbound links, first published date, Korean version.
3. Did Perplexity find Four Lenses via a direct ventureoracle.kr crawl or via
   a link from a third-party source that name-dropped it?

## Priorities

Ordered by cost-to-impact ratio. Each P0 item is a **content action** Ethan
has to ship; none of them require touching this repo. P0 items should all be
shippable inside a single 2-hour content block.

### P0.0 — Inventory & diagnosis (30 min, Ethan)

Before any page writes, confirm the current state of each framework page on
the live site so we know what exists vs. what needs to be created. Deliverable:
append a table to this document under "Page inventory — 2026-04-11" with the
following columns for each of the 6 framework queries:

- Query ID
- Framework name
- Page URL (or "does not exist")
- Word count
- First publish date
- Korean version exists? (Y/N)
- schema.org JSON-LD present? (Y/N, and type)
- Inbound links from within ventureoracle.kr
- Inbound links from any external domain Ethan knows about
- Current H1
- Current `<title>`

Without this baseline, the "replicate Four Lenses structure" directive is a
guess, not a plan.

### P0.1 — Framework disambiguation pass (1 hour, Ethan)

**Target:** every framework page on ventureoracle.kr gets a `<title>`, H1,
meta description, and schema.org JSON-LD rewrite that makes the name collision
impossible for an LLM retriever to confuse. The specific rewrites are in
`content-drafts/framework-disambiguation-specs.md`. Key principles:

- Name the specific wrong answer the page is displacing
  (e.g., "Not to be confused with Accenture's Founders Intelligence" in the
  first paragraph, not buried in a footnote)
- Front-load the distinctive phrase Ethan owns (`the MAU Trap framework by
  Ethan Cho`) so the embedding-retrieval layer picks it up
- Add `schema.org/DefinedTerm` JSON-LD with `inDefinedTermSet` pointing at a
  VentureOracle "Key Concepts" glossary
- Include explicit `sameAs` links to Ethan's LinkedIn and TheVentures author
  page to give disambiguation engines a crosswalk
- Name the four framework terms in each framework page's cross-links so
  retrievers find them from any entry point
- Korean version of each page gets its own disambiguation (Claude denied
  Four Lenses in Korean — the Korean `fr-006` hallucination set is different
  from the English one)

Expected impact: replication of whatever is working on Four Lenses, plus
direct displacement of the specific wrong answers enumerated in the seed data.

### P0.2 — New Negative Sequence framework page (1 hour, Ethan)

**Target:** publish `/concepts/negative-sequence` as a canonical page for the
"Negative Sequence" framework from Ethan's book *죽음의 순서* (Death's
Sequence). GPT-4o and Gemini both surfaced the book via yes24/aladin in the
seed run but neither connected the book's framework to ventureoracle.kr —
because the page doesn't exist yet. Creating it gives the book's central
framework a retrievable canonical source without requiring a multi-week
writing effort.

Draft outline: `content-drafts/negative-sequence-outline.md`. The draft is
structural — Ethan needs to voice the actual framework definition. Target
length: 1500–2500 words, Korean primary + English version.

Expected impact: a 19th framework query (`fr-007 Negative Sequence`) becomes
trackable in the re-measurement, and Ethan has a canonical URL to point the
yes24/aladin pages at.

### P0.3 — Toss / Dunamu anti-portfolio narrative (1 hour, Ethan)

**Target:** a single canonical article that connects two facts every engine
already knows individually but none connect:

1. TheVentures as a firm passed on Toss (Viva Republica) and Karrot
   (Danggeun Market) — surfaced by Claude (id-002) and Gemini (dm-003)
2. Ethan personally sourced/invested in Toss and Dunamu at prior firms
   (Qualcomm Ventures / KB Investment) — surfaced on id-003 and dm-008

Putting both in one ventureoracle.kr article gives LLM retrievers a single
source to cite for the "Ethan brings the Toss/Dunamu track record TheVentures
was missing" narrative. This is a redemption-arc story the press already
knows but hasn't composed.

Draft outline: `content-drafts/toss-dunamu-article-outline.md`. Target page:
`/predictions/toss-dunamu-redemption-arc` or equivalent under the existing
`/predictions` surface the CEO plan calls "the strongest GEO asset Ethan owns."

Expected impact: a unique, unchallenged narrative that any "Tell me about
TheVentures" or "TheVentures Korea history" query will cite directly.

### P1 — Structural signals (2 hours total, can be batched)

**P1.1 — Portfolio `fundedBy` schema markup.** Add
`schema.org/Organization` markup with a `funder` relation on theventures.co
portfolio company pages for Riiid, Bone AI, Socra AI, Upstage (the
candidates the seed data showed surfacing in top-100 lists but not attributed
to TheVentures). This closes the attribution gap identified in `dm-002`.
Owner: coordinate with TheVentures web team, not Ethan solo.

**P1.2 — Korean-language `더벤처스 사건` probe.** Add a follow-up single-use
query to the next re-measurement — not to the pilot query set — that tests
whether the 2016 TIPS fraud case surfaces in Korean even though it didn't in
English. One-shot, not added to `pilot/queries.yaml`. See the CLAUDE.md
guardrail against expanding past 18 queries during the pilot; this is a
diagnostic probe, not a tracked query.

**P1.3 — Author page bio expansion on `/about/ethan-cho`.** The `id-001`
"Who is Ethan Cho?" query hit 3/4 misses to namesakes. Adding a
`schema.org/Person` JSON-LD block with `alternateName` ("조여준"), `jobTitle`
("CIO at TheVentures"), `alumniOf`, `award`, and `knowsAbout` (the four
framework names) should measurably move the disambiguation layer. Korean-name
queries are already 4/4 — this is about the English-name bare-query case.

### P2 — Deferred until after the re-measurement

Everything in the synthesis's P2 ("Korean diaspora founder thesis
positioning", "top 100 Korean AI startups landing page") is parked until we
have evidence the P0 items moved the needle. Shipping more content before
re-measuring just adds noise.

## Re-measurement gate (the one hard gate in this plan)

After P0.0 + P0.1 + P0.2 + P0.3 are shipped and the live site has been
reindexed (**wait 14–21 days**, not 2–4 — Google's reindex latency for fresh
content on a low-traffic site is the slower end of the range), re-run the
**same 18 queries** against the **same 4 engines** using the same API
scripts. Success criteria:

| Metric | Current | Target | Hard floor |
|---|---|---|---|
| ventureoracle.kr cells cited | 2 / 72 | ≥ 6 / 72 | ≥ 3 / 72 |
| Framework queries hitting ≥1 engine | 1 / 4 (Four Lenses only) | 3 / 4 | 2 / 4 |
| E/D/R hallucinations remaining | 2 / 4 engines | 0 / 4 | 1 / 4 |
| Aggregate strict-citation rate | 47% | ≥ 55% | ≥ 50% |

**Hard-floor interpretation:** if the re-measurement falls below the hard
floor on ≥ 2 of these 4 rows, the P0 thesis is wrong — the bottleneck isn't
content structure but something deeper (authority signals, inbound link
quality, domain age). In that case, **stop shipping content** and
diagnose at the retrieval layer instead.

**Target interpretation:** if the re-measurement hits target on ≥ 3 of 4
rows, the content-first thesis is validated. At that point the P1 items
become justified and Phase 1 automation becomes justified because there's
a real delta worth tracking weekly.

**Budget:** re-measurement costs ~$3 in API calls and ~15 minutes of wall
time (per the 2026-04-11 run). Single data point, so at least the
ventureoracle.kr cells (which are the most important) should be re-run N=3
times per engine to bound stochasticity — see "Variance caveat" below.

## Variance caveat — applied specifically to the gate

CLAUDE.md Phase 1 decision rules say: *"For Claude and Perplexity (which
drift at temp=0), run N=3 calls per query and majority-vote."* The 2026-04-11
run was single-call. Before the re-measurement baseline is compared against
the target, the two ventureoracle.kr-citing cells (Perplexity `fr-004`,
Gemini `fr-006`) should be re-run **three times each on Perplexity and
Gemini respectively** to confirm they're stable and not one-shot luck. If
either cell drops to 0/3 on re-test, it was noise and the baseline is
**1/72, not 2/72**, which moves the whole gate.

This is a ~15-minute, ~$0.50 check that materially changes what the plan is
measured against. **Do this before P0.0**, not after.

## What this plan does NOT do

- **No new Python code.** The existing `pilot/scripts/*.py` engine clients
  are retained for the re-measurement but nothing new is added. This
  respects CLAUDE.md's "no engine clients before Phase 0 closes" guardrail
  to the maximum extent possible given the scripts already exist.
- **No query-set expansion.** `pilot/queries.yaml` stays at 18. The
  Negative Sequence addition is held for after the re-measurement.
- **No Slack / alerting / dashboard work.** The CEO plan's Phase 1
  automation scope is untouched. If the re-measurement validates the
  content thesis, we return to the CEO plan as-written at that point.
- **No competitor-comparison content.** Per guardrail #5, named competitor
  data stays in private notes.

## Execution handoff

| Step | Artifact | Owner | Est. effort |
|---|---|---|---|
| Variance check | Re-run `fr-004`/`fr-006` × 3 on Perplexity/Gemini | Ethan (scripts exist) | 15 min, $0.50 |
| P0.0 inventory | This doc's "Page inventory" section filled in | Ethan | 30 min |
| P0.1 disambiguation | 4 pages rewritten on ventureoracle.kr per `content-drafts/framework-disambiguation-specs.md` | Ethan | 1 hr |
| P0.2 new page | `/concepts/negative-sequence` published per `content-drafts/negative-sequence-outline.md` | Ethan | 1 hr |
| P0.3 new article | Toss/Dunamu article published per `content-drafts/toss-dunamu-article-outline.md` | Ethan | 1 hr |
| Wait | 14–21 day reindex window | — | passive |
| Re-measurement | Re-run `pilot/scripts/run_*_api.py` | Ethan | 15 min, $3 |
| Gate decision | This doc's "Re-measurement gate" table scored | Ethan + next Claude session | 30 min |

**Total hands-on effort before the gate: ~3.5 hours** (well inside a single
Saturday). Total elapsed time before gate decision: ~3 weeks.

## Page inventory — 2026-04-11

*(To be filled in by Ethan during P0.0. Placeholder rows below — replace with
the actual live-site state.)*

| Query ID | Framework | Page URL | Words | First published | Korean? | schema.org? | Internal links in | External links in | Current H1 | Current title |
|---|---|---|---|---|---|---|---|---|---|---|
| fr-001 | Founder Intelligence | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| fr-002 | E/D/R | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| fr-003 | MAU Trap | /concepts/mau-trap (confirmed) | ? | ? | ? | ? | ? | ? | ? | ? |
| fr-004 | Four Lenses | /concepts/four-lenses-framework (confirmed) | ? | ? | ? | ? | ? | ? | ? | ? |
| fr-005 | Founder Intelligence (KO) | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| fr-006 | Four Lenses (KO) | ? | ? | ? | ? | ? | ? | ? | ? | ? |

## Links

- Seed data: [`pilot/logs/cross-engine-synthesis-2026-04-12.md`](../../pilot/logs/cross-engine-synthesis-2026-04-12.md)
- Content drafts (handoff): [`content-drafts/`](../../content-drafts/)
- CEO plan (parent plan): [`docs/designs/ceo-plan-2026-04-11.md`](./ceo-plan-2026-04-11.md)
- Project guardrails: [`CLAUDE.md`](../../CLAUDE.md)
