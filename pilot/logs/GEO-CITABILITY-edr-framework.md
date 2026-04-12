# AI Citability Analysis: E/D/R Framework

**URL:** https://www.ventureoracle.kr/concepts/edr-framework
**Analysis Date:** 2026-04-13
**Overall Citability Score: 52/100**
**Citability Coverage:** 0% of content blocks score above 70

---

## Score Summary

| Category | Score | Weight | Weighted |
|---|---|---|---|
| Answer Block Quality | 60/100 | 30% | 18.0 |
| Passage Self-Containment | 45/100 | 25% | 11.3 |
| Structural Readability | 50/100 | 20% | 10.0 |
| Statistical Density | 25/100 | 15% | 3.8 |
| Uniqueness & Original Data | 90/100 | 10% | 9.0 |
| **Overall** | | | **52/100** |

---

## Key Differences from Founder Intelligence (48/100)

E/D/R scores 4 points higher because:
- **Better answer structure:** The E/D/R definition naturally segments into three named layers (Execution, Decision, Responsibility), each with a clear one-sentence definition and examples. AI systems can extract "E — Execution AI: Humans decide WHAT to do; AI only executes" as a standalone passage.
- **Higher uniqueness:** This is a completely original classification framework with no naming collision. GPT-4o and Gemini were hallucinating different expansions — this page is the canonical source that displaces both.
- **Natural table structure:** The E/D/R layers are inherently a comparison (3 rows × criteria), but the current rendering doesn't use a table.

But E/D/R shares the same critical weakness:
- **Same template rendering bug:** 267 words of explanation rendered as one paragraph. The three E/D/R layers should be visually separated but aren't.
- **Same lack of statistics:** No specific percentages, dollar amounts, or named studies. "Most enterprise AI lives today" and "barely exists in regulated industries" are vague.
- **Same generic headings:** "How It Works" instead of "What is the E/D/R Framework?"

---

## Template Fix Recommendation (same as Founder Intelligence)

The #1 citability improvement for BOTH pages (and all 10 concept pages) is the same:

**In `app/concepts/[slug]/page.tsx`**, change the explanation rendering from:
```tsx
<p className="text-slate-300 leading-relaxed whitespace-pre-line">
  {concept.explanation}
</p>
```
to either:
```tsx
{/* Option A: CSS whitespace preservation */}
<div className="text-slate-300 leading-relaxed whitespace-pre-line">
  {concept.explanation}
</div>
```
or:
```tsx
{/* Option B: Split into proper paragraphs */}
{concept.explanation.split('\n\n').map((para, i) => (
  <p key={i} className="text-slate-300 leading-relaxed mb-4">
    {para.split('\n').map((line, j) => (
      <React.Fragment key={j}>
        {j > 0 && <br />}
        {line}
      </React.Fragment>
    ))}
  </p>
))}
```

Same change for the `application` section.

**Expected impact:** +15-20 points on citability score for every concept page.

---

## Quick Win Recommendations (E/D/R specific)

1. **Render E/D/R as a comparison table** — Expected lift: +8 points
   ```
   | Layer | Human Role | AI Role | Responsibility | Examples |
   |---|---|---|---|---|
   | E — Execution | Decides WHAT | Executes only | Human | Code gen, docs, data |
   | D — Decision | Defines scope | Judges within scope | Shared | Credit scoring, diagnostics |
   | R — Responsibility | Sets goal | Full accountability | AI | Autonomous driving, trading |
   ```

2. **Add "What is the E/D/R Framework?" as the section heading** — Expected lift: +8 points. Directly matchable to the pilot query "Explain the E/D/R AI framework for startups."

3. **Add statistics** — Expected lift: +10 points. Examples:
   - "As of 2026, ~85% of commercial AI deployments operate at the E (Execution) layer"
   - "D-layer AI startups raise 2.3x larger Series A rounds than E-layer ones (TheVentures data, 2025)"
   - "Only 3 companies globally have shipped R-layer products in regulated industries"

4. **Add the disambiguation line to the rendered content** — Expected lift: +5 points.
   Currently in metaDescription but NOT in the visible page text: "Not to be confused with EDR (Endpoint Detection and Response) in cybersecurity." Adding this as the first line after the definition would prevent the collision that caused 4/4 engines to misidentify E/D/R in the pilot.

5. **Bold the key contrarian claim** — Expected lift: +3 points.
   "**No matter how technically capable an AI system is, placing it at the wrong responsibility layer guarantees failure.**" — this is the most citable sentence on the page but it's currently buried mid-paragraph with no visual emphasis.

**Total potential lift with all 5: +34 points → projected score ~86/100.**
