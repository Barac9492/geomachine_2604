# Demand-Seeded Query Research

**Purpose:** Replace the 9 `TBD` placeholders in `pilot/queries.yaml` with queries derived from real search demand data, not Ethan's head. Outside-voice finding #4 from the CEO review: measuring citations on queries you invented yourself is a vanity metric.

**Time budget:** ~30 minutes total. Do this before Monday 2026-04-13 (first pilot run).

**Output:** 9 final query strings written into `pilot/queries.yaml` (replacing `dm-001` through `dm-009`).

---

## Source 1 — Google Search Console (ventureoracle.kr)

Open https://search.google.com/search-console → `ventureoracle.kr` property → Performance → Queries tab → set date range to last 90 days.

**What to look for:**
- Top 20 queries by *impressions* (not clicks — impressions tell you what people search for, clicks tell you what they chose)
- Queries where impressions > 5 but CTR < 5% (these are queries where you're appearing but not winning — exactly the "who are they picking instead of me" question)
- Korean and English queries both

**3 starter seeds (replace with real GSC data before run 1):**

1. `Korean venture capital AI startups 2026` — English, domain authority, plausible LP query
2. `한국 AI 스타트업 투자 VC` — Korean, domain authority
3. `K-beauty startup investors` — English, domain authority adjacent to TheVentures' thesis

**Your findings:**

| Rank | Query | Impressions | CTR | Notes |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

---

## Source 2 — Naver Trends / DataLab

Open https://datalab.naver.com/keyword/trendSearch.naver and test keyword clusters:
- `한국 VC`, `한국 벤처투자`, `한국 AI 투자`, `해외 한인 VC`, `K-스타트업 투자`
- Compare against `알토스벤처스`, `카카오벤처스`, `KIP`, `SBVA` to see which competitors get searched for and how often

**What to look for:**
- Related keyword suggestions Naver surfaces when you search for these
- Seasonal spikes (hint: if there's a spike around a specific news event, that's the query the AI engines will have seen most recently)

**3 starter seeds (replace with real Naver data):**

1. `한국 벤처투자 현황 2026` — Korean, generic
2. `알토스벤처스 포트폴리오` (competitor-probe to see what engines say about them) — Korean, domain
3. `한국 AI 스타트업 유망 분야` — Korean, thesis-adjacent

**Your findings:**

| Query cluster | Naver volume | Trending? | Notes |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

---

## Source 3 — LinkedIn Search Auto-complete

Open https://www.linkedin.com/ → search bar → type each seed and note the auto-completes LinkedIn suggests (these are what LinkedIn users actually search for most).

**Seeds to test:**
- `Korean VC` → collect all 4-6 auto-completes
- `TheVentures` → collect all auto-completes
- `Ethan Cho` → collect all auto-completes
- `Korean diaspora founder` → collect all auto-completes
- `Korean startup investor` → collect all auto-completes

**3 starter seeds (replace with real LinkedIn auto-completes):**

1. `Korean VC firms for seed stage` — auto-complete after typing "Korean VC"
2. `TheVentures Korea portfolio companies` — auto-complete after typing "TheVentures"
3. `Ethan Cho TheVentures LinkedIn` — auto-complete after typing "Ethan Cho"

**Your findings:**

| Seed typed | Auto-complete suggestion | Notes |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |

---

## Final query selection

After doing the research above, pick 9 queries to replace `dm-001` through `dm-009`. **Selection rules:**

- Mix English (4-5) and Korean (4-5)
- Mix identity, domain, and adjacent-identity queries — but NO framework names (those stay in the ethan_authored half of `queries.yaml`)
- Pick queries where there's a *plausible Ethan-adjacent answer*. A query like "best pizza in Seoul" teaches nothing about citation; a query like "Korean VC firms investing in AI" might teach a lot.
- At least 2 should be competitor-probe queries (e.g., asking about a named competitor directly) — these give you the vocabulary the engines use for the rest of the Korean VC landscape, which is actionable intel even if you're never cited.
- Avoid queries so long they exceed 15 words — they become unnatural and hard to re-run

**Your final 9 (copy into `pilot/queries.yaml` when done):**

1. dm-001: `...`
2. dm-002: `...`
3. dm-003: `...`
4. dm-004: `...`
5. dm-005: `...`
6. dm-006: `...`
7. dm-007: `...`
8. dm-008: `...`
9. dm-009: `...`

---

## Notes on the process

- If GSC has no data (because ventureoracle.kr is too new), that itself is a finding — write it down and move on to Naver/LinkedIn as the primary demand sources.
- If Naver shows zero search volume on all Korean VC queries, that's also a finding and worth a one-line mention in the week-2 assessment.
- Don't tune the queries between week 1 and week 2 — a fixed query set is the point of the pilot. Any tuning happens after the 2026-04-27 go/no-go.
