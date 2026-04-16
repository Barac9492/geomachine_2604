# Substack → VentureOracle articles.ts sync

Generated: 2026-04-14T08:35:55
Source feed: https://ethancho12.substack.com/feed
Existing articles.ts: /tmp/voracle-lp-post/ventureoracle-site/app/data/articles.ts

## Summary

- **Substack posts fetched**: 20
- **Existing articles in articles.ts**: 32
- **Substack posts already correctly linked**: 18
- **Substack posts needing canonical URL fix on existing articles**: 0
- **Alt-language siblings (manual decision required)**: 1
- **New substack posts (not yet in articles.ts)**: 1

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
| 2026-04-13 | en | 1444 | [LP] Asia’s Last Non-Competitive Venture Market | `lp-asias-last-non-competitive-venture-market` |
