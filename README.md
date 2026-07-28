# Forged Breeding

Nigerian Dwarf breeding decision support for **Forged Farm** (Brian Denton, ADGA Member ID 1660541).  
Markdown sources hold herd identity, Linear Appraisal (LA) scores, goals, and generated reports. Python under `scripts/` ranks breeding pairs — it **loads data from those markdown files** and does not hardcode herd animals or scores.

## Quick start

```bash
# Rank every available doe×buck pair by Breeding Impact Score (BIS)
python3 scripts/bis.py

# Inspect what the loader pulled from the markdown sources
python3 scripts/herd_data.py
```

## Document map & dependencies

`README.md` is the only place that describes how documents relate. Prefer reading this map over chasing cross-links inside the files themselves.

```text
README.md  (this file — anchor)
│
├── DAIRY_CONCEPTS.md          self-contained (ADGA SOP only; no repo deps)
├── GOALS.md                   → DAIRY_CONCEPTS.md (concepts only; once)
├── HERD_ROSTER.md             self-contained
├── HERD_BREEDING_ROSTER.md    → HERD_ROSTER.md only
├── LA_SCORES_2026.md          optional → DAIRY_CONCEPTS.md (only if needed)
├── LA_REFERENCE_SCORES.md     optional → DAIRY_CONCEPTS.md (only if needed)
├── ESTIMATED_BUCK_PROFILE_TEMPLATE.md → scripts/bis.py only
├── LA_REPORT_GUIDELINES.md    may use any source below (listed once in its Inputs table)
│     ├── GOALS.md
│     ├── DAIRY_CONCEPTS.md
│     ├── LA_SCORES_2026.md
│     ├── HERD_BREEDING_ROSTER.md
│     ├── HERD_ROSTER.md
│     ├── LA_REFERENCE_SCORES.md
│     ├── reports/estimated-buck-profile-*.md
│     └── scripts/bis.py
└── reports/*                  generated outputs (not source-of-truth docs)
```

**Rules of thumb**

| Document | May depend on |
|----------|----------------|
| `DAIRY_CONCEPTS.md` | ADGA sources only (no other repo files) |
| `GOALS.md` | `DAIRY_CONCEPTS.md` when needed (avoid unnecessary refs) |
| `HERD_ROSTER.md` | nothing else in the repo |
| `HERD_BREEDING_ROSTER.md` | `HERD_ROSTER.md` only |
| `LA_SCORES_2026.md` | `DAIRY_CONCEPTS.md` only if needed |
| `LA_REFERENCE_SCORES.md` | `DAIRY_CONCEPTS.md` only if needed |
| `ESTIMATED_BUCK_PROFILE_TEMPLATE.md` | `scripts/bis.py` only |
| `LA_REPORT_GUIDELINES.md` | any of the above (minimize; list each once) |
| Any file | `README.md` if it needs the map |

When a dependency is needed, name the file **once** near the top (or in one Inputs table). Do not spam the same path through the body.

## Core documents

| File | Role |
|------|------|
| `GOALS.md` | Herd-specific breeding objectives and preferences |
| `DAIRY_CONCEPTS.md` | Generic ADGA LA concepts (2025 Linear Appraisal SOP), polarity, risks & mitigations, terminology |
| `LA_REPORT_GUIDELINES.md` | Report process / templates / **BIS** |
| `HERD_ROSTER.md` | ADGA identity, Barn Names, LA summary, strengths-to-protect notes |
| `HERD_BREEDING_ROSTER.md` | Who is currently available to breed (does and bucks) |
| `LA_SCORES_2026.md` | Current herd linear traits, categories, Final Scores |
| `LA_REFERENCE_SCORES.md` | Outside / pedigree reference scores (not on-hand partners) |
| `ESTIMATED_BUCK_PROFILE_TEMPLATE.md` | Template for unappraised bucks (+ BIS script inputs) |

## Reports

Written under `reports/`:

| Pattern | Meaning |
|---------|---------|
| `individual-[barn].md` | Individual LA report |
| `breeding-[barn].md` | Doe or Buck Breeding Report (partners ranked by BIS) |
| `herd-[slug].md` | Herd-level summary |
| `planning-….md` | Pair planning report |
| `estimated-buck-profile-….md` | Estimated transmitting profile for unappraised bucks |

Barn Names come from `HERD_ROSTER.md` (e.g. Michael, Snickers, Amber).

## Scripts

All Python lives in `scripts/`.

| Script | Purpose |
|--------|---------|
| `scripts/herd_data.py` | Load available animals + traits from markdown |
| `scripts/bis.py` | Compute / print Breeding Impact Score rankings |

### Data sources (no hardcoded herd)

`herd_data.py` reads:

1. **`HERD_BREEDING_ROSTER.md`** — available does and bucks (Barn Name + Reg #)
2. **`HERD_ROSTER.md`** — Barn Names, owner heights, notes
3. **`LA_SCORES_2026.md`** — linear traits and Final Scores by Reg #
4. **`reports/estimated-buck-profile-*.md`** — for bucks without usable LA, a **`## Script inputs (BIS)`** key/value table

`scripts/bis.py` also reads **`Preferred Rump Angle band: LOW–HIGH`** from `GOALS.md` when present. Functional risks/mitigations stay in `DAIRY_CONCEPTS.md` only.

### Breeding Impact Score (BIS)

Documented in `LA_REPORT_GUIDELINES.md`. In short:

```text
BIS = GapClosure − RiskPenalty − ConfidencePenalty
```

Same doe×buck pair always gets the same BIS in Doe and Buck Breeding Reports. Higher is better for expected net LA improvement after risks. Incomplete doe LA → `N/A`.

## Typical workflow

1. Keep `HERD_BREEDING_ROSTER.md` and `HERD_ROSTER.md` current.
2. Enter new LA scores in `LA_SCORES_2026.md`.
3. For young/unappraised bucks, maintain an estimated profile with a **Script inputs (BIS)** table.
4. Run `python3 scripts/bis.py` and refresh breeding reports per `LA_REPORT_GUIDELINES.md`.

## Language

Use **breeding** / **breed** — never **mating** / **mate** (see `DAIRY_CONCEPTS.md`).
