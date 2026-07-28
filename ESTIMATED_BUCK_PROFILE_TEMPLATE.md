# Estimated Buck Profile Template  
**For young / unappraised bucks**  
**Last updated:** 2026-07-28  

Use this when a buck does not yet have his own Linear Appraisal scores.  
You supply the **full** LA reports (or raw score sheets) for the parents and any relevant progeny. The AI synthesizes the estimated transmitting profile from those complete sources.

---

## How to Use

1. Fill in the short header below (name, status, pedigree notes).
2. Attach or paste the **complete** LA reports / score data for:
   - Sire
   - Dam
   - Any appraised daughters (or other progeny) of the sire that you want considered
3. Ask the AI to generate the Estimated Transmitting Profile (and any pairing/herd analysis) from the full data. Do not pre-summarize.

---

## Template (header only)

```markdown
# Estimated Buck Profile: [Buck Name] ([Reg # if available])

**Status:** Unappraised (or too young)  
**DOB:**  
**Pedigree notes:** (optional brief context)

## Source Data Provided

**Sire:** [Name] ([Reg #])  
- Full LA report / scores attached or included below

**Dam:** [Name] ([Reg #])  
- Full LA report / scores attached or included below

**Sire’s appraised progeny (if any):**  
- [Daughter 1 Name] ([Reg #]) — full report attached
- [Daughter 2 Name] ([Reg #]) — full report attached
- …

## Instructions to AI

Using the complete LA reports listed above (do not rely on any pre-summaries):

1. Extract and compare the relevant linear traits and Final Scores of the sire and dam.
2. Identify patterns across any sire daughters provided.
3. Produce an **Estimated Transmitting Profile** covering:
   - Likely strengths (higher confidence)
   - Possible strengths (moderate confidence)
   - Likely weaknesses or risks
   - Traits with insufficient data
   - Specific outlook for: Rump angle, MSL / mammary support, Teat traits, Dairyness, Strength, Rump width
4. State confidence level and major data gaps.
5. Provide a short Quick Reference paragraph suitable for use in pairing or herd reports.
6. When ranking this buck against appraised herd sires, treat the estimates as directional only and weight real LA scores more heavily.
7. Add a **Script inputs (BIS)** table (see below) so the BIS script can load transmitting values without hardcoding.
```

### Script inputs (BIS) block (required for unappraised bucks used in breeding reports)

```markdown
## Script inputs (BIS)

Machine-readable transmitting midpoints for `scripts/bis.py`. Remove once the buck has his own LA.

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

Keys: `msl`, `tp`, `td`, `dy`, `rw`, `st` (strength), `stat` (stature), `ra`, plus `estimated` / `fs`.

---

## Notes

- Keep source reports complete. The AI is responsible for summarization and pattern detection.
- Update the header and add new progeny reports as they become available.
- Once the buck receives his own LA, replace this estimated profile with the real scores (and drop the Script inputs table).

---

**End of template**
