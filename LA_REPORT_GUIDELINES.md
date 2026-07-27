# LA_REPORT_GUIDELINES.md
**Linear Appraisal Report Templates & Guidelines**  
**Herd:** Forged Farm  
**Breeder:** Brian Denton (Member ID 1660541)  
**Last updated:** 2026-07-27 (default data: LA_SCORES_2026.md)  

Defines how to generate consistent Linear Appraisal (LA) reports.

---

## How to produce a report

When asked to produce a report from these guidelines (e.g. *“Produce a Herd Evaluation based on LA_REPORT_GUIDELINES.md”*), do the following without waiting for extra data:

1. **Read required inputs**
   - This file (templates + rules)
   - `GOALS.md` (objectives, trade-off framework, trait priorities)
   - `LA_SCORES_2026.md` (current herd LA linear traits, category letters, Final Scores)
2. **Pick the report type** from the prompt (Individual / Parentage–Pairing / Herd). If the animal or pairing is named, use that; otherwise for Herd Evaluation use every animal in `LA_SCORES_2026.md`.
3. **Ground every claim in the score file.** Compose Final Score as `GAEV 84` from the four category letters (GENERAL APPEARANCE, DAIRY STRENGTH, BODY CAPACITY, MAMMARY) plus FINAL SCORE. Omit a letter if that category is blank (typical for bucks).

**Example prompts that should work as-is:**
- `Produce a Herd Evaluation based on LA_REPORT_GUIDELINES.md`
- `Produce an Individual Evaluation for Snickers based on LA_REPORT_GUIDELINES.md`
- `Produce a Parentage / Pairing Evaluation for Michael Darling × Amber Waves based on LA_REPORT_GUIDELINES.md`

---

## General Rules (all report types)

1. **Primary objective** = maximize Final Score while supporting longevity and functional durability (see GOALS.md).
2. Present every recommendation as a **package**: expected score impact + functional risks + mitigations.
3. Distinguish high-heritability / high-impact traits (short-to-medium term levers) from low-heritability traits (long-term focus). Explicitly note low-h² traits the animal or herd is **weak** in (need introduction) and **strong** in (need protection).
4. Be specific with numbers (LA scores, heights, category letters) rather than vague language.
5. **Score format:** Always write Final Score and categories as `GAEV 84` (letters first, then numeric score).
6. When an owner height is available, report it alongside the **expected stature score** (miniature scale below) and the official LA stature score for comparison.
7. Favorite animals (Snickers, Tinkles) get extra attention to preserving current strengths (especially liked rump angle).
8. End individual and parentage/pairing reports with clear, actionable breeding notes or a clear recommendation on the proposed mating.
9. Style: clear headings, scannable bullets, consistent GOALS.md terminology, actionable closings — not open-ended discussion.

### Trait priority lens (from GOALS.md)

When ranking improvements or opportunities:

**Higher leverage (usually act first)**
1. Medial Suspensory Ligament
2. Teat Placement & Diameter
3. Dairyness
4. Rump Width
5. Strength
6. Stature (when outside functional range)

**Lower day-to-day priority / slower response**
- Rump angle (mainly when risk of becoming more extreme)
- Rear Udder Arch, Rear Leg set, and other low-h² structural details (track for long-term strategy)

Always pair rump-angle discussion with width/thurl and pelvic capacity as potential mitigations.

### Miniature stature scale (height → expected score)

| Height (inches) | Expected Linear Score |
|-----------------|-----------------------|
| < 17″           | 5                     |
| 18″             | 10                    |
| 19″             | 15                    |
| 20″             | 20                    |
| 21″             | 25                    |
| 22″             | 30                    |
| 23″             | 35                    |
| 24″             | 40                    |
| 25″             | 45                    |

Interpolate for in-between heights (e.g. 20.25″ ≈ 21–22). Report as:
`Owner height: 20.25″ → expected stature score ≈ 21–22`
then compare with the official LA stature score.

---

## Report Type 1: Individual Evaluation

**Purpose:** Evaluate one animal’s current LA performance, identify highest-ROI improvements, and recommend breeding direction.

### Template

```markdown
# Individual LA Evaluation: [Animal Name] ([Reg #])

**Age / Lactation at appraisal:**
**Final Score:** GAEV 84
**Owner height (if measured):** X.XX″ → expected stature score ≈ YY
**Official LA stature score:** ZZ

## Summary
2–4 sentence overview of overall quality, main strengths, and main limitations relative to herd goals.

## Strengths
- Clear positive traits (include scores where helpful)
- Note any low-heritability strengths that should be protected

## Weaknesses / Areas for Improvement
- Ordered roughly by priority (high-h² + high score impact first)
- Flag any functional/longevity concerns

## Highest-ROI Improvement Targets
Ranked easiest / highest-leverage traits based on: current score gap, heritability, scorecard weight, GOALS.md priorities.

## Lower-Priority or Harder Traits
Low impact, already adequate, or low-heritability (slow to change).

## Breeding Notes
- Preferred buck type or specific herd bucks (with rationale)
- Key risks in offspring (e.g., further flattening of rump, loss of a current strength)
- Mitigations worth seeking (e.g., wider thurls)
- Special notes if this is a favorite animal
```

