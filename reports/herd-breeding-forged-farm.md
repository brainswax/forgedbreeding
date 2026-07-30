# Herd Breeding Report: Forged Farm

**Appraisal / data set:** 2026-07-26 LA (`LA_SCORES_2026.md`) + buck mammary / frame fills from `profiles/` (Michael, Smithy, Finale) + Lux estimated phenotype  
**Does on roster (6):** Lizbeth, Sapphire, Snickers, Amber, Tinkles, Lux  
**Bucks on roster (3):** Michael (`VGE 88` + mammary fills), Smithy (`VVE 86` + mammary fills), Finale (unappraised — full estimate)  
**Objective:** Maximize expected herd Final Score / high-impact linears via BIS-ranked pairs  
**Preferred Rump Angle band:** 30–35  

---

## Season Pairing Plan

Primary buck = **highest BIS** for each doe (matches live `python3 scripts/bis.py` with current profiles).

| Doe | Doe FS | Primary buck | BIS | Confirmed runner-up | Notes |
|-----|--------|--------------|-----|---------------------|-------|
| Snickers | `GAEV 84` | **Michael** | **+17.8** | Smithy (+14.9) | Largest herd BIS; dairy + width + closer TP fill (~25); RA 36 — no flatteners |
| Amber | `GEEV 86` | **Michael** | **+16.7** | Smithy (+12.9) | Steep/narrow + wide TP; Michael’s TP fill avoids wide-teat stack penalty |
| Lizbeth | `VEEG 85` | **Michael** | **+14.1** | Smithy (+9.7) | Binding MSL 13 / TP 17; Michael best on-hand mammary + RA into preferred |
| Tinkles | `VVVA 84` | **Michael** | **+9.9** | Smithy (+4.9) | Biggest Michael–Smithy edge (+5.0); RA 38 — protect from flattening |
| Sapphire | `VEVV 88` | **Michael** | **+7.0** | Smithy (+4.0) | Best of modest options; protect dairyness 40 / width 35 |
| Lux | Estimated (dry) | **Michael** | **+5.7** | Smithy (+2.0) | Only clear positive after doe ConfidencePenalty; phenotype still estimated |

**Assignment rules**
- Primary picks maximize BIS per doe — **Michael on every roster doe** once mammary fills are loaded.
- Michael is **oversubscribed**. Service priority by absolute BIS (largest expected LA impact first): **Snickers → Amber → Lizbeth → Tinkles → Sapphire → Lux**.
- If you instead ration Michael by **largest edge over Smithy**: Tinkles (+5.0) → Lizbeth (+4.4) → Amber (+3.8) → Lux (+3.7) → Sapphire (+3.0) → Snickers (+2.9).
- **Confirmed-score fallback** (Michael unavailable): every doe’s runner-up is **Smithy**. Finale is third on all six (and negative on Sapphire/Lux) — use only where his estimated dairy/width package is worth ConfidencePenalty + wide-TP stack.
- **Why the flip from earlier Finale-primary plans:** Michael and Smithy now carry relative mammary fills (`estimated: no`). Michael’s closer TP (~25) avoids the wide-teat stack penalty that still hits Smithy/Finale (~21). GapClosure on fills is ×0.75; full `estimated: yes` ConfidencePenalty applies only to Finale (and Lux as doe).

---

## Recommended Pairs (detail)

Scored does first by BIS descending; Lux last.

### Michael × Snickers — BIS +17.8

**Why this pair:** Clearest on-hand package for the herd’s lowest-dairy / narrow doe — dairyness 30 and width 28 vs her 23/23, plus mammary fills (MSL ≈23, TP ≈25) and RA 34 easing her 36 toward preferred without flattening.

**Likely homozygous / reinforced strengths:** Strength (36 / 36); Body Depth / capacity from Snickers (BD 47, Body `E`) with Michael’s adequate depth; Fore Udder Attachment 39 on the dam side. Dairy, width, and closer teat placement are complementary gains from the sire more than already-shared highs.

**Risks:** Michael MSL/TP are relative fills, not daughter-proven (moderate); MSL may still land only intermediate (doe 18 / fill ≈23, moderate); TD fill ≈20 may run fine (low–moderate); RA already above preferred — do not use flatter partners (moderate if mismanaged).

