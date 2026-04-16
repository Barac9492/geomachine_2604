# GEO re-measurement diff — 2026-04-14

Baseline: 2026-04-11/12 four-engine run. Latest: most recent per-engine log.

## Sources

- **claude**: baseline `run-2026-04-11-claude-api.md` → latest `run-2026-04-14-claude-api.md`
- **openai**: baseline `run-2026-04-12-openai-api.md` → latest `run-2026-04-14-openai-api.md`
- **perplexity**: baseline `run-2026-04-12-perplexity-api.md` → latest `run-2026-04-14-perplexity-api.md`
- **gemini**: baseline `run-2026-04-12-gemini-api.md` → latest `run-2026-04-14-gemini-api.md`

## Gate scorecard

| Metric | Baseline | Now | Target | Hard floor | Verdict |
|---|---|---|---|---|---|
| ventureoracle.kr cells cited | 2 | 3 | ≥ 6 | ≥ 3 | ⚠️ FLOOR |
| Framework queries hitting ≥1 engine | 2 / 6 | 2 / 6 | ≥ 4 | ≥ 3 | ❌ BELOW FLOOR |
| E/D/R hallucination engines | 2 / 4 | 0 / 4 | 0 / 4 | ≤ 1 / 4 | ✅ TARGET |
| Aggregate citation rate | 50% | 50% | ≥ 55% | ≥ 50% | ⚠️ FLOOR |

## Deltas

- **ventureoracle.kr cells:** +1
- **Framework queries with any hit:** +0
- **E/D/R hallucinating engines:** -2
- **Citation rate:** +0.0 points

## Framework query breakdown

| Query | Baseline engines | Now engines |
|---|---|---|
| fr-001 | — | — |
| fr-002 | — | — |
| fr-003 | — | — |
| fr-004 | perplexity | gemini, perplexity |
| fr-005 | — | — |
| fr-006 | gemini | gemini |

## Decision

**MARGINAL** — 1/4 target, 2/4 floor, 1/4 below floor. Ship remaining P1 items and re-run once more in 2-4 weeks before committing to Phase 1.
