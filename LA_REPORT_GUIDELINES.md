# LA_REPORT_GUIDELINES.md
**Linear Appraisal Report Templates & Guidelines**  
**Last updated:** 2026-07-28  

Defines how to generate consistent Linear Appraisal (LA) reports.  
Repo file roles and allowed dependencies: see `README.md`.

**Report types:**
1. Individual Report
2. Planning Report
3. Herd Report
4. Doe Breeding Report
5. Buck Breeding Report
6. Herd Breeding Report

---

## Inputs (read once per report job)

| File | Use for |
|------|---------|
| `GOALS.md` | Objectives, trade-off framework, trait priorities, preferred Rump Angle band |
| `DAIRY_CONCEPTS.md` | ADGA trait definitions, scales, polarity, terminology, functional risks & mitigations |
| `LA_SCORES_2026.md` | Current herd linear traits, category letters, Final Scores |
| `HERD_BREEDING_ROSTER.md` | Who is currently available to breed (does and bucks on hand) |
| `HERD_ROSTER.md` | ADGA identity, Barn Names, LA summary, strengths-to-protect / caveats |
| `LA_REFERENCE_SCORES.md` | Outside / pedigree reference scores (not on-hand partners unless also on the breeding roster) |
| `profiles/estimated-*-profile-*.md` | Estimated phenotype / transmitting values (full estimate or blank fills) |
| `scripts/bis.py` | Breeding Impact Score implementation |

---

## How to produce a report

When asked to produce a report from these guidelines (e.g. *“Produce a Herd Report based on LA_REPORT_GUIDELINES.md”*), do the following without waiting for extra data:

1. **Read the Inputs table above** (only the files needed for that report type).
2. **Pick the report type** from the prompt. If the animal or pairing is named, use that. Otherwise:
   - Herd Report → animals on the breeding roster; scores from the score table.
   - Herd Breeding Report → every available doe×buck on the breeding roster; assign max-BIS pairs.
   - Doe Breeding Report → every available buck on the breeding roster (unless the prompt narrows the set).
   - Buck Breeding Report → every available doe on the breeding roster (unless the prompt narrows the set).
   - Never treat reference-score animals as on-hand breeding partners unless they also appear on the breeding roster.
3. **Ground every claim** in the score table and concepts. Compose Final Score as `GAEV 84` from the four category letters (GENERAL APPEARANCE, DAIRY STRENGTH, BODY CAPACITY, MAMMARY) plus FINAL SCORE. Omit a letter if that category is blank (typical for bucks). Prefer **full ADGA trait names** in prose and tables; abbreviations are fine in compact score shorthand like `VEVV 88`. Pull polarity, risks, and mitigations from concepts; priorities and owner preferences from herd goals. Do not copy preference or mitigation essays into reports.

**Example prompts that should work as-is:**
- `Produce a Herd Report based on LA_REPORT_GUIDELINES.md`
- `Produce an Individual Report for [Barn Name] based on LA_REPORT_GUIDELINES.md`
- `Produce a Planning Report for [Buck] × [Doe] based on LA_REPORT_GUIDELINES.md`
- `Produce a Doe Breeding Report for [Barn Name] based on LA_REPORT_GUIDELINES.md`
- `Produce a Buck Breeding Report for [Barn Name] based on LA_REPORT_GUIDELINES.md`
- `Produce a Herd Breeding Report based on LA_REPORT_GUIDELINES.md`

---

## General Rules (all report types)

