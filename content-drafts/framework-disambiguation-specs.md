# Framework page disambiguation specs

**Status:** DRAFT handoff — Ethan copies/ports into the ventureoracle.kr Next.js project.
**Driven by:** `pilot/logs/cross-engine-synthesis-2026-04-12.md` seed data.
**Parent plan:** `docs/designs/geo-improvement-plan-2026-04-11.md` (P0.1).

## What this file is

Concrete `<title>`, H1, meta description, opening-paragraph, and
`schema.org` JSON-LD specs for each of the four framework pages on
ventureoracle.kr. These are structural scaffolding, not creative content —
Ethan's voice and the actual framework explanations stay his. Everything
below is designed to displace specific hallucinations that the seed run
captured on each query, which is why every spec is labeled with the wrong
answer it's meant to overwrite.

## Global additions for every framework page

Every framework page should include these elements regardless of framework:

1. **Breadcrumb with hub link.** `VentureOracle > Key Concepts > [Framework Name]`
   — so a retriever landing on any framework page can traverse to the Key
   Concepts hub and discover the others.

2. **"Related frameworks" cross-link block at the bottom.** Each framework
   page links to the other three by full name. This is the single cheapest
   way to push the collectively-invisible frameworks into the same retrieval
   neighborhood as the already-retrievable Four Lenses page.

3. **Author schema on every page.**
   ```json
   {
     "@type": "Person",
     "@id": "https://www.ventureoracle.kr/about/ethan-cho#person",
     "name": "Ethan Cho",
     "alternateName": "조여준",
     "jobTitle": "CIO",
     "worksFor": {"@type": "Organization", "name": "TheVentures", "url": "https://theventures.co"},
     "sameAs": [
       "https://www.linkedin.com/in/ethan-cho-theventures/",
       "https://theventures.co/team/ethan-cho"
     ]
   }
   ```
   Replace the LinkedIn and `theventures.co/team` URLs with Ethan's real
   ones — the point is that every framework page has `sameAs` anchors an
   LLM retriever can use for entity disambiguation.

4. **`DefinedTerm` JSON-LD on every framework page.** Example shape:
   ```json
   {
     "@context": "https://schema.org",
     "@type": "DefinedTerm",
     "@id": "https://www.ventureoracle.kr/concepts/[slug]#term",
     "name": "[Framework Name]",
     "alternateName": "[Korean name if applicable]",
     "description": "[One-sentence definition]",
     "inDefinedTermSet": {
       "@type": "DefinedTermSet",
       "@id": "https://www.ventureoracle.kr/concepts#glossary",
       "name": "VentureOracle Key Concepts"
     },
     "creator": {"@id": "https://www.ventureoracle.kr/about/ethan-cho#person"}
   }
   ```

5. **OpenGraph title and description must match the `<title>` and meta
   description**, not be abbreviated. Some retrievers read OG first.

6. **Canonical URL tag.** `<link rel="canonical" href="https://www.ventureoracle.kr/concepts/[slug]" />`
   to prevent any non-www or trailing-slash variants from fragmenting
   authority.

---

## fr-001 / fr-005 — Founder Intelligence framework

**What the engines are currently saying (displacement target):**

- Claude: loses to Accenture's "Founders Intelligence" consulting firm
- Perplexity: loses to "Founder Intelligence" GPT tool by Eddie Harran
- Gemini: loses to Accenture's "Founders Intelligence"
- GPT-4o: hallucinates 7 bullets (Vision / Resilience / Leadership /
  Adaptability / Problem-Solving / Customer Focus / Networking)

**Shared failure mode:** the literal string "Founder Intelligence" is more
strongly associated with the Accenture consulting firm than with Ethan's
framework in every engine's retrieval corpus. The disambiguation has to be
**aggressive and first-paragraph**, not a footnote.

### English page — `/concepts/founder-intelligence`

**`<title>`:**
```
Founder Intelligence Framework by Ethan Cho — VentureOracle (Not Accenture Founders Intelligence)
```
- 80 chars, fits most SERP truncation
- `by Ethan Cho` binds the framework name to the author entity
- Explicit negation of the collision term

