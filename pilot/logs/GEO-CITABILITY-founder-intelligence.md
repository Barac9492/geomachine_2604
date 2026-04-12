# AI Citability Analysis: Founder Intelligence

**URL:** https://www.ventureoracle.kr/concepts/founder-intelligence
**Analysis Date:** 2026-04-13
**Overall Citability Score: 48/100**
**Citability Coverage:** 0% of content blocks score above 70

---

## Score Summary

| Category | Score | Weight | Weighted |
|---|---|---|---|
| Answer Block Quality | 55/100 | 30% | 16.5 |
| Passage Self-Containment | 40/100 | 25% | 10.0 |
| Structural Readability | 45/100 | 20% | 9.0 |
| Statistical Density | 30/100 | 15% | 4.5 |
| Uniqueness & Original Data | 80/100 | 10% | 8.0 |
| **Overall** | | | **48/100** |

---

## Critical Finding: Template Rendering Bug

**The page has 400+ words of substantive content in `concepts.ts` but React renders it as a wall of text.** The `explanation` field contains `\n` newline characters that should create paragraph breaks, but React's `{concept.explanation}` JSX expression collapses all newlines to whitespace.

**Result:** The 232-word "How It Works" section renders as ONE PARAGRAPH. AI systems cannot extract individual passages from a wall of text. This is the single biggest drag on the citability score.

**Fix:** One CSS line on the explanation/application containers: `style={{ whiteSpace: 'pre-line' }}` — or split the text on `\n\n` and wrap each chunk in a `<p>` tag. This would immediately add paragraph breaks and raise the citability score by 15-20 points across all 10 concept pages.

---

## Strongest Content Blocks

### 1. Definition Block -- Score: 72/100
> "Not academic intelligence or test scores, but the composite capacity for good judgment under uncertainty: reading people, timing decisions, driving execution. Persistence, teamwork, and learning ability are all sub-components."

**Why it works:** Uses the "X is [definition]" pattern. Self-contained in 31 words. Names the subject explicitly. Directly answers "What is Founder Intelligence?" Contains the disambiguating clause ("not academic intelligence") that prevents confusion with Accenture's Founders Intelligence. The strongest passage on the page.

### 2. Data Source Attribution -- Score: 65/100
> "Ethan Cho's 20-year career methodology across Qualcomm Ventures, KB Investment, Google Korea, FastVentures, and TheVentures"

**Why it works:** Names specific entities (5 companies + the author). Provides a time-range credential (20-year). Self-contained. Directly answers "who developed Founder Intelligence?"

### 3. Citation Format Section -- Score: 60/100
> APA: Cho, E. (2026). Founder Intelligence. VentureOracle.

**Why it works:** Signals academic-level original authorship. AI systems trained on academic content recognize citation formats as authority markers. Makes the page an authoritative primary source.

---

## Weakest Content Blocks (Rewrite Priority)

### 1. "How It Works" Section -- Score: 38/100

**Current rendering:**
> Founder Intelligence is the set of capacities that determine whether a founder can navigate uncertainty successfully. It is explicitly NOT about academic credentials (학벌), test scores, or raw IQ — those are 'study intelligence' (공부 지능) in Korean, which correlates poorly with startup outcomes. What it IS: 1. Good judgment under uncertainty — in the Kahneman sense... [continues as single 232-word paragraph]

**Problem:** WALL OF TEXT. Five distinct sub-components (judgment, reading nuance, timing, execution, persistence) are jammed into one paragraph because `\n` characters are collapsed by React. The "Korean Diaspora thesis" — the most distinctive and citable content — is buried 150 words deep with no heading or visual break.

**Suggested fix (template-level, affects all concepts):**

In `app/concepts/[slug]/page.tsx`, change the explanation rendering from:
```tsx
{concept.explanation}
```
to:
```tsx
{concept.explanation.split('\n\n').map((para, i) => (
  <p key={i} className="text-slate-300 leading-relaxed mb-4">{para}</p>
))}
```

**Suggested fix (content-level, Founder Intelligence specific):**

