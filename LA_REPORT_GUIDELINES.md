# LA_REPORT_GUIDELINES.md
**Linear Appraisal Report Templates & Guidelines**  
**Herd:** Forged Farm  
**Breeder:** Brian Denton (Member ID 1660541)  
**Last updated:** 2026-07-27 (default data: LA_SCORES_2026.md)  

Defines how to generate consistent Linear Appraisal (LA) reports.

**Report types:**
1. Individual Report
2. Planning Report
3. Herd Report
4. Doe Breeding Report
5. Buck Breeding Report

---

## How to produce a report

When asked to produce a report from these guidelines (e.g. *“Produce a Herd Report based on LA_REPORT_GUIDELINES.md”*), do the following without waiting for extra data:

1. **Read required inputs**
   - This file (templates + rules)
   - `GOALS.md` (objectives, trade-off framework, trait priorities)
   - `DAIRY_CONCEPTS.md` (**ADGA trait definitions, scales, polarity, terminology** — required so reports do not reverse or invent linear meanings)
   - `LA_SCORES_2026.md` (current herd LA linear traits, category letters, Final Scores)
   - `HERD_BREEDING_ROSTER.md` (**who is currently available** for breeding — does and bucks on hand)
   - `HERD_ROSTER.md` (ADGA identity, Barn Names, LA summary, favorites, and other per-animal notes)
   - For Doe Breeding / Buck Breeding Reports (and any unappraised buck): also `reports/estimated-buck-profile-*.md` and/or `LA_REFERENCE_SCORES.md` when an estimated profile exists
2. **Pick the report type** from the prompt (Individual / Planning / Herd / Doe Breeding / Buck Breeding). If the animal or pairing is named, use that; otherwise for a Herd Report use the animals on `HERD_BREEDING_ROSTER.md` (scores from `LA_SCORES_2026.md`). For a Doe Breeding Report, compare against every buck listed as available on the roster (unless the prompt narrows the set). For a Buck Breeding Report, compare against every doe listed as available on the roster (unless the prompt narrows the set). **Never** treat `LA_REFERENCE_SCORES.md` animals as on-hand breeding partners unless they also appear on the roster.
3. **Ground every claim in the score file and in `DAIRY_CONCEPTS.md`.** Compose Final Score as `GAEV 84` from the four category letters (GENERAL APPEARANCE, DAIRY STRENGTH, BODY CAPACITY, MAMMARY) plus FINAL SCORE. Omit a letter if that category is blank (typical for bucks). Prefer **full trait names** in prose and tables (e.g. Stature, Medial Suspensory Ligament, Final Score); abbreviations are fine in compact score shorthand like `VEVV 88`. If unsure about trait polarity (especially Rump Angle or Udder Depth), check `DAIRY_CONCEPTS.md` before writing.

**Example prompts that should work as-is:**
- `Produce a Herd Report based on LA_REPORT_GUIDELINES.md`
- `Produce an Individual Report for Snickers based on LA_REPORT_GUIDELINES.md`
- `Produce a Planning Report for Michael × Amber based on LA_REPORT_GUIDELINES.md`
- `Produce a Doe Breeding Report for Tinkles based on LA_REPORT_GUIDELINES.md`
- `Produce a Buck Breeding Report for Michael based on LA_REPORT_GUIDELINES.md`

---

## General Rules (all report types)

1. **Primary objective** = maximize Final Score while supporting longevity and functional durability (see GOALS.md).
2. Present every recommendation as a **package**: expected score impact + functional risks + mitigations.
3. Distinguish high-heritability / high-impact traits (short-to-medium term levers) from low-heritability traits (long-term focus). Explicitly note low-h² traits the animal or herd is **weak** in (need introduction) and **strong** in (need protection).
4. Be specific with numbers (LA scores, heights, category letters) rather than vague language. Prefer **Barn Names** from `HERD_ROSTER.md` when referring to herd animals in prose; include Reg # or registered name when identity must be unambiguous.
5. **Score format:** Always write Final Score and categories as `GAEV 84` (letters first, then numeric score).
6. When an owner height is available, report it alongside the **expected stature score** (miniature scale below) and the official LA stature score for comparison.
7. Favorite animals (Snickers, Tinkles) get extra attention to preserving current strengths (especially liked rump angle).
8. End Individual, Planning, Doe Breeding, and Buck Breeding Reports with clear, actionable breeding notes or a clear recommendation on the proposed mating.
9. Style: clear headings, scannable bullets, consistent GOALS.md terminology, actionable closings — not open-ended discussion. Prefer **Barn Names** from `HERD_ROSTER.md` in prose.
10. For Doe Breeding Reports: compare **every available buck** from `HERD_BREEDING_ROSTER.md` against that doe’s gaps and strengths-to-protect; pick one primary recommendation (and optionally a runner-up). Weight real LA scores more heavily than estimated transmitting profiles.
11. For Buck Breeding Reports: compare **every available doe** from `HERD_BREEDING_ROSTER.md` against that buck’s strengths and risks; pick one primary recommendation (and optionally a runner-up / ranked shortlist). Weight real LA scores more heavily than estimated transmitting profiles. Favorites’ protected traits still constrain which does are good partners.
12. **Report filenames:** `reports/[type]-[barn-name-or-herd].md` — e.g. `individual-snickers.md`, `breeding-michael.md`, `herd-forged-farm.md`, `planning-michael-x-amber.md`. Use lowercase barn names; for herd-level reports use the herd slug.

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

