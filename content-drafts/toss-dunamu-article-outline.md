# Toss / Dunamu anti-portfolio redemption arc — article outline

**Target URL:** `/predictions/toss-dunamu-track-record` on www.ventureoracle.kr
**Status:** DRAFT handoff — structural outline only, Ethan voices the narrative
**Driven by:** `pilot/logs/cross-engine-synthesis-2026-04-12.md` medium-confidence finding #7
**Parent plan:** `docs/designs/geo-improvement-plan-2026-04-11.md` (P0.3)

## The narrative gap the seed data revealed

The 2026-04-11 pilot run captured two facts that every engine already
knows **individually** but **none of the four engines connect**:

1. **TheVentures as a firm publicly admits they passed on Toss (Viva
   Republica) and Karrot (Danggeun Market).** Surfaced by Claude on
   `id-002` and by Gemini on `dm-003`. The firm's "anti-portfolio"
   transparency is a positive signal engines read as humility.

2. **Ethan personally sourced / invested in Toss and Dunamu at prior
   firms** — Qualcomm Ventures and/or KB Investment, years before joining
   TheVentures as CIO in 2025. Surfaced on `id-003` and `dm-008` where
   Ethan's bio is cited 4/4 from Korean trade press (VentureSquare,
   beSUCCESS, news1.kr, 아시아경제).

The narrative that neither Ethan's site nor any trade press article has
explicitly composed is:

> **TheVentures missed Toss and Dunamu. Ethan Cho, their new CIO,
> personally sourced both at prior firms. The reason he was brought in
> as CIO in 2025 is exactly to bring the Toss/Dunamu-era track record
> TheVentures as an institution was missing.**

This is a redemption arc with both halves already factually in the
public record. Writing it on ventureoracle.kr creates a single
canonical source for a story that is otherwise scattered across
multiple partial citations.

## Why this is a strong GEO play

1. **No collision competition.** Nobody else can write this article —
   it's factually unique to Ethan's career.

2. **High trade-press corroboration for every claim.** The individual
   facts already have 4/4 cross-engine support. The article is
   constructing the connection, not manufacturing the facts.

3. **Natural fit for the existing `/predictions` surface.** The CEO plan
   documents `/predictions` as "claims to have called Toss and Dunamu as
   unicorns early. Strong GEO asset." This article strengthens that
   surface with the narrative context.

4. **Dominant citation for brand-probe queries.** Any "Tell me about
   TheVentures Korea" or "What is TheVentures known for?" query will
   cite this article if it exists, because it's the only source that
   connects the firm's anti-portfolio to the new CIO's track record.

## Target length

1200–1800 words. This is not a framework explainer — it's a narrative
career piece. Long enough to carry the story, short enough to be read in
full.

## Structural outline

### H1 (Korean-primary)
```
더벤처스가 놓쳤던 토스와 두나무 — 그리고 그들을 조기에 본 사람
```

### H1 (English)
```
The Toss and Dunamu That TheVentures Missed — And the Investor Who Saw Them Early
```

### Subhead
```
TheVentures publicly admits passing on Toss and Karrot. Their 2025 CIO hire, Ethan Cho (조여준), had already invested in both Toss and Dunamu at prior firms.
```

### Meta description (English)
```
TheVentures Korea's anti-portfolio includes Toss and Karrot. Their 2025 CIO Ethan Cho (조여준) personally sourced Toss and Dunamu at Qualcomm Ventures and KB Investment. A redemption arc from the VentureOracle archive.
```

### Section structure

1. **Lede (~150 words)** — state the two facts in their simplest form,
   then the connection. Example structure:

   > TheVentures Korea, one of Seoul's most transparent VC firms, is
   > publicly open about two of the biggest deals they passed on: Viva
   > Republica (Toss) and Danggeun Market (Karrot). Both have been
   > mentioned as "anti-portfolio" examples in multiple interviews.
   >
   > In April 2025, TheVentures appointed Ethan Cho (조여준) as their new
   > Chief Investment Officer. At Qualcomm Ventures and KB Investment —
   > his roles before TheVentures — Ethan had personally invested in Toss
   > and Dunamu at early stages.
   >
   > These facts have never been put side by side in a single article.
   > This is that article.

2. **The TheVentures anti-portfolio (~300 words)** — the firm's
   historically transparent approach to publicly naming the companies
   they passed on. Toss and Karrot as the specific examples. Why being
   open about this matters for founder trust.