**Kid selection:** Prefer daughters with dairyness clearly above the dam, Rump Width ≥ intermediate, MSL and teat placement better than the dam’s weak/wide side, and RA in or approaching 30–35. Cull-lean on kids that stay low-dairy, narrow, wide-teated, or flatter than the dam. Sons: keep dairy + width without extreme flat rumps. Full ranking: `reports/breeding-snickers.md`.

### Michael × Amber — BIS +16.7

**Why this pair:** Best fix for the steepest/narrowest scored doe (RA 21, RW 21) while TP fill ≈25 avoids the wide-teat stack that penalizes Smithy/Finale against her 17.

**Likely homozygous / reinforced strengths:** Dairyness (36 / 30 — protect hers); Strength (34 / 36); rear-udder package from Amber (RUH 40, RUA 34, FU 35). Width and rump angle are complementary from Michael.

**Risks:** Mammary fills small-n (moderate); MSL still below strong (17 / ≈23, moderate); mild dairyness dilution vs her 36 (low–moderate); TD fill ≈20 (low–moderate).

**Kid selection:** Keep kids that add Rump Width and move RA toward 30–35 without losing dairy character or rear-udder quality. Favor closer teat placement and stronger MSL than the dam. Avoid retaining very narrow or still-steep daughters. See `reports/breeding-amber.md`.

### Michael × Lizbeth — BIS +14.1

**Why this pair:** Strongest on-hand answer to the herd’s weakest MSL (13) and widest TP (17) on a high-dairy, usable-width doe; RA 34 corrects steep 23 into preferred.

**Likely homozygous / reinforced strengths:** Dairyness (38 / 30 — protect hers); Strength (36 / 36); Rump Width (31 / 28); Teat Diameter intermediate (25 / ≈20 fill — watch fineness); Rear Udder Arch / Height from Lizbeth (34 / 35). Dairy Strength `E` should remain a package strength.

**Risks:** MSL fill only intermediate vs a floor of 13 — not an elite suspensory fix (moderate–higher); TP fill unproven (moderate); dairyness dilution if kids read like Michael’s 30 (moderate); mammary fills not daughter-proven (moderate).

**Kid selection:** Daughters must show MSL and teat placement clearly better than the dam to earn keepers; protect dairyness and width. Do not keep replacements that repeat MSL ≤20 with wide teats. See `reports/breeding-lizbeth.md`.

### Michael × Tinkles — BIS +9.9

**Why this pair:** Best BIS and largest edge over Smithy on a flat-RA, weak-MSL, wide-TP first-freshener; RA 34 eases her 38 toward preferred without going flatter.

**Likely homozygous / reinforced strengths:** Dairyness (36 / 30); Strength (37 / 36); capacity adequate both sides. Aladdin-side flat-RA / weak-MSL / wide-TP pattern is what Michael is meant to counter, not reinforce.

**Risks:** Young doe (moderate); RA already 38 — no flatteners (moderate–higher if mismanaged); Mammary `A` / MSL 17 / TP 20 may persist if fills overstate transmitting (moderate); RW 25 vs Michael 28 is only modest width help (low–moderate).

**Kid selection:** Prefer kids that ease rump angle into 30–35, improve MSL/teats vs the dam, and hold dairyness/strength. Deprioritize flat-rumped or still-wide-teated keepers. See `reports/breeding-tinkles.md` and `reports/planning-aladdin-x-cuddles.md` for parental background.

### Michael × Sapphire — BIS +7.0

**Why this pair:** Highest BIS among limited options on the herd ceiling doe — mainly MSL/TP fill and RA correction; not a Final Score chase.

**Likely homozygous / reinforced strengths:** Dairyness (40 / 30 — **protect** her elite dairy); Rear Udder Height / Arch / Fore Udder from Sapphire (39 / 37 / 37); General Appearance / Mammary letters already strong (`VEVV 88`). Width (35) is hers to protect; Michael 28 dilutes less than Smithy 24.

**Risks:** Net improvement modest vs her already-high FS (moderate); possible dilution of Rump Width 35 and elite dairyness (moderate–higher); mammary fills unproven (moderate). This is gap-cover more than upgrade.