**Rump Angle scale (ADGA linear):** **Low = steep**, **high = level/flat** (toward inverted). See `DAIRY_CONCEPTS.md`. “Further flattening” means moving the score **up** toward 50. Always pair flattening risk with width/thurl and pelvic capacity as potential mitigations.

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

## Report Type 1: Individual Report

**Purpose:** Evaluate one animal’s current LA performance, identify highest-ROI improvements, and recommend breeding direction.

### Template

```markdown
# Individual Report: [Animal Name] ([Reg #])

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
- Write reports to `reports/` as `individual-[barn-name].md`.

---

## Report Type 2: Planning Report

**Purpose:** Use LA scores of two animals (sire + dam, or prospective pair) to explain/predict an existing offspring’s profile **or** forecast a planned mating. Supports both retrospective analysis and forward breed planning.

### Template

```markdown
# Planning Report

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
- Write reports to `reports/` as `planning-[barn]-x-[barn].md` (or similar pair slug).

---

## Report Type 3: Herd Report

**Purpose:** Strategic overview of the appraised herd — collective strengths to lock in, gaps, weaknesses at risk of becoming fixed, and highest-leverage opportunities.

### Template

```markdown
# Herd Report
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
- Write reports to `reports/` as `herd-[herd-slug].md` (e.g. `herd-forged-farm.md`).

---

## Report Type 4: Doe Breeding Report

**Purpose:** For one doe, compare each buck currently on hand — pros, cons, and fit to her improvement targets — then recommend which buck to breed her to. Decision aid for the breeding season; not a full Individual Report (use Type 1 for that) and not a deep single-pair forecast (use Type 2 Planning Report for that).

### Template

```markdown
# Doe Breeding Report: [Doe Name] ([Reg #])

**Doe Final Score:** GAEV 84
**Lactation / appraisal context:** (e.g. first-freshener 2026; favorite — protect Rump Angle)
**Bucks compared:** [list names + Final Scores or “estimated”]
**Doe priorities this breeding:** (3–5 bullets from her gaps + strengths to protect, ordered by GOALS.md leverage)

## Doe Snapshot
2–4 sentences: overall quality, binding limits, and what must not be lost in offspring.

## Buck Comparisons

### [Buck 1 Name] ([Reg #]) — [Final Score or “Estimated”]
**Pros (for this doe)**
- Specific traits/scores that address her gaps or reinforce her strengths

**Cons / risks (for this doe)**
- Stacking faults, extremes, or erosion of protected strengths
- Note severity: low / moderate / higher

**Fit summary:** One sentence on overall fit.

### [Buck 2 Name] …
(repeat for every buck on hand)

## Side-by-Side (optional but preferred)
Compact table: each buck vs the doe’s priority traits (e.g. Medial Suspensory Ligament, Teat Placement, Dairyness, Rump Width, Rump Angle, Strength). Use buck’s own scores where scored; for unappraised bucks, cite estimated transmitting outlook and mark as estimated.

## Recommendation
**Primary pick:** [Buck] — why this package best matches her priorities (expected Final Score / trait impact + main risk + mitigation).

**Runner-up (optional):** [Buck] — when to prefer this instead.

**Avoid or deprioritize:** [Buck(s)] — brief reason.

## Benefit / Risk / Mitigation Package (recommended mating)
- Expected benefit to Final Score and key goals
- Main functional / longevity risks
- Mitigations
- Overall package assessment (favorable / conditional / weak)

