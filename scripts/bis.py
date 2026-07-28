#!/usr/bin/env python3
"""Breeding Impact Score (BIS) — see LA_REPORT_GUIDELINES.md § Breeding Impact Score.

Herd animals and scores are loaded from markdown via herd_data.py — nothing animal-specific
is hardcoded here.
"""

from __future__ import annotations

from herd_data import load_breeding_animals

# Formula constants (not herd data) — keep in sync with LA_REPORT_GUIDELINES.md
WEIGHTS = {
    "msl": 5.0,
    "tp": 4.0,
    "td": 3.0,
    "dy": 4.0,
    "rw": 3.0,
    "st": 2.0,
    "stat": 1.0,
}
GAP_THRESHOLD = 30
STRONG_THRESHOLD = 32
ESTIMATE_POSITIVE_MULT = 0.50
CONFIDENCE_PENALTY_ESTIMATED = 8.0


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


def gap_closure(doe: dict, buck: dict) -> float:
    return sum(
        trait_contrib(w, doe[k], buck[k], buck["estimated"])
        for k, w in WEIGHTS.items()
    )


def risk_penalty(doe: dict, buck: dict) -> tuple[float, list[str]]:
    pen = 0.0
    reasons: list[str] = []
    dra, pra, prw = doe["ra"], buck["ra"], buck["rw"]

    if doe["protect_ra"] and dra is not None and pra is not None:
        if pra > dra:
            p = 2.0 + 0.4 * (pra - dra)
            pen += p
            reasons.append(f"further flatten liked RA +{p:.1f}")
        elif pra < dra - 4:
            p = 1.5 + 0.25 * (dra - pra)
            pen += p
            reasons.append(f"steepen liked RA +{p:.1f}")

    if dra is not None and pra is not None and dra <= 25 and pra > dra:
        amt = pra - dra
        if prw is not None and prw < 26:
            p = min(1.0 + 0.35 * amt, 5.0)
            pen += p
            reasons.append(f"flatten steep without width buffer +{p:.1f}")
        else:
            p = min(0.3 + 0.12 * amt, 2.0)
            pen += p
            reasons.append(f"flatten steep with width buffer +{p:.1f}")

    if doe["msl"] is not None and doe["msl"] <= 20:
        p_msl = buck["msl"]
        if p_msl is None:
            pen += 1.5
            reasons.append("unproven MSL +1.5")
        elif p_msl <= 22:
            pen += 3.0
            reasons.append("soft MSL stack +3.0")

    if doe["tp"] is not None and doe["tp"] <= 21:
        p_tp = buck["tp"]
        if p_tp is None:
            pen += 1.0
            reasons.append("unproven TP +1.0")
        elif p_tp <= 22:
            pen += 2.5
            reasons.append("soft TP stack +2.5")

    return pen, reasons


def bis_pair(doe: dict | None, buck: dict) -> dict:
    """Score one doe×buck pair from loaded trait dicts."""
    if doe is None:
        return {
            "bis": None,
            "gap_closure": None,
            "risk_penalty": None,
            "confidence_penalty": None,
            "reasons": ["incomplete doe LA"],
        }
    gc = gap_closure(doe, buck)
    rp, reasons = risk_penalty(doe, buck)
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
    rows = [(b, bis_pair(does[doe_name], bucks[b])) for b in bucks]
    rows.sort(
        key=lambda x: (x[1]["bis"] is not None, x[1]["bis"] if x[1]["bis"] is not None else -999),
        reverse=True,
    )
    return rows


def rank_does_for_buck(buck_name: str, does: dict, bucks: dict) -> list[tuple[str, dict]]:
    rows = [(d, bis_pair(does[d], bucks[buck_name])) for d in does]
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
    does, bucks = load_breeding_animals()

    print("Doe Breeding rankings (bucks by BIS)")
    for d in does:
        print(f"\n{d}")
        for b, m in rank_bucks_for_doe(d, does, bucks):
            print(
                f"  {b:8} {format_bis(m['bis'])}  "
                f"(gap={m['gap_closure']}, risk={m['risk_penalty']}, conf={m['confidence_penalty']})"
            )

    print("\nBuck Breeding rankings (does by BIS)")
    for b in bucks:
        print(f"\n{b}")
        for d, m in rank_does_for_buck(b, does, bucks):
            print(f"  {d:10} {format_bis(m['bis'])}")