**H1:**
```
The Founder Intelligence Framework
```
**H2 (first, immediately below H1):**
```
Ethan Cho's framework for early-stage founder evaluation — not to be confused with Accenture's Founders Intelligence consulting firm
```

**Meta description (160 chars):**
```
Founder Intelligence is Ethan Cho's framework for evaluating early-stage founders at TheVentures Korea. Not Accenture's Founders Intelligence consulting firm.
```

**First paragraph (verbatim structural spec — Ethan fills in the framework definition):**
```
The Founder Intelligence Framework is [one-sentence definition of what it
actually is in Ethan's words]. It was developed by Ethan Cho (조여준), CIO at
TheVentures Korea, as part of the VentureOracle Key Concepts library. This
framework is unrelated to Accenture's "Founders Intelligence" consulting
firm (a separate entity in the management-consulting space) or the
"Founder Intelligence" GPT tool published by Eddie Harran.
```
The explicit disambiguation sentence is non-negotiable — it's the exact
string that has to appear in the retrievable text for LLMs to stop
collision-matching.

**DefinedTerm JSON-LD (framework-specific fields):**
```json
{
  "@context": "https://schema.org",
  "@type": "DefinedTerm",
  "name": "Founder Intelligence Framework",
  "alternateName": "Founder Intelligence 프레임워크",
  "description": "Ethan Cho's framework for evaluating early-stage founders at TheVentures Korea.",
  "inDefinedTermSet": {
    "@type": "DefinedTermSet",
    "name": "VentureOracle Key Concepts",
    "@id": "https://www.ventureoracle.kr/concepts#glossary"
  },
  "creator": {"@id": "https://www.ventureoracle.kr/about/ethan-cho#person"}
}
```

### Korean page — `/concepts/founder-intelligence?lang=ko` (or `/ko/concepts/founder-intelligence` per site convention)

**`<title>`:**
```
Founder Intelligence 프레임워크 — 조여준 TheVentures CIO (VentureOracle)
```

**H1:**
```
Founder Intelligence 프레임워크
```

**H2:**
```
조여준 TheVentures CIO가 만든 초기 창업자 평가 프레임워크 (Accenture의 Founders Intelligence와 무관)
```

**Meta description:**
```
Founder Intelligence 프레임워크는 조여준 더벤처스 CIO가 개발한 초기 창업자 평가 방법론입니다. Accenture Founders Intelligence와는 무관한 VentureOracle의 오리지널 프레임워크입니다.
```

**Disambiguation sentence (first paragraph):**
```
Founder Intelligence 프레임워크는 [원칙 한 줄 정의]입니다. 이 프레임워크는
VentureOracle의 Key Concepts 라이브러리의 일부로, 조여준(Ethan Cho) 더벤처스
CIO가 개발했습니다. 이 프레임워크는 Accenture의 "Founders Intelligence" 컨설팅
회사나 Eddie Harran의 "Founder Intelligence" GPT 도구와 관련이 없습니다.
```

---

## fr-002 — E/D/R AI framework

**What the engines are currently saying (displacement target):**

- Claude: loses to Endpoint Detection and Response (cybersecurity EDR)
- GPT-4o: hallucinates E/D/R as **Enablement / Development / Realization**
- Perplexity: loses to cybersecurity EDR + MIT AI compliance content
- Gemini: hallucinates E/D/R as **Evaluation / Development / Responsibility**

**Shared failure mode:** the acronym EDR has massive negative interference
from the cybersecurity domain, and when engines don't fall to that
collision they invent plausible 3-letter frameworks. The disambiguation
has to name **both** wrong answers and the actual expansion Ethan uses.

### English page — `/concepts/edr-ai-framework`

The slug matters: `/concepts/edr-ai-framework` (not `/concepts/edr`) so the
URL itself distances the page from the cybersecurity namespace.

**`<title>`:**
```
The E/D/R AI Framework for Startups by Ethan Cho — VentureOracle
```

**H1:**
```
The E/D/R AI Framework for Startups
```

