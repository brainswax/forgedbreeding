# Herd Breeding Report: Forged Farm

**Appraisal / data set:** 2026-07-26 LA (`LA_SCORES_2026.md`) + buck mammary / frame fills from `profiles/` (Michael, Smithy, Finale) + Lux estimated phenotype  
**Does on roster (6):** Lizbeth, Sapphire, Snickers, Amber, Tinkles, Lux  
**Bucks on roster (3):** Michael (`VGE 88` + mammary fills), Smithy (`VVE 86` + mammary fills), Finale (unappraised — full estimate)  
**Objective:** Maximize expected herd Final Score / high-impact linears via BIS-ranked pairs  
**Preferred Rump Angle band:** 30–35  

**Template note:** Pairing plan is unchanged under the revised guidelines (priority ≠ heritability). What changes is explicit **low-h² breed-in / protect** tracking — those traits are not “lower priority,” only slower to move.

---

## Season Pairing Plan

Primary buck = **highest BIS** for each doe (matches live `PYTHONPATH=scripts python3 scripts/bis.py`).

| Doe | Doe FS | Primary buck | BIS | Confirmed runner-up | Notes |
|-----|--------|--------------|-----|---------------------|-------|
| Snickers | `GAEV 84` | **Michael** | **+17.8** | Smithy (+14.9) | Largest herd BIS; dairy + width + closer TP fill (~25); RA 36 — no flatteners |
| Amber | `GEEV 86` | **Michael** | **+16.7** | Smithy (+12.9) | Steep/narrow + wide TP; Michael’s TP fill avoids wide-teat stack penalty |
| Lizbeth | `VEEG 85` | **Michael** | **+14.1** | Smithy (+9.7) | Binding MSL 13 / TP 17; Michael best on-hand mammary + RA into preferred |
| Tinkles | `VVVA 84` | **Michael** | **+9.9** | Smithy (+4.9) | Biggest Michael–Smithy edge (+5.0); RA 38 — protect from flattening |
| Sapphire | `VEVV 88` | **Michael** | **+7.0** | Smithy (+4.0) | Best BIS among modest options; **protect** dairyness 40 / width 35 / **RUA 37** |
| Lux | Estimated (dry) | **Michael** | **+5.7** | Smithy (+2.0) | Only clear positive after doe ConfidencePenalty; phenotype still estimated |

**Assignment rules**
- Primary picks maximize BIS per doe — **Michael on every roster doe** once mammary fills are loaded.
- Michael is **oversubscribed**. Service priority by absolute BIS: **Snickers → Amber → Lizbeth → Tinkles → Sapphire → Lux**.
- If rationing Michael by **largest edge over Smithy**: Tinkles (+5.0) → Lizbeth (+4.4) → Amber (+3.8) → Lux (+3.7) → Sapphire (+3.0) → Snickers (+2.9).
- **Confirmed-score fallback** (Michael unavailable): every doe’s runner-up is **Smithy**. Finale is third on all six (negative on Sapphire/Lux).
- BIS does **not** score Rear Udder Arch or Rear Legs Side View — those still constrain **keeper selection** under Low-Heritability Traits below even when Michael remains primary.

---

## Recommended Pairs (detail)

Scored does first by BIS descending; Lux last.

### Michael × Snickers — BIS +17.8

**Why this pair:** Clearest on-hand package for the herd’s lowest-dairy / narrow doe — dairyness 30 and width 28 vs her 23/23, plus mammary fills (MSL ≈23, TP ≈25) and RA 34 easing her 36 toward preferred without flattening.

**Likely homozygous / reinforced strengths:** Strength (36 / 36); Body Depth / capacity from Snickers (BD 47, Body `E`); Fore Udder Attachment 39 on the dam side. Dairy, width, and closer teat placement are complementary from the sire.

**Risks:** Michael MSL/TP are relative fills, not daughter-proven (moderate); MSL may still land only intermediate (doe 18 / fill ≈23, moderate); TD fill ≈20 may run fine (low–moderate); RA already above preferred — no flatteners (moderate if mismanaged).

**Kid selection:** Prefer dairyness above the dam, Rump Width ≥ intermediate, MSL/TP better than her weak/wide side, RA in or near 30–35. **Low-h²:** breed in better Rear Legs Side View than her posty 21 (Michael 35 helps on paper); hold Rear Udder Arch near her 32+. Cull-lean on low-dairy, narrow, wide-teated, flat, or still-posty keepers. See `reports/breeding-snickers.md`.

### Michael × Amber — BIS +16.7