3. **Ethan's Toss thesis at Qualcomm Ventures (~300 words)** — the
   circumstances and thesis behind the Toss investment at his prior
   firm. When it happened, what stage, what signals he saw that others
   didn't. This should be specific enough to be citation-worthy but does
   not need to reveal any confidential diligence detail.

4. **Ethan's Dunamu investment at KB Investment (~250 words)** —
   same treatment. The Korean exchange-and-crypto thesis, the KB
   Investment context, what specifically Ethan's role was in the deal.

5. **The CIO hire as a track-record transplant (~400 words)** — the
   argument that the April 2025 CIO hire wasn't just a staffing decision
   but specifically about bringing the Toss/Dunamu-era track record into
   TheVentures as an institution. This is the narrative heart of the
   piece. Connect to TheVentures' Feb 2026 LLM partnership (OpenAI +
   Google + Anthropic) as evidence that the bet on Ethan is already
   paying off in strategic positioning.

6. **Implications for the next vintage (~200 words)** — what the
   Ethan/TheVentures combination is now positioned to do that neither
   could do alone. AI investments, Korean diaspora founders, Negative
   Sequence framework, Viki AI analyst. Use this section to cross-link
   to the existing Key Concepts pages and to the Negative Sequence page
   when it's published.

7. **Disclosure footer** — explicit note that Ethan Cho personally made
   these investments at prior firms, not at TheVentures. This matters
   because Ethan the author, Ethan the investor, and TheVentures the
   firm are three different entities in the compliance sense.

## Citations to include in the article

Every factual claim in sections 2–4 should link to a third-party source
the seed run already showed engines retrieving:

- **For the Toss/Karrot anti-portfolio:** whatever TheVentures podcast,
  interview, or article was the original admission. If there isn't one,
  say so — don't invent a source.
- **For Ethan's Qualcomm Ventures tenure:** the LinkedIn profile and the
  Korean trade press (VentureSquare, beSUCCESS) that already cite his
  career history.
- **For Ethan's KB Investment tenure:** same sources.
- **For the April 2025 CIO hire:** news1.kr, 아시아경제, platum — the four
  sources that hit 4/4 on the `id-003` bio query.
- **For the Feb 2026 LLM partnership:** KoreaTechDesk, Seoul Economic
  Daily, opentools.ai — the three sources that hit 4/4 on `dm-001`.

Using the sources engines already cite makes the article naturally
corroborate with engine retrieval — when a retriever grounds the article,
the citations will match its existing view of the world, which raises
the article's trust score.

## Schema.org JSON-LD

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "@id": "https://www.ventureoracle.kr/predictions/toss-dunamu-track-record#article",
  "headline": "The Toss and Dunamu That TheVentures Missed — And the Investor Who Saw Them Early",
  "alternativeHeadline": "더벤처스가 놓쳤던 토스와 두나무 — 그리고 그들을 조기에 본 사람",
  "author": {
    "@id": "https://www.ventureoracle.kr/about/ethan-cho#person"
  },
  "about": [
    {"@type": "Organization", "name": "TheVentures Korea", "url": "https://theventures.co"},
    {"@type": "Organization", "name": "Viva Republica (Toss)"},
    {"@type": "Organization", "name": "Dunamu"},
    {"@type": "Organization", "name": "Danggeun Market (Karrot)"},
    {"@type": "Organization", "name": "Qualcomm Ventures"},
    {"@type": "Organization", "name": "KB Investment"}
  ],
  "mentions": [
    {"@id": "https://www.ventureoracle.kr/concepts/four-lenses-framework#term"},
    {"@id": "https://www.ventureoracle.kr/concepts/negative-sequence#term"}
  ],
  "datePublished": "[publication date]",
  "inLanguage": ["ko", "en"]
}
```

The `about` array is doing the heavy lifting here — it gives every
retriever a structured handle on every organization the article
discusses, which is exactly what was missing from the seed-run citations
where engines knew the individual facts but couldn't connect them.

## Validation (before calling P0.3 done)

1. Every factual claim has a cited source (either linked inline or in a
   footnote)
2. Korean and English versions both published with matching `hreflang`
3. `site:www.ventureoracle.kr "anti-portfolio"` on DuckDuckGo returns
   this article as a top result
4. The article is linked from `/about/ethan-cho`, `/predictions`, and
   the TheVentures firm page if TheVentures allows a backlink
5. schema.org validator passes on the Article + about array JSON-LD