1. **Primary objective** = maximize Final Score while supporting longevity and functional durability (per herd goals).
2. Present every recommendation as a **package**: expected score impact + functional risks + mitigations (risks/mitigations from concepts; priorities from herd goals).
3. Distinguish high-heritability / high-impact traits (short-to-medium term levers) from low-heritability traits (long-term focus). Explicitly note low-h² traits the animal or herd is **weak** in (need introduction) and **strong** in (need protection).
4. Be specific with numbers (LA scores, heights, category letters) rather than vague language. Prefer **Barn Names** from the herd roster in prose; include Reg # or registered name when identity must be unambiguous. Use **breeding** / **breed** — never **mating** / **mate** (concepts language rules).
5. **Score format:** Always write Final Score and categories as `GAEV 84` (letters first, then numeric score).
6. When an owner height is available, report it alongside the **expected stature score** (miniature scale below) and the official LA stature score for comparison.
7. End Individual, Planning, Doe Breeding, and Buck Breeding Reports with clear, actionable breeding notes or a clear recommendation on the proposed breeding.
8. Style: clear headings, scannable bullets, actionable closings — not open-ended discussion.
9. For Doe Breeding Reports: compare **every available buck** on the breeding roster; compute **BIS** for each pair; list **most → least by BIS**; primary pick = highest BIS.
10. For Buck Breeding Reports: compare **every available doe** on the breeding roster; compute BIS for each pair (same score as the doe-side report); list **most → least by BIS**; primary pick = highest BIS.
11. **Report filenames:** `reports/[type]-[barn-name-or-herd].md` — e.g. `individual-[barn].md`, `breeding-[barn].md`, `herd-[herd-slug].md`, `herd-breeding-[herd-slug].md`, `planning-[buck]-x-[doe].md`.
12. For Herd Breeding Reports: assign **every available doe** on the breeding roster a primary buck by **max BIS** (same scores as Doe/Buck Breeding Reports); if one buck is primary for many does, add a **service-priority** order (highest BIS first, then largest BIS edge over the confirmed runner-up) and a confirmed-score fallback plan.

### Trait priority lens

Rank improvements using the ordered priorities in herd goals. Do not maintain a second hardcoded priority list here.

### Breeding Impact Score (BIS)

Use BIS to rank breeding selections consistently across Doe and Buck Breeding reports. **The same doe×buck pair must receive the same BIS** in both report types.

```
BIS = GapClosure − RiskPenalty − ConfidencePenalty
```

- Higher = more preferred for expected net LA improvement (after risks).
- Round to **1 decimal**. Incomplete doe LA with **no** estimated profile → **BIS N/A** (list last). Incomplete/dry does **with** an estimated profile (`estimated: yes`) are scorable; ConfidencePenalty applies.
- Implementation: the BIS script listed in Inputs (loads animals/scores from markdown; Rump Angle preference band from herd goals when present). **Do not hardcode herd animals or owner preferences in scripts.**

| BIS | Meaning |
|-----|---------|
| **Positive** | Gap closure outweighs scored risks / uncertainty |
| **Near 0** | Roughly break-even after risks |
| **Negative** | Risks, dilution, or missing mammary proof outweigh gains |
| **N/A** | Cannot score (incomplete LA) |

**GapClosure** — weighted traits (default weights follow typical goals leverage):

| Trait | Key | Weight (W) |
|-------|-----|------------|
| Medial Suspensory Ligament | `msl` | 5.0 |
| Teat Placement | `tp` | 4.0 |
| Teat Diameter | `td` | 3.0 |
| Dairyness | `dy` | 4.0 |
| Rump Width | `rw` | 3.0 |
| Strength | `st` | 2.0 |
| Rump Angle | `ra` | 2.0 |
| Stature | `stat` | 1.0 |

For each trait with numeric doe score `D` and partner value `P` (except Rump Angle):

1. **Gap fill** (doe below 30 and partner higher): `W × min((P−D)/5, 2.0)` (×**0.75** if that partner trait is profile-estimated).
2. **Dilution** (doe at/above 32 and partner lower): `W × max((P−D)/5, −1.5) × 0.5`.
3. Otherwise 0. Partner unscored → 0 for that trait.

**Rump Angle GapClosure:** If herd goals define `Preferred Rump Angle band: LOW–HIGH`, credit partners closer to that band than the doe. If no band is defined, skip RA GapClosure.

**RiskPenalty** (functional basis in concepts):

| Condition | Penalty |
|-----------|---------|
| Doe RA above herd preferred upper bound and partner further flattens | `2.0 + 0.4×(partner−doe)` |
| Partner RA in the relatively level range (~≥30) and partner Rump Width &lt; 26 | `+1.5` |
| Doe MSL ≤ 20 and partner unscored for MSL | `+1.5` |
| Doe MSL ≤ 20 and partner MSL ≤ 22 | `+3.0` |
| Doe Teat Placement ≤ 21 (wide) and partner unscored | `+1.0` |
| Doe Teat Placement ≤ 21 and partner TP ≤ 22 | `+2.5` |

