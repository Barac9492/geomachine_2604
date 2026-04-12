# Next scheduled pilot re-run

**Date:** 2026-05-03 (Saturday, 21 days after session)
**Trigger:** manual — run the command below from this repo's root

## What to run

```bash
cd ~/GEOMachine_2604

# Full 72-cell pilot (4 engines × 18 queries)
python pilot/scripts/run_claude_api.py
python pilot/scripts/run_openai_api.py
python pilot/scripts/run_perplexity_api.py
python pilot/scripts/run_gemini_api.py

# Auto-score against the Apr 11 baseline
python pilot/scripts/geo_remeasure_diff.py

# Read the verdict
cat pilot/logs/remeasure-diff-*.md | tail -80
```

**Expected cost:** ~$3.50
**Expected wall time:** ~15 min
**Output:** `pilot/logs/remeasure-diff-YYYY-MM-DD.md` with PASS / MARGINAL / FAIL gate

## What you're measuring

Changes shipped on 2026-04-12 that should propagate by the re-run date:

1. `/concepts/founder-intelligence` — new page, should displace Accenture collision on fr-001
2. `/concepts/edr-framework` — new page, should displace GPT-4o/Gemini hallucinations on fr-002
3. 7 concept pages with strengthened Ethan Cho attribution (metaDescription + keywords)
4. 16 new substack articles at `/insights/*` increasing ventureoracle.kr surface area
5. 8 substackUrl hygiene fixes (cleaner JSON-LD sameAs)

## Gate thresholds (from geo-improvement-plan)

| Metric | Baseline (Apr 11) | Target | Floor |
|---|---|---|---|
| ventureoracle.kr cited (cells) | 2 | ≥5 | ≥3 |
| Framework query hits (of 6 framework queries × 4 engines = 24 cells) | 2 | ≥8 | ≥4 |
| E/D/R hallucination count | 2 (GPT-4o + Gemini) | 0 | ≤1 |
| Overall citation rate | 47% | ≥55% | ≥50% |

## Mini-pilot (2026-04-13, framework queries only, Perplexity + Gemini)

Run ~15 hours after content push. Result: 1/12 vo hits (baseline was 2/12).
- Perplexity fr-004: stable (vo=YES, same as baseline)
- Gemini fr-006: drifted (vo=no, was YES — n=1 variance)
- All new pages: vo=no (expected — not yet indexed)

**Interpretation:** changes need full reindex cycle to propagate. Nothing to act on until 2026-05-03.
