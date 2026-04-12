# Substack → VentureOracle articles.ts sync

Generated: 2026-04-12T09:23:25
Source feed: https://ethancho12.substack.com/feed
Existing articles.ts: /Users/yeojooncho/clawd/ventureoracle-site/app/data/articles.ts

## Summary

- **Substack posts fetched**: 20
- **Existing articles in articles.ts**: 17
- **Substack posts already correctly linked**: 3
- **Substack posts needing canonical URL fix on existing articles**: 0
- **Alt-language siblings (manual decision required)**: 2
- **New substack posts (not yet in articles.ts)**: 15

## Output files

- `new-articles.ts` — TypeScript `Article[]` fragment with the new posts.
  Review, adjust Korean titles if needed, then append to articles.ts.
- `canonical-url-updates.md` — Health check of canonical URLs across
  the existing articles. Identifies substack-root canonicals (SEO bug),
  already-correct ones, alt-language siblings, and ventureoracle-native
  content that should be left alone.

## Integration steps

1. Read `canonical-url-updates.md` and apply the per-post URL updates to
   `app/data/articles.ts` in the ventureoracle-site Next.js repo.
2. Read `new-articles.ts`, review each new article's:
   - `title` (for Korean posts, replace `[Korean] ...` with a real English
     title so `/insights` cards display in English)
   - `slug` (ensure it's stable and SEO-friendly)
   - `category` (inferred automatically, check for correctness)
   - `excerpt` (first paragraph; may need hand-polish)
3. Append the new article objects into the existing `articles: Article[]`
   array in `app/data/articles.ts`.
4. Run `npm run build` to verify no TypeScript errors and check that the
   static params include the new slugs.
5. Commit + push. Vercel auto-deploys.

## New posts at a glance

| Date | Language | Words | Title | Slug |
|---|---|---|---|---|
| 2026-04-10 | en | 1242 | Korea’s $13 Billion Venture Market Has a Body Composition Pr | `koreas-13-billion-venture-market-has-a-body-composition-prob` |
| 2026-04-09 | en | 1163 | [For non-Korean LPs] Why Korea Is the Most Mispriced Startup | `for-non-korean-lps-why-korea-is-the-most-mispriced-startup-m` |
| 2026-04-08 | ko | 1233 | When the Myth Arrives, Something Dies | `when-myth-arrives-something-dies` |
| 2026-04-08 | en | 891 | [For Non-Korean LPs] The Inverted Risk Curve | `for-non-korean-lps-the-inverted-risk-curve` |
| 2026-04-02 | ko | 1005 | Kakao's 'Focus and Choice' Is a Polite Name for Diversificat | `kakao-focus-diversification-failure` |
| 2026-04-01 | ko | 1001 | The Code Is Safe. We Are Not. | `code-safe-we-are-not` |
| 2026-03-26 | ko | 1441 | Why Korea May Lose the AI Race Even While Using AI Best | `why-korea-may-lose-ai-race-while-using-ai-best` |
| 2026-03-14 | ko | 775 | The World Google Is Dreaming Of | `world-google-is-dreaming-of` |
| 2026-03-10 | en | 674 | Why we invested in a rice company | `why-we-invested-in-a-rice-company` |
| 2026-03-01 | ko | 1078 | You're Fired. Kind of. | `youre-fired-kind-of` |
| 2026-02-20 | ko | 814 | Your Boss Will Hate This Post | `your-boss-will-hate-this-post` |
| 2026-02-18 | ko | 89 | Anger Is Not Free | `anger-is-not-free` |
| 2026-02-16 | ko | 982 | The 20-Watt Genius and the 1000-Watt Fool | `20-watt-genius-1000-watt-fool` |
| 2026-02-15 | ko | 1406 | Chains, Debt, Algorithms | `chains-debt-algorithms` |
| 2026-02-13 | ko | 748 | What Lucent Block Actually Revealed | `what-lucent-block-actually-revealed` |