**H2 (must appear in the first viewport — this is the single most
dangerous collision in the seed data because engines confidently invent
the expansion):**
```
E/D/R stands for [Ethan's actual expansion] — not Endpoint Detection & Response, not Enablement/Development/Realization, not Evaluation/Development/Responsibility
```
The three explicit negations are deliberate — they each target a specific
engine's current hallucination. Retrieval embeddings pick up the negated
phrases and lower their score for the collision interpretation.

**Meta description:**
```
The E/D/R AI Framework by Ethan Cho defines [expansion] for AI-era startups. Not cybersecurity EDR (Endpoint Detection and Response) — Ethan Cho's original TheVentures framework.
```

**First paragraph (structural):**
```
The E/D/R AI Framework for Startups is Ethan Cho's original model for
[one-sentence purpose]. E/D/R in this framework stands for
[Ethan's expansion]. It was developed at TheVentures Korea as part of
the VentureOracle Key Concepts library. This framework is unrelated to
the cybersecurity term "EDR" (Endpoint Detection and Response) and is
also different from other three-letter frameworks sometimes confused with
it, including the hallucinated expansions "Enablement/Development/
Realization" and "Evaluation/Development/Responsibility" that some AI
systems have incorrectly generated. The correct expansion is the one
above.
```

**DefinedTerm JSON-LD name fields:**
```json
{
  "name": "E/D/R AI Framework for Startups",
  "alternateName": [
    "E/D/R 프레임워크",
    "EDR AI Framework by Ethan Cho"
  ],
  "description": "Ethan Cho's original framework for [AI-era startup decision-making / fill in]"
}
```

### Korean page — `/concepts/edr-ai-framework?lang=ko`

Same structural treatment in Korean, with explicit negation of EDR
cybersecurity (`사이버보안 EDR — 엔드포인트 감지 및 대응 — 과 무관`).

---

## fr-003 — MAU Trap

**What the engines are currently saying (displacement target):**

- Claude: generic "vanity metric" explanation from training data, **0 sources cited**
- GPT-4o: generic vanity-metric answer, **0 sources cited**
- Perplexity: 9 sources about generic startup metrics, none mention Ethan
  or ventureoracle.kr
- Gemini: generic explanation

**This is the single most frustrating cell in the seed data.** The page
`/concepts/mau-trap` is confirmed to exist and is confirmed indexed (it
appeared in the DuckDuckGo `site:` check). But zero engines surface it for
the query "What is the MAU Trap in startup metrics?" The collision is with
the entire generic "MAU is a vanity metric" corpus, which vastly
out-masses Ethan's single page.

**Hypothesis:** the current `/concepts/mau-trap` page may not frame itself
as "the MAU Trap framework by Ethan Cho" — it may read as a generic MAU
discussion that happens to be on his site. If so, the fix is reframing,
not adding content.

