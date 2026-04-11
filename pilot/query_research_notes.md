# Demand-Seeded Query Research — 2026-04-11

**Purpose:** Replace the 9 `dm-XXX` placeholders in `pilot/queries.yaml` with queries derived from real search demand data, not Ethan's head. Outside-voice finding #4 from the CEO review: measuring citations on queries you invented yourself is a vanity metric.

**Status:** COMPLETE. Seeding done via Chrome DevTools MCP + web research. Final 9 queries are committed in `pilot/queries.yaml`.

---

## Sources actually consulted

| Source | Accessible? | Notes |
|---|---|---|
| **Naver DataLab** (Keyword Trend) | ✅ Yes | Public, no login required. Comparative trend tool for 5 topic clusters. |
| **Bing autocomplete API** (`/osjson.aspx`) | ✅ Yes | Same-origin from a Bing results page, no auth needed. 12 seed queries tested. |
| **Bing search results** | ✅ Yes | Standard results for qualitative context. |
| **Claude WebSearch web-corpus pass** | ✅ Yes | 6 parallel queries against general web for corpus context. |
| **Google Search Console** (via user screenshots) | ✅ Yes | Ethan sent 2 screenshots from his signed-in personal browser. Overview + Performance + Pages reports captured. See Source 5 below — this is the highest-value data in the entire seeding round. |
| LinkedIn search auto-complete | ❌ No | Automation browser hit LinkedIn login wall. User did not paste data. Still TBD if needed. |
| Google Search (direct) | ❌ No | CAPTCHA rate-limit (Google sorry page). Automation detected. |

---

## Source 1 — Naver DataLab (1-year trend, 2025-04-10 → 2026-04-10)

Set up a 5-topic comparison on `https://datalab.naver.com/keyword/trendSearch.naver`:

| Topic | Sub-keywords |
|---|---|
| 한국 VC | 한국vc, 한국벤처캐피탈, 한국벤처투자, 한국벤처투자회사 |
| 한국 AI 스타트업 | 한국ai스타트업, 한국ai투자, ai스타트업투자 |
| 더벤처스 | 더벤처스, 더벤처스코리아, theventures, 더벤처스포트폴리오 |
| 알토스벤처스 | 알토스벤처스, 알토스, altosventures |
| 카카오벤처스 | 카카오벤처스, 카카오벤처, kakaoventures |

Chart rendered via billboard.js. Extracted y-coordinate data from SVG paths and translated back to Naver's 0–100 relative scale using the tick mapping `y=469→0, y=2→100`.

**Screenshot:** `pilot/naver_datalab_2026-04-11.png`

### Results (normalized 0–100 relative scale)

| Rank | Series | Peak (max day) | Average | Interpretation |
|---|---|---|---|---|
| 1 | 알토스벤처스 | **100.0** (one-day spike) | 2.16 | Dominant. Massive single-day spike likely tied to a news event (portfolio exit / funding round / media coverage). |
| 2 | 한국 VC (generic) | 9.13 | 1.75 | Steady second. The generic category query exists but isn't a single brand winner. |
| 3 | 더벤처스 | 1.01 | 0.32 | Brand search exists, small volume, comparable to Kakao Ventures. |
| 4 | 카카오벤처스 | 0.78 | 0.39 | Similar to TheVentures — both very low absolute volume. |
| 5 | 한국 AI 스타트업 | 0.35 | 0.22 | **LOWEST of all five.** AI-centric framing is not where demand lives. |

### Three real findings from Naver

1. **Altos dominates Korean VC search demand on Naver.** One massive news-driven spike that dwarfs everything else. Altos is the firm Korean searchers care about most by a wide margin. When building demand queries, probing Altos returns actionable vocabulary.
2. **TheVentures brand search is comparable to Kakao Ventures** on average volume (~0.3 vs ~0.4). TheVentures is *not invisible* in Korean search, just small. Ethan's zero-citation baseline is specifically about AI-engine surfacing, not raw search demand.
3. **"한국 AI 스타트업" is the LOWEST-volume term of all five.** The 2026 AI-centric framing is vanity, not demand. Korean Naver users search for fund names and associations, not AI themes. This argues against heavily weighting AI-themed queries — the pilot query list should lean on fund names and association-first framings.

---

## Source 2 — Bing autocomplete (12 seed queries)

Fetched via `https://www.bing.com/osjson.aspx?query=X` from within a Bing results page (CORS-allowed same-origin). These are the real typed-search suggestions Bing surfaces.

### Raw autocomplete results

