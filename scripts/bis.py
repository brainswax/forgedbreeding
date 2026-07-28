#!/usr/bin/env python3
"""Breeding Impact Score (BIS) — see LA_REPORT_GUIDELINES.md § Breeding Impact Score."""

from __future__ import annotations

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

# Current herd inputs (from LA_SCORES_2026.md + estimated Finale profile)
DOES = {
    "Lizbeth": dict(msl=13, tp=17, td=25, dy=38, rw=31, st=36, stat=25, ra=23, protect_ra=False, fs="VEEG 85"),
    "Sapphire": dict(msl=17, tp=21, td=21, dy=40, rw=35, st=29, stat=32, ra=24, protect_ra=False, fs="VEVV 88"),
    "Snickers": dict(msl=18, tp=20, td=21, dy=23, rw=23, st=36, stat=22, ra=36, protect_ra=True, fs="GAEV 84"),
    "Amber": dict(msl=17, tp=17, td=20, dy=36, rw=21, st=34, stat=23, ra=21, protect_ra=False, fs="GEEV 86"),
    "Tinkles": dict(msl=17, tp=20, td=24, dy=36, rw=25, st=37, stat=23, ra=38, protect_ra=True, fs="VVVA 84"),
    "Lux": None,  # incomplete LA → BIS N/A
}

BUCKS = {
    "Michael": dict(msl=None, tp=None, td=None, dy=30, rw=28, st=36, stat=40, ra=34, estimated=False, fs="VGE 88"),
    "Smithy": dict(msl=None, tp=None, td=None, dy=33, rw=24, st=36, stat=34, ra=28, estimated=False, fs="VVE 86"),
    "Finale": dict(msl=24.5, tp=21.0, td=26.0, dy=33.0, rw=30.0, st=30.0, stat=28.0, ra=28.5, estimated=True, fs="estimated"),
}


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


def bis(doe_name: str, buck_name: str) -> dict:
    """Return BIS for a doe×buck pair. Same value from either report type."""
    doe = DOES[doe_name]
    buck = BUCKS[buck_name]
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


def rank_bucks_for_doe(doe_name: str) -> list[tuple[str, dict]]:
    rows = [(b, bis(doe_name, b)) for b in BUCKS]
    rows.sort(
        key=lambda x: (x[1]["bis"] is not None, x[1]["bis"] if x[1]["bis"] is not None else -999),
        reverse=True,
    )
    return rows


def rank_does_for_buck(buck_name: str) -> list[tuple[str, dict]]:
    rows = [(d, bis(d, buck_name)) for d in DOES]
    rows.sort(
        key=lambda x: (x[1]["bis"] is not None, x[1]["bis"] if x[1]["bis"] is not None else -999),
        reverse=True,
    )
    return rows


if __name__ == "__main__":
    print("Doe Breeding rankings (bucks by BIS)")
    for d in DOES:
        print(f"\n{d}")
        for b, m in rank_bucks_for_doe(d):
            print(
                f"  {b:8} {format_bis(m['bis'])}  "
                f"(gap={m['gap_closure']}, risk={m['risk_penalty']}, conf={m['confidence_penalty']})"
            )

    print("\nBuck Breeding rankings (does by BIS)")
    for b in BUCKS:
        print(f"\n{b}")
        for d, m in rank_does_for_buck(b):
            print(f"  {d:10} {format_bis(m['bis'])}")
