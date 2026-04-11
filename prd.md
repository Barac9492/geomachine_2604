# GEO Tracker — PRD v0.1

**Owner:** Ethan Cho (조여준), CIO, TheVentures
**Date:** April 11, 2026
**Status:** Draft for review

---

## One-line definition

A tool that queries major AI engines on a fixed schedule, automatically detects whether Ethan, TheVentures, or his proprietary frameworks are cited in the responses, and tracks the results as a time series.

## Why build this

The GEO strategy is already in motion. Content is being produced, frameworks have been named, the personal site (ventureoracle.kr) is being optimized. What is missing is the measurement layer. A baseline reading in early 2026 confirmed zero AI engine citation. Since then, no system has tracked whether that has changed.

Without measurement, every piece of content is a guess. With measurement, content priorities become a function of data: which framework is starting to land, which query is still owned by competitors, which engine indexes new material fastest.

## What it measures

**Engines (4)**
ChatGPT, Claude, Perplexity, Gemini. Each accessed via official API.

**Query categories (3, total 15-20 queries)**

1. **Direct identity queries** — "Who is Ethan Cho?", "Tell me about TheVentures Korea", "조여준 CIO TheVentures"
2. **Domain authority queries** — "Who are the top Korean VC investors?", "Korean diaspora founder thesis", "한국 AI 투자 전문가", "Best LinkedIn voices on Korean venture capital"
3. **Framework queries** — "What is the Founder Intelligence framework?", "E/D/R AI framework", "MAU Trap startup metric", "Four Lenses VC framework"

**Metrics per response**

- Direct citation flag (Ethan, TheVentures, or any proprietary framework name appears)
- Citation context (positive / neutral / negative)
- Citation position (early / mid / late in response)
- Source links present and their domains (ventureoracle.kr, LinkedIn, Substack, third-party media)
- Competitor co-mentions (KIP, Altos, Kakao Ventures, SBVA, Strong Ventures)

## How it works

```
Weekly trigger (Monday 9am KST)
    ↓
Each query × each engine = approx. 60-80 API calls
    ↓
Keyword matching + LLM-based context classification
    ↓
Results stored in SQLite (date, engine, query, full response, metrics)
    ↓
HTML dashboard auto-generated
    ↓
Weekly email summary sent to Ethan
```

## Outputs

**1. Weekly email digest**
- Citation count this week vs last week
- Newly cited queries
- Lost queries
- Top 5 source domains the engines pulled from

**2. Time-series dashboard (browser)**
- Citation rate over time, broken down by category and engine
- Per-framework recognition trend
- Share of voice vs named competitors

**3. Raw response archive**
Every response saved as markdown. Doubles as research material for content writing — what AI says about Ethan today is the rough draft for what next month's content needs to correct.

## Cost

- ChatGPT API: ~$0.01-0.05 per call
- Claude API: ~$0.01-0.05 per call
- Perplexity API: ~$0.005 per call
- Gemini API: ~$0.01 per call

80 calls per week × 4 weeks ≈ $15-30 per month. Negligible.

## Build plan with Claude Code

1. **Week 1** — Minimum version. One engine (Claude API), one query, one stored result. Confirm the loop works end-to-end.
2. **Week 2** — All four engines connected. Full query list loaded from a config file Ethan can edit himself.
3. **Week 3** — Citation classification layer. Each response is sent back to Claude with a structured prompt asking whether Ethan was cited and how.
4. **Week 4** — HTML dashboard generation and weekly email automation.
5. **Week 5** — Deployment to Railway (where SlackOS already runs) with a weekly cron schedule.

Each week Ethan reviews the output and gives feedback. No code reading required.

## Success criteria

Three months from launch:
- Data is accumulating automatically every week without manual intervention
- A clear trend line exists showing citation rate moving from zero
- Ethan can answer the question "which queries do I still lose, and to whom" with data
- The output is feeding the next quarter's content priority decisions

## Intended secondary effects

The tracker is itself content-generative.

- "How I measure GEO for myself" — English LinkedIn post, build-in-public angle
- "Korean VC GEO Index — Q2 2026" — quarterly public report establishing Ethan as the person who defined the measurement standard for the category
- Productized version sold as a monthly subscription to other Korean VCs and operators who want the same visibility but lack the framework. This is the SaaS leg of the agency-to-SaaS path defined in the GEO Business PRD.

The tracker is not the business. The tracker is the instrument that makes the business measurable, the content credible, and the eventual SaaS defensible.

---

**Open decisions**

1. Final query list — confirm now, or draft separately after PRD is approved?
2. Measurement cadence — weekly, or biweekly to align with content publishing rhythm and reduce noise?
3. Who else gets the weekly digest — Ethan only, or also a select trusted reader for accountability?