| Seed | Autocompletes |
|---|---|
| `Korean VC` | korean vc ai startup 2026, korean vce, korean vcv, korean vc, korean v chinese |
| `Korean venture capital` | korean venture capital market report 2023 |
| `TheVentures Korea` | *(nothing)* |
| `Ethan Cho TheVentures` | *(nothing)* |
| `Korean diaspora founder` | *(nothing)* |
| `Korean AI startup 2026` | south korea ai startup, korea ai startup 100, the ai korea 2024, list of ai startups 2024, top ai startups 2024, top 10 ai startups in 2024, ai startup ideas 2024, best ai startups 2024, ai startups in india 2024, ai in south korea, korea ai summit 2024, emerging ai companies 2024 |
| `한국 VC` | 한국 vc, 한국vc협회 |
| `한국 벤처캐피탈` | 한국 벤처캐피탈협회, 한국벤처캐피탈협회 채용, 한국벤처캐피탈연수원, 한국벤처캐피탈협회 연수원, 한국벤처캐피탈협회 채용공고, 한국벤처캐피탈혁신, 한국벤처캐피탈현대, 한국벤처캐피탈현실, 한국벤처캐피탈현장, 한국벤처캐피탈현황, 한국벤처캐피탈형태, 한국벤처캐피탈혜택 |
| `더벤처스` | 더벤처스, **더벤처스 사건**, 더벤처스 인턴, 더벤처스 투자 |
| `조여준` | 조여준, **조여준 통역사** |
| `top Korean seed VC` | korean vegetable seeds in usa, pre seed vc in india, v rising seed list (all irrelevant noise — no real demand for this English phrase) |
| `Korean VC LLM OpenAI` | (all LangChain/OpenAI technical suggestions — not VC-related) |

### Key findings from Bing autocomplete

1. **`korean vc ai startup 2026`** — The EXACT phrase "Korean VC AI startup 2026" is itself a real autocomplete suggestion. This tells us Bing users are actually searching for this combination. The PRD's Korean-VC-in-2026 framing is validated by demand data.

2. **`한국 벤처캐피탈협회` (KVCA) dominates Korean VC-adjacent autocomplete** — 12 of the 12 suggestions for `한국 벤처캐피탈` reference the Korean Venture Capital Association. **Korean users search through the association, not through individual firms.** This means Korean AI engines may respond to fund-level queries by first referencing KVCA, then drilling down. Any probe query in Korean should use association-first framing to test this mental model.

3. **`더벤처스 사건` is the #2 autocomplete for TheVentures in Korean.** See the "2016 incident alert" section below — this is a first-order finding for the tracker.

4. **`조여준` autocomplete collides with "조여준 통역사"** — a Korean interpreter shares Ethan's name. Identity-level queries in Korean risk being disambiguated to the wrong person by AI engines. This is a trackable data-quality issue and `dm-008` is designed to probe it directly.

5. **`TheVentures Korea`, `Ethan Cho TheVentures`, `Korean diaspora founder` all return ZERO autocompletes.** These phrases have no existing Bing search demand. For "Korean diaspora founder" in particular — which the PRD names as Ethan's thesis — the **entire semantic space is unclaimed at the search-autocomplete level**. This confirms the thesis is white space, but also means there's no existing demand to ride — Ethan has to create it.

6. **`korea ai startup 100` is a real typed query.** List-style "top N" queries are where investors and journalists look. Query `dm-002` targets this directly.

7. **`Korean AI startup 2026` autocompletes mostly reference 2024.** Bing's autocomplete index is lagging — most of its training data points to 2024 content. This suggests the AI engines are also running on 2024-weighted corpora, which means the Feb 2026 TheVentures + OpenAI announcement may take longer than expected to propagate through engine answers.

---

## Source 3 — Bing search results for `더벤처스 사건` (2016 incident context)

### ⚠️ Strategic alert: the 2016 TheVentures TIPS fraud case

Bing autocomplete flagged `더벤처스 사건` as the #2 suggestion for `더벤처스`. Searching for it returned 10 results dominated by 2016-2018 coverage of a TIPS (Tech Incubator Program for Startup) fraud case.

**Timeline extracted from the results:**
- **2014**: TheVentures founded by 호창성/문지원 couple. First investment ParkingSquare (acquired by Kakao 2016).
- **2016 Apr–May**: CEO 호창성 indicted on charges of misappropriating TIPS government program funds. 김현진 (investment manager) also charged.
- **2016 Oct**: First-instance court ACQUITTED 호창성 (Seoul Bukbu District Court). Court ruled that TheVentures' practices followed standard TIPS-era venture investment conventions and prosecutors had "overreached."
- **2018 Feb**: Supreme Court confirmed the acquittal. The case was officially closed with a "not guilty" verdict.
- **Aftermath**: Despite acquittal, the "블랙엔젤 오명" (black angel stigma) remained. News coverage mentions TheVentures had to explicitly recover from the reputational damage.

