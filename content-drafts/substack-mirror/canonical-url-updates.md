# Canonical URL health check for existing articles

Source feed: https://ethancho12.substack.com/feed
Existing articles.ts: /tmp/voracle-substack-integration/ventureoracle-site/app/data/articles.ts
Generated: 2026-04-12T09:34:17

## Current state of canonical URLs across 17 articles

- **4 articles** use the substack ROOT (`https://ethancho12.substack.com`).
  This is the SEO bug: every one of these claims the substack homepage as canonical,
  which dilutes the signal. These need per-post canonical URLs.
- **22 articles** already use correct per-post substack canonicals.
  Nothing to do for these.
- **4 articles** are self-canonical (point at `ventureoracle.kr/insights/<slug>`).
  These are ventureoracle.kr-native content, never cross-posted on substack.
  Leave them alone.

## Articles that need a canonical URL fix

_No fixable matches found — either the matcher missed them or the_
_6 substack-root articles don't have recent substack counterparts._

## Articles already with correct canonical URLs

**17 articles are already correct** (exact URL match).
No action required.

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
- `2-million-users-worthless` → `https://ethancho12.substack.com/p/your-startups-2-million-users-are`

## Alt-language siblings (Korean/English pairs)

**2 substack posts** fuzzy-matched to existing articles
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
| `https://ethancho12.substack.com/p/openai-9` | `openai-hardware-dilemma` | `https://ethancho12.substack.com/p/openais-65-billion-hardware-dilemma` |

## Substack-root articles without a detected match

**4 articles** use the substack root canonical but
the matcher couldn't find a corresponding substack post. Two possibilities:

1. The post WAS on substack but is no longer in the RSS feed
   (substack's public feed returns ~20 most recent posts).
2. The post was never actually on substack and the root canonical is a leftover placeholder.

For each, either (a) search substack manually for the actual post URL and
apply it, or (b) change the canonical to `https://ventureoracle.kr/insights/<slug>`
(self-canonical) if it's a ventureoracle-native article.

- `advisor-equity-trap-5-percent` — The 5% Advisor Trap: How Founders Destroy Their Cap Tables Before Series A
- `amazon-nuclear-ai-datacenters` — "Nuclear Power for AI: Why Amazon's Betting on Reactors
- `goldman-ai-proof-software-basket` — Goldman's AI-Proof Portfolio: Which Companies Survive AGI?
- `ai-kills-bond-sale-credit-risk` — The $600M Warning: How AI Fear Just Killed a Bond Sale

## VentureOracle-native content (leave alone)

- `deepseek-r1-korean-vc` → `https://ventureoracle.kr/insights/deepseek-r1-korean-vc`
- `the-380-billion-question` → `https://ventureoracle.kr/insights/the-380-billion-question`
- `emotional-debt` → `https://ventureoracle.kr/insights/emotional-debt`
- `ai-private-credit-disruption` → `https://ventureoracle.kr/insights/ai-private-credit-disruption`