**Kid selection:** Keep only daughters that hold dairyness near the dam, keep width strong, and improve MSL/teat placement. Cull-lean on kids that lose dairy character or narrow up. Outside proven mammary still beats any on-hand buck long-term. See `reports/breeding-sapphire.md`.

### Michael × Lux — BIS +5.7

**Why this pair:** Only clearly positive BIS after estimated-doe ConfidencePenalty; mammary fills (MSL ≈23 / TP ≈25) address the Sleepnstag-side weak-MSL / wide-TP pattern while RA 34 stays in preferred with her ~31 est.

**Likely homozygous / reinforced strengths:** Unknown until Lux is scored; estimate suggests dairyness (~37) and usable width (~29) to protect if the dam side expresses.

**Risks:** Lux phenotype estimated — gaps may differ when scored (moderate–higher); Michael mammary fills small-n (moderate); dairyness 30 below her ~37 est. (low–moderate); doe ConfidencePenalty already in the BIS.

**Kid selection:** Provisional — freshen and score Lux before locking replacements. Prefer kids that appraise cleanly for MSL, teat placement, dairyness, and width. Recompute BIS after her LA. See `reports/breeding-lux.md`.

---

## Buck Utilization

| Buck | Role this season | Load |
|------|------------------|------|
| **Michael** | Primary on all six does | **High** — ration by BIS list above; mammary fills drive the ranking but are not daughter-proven |
| **Smithy** | Confirmed runner-up everywhere; dairy lift when Michael is reserved | Medium — wide TP fill (~21) still stacks on wide-teat does; narrow RW 24 limits Amber/Sapphire/Snickers-type width work |
| **Finale** | Estimated third option; dairy/width thematic cover only | Low — ConfidencePenalty + wide-TP stack leave him behind both appraised sires on every doe |

---

## Outside Genetics — Biggest Herd Levers

Herd-wide binding gaps remain **Medial Suspensory Ligament** (scored does 13–18; Lux ~16.5 est.) and **Teat Placement** (17–21, wide). On-hand bucks now supply **intermediate MSL fills (~23–23.5)** and Michael’s **closer TP fill (~25)** — better than “unproven blank,” still not a proven strong-suspensory / elite-teat solution.

**Outside buck (preferred)** — transmitting evidence (own daughters or strong dam/sister mammary) with:
1. **Medial Suspensory Ligament** clearly above intermediate — target daughters/means roughly **≥28–32** (herd floor is 13–18)
2. **Teat Placement** closer / less wide — target roughly **≥25–30** sustained in progeny (Michael’s fill is ~25 on paper only)
3. Hold or add **Dairyness** (≥30) and **Rump Width** (≥28) so Snickers/Amber-type gaps are not reopened
4. **Rump Angle** that moves animals toward **30–35** (not a flattener for Snickers/Tinkles)
5. Prefer **progeny-proven mammary** over another unproven dairy/width sire — those frame levers are already covered by Michael/Smithy/Finale

**Outside doe (optional):** A mid/high-80s+ doe with **strong MSL and closer teat placement** plus dairyness would add dams that do not stack the herd’s mammary floor. Sapphire supplies elite dairy/width; she is not the mammary fix.

**What not to chase first this season:** Another tall/generalist buck without mammary proof; low-h² fine-tuning (rear leg set, feet) ahead of MSL/TP; outside genetics that mainly duplicate Michael’s strength/RA package.

---

## Season Notes

- This report assumes current profile fills: Michael MSL/TP/TD, Smithy MSL/TP/TD, Finale full estimate, Lux full estimate. Refresh after Michael/Smithy daughters appraise, Finale’s first LA, and Lux’s first scored LA (`PYTHONPATH=scripts python3 scripts/bis.py`, then rewrite).
- Young first-fresheners (Snickers, Amber, Sapphire, Tinkles): mammary may still mature — weight kid selection on second-look appraisals when possible.
- Protect Snickers RA 36 and Tinkles RA 38 from further flattening in every pairing decision.
- Per-animal rankings may lag this matrix until doe/buck breeding reports are regenerated — trust live BIS for pairing, then refresh `reports/breeding-*.md`.
- Accuracy caution from `reports/planning-aladdin-x-cuddles.md`: midpoints miss extremes; keep/pass on **weak MSL, wide TP, and flat RA** still matters more than optimistic averages.