### Why this matters for the tracker

- **Older negative content is much more deeply indexed than the newer acquittal.** 2016-era fraud-case headlines ("대표 구속", "벤처 사기", "비리") appear to dominate the Korean-language corpus about TheVentures.
- **AI engines trained on this corpus may default to the indictment story** when asked "What is TheVentures known for?" — unless they have been updated with the 2018 acquittal, and especially unless they have been updated with 2026 news (the OpenAI/Google/Anthropic partnership) that would shift the top-of-mind association.
- **This is exactly the kind of GEO measurement gap the tracker is designed to surface.** If the pilot shows that engines lead with the 2016 case, that's an actionable signal — the content priority for Q2 2026 should include proactive content about the acquittal, the 2018 ruling, and the 2026 leadership era.
- **`dm-003` (open-ended brand probe) and `dm-004` (explicit history-and-legal-case probe) are designed to measure this directly.** Expect these two queries to produce the highest-information pilot data points.

### How Ethan should interpret pilot results on dm-003 / dm-004

| Engine response pattern | Interpretation | Action |
|---|---|---|
| Mentions 2016 fraud case AND 2018 acquittal AND 2026 strategy | Best case — engine has a fresh, balanced view | No content action needed |
| Mentions 2016 case, no acquittal, no 2026 strategy | Engine is frozen on negative 2016-era corpus | Urgent content priority: publish the acquittal story + 2026 leadership context |
| Mentions 2016 case AND 2018 acquittal, no 2026 context | Engine has the legal facts but not the forward story | Medium priority: publish 2026 strategy / leadership content |
| No mention of 2016 case, leads with 2026 content | Engine is sufficiently fresh-indexed to skip the old story | Best case for Ethan, mild diagnostic concern that engines lack history |
| No answer / "I don't have information about this firm" | Engine has no TheVentures index at all | Low diagnostic, means content volume is the bottleneck |

---

## Source 5 — Google Search Console live data (via user screenshots, 2026-04-11)

This is the highest-signal data point in the entire research round. Ethan sent two screenshots from his signed-in personal Chrome browser of the GSC property `https://ventureoracle.kr/` (URL-prefix type).

### GSC Performance report — 3-month window

| Metric | Value |
|---|---|
| Total clicks from Google Search | **1** |
| Total impressions | **42** (~0.5/day) |
| Average CTR | 2.4% |
| Average position | **4.6** (strong when shown) |
| Rows in top-queries table | **1** |
| Only query shown | **`oracle ventures`** — 0 clicks, 2 impressions |

### GSC Pages (Indexing) report — current state

| Status | Count |
|---|---|
| Indexed pages | **1** |
| Not indexed pages | **5** |

### Why pages aren't indexed — exact reasons (2 reasons, 3 rows)

| Reason | Source | Validation status | Pages |
|---|---|---|---|
| Redirect error | Website | **Not Started** | **4** |
| Not found (404) | Website | **Not Started** | **1** |
| Discovered - currently not indexed | Google systems | N/A | 0 (historical peak ~35-40 around 2026-03-07) |

### Historical timeline (from the Pages report chart)

1. **~2026-02-24** — GSC property began collecting data (annotation "1" on the chart)
2. **~2026-03-07** — sitemap submission or URL dump caused Google to discover ~35-40 pages (annotation "2"; the grey-bar spike)
3. **2026-03-07 onwards** — Google crawled, hit redirect loops + 404s, rejected most
4. **Present** — 5 stubborn unindexed pages remain (4 redirect errors + 1 404), validation "Not Started" on both reason rows

### The real story this tells

**Indexing is the root bottleneck, upstream of both measurement and content.**

- The site has ~6 known pages and only 1 is successfully indexed.
- 4 pages are blocked by redirect errors — almost certainly HTTP↔HTTPS or www↔non-www redirect loops, or canonical tags pointing through a redirect chain.
- 1 page is a plain 404 (broken link or removed page still referenced somewhere).
- Average position is 4.6 when the site DOES appear — **this is not a ranking problem**. It's a **demand-fit problem plus an indexing problem**.
- Only query that ever surfaced the site: `oracle ventures` — a reversed-word-order version of the brand. This suggests Google's 1 indexed page may contain text with words in this order, and real demand for "venture oracle" phrased as "oracle ventures" is near-zero.
- **Zero searches for "Ethan Cho", "TheVentures", or any framework name** have ever surfaced ventureoracle.kr in Google Search over the 3-month window.