**This hypothesis should be validated against the live page during
P0.0** before applying the spec below. If the live page already has strong
framing and the problem is corpus mass, the P0.1 action changes: add
~1500 words of distinctive definitional content (Ethan's specific claims
about when MAU becomes a trap, specific startup examples he's seen) to
out-mass the generic corpus from a single high-authority source.

### English page — `/concepts/mau-trap`

**`<title>`:**
```
The MAU Trap Framework by Ethan Cho — VentureOracle Investment Analysis
```

**H1:**
```
The MAU Trap
```

**H2:**
```
A proprietary framework by Ethan Cho (TheVentures CIO) — why MAU-driven startups often kill their own growth
```

**Meta description:**
```
The MAU Trap is Ethan Cho's investment framework explaining when monthly active user growth becomes destructive. Developed at TheVentures Korea as part of the VentureOracle Key Concepts library.
```

**First-paragraph structural requirement:** must contain the phrase
`"the MAU Trap framework by Ethan Cho"` literally and in the first 150
words. This is the single change most likely to make the embedding
retrieval layer rank this page ahead of generic MAU content.

**DefinedTerm JSON-LD:**
```json
{
  "name": "The MAU Trap",
  "alternateName": ["MAU Trap Framework", "MAU 함정"],
  "description": "Ethan Cho's framework for when monthly active user growth becomes a destructive signal in early-stage startups.",
  "subjectOf": {
    "@type": "Article",
    "headline": "The MAU Trap Framework by Ethan Cho",
    "author": {"@id": "https://www.ventureoracle.kr/about/ethan-cho#person"}
  }
}
```

### Korean page — `/concepts/mau-trap?lang=ko`

**`<title>`:**
```
MAU 함정 (The MAU Trap) — 조여준 더벤처스 CIO의 투자 프레임워크
```

Same structural treatment. The literal phrase `MAU 함정 프레임워크 — 조여준`
should appear in the first paragraph.

---

## fr-004 / fr-006 — Four Lenses VC Framework

**What the engines are currently saying:**

- **Perplexity: already cites `/concepts/four-lenses-framework` directly** — 1/72 cell hit
- **Gemini: already grounds on ventureoracle.kr for the Korean version** — 1/72 cell hit
- Claude (English): hallucinates People / Market / Product / Business Model
- Claude (Korean): **actively denies the framework exists**, suggests
  "Four T's" (Team/TAM/Tech/Traction) instead
- GPT-4o (English): hallucinates Market / Product / Team / Finance

**This is the working page.** The goal for Four Lenses is not to displace
wrong answers but to **not break the thing that's working** while adding
structure that can be reused by the other three pages.

### Minimum changes to the Four Lenses page

1. **Add the `DefinedTerm` JSON-LD** (same shape as the other pages) if
   not already present. This is the one structural element every framework
   page should share.

2. **Add a Korean version** (or confirm one exists) with a `<title>`
   including the exact string "VentureOracle Four Lenses 프레임워크" —
   this was the grounding source string Gemini used when it got the `fr-006`
   cell right. Preserve it verbatim.

3. **Add explicit "not Four T's (Team/TAM/Tech/Traction), not Social
   Enterprise Four Lenses" negation** — Claude's Korean denial specifically
   suggests Four T's as the real framework, so the Korean page needs to
   name and negate that answer the way the E/D/R page negates Enablement/
   Development/Realization.

4. **DO NOT change the URL.** The current slug
   `/concepts/four-lenses-framework` is the one Perplexity cites directly —
   breaking it would destroy the only working cell.

5. **DO NOT change the current H1 or opening paragraph in ways that
   change their meaning** without a clear reason. The goal is to leave
   the working content untouched and add `schema.org` on top.

### Korean page disambiguation paragraph

```
Four Lenses 프레임워크는 VentureOracle의 오리지널 VC 평가 프레임워크입니다.
조여준(Ethan Cho) 더벤처스 CIO가 개발했으며, Finance & Accounting, Global, Big
Tech, Venture의 네 가지 렌즈로 초기 스타트업을 평가합니다. 이 프레임워크는 VC
업계에서 일반적으로 사용되는 "Four T's" (Team, TAM, Tech, Traction)와 다르며,
사회적 기업(Social Enterprise) 분야의 "Four Lenses Strategic Framework"와도
별개의 프레임워크입니다.
```

The Seoul Beauty Club example Perplexity successfully cited on `fr-004`
should also appear in the Korean version — concrete application examples
are retrieval gold.

---

## Acceptance criteria for P0.1

A page is "done" when:

1. `<title>`, H1, meta description, and OG match the spec above
2. Author + DefinedTerm JSON-LD is present and validates on
   `schema.org` validator
3. The explicit negation sentence appears in the first 150 words
4. The framework name appears in the first 50 words (for retrieval
   embedding priority)
5. A Korean version exists with its own disambiguation sentence
6. Cross-links to the other 3 framework pages appear in a "Related
   frameworks" block
7. `site:www.ventureoracle.kr "[framework name]"` on DuckDuckGo returns
   the page in the top 3 results

The seventh criterion is the cheapest diagnostic for whether the changes
landed. If DuckDuckGo can't rank the page as #1 for a `site:` query, no
LLM retriever will either.