**Why this pair:** Best fix for the steepest/narrowest scored doe (RA 21, RW 21) while TP fill ≈25 avoids the wide-teat stack that penalizes Smithy/Finale against her 17.

**Likely homozygous / reinforced strengths:** Dairyness (36 / 30 — protect hers); Strength (34 / 36); rear-udder package from Amber (RUH 40, RUA 34, FU 35). Width and rump angle are complementary from Michael.

**Risks:** Mammary fills small-n (moderate); MSL still below strong (17 / ≈23, moderate); mild dairyness dilution vs her 36 (low–moderate); TD fill ≈20 (low–moderate).

**Kid selection:** Keep kids that add Rump Width and move RA toward 30–35 without losing dairy or rear-udder quality. Favor closer TP and stronger MSL than the dam. **Low-h² protect:** Rear Udder Arch 34 and RLSV 34 — do not keep daughters that clearly lose arch or leg set while chasing mammary. See `reports/breeding-amber.md`.

### Michael × Lizbeth — BIS +14.1

**Why this pair:** Strongest on-hand answer to the herd’s weakest MSL (13) and widest TP (17) on a high-dairy, usable-width doe; RA 34 corrects steep 23 into preferred.

**Likely homozygous / reinforced strengths:** Dairyness (38 / 30 — protect hers); Strength (36 / 36); Rump Width (31 / 28); Rear Udder Arch / Height from Lizbeth (34 / 35). Dairy Strength `E` should remain a package strength.

**Risks:** MSL fill only intermediate vs a floor of 13 (moderate–higher); TP fill unproven (moderate); dairyness dilution if kids read like Michael’s 30 (moderate); mammary fills not daughter-proven (moderate).

**Kid selection:** Daughters must show MSL and teat placement clearly better than the dam; protect dairyness and width. **Low-h² protect:** Rear Udder Arch 34 and RLSV 32 — keepers should not drop arch while fixing mammary. See `reports/breeding-lizbeth.md`.

### Michael × Tinkles — BIS +9.9

**Why this pair:** Best BIS and largest edge over Smithy on a flat-RA, weak-MSL, wide-TP first-freshener; RA 34 eases her 38 toward preferred without going flatter.

**Likely homozygous / reinforced strengths:** Dairyness (36 / 30); Strength (37 / 36). Aladdin-side flat-RA / weak-MSL / wide-TP pattern is what Michael is meant to counter.

**Risks:** Young doe (moderate); RA already 38 — no flatteners (moderate–higher if mismanaged); Mammary `A` / MSL 17 / TP 20 may persist if fills overstate transmitting (moderate); RW 25 vs Michael 28 is only modest width help (low–moderate).

**Kid selection:** Prefer RA into 30–35, MSL/TP better than dam, hold dairyness/strength. **Low-h² breed in:** RLSV 26 leans posty — prefer sisters closer to intermediate (Michael 35 is the better on-hand leg set); hold RUA ≥ her 31. See `reports/breeding-tinkles.md` and `reports/planning-aladdin-x-cuddles.md`.

### Michael × Sapphire — BIS +7.0

**Why this pair:** Highest BIS among limited options on the herd ceiling doe — mainly MSL/TP fill and RA correction; not a Final Score chase.

**Likely homozygous / reinforced strengths:** Dairyness (40 / 30 — **protect**); Rear Udder Height / Arch / Fore Udder from Sapphire (39 / **37** / 37); `VEVV 88` package. Width (35) is hers to protect; Michael 28 dilutes less than Smithy 24.

**Risks:** Modest net vs already-high FS (moderate); possible dilution of width 35 and elite dairyness (moderate–higher); mammary fills unproven (moderate). **Low-h² risk:** Michael’s own RUA 28 sits well below her arch 37 — BIS ignores this, but arch is slow to recover if lost.

**Kid selection:** Keep only daughters that hold dairyness near the dam, keep width strong, and improve MSL/TP. **Low-h² protect (explicit):** cull-lean on keepers that lose Rear Udder Arch or RLSV 33 toward posty/sickled extremes even if mammary looks better. Outside proven mammary still beats on-hand bucks long-term. See `reports/breeding-sapphire.md`.

### Michael × Lux — BIS +5.7

**Why this pair:** Only clearly positive BIS after estimated-doe ConfidencePenalty; mammary fills (MSL ≈23 / TP ≈25) address the Sleepnstag-side weak-MSL / wide-TP pattern while RA 34 stays in preferred with her ~31 est.

**Likely homozygous / reinforced strengths:** Unknown until Lux is scored; estimate suggests dairyness (~37) and usable width (~29) to protect if the dam side expresses.