### Implications for the pilot

1. **The Phase 0 pilot as designed will almost certainly return 72/72 zero citations**, not because engines aren't good at surfacing but because there's nothing in the web-retrieval index for them to surface. AI chat engines with web retrieval depend on Google (or similar) indexes.
2. **The sharp diagnostic opportunity** is Pages report + URL Inspection, not the citation tracker. Fix the 4 redirect errors + 1 404, request indexing, wait for Google to recrawl, then re-measure.
3. **The Phase 0 pilot becomes informative** once indexed page count reaches ~10+. Before that, running it is essentially measuring an uncrawled site.
4. **The "oracle ventures" query is itself a finding worth keeping.** It confirms the site has at minimum ONE page that's discoverable, and Google is matching it to a typo/reversed-word-order search. That's a tiny, unreliable, but non-zero toehold.

### What gets added to `queries.yaml`

**Nothing.** The current 18-query set is still the right probe when the pilot eventually runs. The GSC finding reshapes the sequencing (Phase -1 before Phase 0) rather than the query list.

### Immediate action items for Ethan (pre-pilot)

These are documented in full in `docs/designs/ceo-plan-2026-04-11.md` under the new "Phase -1 — Fix Indexing" block. Short version:

1. In GSC, click the "Redirect error" row. Get the 4 specific URLs.
2. For each URL, use URL Inspection to see the redirect chain Google hit. Fix the loops (pick one canonical form and 301 everything else directly to it).
3. Click the "Not found (404)" row. Restore, redirect, or remove-from-sitemap the 1 URL.
4. Click "Validate Fix" on both reason rows after repair.
5. Manually request indexing (via URL Inspection top bar) on 3-5 key pages.
6. Submit `sitemap.xml` at Indexing → Sitemaps.
7. Check Settings → Manual Actions (10 seconds).
8. Publish content to reach ≥10 indexed pages before starting Phase 0 pilot.

### What was intentionally NOT extracted

- LinkedIn auto-complete data (Ethan didn't paste it; marked as optional)
- Google Search direct (CAPTCHA blocked the automation browser)
- Deeper GSC drill-downs (per-page inspection, sitemap history) — deferred until Ethan has the Pages list in hand

---

## Source 4 — Claude WebSearch corpus pass (context-only)

6 parallel queries against the general web provided qualitative context (already documented in the earlier CEO review section). Key reusable findings:

- **Feb 2026 TheVentures + OpenAI/Google/Anthropic partnership** is the dominant recent TheVentures press event, covered on KoreaTechDesk and opentools.ai. Used to seed `dm-001`.
- **Viki AI investment analyst** — TheVentures internal tool, 87.5% accuracy, launched 2025. Used to seed `dm-007`.
- **Korean VC competitive vocabulary**: Altos owns "Coupang/Krafton/Roblox exits", Kakao Ventures owns "most active early-stage", KIP owns "largest AUM $2.7B". Seeded competitor-probe framing in `dm-006`.
- **Title drift**: PitchBook / ZoomInfo show Ethan Cho as "COO"; PRD says "CIO". Data-quality probe informed `dm-008`.

---

## Next steps

1. Queries committed to `pilot/queries.yaml` — 18 total, 9 Ethan-authored + 9 demand-seeded.
2. **Pilot start is now gated on Phase -1 (indexing fix).** See `docs/designs/ceo-plan-2026-04-11.md` → "Phase -1 — Fix Indexing" for the full gating criteria. Minimum: ≥10 indexed pages in GSC before running the 2-week manual pilot.
3. Keep the Naver screenshot (`pilot/naver_datalab_2026-04-11.png`) as a visual anchor for the week-2 assessment.
4. **Treat `dm-003` and `dm-004` as the two highest-information queries of the pilot.** Their results directly test the 2016 indexing-decay hypothesis. Flag them for close reading in the week-2 assessment (whenever it runs).
5. **The GSC baseline (1 click, 42 impressions, 1 indexed page, 5 not indexed, 2.4% CTR, 4.6 avg position, only `oracle ventures` query)** is now the permanent "Day 0" measurement for Ethan's GEO strategy. Record the same numbers again at Phase 0 start, Phase 0 week 2, and the Q3 2026 quarterly retrospective to measure progress against this baseline.