## Breeding Notes
- Timing / re-appraisal caveats (e.g. young first-freshener mammary may still mature)
- If no on-hand buck adequately fixes a top-priority gap (often Medial Suspensory Ligament or Teat Placement), say so plainly and note that outside genetics may still be warranted later
```

### Type-specific notes
- Default buck set = **Available bucks** in `HERD_BREEDING_ROSTER.md` (not reference-score animals).
- Ground pros/cons in **numbers** relative to this doe, not generic buck praise.
- Favorites (Snickers, Tinkles): explicitly score each buck on whether he protects liked Rump Angle (and other named strengths).
- Estimated bucks: label every claim as estimated; never rank an estimate above a clearly better appraised package without stating the uncertainty.
- Keep the Individual Report’s breeding notes consistent if one already exists; this report should be able to stand alone.
- Write reports to `reports/` as `breeding-[barn-name].md` (lowercase barn name).

---

## Report Type 5: Buck Breeding Report

**Purpose:** For one buck, compare each doe currently available — pros, cons, and fit to what he can improve or risks stacking — then recommend which doe(s) to breed him to. Mirror of the Doe Breeding Report; not a full Individual Report (use Type 1) and not a deep single-pair forecast (use Type 2 Planning Report).

### Template

```markdown
# Buck Breeding Report: [Buck Name] ([Reg #])

**Buck Final Score:** VGE 88 (or “Estimated” + pointer to estimated profile)
**Appraisal / profile context:** (e.g. appraised 2026; or unappraised — using estimated transmitting profile)
**Does compared:** [list names + Final Scores]
**Buck priorities this breeding:** (3–5 bullets — what he best improves; what he must not stack; ordered by GOALS.md leverage)

## Buck Snapshot
2–4 sentences: overall quality / estimated transmitting outlook, clearest strengths, and main risks he brings to a mating.

## Doe Comparisons

### [Doe 1 Name] ([Reg #]) — [Final Score]
**Pros (for this buck)**
- Specific doe traits/scores that complement his strengths or that he can improve
- Note if she already supplies what he lacks (e.g. width, dairyness, teat placement)

**Cons / risks (for this buck)**
- Stacking faults both share, extremes, or erosion of her protected strengths (especially favorites)
- Note severity: low / moderate / higher

**Fit summary:** One sentence on overall fit.

### [Doe 2 Name] …
(repeat for every available doe)

## Side-by-Side (optional but preferred)
Compact table: each doe vs the buck’s priority transmitting traits (e.g. Medial Suspensory Ligament, Teat Placement, Dairyness, Rump Width, Rump Angle, Strength). Use doe scores from `LA_SCORES_2026.md`; for the buck, use his own scores or estimated outlook (marked estimated).

## Recommendation
**Primary pick:** [Doe] — why this package best uses his strengths without stacking his risks (expected Final Score / trait impact + main risk + mitigation).

**Runner-up (optional):** [Doe] — when to prefer this instead.

**Also acceptable / ranked shortlist (optional):** brief list if several does fit similarly.

**Avoid or deprioritize:** [Doe(s)] — brief reason (e.g. shared soft Medial Suspensory Ligament; favorite Rump Angle at risk).

## Benefit / Risk / Mitigation Package (recommended mating)
- Expected benefit to Final Score and key goals
- Main functional / longevity risks
- Mitigations
- Overall package assessment (favorable / conditional / weak)

## Breeding Notes
- How heavily to use this buck this season (primary service vs limited)
- If he is estimated / unappraised, restate uncertainty and preference for confirming with his own LA or early daughters
- If no available doe is a clean fit for his risk profile, say so and suggest holding semen/service or waiting on outside does
```

### Type-specific notes
- Default doe set = **Available does** in `HERD_BREEDING_ROSTER.md` (exclude only if the prompt says so; check `HERD_ROSTER.md` for incomplete-LA or other per-animal caveats).
- Ground pros/cons in **numbers** relative to this buck, not generic doe praise.
- Frame each doe as: what the buck **improves in her**, what she **covers for him**, and what they **risk stacking**.
- Favorites (Snickers, Tinkles): only recommend if the buck package protects liked Rump Angle (and other named strengths); otherwise deprioritize with an explicit reason.
- Estimated bucks: label every claim as estimated; be more conservative on primary picks.
- Keep any existing Individual Report or Doe Breeding Report recommendations consistent where the same pair appears; this report should still stand alone.
- Write reports to `reports/` as `breeding-[barn-name].md` (lowercase barn name). Same filename pattern as Doe Breeding Reports — one breeding report per animal.

---

**End of LA_REPORT_GUIDELINES.md**