**Risks:** Lux phenotype estimated (moderate–higher); Michael mammary fills small-n (moderate); dairyness 30 below her ~37 est. (low–moderate).

**Kid selection:** Provisional — freshen and score Lux before locking replacements. Prefer clean MSL, TP, dairyness, and width. Score her RLSV/RUA before treating low-h² as breed-in or protect. See `reports/breeding-lux.md`.

---

## Buck Utilization

| Buck | Role this season | Load |
|------|------------------|------|
| **Michael** | Primary on all six does | **High** — mammary fills drive BIS; RLSV 35 helps Snickers/Tinkles breed-in; RUA 28 is a **protect risk** on Sapphire-class arches |
| **Smithy** | Confirmed runner-up; dairy lift when Michael is reserved | Medium — wide TP fill (~21) stacks on wide-teat does; RW 24 limits width work; RUA 33 / RLSV 33 are friendlier low-h² cover than Michael on elite-arch does |
| **Finale** | Estimated third option | Low — ConfidencePenalty + wide-TP stack behind both appraised sires on every doe |

---

## Low-Heritability Traits (breed in / protect)

Slow to change — **not** “lower priority.” BIS does not weight these; keeper and next-partner decisions must.

### Breed in
| Trait | Where weak | Action |
|-------|------------|--------|
| **Rear Legs Side View** | Snickers **21** (posty); Tinkles **26** (leans posty) | Prefer keepers with more intermediate set; Michael (35) and Smithy (33) are the better on-hand leg-set sires — still multi-generational |
| **Rear Udder Arch** | No herd-wide floor crisis, but Lux unscored; do not let mediocre arch become the mean | When adding outside genetics or ranking sisters, prefer animals that bring arch **with** mammary — do not assume arch will “come along” after MSL/TP fixes |

### Protect
| Trait | Where strong | Action |
|-------|--------------|--------|
| **Rear Udder Arch** | Sapphire **37**; Lizbeth / Amber **34**; Snickers **32** | Do not casually breed arch out while chasing MSL/TP. On Sapphire × Michael, watch for RUA dilution (sire 28 vs dam 37) in keepers |
| **Rear Legs Side View** | Sapphire **33**; Amber **34**; Lizbeth **32**; Smithy/Michael appraised legs solid | Avoid stacking posty extremes; do not treat Snickers-like 21 as acceptable just because dairy/width improved |

---

## Outside Genetics — Biggest Herd Levers

Herd-wide **near-term** binding gaps remain **Medial Suspensory Ligament** (scored does 13–18; Lux ~16.5 est.) and **Teat Placement** (17–21, wide). On-hand bucks supply intermediate MSL fills (~23–23.5) and Michael’s closer TP fill (~25) — better than blanks, not progeny-proven elite mammary.

**Outside buck (preferred)** — transmitting evidence with:
1. **Medial Suspensory Ligament** clearly above intermediate — daughters/means roughly **≥28–32**
2. **Teat Placement** closer — roughly **≥25–30** in progeny
3. Hold **Dairyness** (≥30) and **Rump Width** (≥28)
4. **Rump Angle** toward **30–35** (not a flattener for Snickers/Tinkles)
5. Bonus (low-h², still important): strong **Rear Udder Arch** and intermediate **Rear Legs Side View** so Sapphire-class protect traits and Snickers/Tinkles breed-in needs are not ignored
6. Prefer **progeny-proven mammary** over another unproven dairy/width sire

**Outside doe (optional):** Mid/high-80s+ with **strong MSL and closer teats**, plus dairyness; extra value if she also brings arch / leg set the herd must breed in or protect.

**What not to chase first this season:** Another tall/generalist buck without mammary proof; outside genetics that only duplicate Michael’s strength/RA package. That is **season sequencing**, not a reason to drop low-h² breed-in/protect from keeper rules.

---

## Season Notes

- Pairing unchanged vs prior Michael-primary plan; refresh after Michael/Smithy daughters appraise, Finale’s first LA, and Lux’s first scored LA.
- Young first-fresheners: mammary may still mature — weight final keepers on second-look appraisals when possible.
- Protect Snickers RA 36 and Tinkles RA 38 from further flattening in every pairing decision.
- Per-animal `reports/breeding-*.md` may lag this matrix — trust live BIS for pairing, then refresh those files.
- Accuracy caution from `reports/planning-aladdin-x-cuddles.md`: midpoints miss extremes; keep/pass on **weak MSL, wide TP, flat RA**, and the low-h² breed-in/protect list above.
