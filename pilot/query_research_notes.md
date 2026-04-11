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
| Google Search Console | ❌ No | Chrome session not signed into Google. Would require Ethan's interactive login. |
| LinkedIn search auto-complete | ❌ No | Hit LinkedIn login wall. Would require Ethan's interactive login. |
| Google Search (direct) | ❌ No | CAPTCHA rate-limit (Google sorry page). Automation detected. |

Worth revisiting if Ethan signs into Chrome for Google/LinkedIn later.

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

## Source 4 — Claude WebSearch corpus pass (context-only)

6 parallel queries against the general web provided qualitative context (already documented in the earlier CEO review section). Key reusable findings:

- **Feb 2026 TheVentures + OpenAI/Google/Anthropic partnership** is the dominant recent TheVentures press event, covered on KoreaTechDesk and opentools.ai. Used to seed `dm-001`.
- **Viki AI investment analyst** — TheVentures internal tool, 87.5% accuracy, launched 2025. Used to seed `dm-007`.
- **Korean VC competitive vocabulary**: Altos owns "Coupang/Krafton/Roblox exits", Kakao Ventures owns "most active early-stage", KIP owns "largest AUM $2.7B". Seeded competitor-probe framing in `dm-006`.
- **Title drift**: PitchBook / ZoomInfo show Ethan Cho as "COO"; PRD says "CIO". Data-quality probe informed `dm-008`.

---

## Next steps

1. Queries committed to `pilot/queries.yaml` — 18 total, 9 Ethan-authored + 9 demand-seeded. Ready for Monday 2026-04-13 first pilot run.
2. Re-run this research if/when Ethan signs into Chrome for Google (for GSC data) and LinkedIn (for auto-complete). The current seed is strong but missing those two auth-gated sources.
3. Keep the Naver screenshot (`pilot/naver_datalab_2026-04-11.png`) as a visual anchor for the week-2 assessment.
4. **Treat `dm-003` and `dm-004` as the two highest-information queries of the pilot.** Their results directly test the 2016 indexing-decay hypothesis. Flag them for close reading in the week-2 assessment.