### Type-specific notes
- Always reference the animal’s actual linear scores.
- For young first-fresheners, note that some mammary traits may still mature.

---

## Report Type 2: Parentage / Pairing Evaluation

**Purpose:** Use LA scores of two animals (sire + dam, or prospective pair) to explain/predict an existing offspring’s profile **or** forecast a planned mating. Supports both retrospective analysis and forward breed planning.

### Template

```markdown
# Parentage / Pairing LA Evaluation

**Mode:** [Existing offspring analysis | Prospective mating]

**Pair:**
- Sire / prospective sire: [Name] ([Reg #]) — key LA summary
- Dam / prospective dam: [Name] ([Reg #]) — key LA summary

**(If analyzing an existing animal)** Offspring: [Name] ([Reg #])

## Parental / Pair Score Summary
Side-by-side comparison of the most relevant linear traits and Final Scores.

## Traits Likely Reinforced or Improved
- Both strong → higher probability of good offspring outcomes
- One strong + other adequate (complementary)
- Clear expected gains relative to the weaker parent

## Traits at Risk or Likely Weak
- Both weak or below intermediate → elevated transmission risk
- One extreme that could be transmitted
- Stacking of the same fault

## Expected Profile of Offspring
Plain-language prediction of what the mating is most and least likely to deliver, emphasizing high-h² / high-impact traits (MSL, teats, dairyness, width, etc.), functional risks (e.g., rump angle becoming more extreme), and low-h² traits that may be reinforced or eroded.

## Benefit / Risk / Mitigation Package
- Expected contribution to Final Score and key goals
- Main functional or longevity risks
- Practical mitigations (if any)
- Overall assessment of the package

## Breeding Implications / Recommendation
- Existing animal: how it should be used given parental background
- Prospective mating: recommended, conditional, or better avoided
- Long-term low-h² considerations (gaps to fill or strengths to protect)
```

### Type-specific notes
- With full linear histories, prioritize high-h² traits for short-term predictions; still note low-h² patterns.
- If one animal lacks LA data, state that limitation and use whatever category scores or progeny data are available.
- Main tool for evaluating the young third buck once parental scores are supplied, and for comparing alternative buck × doe combinations.

---

## Report Type 3: Herd Evaluation

**Purpose:** Strategic overview of the appraised herd — collective strengths to lock in, gaps, weaknesses at risk of becoming fixed, and highest-leverage opportunities.

### Template

```markdown
# Herd LA Evaluation
**Appraisal period / data set:**
**Animals included:** (list or count of does and bucks)

## Overall Snapshot
Short paragraph on general quality (score range, category balance, etc.).

## Herd Strengths
- Traits where multiple animals score well
- Low-heritability strengths that exist and should be protected
- Notable individual standouts

## Herd Weaknesses & Gaps
- Consistently suboptimal traits across a meaningful portion of the herd
- Ordered by importance (high-h² + high impact first, then important low-h² gaps)
- Functional/longevity patterns of concern

## Strengths to Lock In (Build Consistency)
- Good/excellent traits across multiple animals or in key breeding animals — the foundation of long-term consistency; deliberately retain and reinforce
- Include high-h² strengths (easier to keep) and low-h² strengths (harder to recover if lost)
- Note which current bucks or does best fix these strengths in the next generation

## Weaknesses at Risk of Becoming Fixed
- Faults on both sides of multiple potential matings
- Patterns harder to remove if repeatedly stacked — call out to avoid or dilute

## Highest-Leverage Opportunities
Concrete actions that move the most Final Score and functional quality in the next 1–3 generations:
- Specific trait focuses
- Use of current herd bucks
- Traits that warrant outside genetics
- Long-term low-h² projects
- Lock in existing strengths while correcting gaps

## Buck Utilization Summary
How current appraised bucks (and any evaluated young buck) best fit herd needs.

## Strategic Notes
Broader observations (age structure, favorite-animal considerations, re-appraisal timing, etc.).
```

### Type-specific notes
- Stay strategic — do not repeat every individual score.
- Emphasize locking in strengths: consistency comes from retaining good traits, not only from fixing faults.
- Surface both high-h² quick wins and low-h² multi-generational projects.

---

**End of LA_REPORT_GUIDELINES.md**
