# Canonical URL health check for existing articles

Source feed: https://ethancho12.substack.com/feed
Existing articles.ts: /tmp/voracle-lp-post/ventureoracle-site/app/data/articles.ts
Generated: 2026-04-14T08:35:55

## Current state of canonical URLs across 17 articles

- **0 articles** use the substack ROOT (`https://ethancho12.substack.com`).
  This is the SEO bug: every one of these claims the substack homepage as canonical,
  which dilutes the signal. These need per-post canonical URLs.
- **24 articles** already use correct per-post substack canonicals.
  Nothing to do for these.
- **0 articles** are self-canonical (point at `ventureoracle.kr/insights/<slug>`).
  These are ventureoracle.kr-native content, never cross-posted on substack.
  Leave them alone.
- **8 articles** have non-standard canonical URLs. Review manually.

## Articles that need a canonical URL fix

_No fixable matches found — either the matcher missed them or the_
_6 substack-root articles don't have recent substack counterparts._

## Articles already with correct canonical URLs

**18 articles are already correct** (exact URL match).
No action required.

- `hormuz-frightened-not-in-tehran` → `https://ethancho12.substack.com/p/5de`
- `ventureoracle-001-hormuz-oil-lag` → `https://ethancho12.substack.com/p/ventureoracle-001`
- `koreas-13-billion-venture-market-has-a-body-composition-prob` → `https://ethancho12.substack.com/p/koreas-13-billion-venture-market`
- `for-non-korean-lps-why-korea-is-the-most-mispriced-startup-m` → `https://ethancho12.substack.com/p/for-non-korean-lps-why-korea-is-the`
- `when-myth-arrives-something-dies` → `https://ethancho12.substack.com/p/43f`
- `for-non-korean-lps-the-inverted-risk-curve` → `https://ethancho12.substack.com/p/for-non-korean-lps-the-inverted-risk`
- `kakao-focus-diversification-failure` → `https://ethancho12.substack.com/p/5ab`
- `code-safe-we-are-not` → `https://ethancho12.substack.com/p/dae`
- `why-korea-may-lose-ai-race-while-using-ai-best` → `https://ethancho12.substack.com/p/ai-d53`
- `world-google-is-dreaming-of` → `https://ethancho12.substack.com/p/google`
- `why-we-invested-in-a-rice-company` → `https://ethancho12.substack.com/p/why-we-invested-in-a-rice-company`
- `youre-fired-kind-of` → `https://ethancho12.substack.com/p/youre-fired-kind-of`
- `your-boss-will-hate-this-post` → `https://ethancho12.substack.com/p/0fe`
- `anger-is-not-free` → `https://ethancho12.substack.com/p/dfe`
- `20-watt-genius-1000-watt-fool` → `https://ethancho12.substack.com/p/20-1000`
- `chains-debt-algorithms` → `https://ethancho12.substack.com/p/b0d`
- `what-lucent-block-actually-revealed` → `https://ethancho12.substack.com/p/a6b`
- `openai-hardware-dilemma` → `https://ethancho12.substack.com/p/openais-65-billion-hardware-dilemma`

## Alt-language siblings (Korean/English pairs)

**1 substack posts** fuzzy-matched to existing articles
that already have a correct per-post substack canonical for the OTHER
language version. These are effectively translated siblings. Three options:

1. **Add as separate article** — creates a bilingual duplicate pair under
   a new slug like `<existing-slug>-ko` or `<existing-slug>-en`.
2. **Embed inside existing article** — populate the `titleKo` field on the
   existing article with the sibling's title. No new slug created.
3. **Leave alone** — accept that only one language surfaces on ventureoracle.kr.

| Sibling post URL | Paired with article | Pair existing URL |
|---|---|---|
| `https://ethancho12.substack.com/p/the-optimism-tax-what-18-billion` | `the-optimism-tax` | `https://ethancho12.substack.com/p/the-optimism-tax` |

## Substack-root articles without a detected match

_None._

## VentureOracle-native content (leave alone)