**ConfidencePenalty:** **`+2.0`** if the partner is fully estimated / unappraised (`estimated: yes`); **`+2.0`** if the doe is fully estimated (incomplete/dry LA replaced by a profile with `estimated: yes`). Stack both when applicable. **`0`** for mammary/blank fills on an appraised animal (`estimated: no`) — those traits already use the ×0.75 GapClosure multiplier.

**Profiles:** Matching `profiles/estimated-*-profile-*.md` files supply Script inputs. Appraised animals: official LA wins; profile **fills blanks** only. Incomplete/dry does or unappraised bucks: full profile values with `estimated: yes`. Mark estimated claims in report prose.

**Report requirements:** BIS-descending order; BIS in headings; Side-by-Side BIS row preferred; primary = highest BIS. Discuss risks/mitigations from concepts — do not paste preference or mitigation tables into every report.

### Miniature stature scale (height → expected score)

Official miniature inch→score table from ADGA Linear Appraisal SOP Appendix A. Stature is measured and recorded as a linear on all goats [2024].

| Height (inches) | Expected Linear Score |
|-----------------|-----------------------|
| ≤ 17″           | 5                     |
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
# Individual Report: [Registered Name] ([Reg #])

**Barn Name:** [Barn Name]
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
Ranked easiest / highest-leverage traits based on: current score gap, heritability, scorecard weight, herd-goal priorities.

## Lower-Priority or Harder Traits
Low impact, already adequate, or low-heritability (slow to change).

## Breeding Notes
- Preferred buck type or top on-hand buck by **BIS** (cite BIS and point to `reports/breeding-[barn].md` for the full ranking)
- Key risks in offspring (from scores + concepts)
- Mitigations (from concepts when applicable)
- Special notes for named strengths-to-protect (from herd roster / herd goals)
```

### Type-specific notes
- Use full **registered name** in the report title; use **Barn Name** everywhere else in the body.
- Always reference the animal’s actual linear scores.
- For young first-fresheners, note that some mammary traits may still mature.
- Omit owner-height lines when no measurement is available (do not invent heights).
- In **Breeding Notes**, name the current top on-hand buck by **BIS** and state main package risks; do not re-litigate the full buck comparison here.
- Write reports to `reports/` as `individual-[barn-name].md`.

---

## Report Type 2: Planning Report

**Purpose:** Use LA scores of two animals (sire + dam, or prospective pair) to explain/predict an existing offspring’s profile **or** forecast a planned breeding. Supports both retrospective analysis and forward breed planning.

### Template

```markdown
# Planning Report

**Mode:** [Existing offspring analysis | Prospective breeding]

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
Plain-language prediction of what the breeding is most and least likely to deliver, emphasizing high-h² / high-impact traits (MSL, teats, dairyness, width, etc.), functional risks (e.g., rump angle becoming more extreme), and low-h² traits that may be reinforced or eroded.

## Benefit / Risk / Mitigation Package
- Expected contribution to Final Score and key goals
- Main functional or longevity risks
- Practical mitigations (if any)
- Overall assessment of the package

## Breeding Implications / Recommendation
- Existing animal: how it should be used given parental background
- Prospective breeding: recommended, conditional, or better avoided
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
- Faults on both sides of multiple potential breedings
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
Broader observations (age structure, strengths-to-protect, re-appraisal timing, etc.).
```

### Type-specific notes
- Stay strategic — do not repeat every individual score.
- Emphasize locking in strengths: consistency comes from retaining good traits, not only from fixing faults.
- Surface both high-h² quick wins and low-h² multi-generational projects.
- Write reports to `reports/` as `herd-[herd-slug].md`.

---

## Report Type 4: Doe Breeding Report

**Purpose:** For one doe, compare each buck currently on hand — pros, cons, and fit to her improvement targets — then recommend which buck to breed her to. Decision aid for the breeding season; not a full Individual Report (use Type 1 for that) and not a deep single-pair forecast (use Type 2 Planning Report for that).

### Template

```markdown
# Doe Breeding Report: [Doe Name] ([Reg #])

**Doe Final Score:** GAEV 84
**Lactation / appraisal context:** (e.g. first-freshener 2026; strengths to protect from roster/goals)
**Bucks compared (BIS order):** [list names + Final Scores or “estimated” + BIS, highest first]
**Doe priorities this breeding:** (3–5 bullets from her gaps + strengths to protect, ordered by herd-goal leverage)

