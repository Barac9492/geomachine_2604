# Negative Sequence framework — new page outline

**Target URL:** `/concepts/negative-sequence` on www.ventureoracle.kr
**Status:** DRAFT handoff — structural outline only, Ethan fills framework content
**Driven by:** `pilot/logs/cross-engine-synthesis-2026-04-12.md` medium-confidence finding #6
**Parent plan:** `docs/designs/geo-improvement-plan-2026-04-11.md` (P0.2)

## Why this page needs to exist

GPT-4o (on `id-003`) and Gemini (on `dm-008`) both independently surfaced
Ethan's book *죽음의 순서 (Death's Sequence)* via yes24 and aladin.co.kr in
the 2026-04-11 seed run. Full title: *[전자책] 죽음의 순서 — AI 시대, 한국
스타트업의 유일한 생존 공식*. Both engines mentioned that the book contains
a framework called "**Negative Sequence**" about turning Korea's demographic
cliff into an AI-era global opportunity.

But **neither engine could link that framework to a dedicated page on
ventureoracle.kr — because no such page exists.** The book gets cited, the
framework name gets mentioned, and then the retrieval trail dead-ends at
the retailer pages.

Creating `/concepts/negative-sequence` gives the book's central framework a
canonical, retrievable URL and wires it into the VentureOracle Key Concepts
graph alongside the four existing frameworks. This is one of the highest
cost-to-impact actions in the plan because:

1. **The retrieval signal already exists** — two engines already associate
   "Negative Sequence" with Ethan. The page just has to be there to catch
   the citation.
2. **No collision risk** — "Negative Sequence" has much less retrieval
   interference than "Founder Intelligence" or "EDR" (the only collision is
   with mathematical sequences, which LLM retrievers can disambiguate by
   context once the VentureOracle page exists).
3. **The content source already exists** — the framework is defined in
   Ethan's book, which is already online at yes24 and aladin. Ethan isn't
   writing a new framework; he's hoisting an existing one.

## Target length

1500–2500 words, Korean primary, English version for the second pass. The
Korean version is primary because the book is Korean, the existing
retrieval signal comes from Korean retailers, and Korean bio queries
(`조여준`, `더벤처스`) are already 4/4 perfect in the seed data — meaning the
Korean-language surface of Ethan's brand is retrievable in a way the
English surface isn't yet.

## Structural outline

### H1 (Korean)
```
Negative Sequence — AI 시대 한국 스타트업의 유일한 생존 공식
```

### H1 (English)
```
The Negative Sequence Framework — Korea's Demographic Cliff as an AI-Era Advantage
```

### Meta description (Korean, 160 chars)
```
Negative Sequence는 조여준(Ethan Cho) 더벤처스 CIO가 개발한 프레임워크로, 한국의 인구 절벽을 AI 시대 글로벌 기회로 전환하는 관점을 제시합니다. 책 '죽음의 순서' 핵심 프레임워크.
```

### Meta description (English, 160 chars)
```
Negative Sequence is Ethan Cho's framework for reframing Korea's demographic decline as a competitive advantage in the AI era. The core framework from his book Death's Sequence.
```

### Section structure (what Ethan fills in)

The page should follow a structure that mirrors the Four Lenses page (the
proven-retrievable framework page on the site). Target sections:

1. **One-sentence definition** — the first 50 words of the page should
   contain the exact phrase "Negative Sequence framework by Ethan Cho" and
   a single-sentence definition.

2. **Origin and context** — brief (~200 words) on why the framework
   exists: Korea's demographic trajectory, the AI-era inflection, and why
   most Korean VC thinking is missing the reframing.

3. **The framework itself** — the core content. Ethan's book already has
   this; this section is the ventureoracle.kr canonical transcription.
   Target ~800 words. Should name the distinct stages or lenses of the
   framework (whatever structure the book uses).

4. **A worked example** — at least one concrete case study of a startup
   decision through the Negative Sequence lens. Concrete examples are
   retrieval gold — Perplexity cited Four Lenses partly on the strength of
   the Seoul Beauty Club example.

5. **Relationship to other VentureOracle frameworks** — ~200 words
   connecting Negative Sequence to Four Lenses, Founder Intelligence,
   E/D/R, and MAU Trap. This is the cross-link block that makes each
   framework page pull the others into the same retrieval neighborhood.

6. **Book reference and further reading** — explicit link to the yes24
   and aladin pages for *죽음의 순서*. This is the **reverse of the usual
   direction**: we're using the retailer pages as authority anchors for
   the ventureoracle.kr page, not the other way around. Since the
   retailer pages already carry the retrieval signal, explicitly linking
   to them from ventureoracle.kr lets retrievers traverse back.

## Schema.org JSON-LD

```json
{
  "@context": "https://schema.org",
  "@type": "DefinedTerm",
  "@id": "https://www.ventureoracle.kr/concepts/negative-sequence#term",
  "name": "Negative Sequence Framework",
  "alternateName": [
    "Negative Sequence",
    "죽음의 순서",
    "Death's Sequence Framework"
  ],
  "description": "Ethan Cho's framework for reframing Korea's demographic decline as a competitive advantage in the AI era. The core framework from his book '죽음의 순서 (Death's Sequence)'.",
  "inDefinedTermSet": {
    "@type": "DefinedTermSet",
    "@id": "https://www.ventureoracle.kr/concepts#glossary",
    "name": "VentureOracle Key Concepts"
  },
  "creator": {
    "@type": "Person",
    "@id": "https://www.ventureoracle.kr/about/ethan-cho#person",
    "name": "Ethan Cho",
    "alternateName": "조여준"
  },
  "subjectOf": {
    "@type": "Book",
    "name": "죽음의 순서 - AI 시대, 한국 스타트업의 유일한 생존 공식",
    "alternateName": "Death's Sequence: The Only Survival Formula for Korean Startups in the AI Era",
    "author": {"@id": "https://www.ventureoracle.kr/about/ethan-cho#person"},
    "sameAs": [
      "https://www.yes24.com/[the actual yes24 URL for the book]",
      "https://www.aladin.co.kr/[the actual aladin URL for the book]"
    ]
  }
}
```

The `sameAs` on the Book subtype is important — it's the crosswalk that
lets LLM retrievers that already have the yes24/aladin signal recognize
ventureoracle.kr/concepts/negative-sequence as the canonical page for the
same entity.

## Cross-linking from existing pages

After this page is published, add links to it from:

1. **`/about/ethan-cho`** — in a "Books and Frameworks" block. Text:
   `Ethan's book 죽음의 순서 outlines the Negative Sequence framework for
   AI-era Korean startups. Read the framework here.`
2. **Key Concepts landing page** — add as the 5th framework card.
3. **Each of the 4 existing framework pages** — in the "Related
   frameworks" cross-link block (specified in
   `framework-disambiguation-specs.md`).
4. **`/predictions`** — if any of Ethan's predictions can be framed
   through the Negative Sequence lens, link back from the prediction page
   to the framework page.

## Validation (before calling P0.2 done)

1. `site:www.ventureoracle.kr "Negative Sequence"` on DuckDuckGo returns
   the page as #1
2. `schema.org` validator passes on the DefinedTerm + Book JSON-LD
3. The Korean version is linked from the English version via
   `hreflang` alternate tag
4. The page is in the sitemap.ts output and the next Vercel build
   publishes it under the www hostname
