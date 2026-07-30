# Estimated Profile Template  
**For unappraised animals, dry/incomplete LA, and blank-trait fills**  
**Last updated:** 2026-07-29  

Use this when an animal needs trait estimates that official LA does not provide:

1. **Unappraised / dry / incomplete LA** — full estimated phenotype or transmitting profile (`estimated: yes` in Script inputs). BIS applies ConfidencePenalty.
2. **Appraised animal with blank traits** — profile fills blanks only (common: mammary on bucks); set `estimated: no`. Official LA wins for any trait already scored; the loader only **fills blanks**.

Applies to **bucks and does**. You supply complete LA reports (or raw score sheets) for parents, siblings, and/or progeny. The AI synthesizes the estimate from those sources.

**Write finished profiles to `profiles/`** (not `reports/`):

| Pattern | Use |
|---------|-----|
| `estimated-profile-[slug].md` | Preferred generic name |
| `estimated-buck-profile-[slug].md` | Still valid (existing buck profiles) |
| `estimated-doe-profile-[slug].md` | Optional doe-specific name |

Include the animal’s **Reg #** in the title line so the BIS loader can match it.

---

## How to Use

1. Fill in the short header below (name, status, pedigree notes).
2. Attach or paste the **complete** LA reports / score data for:
   - The animal’s own LA (if any)
   - Sire / dam / siblings (especially useful for dry or unappraised does)
   - Appraised daughters / progeny (especially useful for buck mammary estimates)
3. Ask the AI to generate the Estimated Profile from the full data. Do not pre-summarize.
4. Save under `profiles/` using a pattern above.

---

## Template (header only)

```markdown
# Estimated Profile: [Animal Name] ([Reg # if available])

**LA status:** Unappraised | Incomplete / dry | Appraised (`VEE 90`) — blanks filled from relatives  
**Sex:** Female | Male  
**DOB:**  
**Pedigree notes:** (optional brief context)

## Source Data Provided

**Own LA (if any):** …
**Sire / dam / siblings (if used):** …
**Appraised daughters / progeny (if used):** …
- [Relative 1 Name] ([Reg #]) — full report attached
- …

## Instructions to AI

Using the complete LA reports listed above (do not rely on any pre-summaries):

1. Extract own scores (if any) and relative / progeny patterns.
2. Produce an **Estimated Profile** covering strengths, risks, confidence, and (for bucks) mammary transmitting outlook — or (for does) expected own phenotype.
3. Add a **Script inputs (BIS)** table (see below).
```

### Script inputs (BIS) block

**Full estimate** (`estimated: yes` — ConfidencePenalty in BIS; use for unappraised bucks or incomplete/dry does):

```markdown
## Script inputs (BIS)

| key | value |
|-----|-------|
| estimated | yes |
| fs | estimated |
| msl | 24.5 |
| tp | 21 |
| td | 26 |
| dy | 33 |
| rw | 30 |
| st | 30 |
| stat | 28 |
| ra | 28.5 |
```

**Blank fills only** (`estimated: no` — typical for appraised bucks’ mammary):

```markdown
## Script inputs (BIS)

Official LA supplies scored traits. These values fill blanks only.

| key | value |
|-----|-------|
| estimated | no |
| fs | VGE 88 |
| msl | 24.5 |
| tp | 21 |
| td | 26 |
```

**BIS GapClosure keys:** `msl`, `tp`, `td`, `dy`, `rw`, `st` (strength), `stat` (stature), `ra`, plus `estimated` / `fs`.  
Positive GapClosure on profile-filled **partner** traits uses the estimate multiplier (×0.75). Full `ConfidencePenalty` (+2) applies when `estimated: yes` on the buck and/or the doe.

**Planning / narrative keys (include when daughter or relative data exists):** `bd` (body depth), `rlsv` (rear legs side view), `ud` (udder depth), and optionally `fa` / `rh` / `rua`. The BIS loader ignores unknown keys today; still record them in Script inputs and the daughter-pattern tables so planning reports are complete.

---

## Notes

- Keep source reports complete. The AI is responsible for summarization and pattern detection.
- Store profiles under `profiles/`.
- **Bucks:** mammary is almost never on the score sheet — prefer daughter-based midpoints when daughters exist. When typed daughters exist, also publish **BD, strength, RLSV, UD**, and attachment midpoints — not only BIS mammary/frame keys.
- **Does:** when dry or unscored, prefer dam + paternal half-sib / sire-daughter patterns for a phenotype estimate; mark confidence clearly.
- Once an animal receives usable own LA, refresh the profile (`estimated: no` + blank fills) or remove full-estimate keys that official scores now cover.

---

**End of template**
