# Estimated Buck Profile Template  
**For unappraised bucks, and for filling mammary (or other blank) linears on appraised bucks**  
**Last updated:** 2026-07-28  

Use this when a buck needs transmitting estimates that official LA does not provide:

1. **Unappraised / too young** — full estimated transmitting profile (`estimated: yes` in Script inputs).
2. **Appraised buck with blank mammary** — profile supplies progeny-based mammary midpoints (`msl`, `tp`, `td`); set `estimated: no`. Official LA wins for any trait already scored; the loader only **fills blanks**.

You supply the **full** LA reports (or raw score sheets) for the parents and/or relevant progeny. The AI synthesizes the estimated transmitting profile from those complete sources.

**Write finished profiles to `profiles/estimated-buck-profile-[slug].md`** (not `reports/`).

---

## How to Use

1. Fill in the short header below (name, status, pedigree notes).
2. Attach or paste the **complete** LA reports / score data for:
   - The buck’s own LA (if appraised)
   - Sire / dam (if useful)
   - Appraised daughters (or other progeny) — **required for mammary estimates on bucks**
3. Ask the AI to generate the Estimated Transmitting Profile from the full data. Do not pre-summarize.
4. Save the result under `profiles/` using the naming pattern above. Include the buck’s **Reg #** in the title line so the BIS loader can match it.

---

## Template (header only)

```markdown
# Estimated Buck Profile: [Buck Name] ([Reg # if available])

**LA status:** Unappraised | Appraised (`VEE 90`) — mammary estimated from daughters  
**DOB:**  
**Pedigree notes:** (optional brief context)

## Source Data Provided

**Own LA (if any):** …
**Sire / dam (if used):** …
**Appraised daughters / progeny:** …
- [Daughter 1 Name] ([Reg #]) — full report attached
- …

## Instructions to AI

Using the complete LA reports listed above (do not rely on any pre-summaries):

1. Extract own scores (if any) and progeny patterns for mammary and other blank traits.
2. Produce an **Estimated Transmitting Profile** covering strengths, risks, confidence, and mammary outlook.
3. Add a **Script inputs (BIS)** table (see below).
```

### Script inputs (BIS) block

**Unappraised buck** (`estimated: yes` — full ConfidencePenalty in BIS):

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

**Appraised buck — mammary (or other) fills only** (`estimated: no`):

```markdown
## Script inputs (BIS)

Official LA supplies scored traits. These values fill blanks only (typically mammary).

| key | value |
|-----|-------|
| estimated | no |
| fs | VEE 90 |
| msl | 24.5 |
| tp | 21 |
| td | 26 |
```

Keys: `msl`, `tp`, `td`, `dy`, `rw`, `st` (strength), `stat` (stature), `ra`, plus `estimated` / `fs`.  
Positive GapClosure on profile-filled traits uses the estimate multiplier (×0.75). Full `ConfidencePenalty` applies only when `estimated: yes`.

---

## Notes

- Keep source reports complete. The AI is responsible for summarization and pattern detection.
- Store profiles under `profiles/`.
- Mammary on bucks is almost never on the score sheet — prefer daughter-based midpoints when daughters exist.
- Once an unappraised buck receives his own LA, keep or refresh the profile for mammary fills (`estimated: no`) rather than deleting it outright.

---

**End of template**
