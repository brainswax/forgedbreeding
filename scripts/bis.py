#!/usr/bin/env python3
"""Breeding Impact Score (BIS) — see LA_REPORT_GUIDELINES.md § Breeding Impact Score.

Herd animals and scores are loaded from markdown via herd_data.py.
Rump Angle preference band is loaded from GOALS.md when present — not hardcoded.
"""

from __future__ import annotations

from herd_data import load_breeding_animals, load_preferred_ra_band

# Formula constants (not herd preferences) — keep in sync with LA_REPORT_GUIDELINES.md
WEIGHTS = {
    "msl": 5.0,
    "tp": 4.0,
    "td": 3.0,
    "dy": 4.0,
    "rw": 3.0,
    "st": 2.0,
    "stat": 1.0,
}
RA_WEIGHT = 2.0
# Relatively level rump range on ADGA linear scale (see DAIRY_CONCEPTS.md)
LEVEL_RA_THRESHOLD = 30.0
NARROW_RW_THRESHOLD = 26.0
GAP_THRESHOLD = 30
STRONG_THRESHOLD = 32
ESTIMATE_POSITIVE_MULT = 0.75
CONFIDENCE_PENALTY_ESTIMATED = 2.0


def trait_contrib(weight: float, doe_v, partner_v, estimated: bool) -> float:
    if doe_v is None or partner_v is None:
        return 0.0
    if doe_v < GAP_THRESHOLD and partner_v > doe_v:
        unit = min((partner_v - doe_v) / 5.0, 2.0)
        c = weight * unit
        return c * ESTIMATE_POSITIVE_MULT if estimated else c
    if doe_v >= STRONG_THRESHOLD and partner_v < doe_v:
        unit = max((partner_v - doe_v) / 5.0, -1.5)
        return weight * unit * 0.5
    return 0.0


def ra_distance(score: float, low: float, high: float) -> float:
    """0 if inside preferred band; else how far outside."""
    if low <= score <= high:
        return 0.0
    if score < low:
        return low - score
    return score - high


def ra_contrib(doe_ra, partner_ra, estimated: bool, band: tuple[float, float] | None) -> float:
    if band is None or doe_ra is None or partner_ra is None:
        return 0.0
    low, high = band
    improvement = ra_distance(doe_ra, low, high) - ra_distance(partner_ra, low, high)
    if improvement > 0:
        c = RA_WEIGHT * min(improvement / 5.0, 2.0)
        return c * ESTIMATE_POSITIVE_MULT if estimated else c
    if improvement < 0:
        return RA_WEIGHT * max(improvement / 5.0, -1.5) * 0.5
    return 0.0


def gap_closure(doe: dict, buck: dict, band: tuple[float, float] | None) -> float:
    total = sum(
        trait_contrib(w, doe[k], buck[k], buck["estimated"])
        for k, w in WEIGHTS.items()
    )
    total += ra_contrib(doe.get("ra"), buck.get("ra"), buck["estimated"], band)
    return total


def risk_penalty(
    doe: dict, buck: dict, band: tuple[float, float] | None
) -> tuple[float, list[str]]:
    pen = 0.0
    reasons: list[str] = []
    dra, pra, prw = doe.get("ra"), buck.get("ra"), buck.get("rw")

    protect_above = band[1] if band else None
    if (
        protect_above is not None
        and dra is not None
        and pra is not None
        and dra > protect_above
        and pra > dra
    ):
        p = 2.0 + 0.4 * (pra - dra)
        pen += p
        reasons.append(f"further flatten RA>{protect_above:.0f} +{p:.1f}")

    # Level-range angle + narrow width (DAIRY_CONCEPTS kidding mitigation)
    if (
        pra is not None
        and pra >= LEVEL_RA_THRESHOLD
        and prw is not None
        and prw < NARROW_RW_THRESHOLD
    ):
        pen += 1.5
        reasons.append(f"RA≥{LEVEL_RA_THRESHOLD:.0f} with narrow width +1.5")

    if doe.get("msl") is not None and doe["msl"] <= 20:
        p_msl = buck.get("msl")
        if p_msl is None:
            pen += 1.5
            reasons.append("unproven MSL +1.5")
        elif p_msl <= 22:
            pen += 3.0
            reasons.append("weak MSL stack +3.0")

    if doe.get("tp") is not None and doe["tp"] <= 21:
        p_tp = buck.get("tp")
        if p_tp is None:
            pen += 1.0
            reasons.append("unproven teat placement +1.0")
        elif p_tp <= 22:
            pen += 2.5
            reasons.append("wide teat placement stack +2.5")

    return pen, reasons


def bis_pair(
    doe: dict | None,
    buck: dict,
    band: tuple[float, float] | None = None,
) -> dict:
    """Score one doe×buck pair from loaded trait dicts."""
    if band is None:
        band = load_preferred_ra_band()
    if doe is None:
        return {
            "bis": None,
            "gap_closure": None,
            "risk_penalty": None,
            "confidence_penalty": None,
            "reasons": ["incomplete doe LA"],
        }
    gc = gap_closure(doe, buck, band)
    rp, reasons = risk_penalty(doe, buck, band)
    cp = CONFIDENCE_PENALTY_ESTIMATED if buck["estimated"] else 0.0
    score = round(gc - rp - cp, 1)
    return {
        "bis": score,
        "gap_closure": round(gc, 2),
        "risk_penalty": round(rp, 2),
        "confidence_penalty": cp,
        "reasons": reasons,
    }


def format_bis(score) -> str:
    if score is None:
        return "N/A"
    return f"{score:+.1f}"


def rank_bucks_for_doe(doe_name: str, does: dict, bucks: dict) -> list[tuple[str, dict]]:
    band = load_preferred_ra_band()
    rows = [(b, bis_pair(does[doe_name], bucks[b], band)) for b in bucks]
    rows.sort(
        key=lambda x: (x[1]["bis"] is not None, x[1]["bis"] if x[1]["bis"] is not None else -999),
        reverse=True,
    )
    return rows


def rank_does_for_buck(buck_name: str, does: dict, bucks: dict) -> list[tuple[str, dict]]:
    band = load_preferred_ra_band()
    rows = [(d, bis_pair(does[d], bucks[buck_name], band)) for d in does]
    rows.sort(
        key=lambda x: (x[1]["bis"] is not None, x[1]["bis"] if x[1]["bis"] is not None else -999),
        reverse=True,
    )
    return rows


def bis(doe_name: str, buck_name: str, does: dict | None = None, bucks: dict | None = None) -> dict:
    """Return BIS for a doe×buck pair by Barn Name. Loads herd data if not provided."""
    if does is None or bucks is None:
        does, bucks = load_breeding_animals()
    return bis_pair(does[doe_name], bucks[buck_name])


if __name__ == "__main__":
    band = load_preferred_ra_band()
    print(f"Preferred RA band from GOALS.md: {band}")
    does, bucks = load_breeding_animals()

    print("\nDoe Breeding rankings (bucks by BIS)")
    for d in does:
        print(f"\n{d}")
        for b, m in rank_bucks_for_doe(d, does, bucks):
            print(
                f"  {b:8} {format_bis(m['bis'])}  "
                f"(gap={m['gap_closure']}, risk={m['risk_penalty']}, conf={m['confidence_penalty']})"
                f"  {m['reasons']}"
            )

    print("\nBuck Breeding rankings (does by BIS)")
    for b in bucks:
        print(f"\n{b}")
        for d, m in rank_does_for_buck(b, does, bucks):
            print(f"  {d:10} {format_bis(m['bis'])}")