## Doe Snapshot
2–4 sentences: overall quality, binding limits, and what must not be lost in offspring.

## Buck Comparisons
List **most → least preferred by BIS**. Incomplete/estimated partners still appear, ranked by their BIS (N/A last).

### 1. [Buck 1 Name] ([Reg #]) — [Final Score or “Estimated”] — **BIS +X.X**
**Pros (for this doe)**
- Specific traits/scores that address her gaps or reinforce her strengths

**Cons / risks (for this doe)**
- Stacking faults, extremes, or erosion of protected strengths
- Note severity: low / moderate / higher

**Fit summary:** One sentence on overall fit.

### 2. [Buck 2 Name] … — **BIS …**
(repeat for every buck on hand, in BIS order)

## Side-by-Side (optional but preferred)
Compact table: each buck vs the doe’s priority traits (e.g. Medial Suspensory Ligament, Teat Placement, Dairyness, Rump Width, Rump Angle, Strength). Include a **BIS** row. Use buck’s own scores where scored; for unappraised bucks, cite estimated transmitting outlook and mark as estimated. Column order = BIS order.

## Recommendation
**Primary pick:** [Buck] (BIS +X.X) — why this package best matches her priorities (expected Final Score / trait impact + main risk + mitigation).

**Runner-up (optional):** [Buck] (BIS …) — when to prefer this instead.

**Avoid or deprioritize:** [Buck(s)] (BIS …) — brief reason.

## Benefit / Risk / Mitigation Package (recommended breeding)
- Expected benefit to Final Score and key goals
- Main functional / longevity risks
- Mitigations
- Overall package assessment (favorable / conditional / weak)

## Breeding Notes
- Timing / re-appraisal caveats (e.g. young first-freshener mammary may still mature)
- If no on-hand buck adequately fixes a top-priority gap (often Medial Suspensory Ligament or Teat Placement), say so plainly and note that outside genetics may still be warranted later
```

### Type-specific notes
- Default buck set = **Available bucks** on the breeding roster (not reference-score animals).
- Rank and recommend using **BIS** (§ Breeding Impact Score); do not hand-rank against the score without stating why.
- Ground pros/cons in **numbers** relative to this doe, not generic buck praise.
- When the herd roster or herd goals name strengths to protect, those must appear in prose and may feed BIS risk penalties.
- Estimated bucks: label every claim as estimated; BIS already applies ConfidencePenalty.
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
**Does compared (BIS order):** [list names + Final Scores + BIS, highest first]
**Buck priorities this breeding:** (3–5 bullets — what he best improves; what he must not stack; ordered by herd-goal leverage)

## Buck Snapshot
2–4 sentences: overall quality / estimated transmitting outlook, clearest strengths, and main risks he brings to a breeding.

## Doe Comparisons
List **most → least preferred by BIS**. Incomplete LA does appear last as **BIS N/A**.

### 1. [Doe 1 Name] ([Reg #]) — [Final Score] — **BIS +X.X**
**Pros (for this buck)**
- Specific doe traits/scores that complement his strengths or that he can improve
- Note if she already supplies what he lacks (e.g. width, dairyness, teat placement)

**Cons / risks (for this buck)**
- Stacking faults both share, extremes, or erosion of her protected strengths
- Note severity: low / moderate / higher

**Fit summary:** One sentence on overall fit.

### 2. [Doe 2 Name] … — **BIS …**
(repeat for every available doe, in BIS order)

## Side-by-Side (optional but preferred)
Compact table: each doe vs the buck’s priority transmitting traits (e.g. Medial Suspensory Ligament, Teat Placement, Dairyness, Rump Width, Rump Angle, Strength). Include a **BIS** row. Use doe scores from the score table; for the buck, use his own scores or estimated outlook (marked estimated). Column order = BIS order.

## Recommendation
**Primary pick:** [Doe] (BIS +X.X) — why this package best uses his strengths without stacking his risks (expected Final Score / trait impact + main risk + mitigation).

**Runner-up (optional):** [Doe] (BIS …) — when to prefer this instead.

**Also acceptable / ranked shortlist (optional):** brief list with BIS if several does fit similarly.

**Avoid or deprioritize:** [Doe(s)] (BIS …) — brief reason (e.g. shared weak Medial Suspensory Ligament; stacking narrow Rump Width).

## Benefit / Risk / Mitigation Package (recommended breeding)
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
- Default doe set = **Available does** on the breeding roster (exclude only if the prompt says so; check the herd roster for incomplete-LA or other per-animal caveats).
- Rank and recommend using **BIS**; pair scores must match the corresponding Doe Breeding Report.
- Ground pros/cons in **numbers** relative to this buck, not generic doe praise.
- Frame each doe as: what the buck **improves in her**, what she **covers for him**, and what they **risk stacking**.
- Only recommend does whose named strengths-to-protect are compatible with this buck’s package when BIS is competitive; otherwise deprioritize with an explicit reason (and show the BIS).
- Estimated bucks: label every claim as estimated; be more conservative on primary picks when several BIS values are close after ConfidencePenalty.
- Keep any existing Individual Report or Doe Breeding Report recommendations consistent where the same pair appears; this report should still stand alone.
- Write reports to `reports/` as `breeding-[barn-name].md` (lowercase barn name). Same filename pattern as Doe Breeding Reports — one breeding report per animal.

---

## Report Type 6: Herd Breeding Report

**Purpose:** Season-level pairing plan for the whole breeding roster — one best on-hand buck for each available doe (by BIS), plus homozygous/reinforced strengths, risks, kid-selection notes, and what outside genetics would move the herd most. Complements Type 3 Herd Report (strategic overview) and Types 4–5 (per-animal rankings); does not replace them.

### Template

```markdown
# Herd Breeding Report: [Herd Name]