Add a sub-heading "The Korean Diaspora Thesis" (H3) above the diaspora paragraph to make it individually extractable. Add statistics: "Korean-origin founders in the US represent X% of YC's top-performing cohorts" or similar verifiable claim.

### 2. "Practical Application" Section -- Score: 42/100

**Current rendering:**
> For VC underwriting: evaluate founders on Founder Intelligence dimensions, not on resume prestige. Specifically look for evidence of (1) reading complex social or competitive situations correctly in their past, (2) timing calls made — even wrong ones, if the reasoning was sound at the time, (3) execution under organizational resistance, and (4) intellectual honesty about what they do not know. [continues as single 126-word paragraph]

**Problem:** The 4-point evaluation checklist is embedded in prose, not rendered as a numbered list. AI systems extract lists with much higher accuracy than inline numbered items. No statistics or specific outcomes referenced.

**Suggested rewrite:**

```
## How VCs Should Evaluate Founder Intelligence

Evaluate founders on these four Founder Intelligence dimensions, not on resume prestige:

1. **Pattern recognition under complexity** — Evidence of reading complex social or competitive situations correctly in their past
2. **Timing quality** — Timing calls made, even wrong ones, assessed by reasoning soundness at the time of the decision
3. **Execution against friction** — Track record of executing under organizational resistance, not just in ideal conditions
4. **Intellectual honesty** — Demonstrated candor about gaps in their knowledge or model

For deal sourcing: Korean-origin founders with US training are structurally undervalued by VCs who anchor on credentials or Silicon Valley archetype matching.
```

### 3. Missing: "What is Founder Intelligence?" Question-Based Heading -- Score: 0/100

**Problem:** No question-based heading exists on the page. The heading "How It Works" is generic and not directly matchable to AI queries like "What is the Founder Intelligence framework?" If someone asks ChatGPT "What is Founder Intelligence?", the engine needs to find a heading that matches the query.

**Suggested fix:** Change `<h2>How It Works</h2>` to `<h2>What is Founder Intelligence?</h2>` in the template, or better: render the `term` field as a question-based heading: `What is ${concept.term}?`

---

## Quick Win Reformatting Recommendations

1. **Split explanation text into paragraphs (template fix)** — Expected citability lift: +15 points. One CSS line or one `.split('\n\n').map()` call. Affects all 10 concept pages.

2. **Add question-based heading "What is Founder Intelligence?"** — Expected citability lift: +8 points. Directly matchable to AI queries.

3. **Render the 4-point evaluation checklist as a numbered HTML list** — Expected citability lift: +5 points. Lists are extracted with 2-3x higher accuracy by AI systems.

4. **Add 3-5 specific statistics** — Expected citability lift: +10 points. Examples: "Korean-born founders represent X% of YC's top-decile outcomes", "Founders scoring high on FI dimensions have Y% higher survival rates at 5 years" (if Ethan has this data from his 20 years).

5. **Add a comparison table: Founder Intelligence vs. Traditional VC Evaluation** — Expected citability lift: +5 points. AI systems extract tables with high accuracy. Two columns: "What traditional VCs evaluate" vs. "What Founder Intelligence evaluates."

**Total potential lift with all 5: +43 points → projected score ~91/100.**

---

## Per-Section Scores

| Section Heading | Words | Answer Quality | Self-Contained | Structure | Stats | Unique | Overall |
|---|---|---|---|---|---|---|---|
| Definition block | 31 | 85 | 90 | 50 | 20 | 90 | 72 |
| How It Works | 232 | 55 | 30 | 35 | 25 | 80 | 43 |
| Practical Application | 126 | 50 | 40 | 40 | 20 | 75 | 44 |
| Data Source | 20 | 70 | 80 | 60 | 50 | 60 | 65 |
| How to Cite | 40 | 45 | 70 | 70 | 10 | 80 | 53 |
| Related Concepts | 100 | 40 | 50 | 60 | 30 | 40 | 43 |
| Related Articles | 120 | 30 | 30 | 50 | 40 | 30 | 34 |