**Appraisal / data set:**
**Does on roster:** (count + names)
**Bucks on roster:** (count + names)
**Objective:** Maximize expected herd Final Score / high-impact linears via BIS-ranked pairs

## Season Pairing Plan

Table: Doe | Doe FS | Primary buck | BIS | Confirmed runner-up | Notes

Then short bullets:
- How primary picks were chosen (max BIS per doe)
- Service priority if one buck is oversubscribed
- Confirmed-score fallback plan (e.g. when estimated bucks are capped)

## Recommended Pairs (detail)

One subsection per recommended pair, scored does first (BIS descending), incomplete-LA last:

### [Buck] × [Doe] — BIS +X.X
**Why this pair:** 1–2 sentences on gap closure vs herd goals.
**Likely homozygous / reinforced strengths:** Traits both sides score well (≥~30 or clear standout) — what kids are most likely to inherit as a package.
**Risks:** Stacked faults, extremes, estimate uncertainty, strengths-to-protect — severity low / moderate / higher.
**Kid selection:** What to keep / cull-lean on in daughters and sons (MSL, teats, dairyness, width, RA band, etc.).

## Buck Utilization

Brief: which bucks carry the season, which are situational, which are limited by estimate or width.

## Outside Genetics — Biggest Herd Levers

**Outside buck (preferred):** Concrete trait targets (scores/ranges) that close herd-wide gaps the on-hand bucks cannot.
**Outside doe (optional):** When adding dams would help more than another sire.
**What not to chase first:** Traits already strong herd-wide or low-h² distractions this season.

## Season Notes

Timing, re-appraisal (young bucks/does), Lux/incomplete-LA handling, when to refresh this report.
```

### Type-specific notes
- Default animal set = **`HERD_BREEDING_ROSTER.md`** only.
- Primary pair for each doe = **highest BIS** among available bucks (must match that doe’s Doe Breeding Report). Incomplete doe LA → primary still named if useful, but BIS **N/A** and deprioritize.
- Do not invent a second ranking system; if you override max-BIS for capacity or confirmed-score preference, say so explicitly and show the BIS cost.
- **Homozygous / reinforced** = both parents strong or clearly above intermediate on the same trait (or dam elite + sire at least adequate). Mark estimated buck traits as estimated.
- Outside-genetics section must name the herd’s binding gaps (usually Medial Suspensory Ligament and Teat Placement when bucks lack proven mammary transmitting) with target score bands — not vague “better udders.”
- Keep per-pair detail shorter than a Planning Report; point to `reports/breeding-[barn].md` for full rankings.
- Write reports to `reports/` as `herd-breeding-[herd-slug].md` (e.g. `herd-breeding-forged-farm.md`).

---

**End of LA_REPORT_GUIDELINES.md**
