#!/usr/bin/env python3
"""Load breeding-roster animals and LA traits from repo markdown — no hardcoded herd data."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BREEDING_ROSTER = ROOT / "HERD_BREEDING_ROSTER.md"
HERD_ROSTER = ROOT / "HERD_ROSTER.md"
LA_SCORES = ROOT / "LA_SCORES_2026.md"
GOALS = ROOT / "GOALS.md"
ESTIMATED_PROFILES_GLOB = "profiles/estimated-buck-profile-*.md"


def load_preferred_ra_band(path: Path = GOALS) -> tuple[float, float] | None:
    """Parse `Preferred Rump Angle band: LOW–HIGH` from GOALS.md. None if absent."""
    if not path.exists():
        return None
    text = path.read_text()
    m = re.search(
        r"Preferred Rump Angle band:\*?\*?\s*(\d+(?:\.\d+)?)\s*[–\-]\s*(\d+(?:\.\d+)?)",
        text,
        re.I,
    )
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))

# LA_SCORES_2026.md column header → BIS trait key
SCORE_COLUMNS = {
    "STATURE": "stat",
    "STRENGTH": "st",
    "DAIRYNESS": "dy",
    "RUMP ANGLE": "ra",
    "RUMP WIDTH": "rw",
    "MEDIAL SUSPENSORY LIGAMENT": "msl",
    "TEAT PLACEMENT REAR VIEW": "tp",
    "TEAT DIAMETER": "td",
}

# Keys expected on every animal trait dict used by BIS
TRAIT_KEYS = ("msl", "tp", "td", "dy", "rw", "st", "stat", "ra")


def _parse_float(raw: str):
    raw = raw.strip()
    if not raw or raw.upper() in {"NA", "—", "-", "N/A"}:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def parse_breeding_roster(path: Path = BREEDING_ROSTER) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Return (does, bucks) as lists of (barn_name, reg#)."""
    text = path.read_text()
    does: list[tuple[str, str]] = []
    bucks: list[tuple[str, str]] = []
    section = None
    for line in text.splitlines():
        if line.startswith("## Does"):
            section = "does"
            continue
        if line.startswith("## Bucks"):
            section = "bucks"
            continue
        if line.startswith("## "):
            section = None
            continue
        m = re.match(r"^- +(.+?) +\((PD\d+)\)\s*$", line.strip())
        if not m or section is None:
            continue
        entry = (m.group(1).strip(), m.group(2))
        if section == "does":
            does.append(entry)
        else:
            bucks.append(entry)
    return does, bucks


def parse_herd_roster_meta(path: Path = HERD_ROSTER) -> dict[str, dict]:
    """Map reg# → {barn_name, sex, notes, owner_height_in}."""
    text = path.read_text()
    meta: dict[str, dict] = {}
    current_reg = None
    current: dict = {}

    def flush():
        nonlocal current_reg, current
        if current_reg and current.get("barn_name"):
            meta[current_reg] = current
        current_reg = None
        current = {}

    for line in text.splitlines():
        heading = re.match(r"^### (.+)\((PD\d+)\)\s*$", line)
        if heading:
            flush()
            current_reg = heading.group(2)
            current = {
                "barn_name": None,
                "sex": None,
                "notes": "",
                "owner_height_in": None,
                "registered_name": heading.group(1).strip(),
            }
            continue
        if current_reg is None:
            continue
        if m := re.match(r"^\*\*Barn Name:\*\*\s*(.+?)\s*$", line):
            current["barn_name"] = m.group(1).strip()
        elif m := re.match(r"^\*\*Sex:\*\*\s*(.+?)\s*$", line):
            current["sex"] = m.group(1).strip()
        elif m := re.match(r"^\*\*Owner height:\*\*\s*([0-9.]+)\s*\"?\s*$", line):
            current["owner_height_in"] = float(m.group(1))
        elif m := re.match(r"^\*\*Notes:\*\*\s*(.+?)\s*$", line):
            current["notes"] = m.group(1).strip()
    flush()
    return meta


def parse_la_scores(path: Path = LA_SCORES) -> dict[str, dict]:
    """Map reg# → trait dict + fs string + incomplete flag."""
    lines = path.read_text().splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.startswith("| Registration Number"):
            header_idx = i
            break
    if header_idx is None:
        raise ValueError(f"No LA score table header in {path}")

    headers = [h.strip() for h in lines[header_idx].strip("|").split("|")]
    # skip separator row
    out: dict[str, dict] = {}
    for line in lines[header_idx + 2 :]:
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        row = dict(zip(headers, cells))
        reg = row.get("Registration Number", "").strip()
        if not re.fullmatch(r"PD\d+", reg):
            continue

        traits = {k: None for k in TRAIT_KEYS}
        for col, key in SCORE_COLUMNS.items():
            traits[key] = _parse_float(row.get(col, ""))

        ga = row.get("GENERAL APPEARANCE", "").strip()
        ds = row.get("DAIRY STRENGTH", "").strip()
        bc = row.get("BODY CAPACITY", "").strip()
        mam = row.get("MAMMARY", "").strip()
        final = row.get("FINAL SCORE", "").strip()

        letters = "".join(x for x in (ga, ds, bc, mam) if x)
        if final.upper() == "NA" or not final:
            fs = "NA"
            incomplete = True
        else:
            fs = f"{letters} {final}" if letters else final
            # Incomplete if no scored structure traits at all
            incomplete = all(traits[k] is None for k in ("st", "dy", "ra", "rw"))

        out[reg] = {
            **traits,
            "fs": fs,
            "incomplete": incomplete,
            "estimated": False,
            "sex": row.get("SEX", "").strip().upper(),
        }
    return out


def parse_estimated_bis_inputs(path: Path) -> dict:
    """
    Parse a ## Script inputs (BIS) key/value table from an estimated buck profile.

    Expected markdown:

    ## Script inputs (BIS)
    | key | value |
    |-----|-------|
    | estimated | yes |
    | msl | 24.5 |
    ...
    """
    text = path.read_text()
    m = re.search(
        r"## Script inputs \(BIS\)\s*\n(?:.*?\n)*?\| *key *\| *value *\|.*\n\|[-| ]+\|\s*\n((?:\|.*\|\s*\n)+)",
        text,
        re.I,
    )
    if not m:
        raise ValueError(f"No ## Script inputs (BIS) table in {path}")

    values: dict = {k: None for k in TRAIT_KEYS}
    values["estimated"] = True
    values["fs"] = "estimated"
    values["incomplete"] = False

    for row in m.group(1).strip().splitlines():
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) < 2:
            continue
        key, raw = cells[0].lower(), cells[1]
        if key == "estimated":
            values["estimated"] = raw.lower() in {"yes", "true", "1", "y"}
        elif key == "fs":
            values["fs"] = raw
        elif key in TRAIT_KEYS:
            values[key] = _parse_float(raw)
    return values


def merge_profile_fills(base: dict, profile_values: dict) -> tuple[dict, set[str]]:
    """
    Fill missing trait keys from a profile. Official LA values win when present.

    Returns (merged trait dict for TRAIT_KEYS, set of keys filled from the profile).
    """
    filled: set[str] = set()
    merged = {k: base.get(k) for k in TRAIT_KEYS}
    for key in TRAIT_KEYS:
        if merged[key] is None and profile_values.get(key) is not None:
            merged[key] = profile_values[key]
            filled.add(key)
    return merged, filled


def find_estimated_profile(reg: str, barn_name: str) -> Path | None:
    """Locate profile whose title Reg # matches, else title barn-name match."""
    paths = sorted(ROOT.glob(ESTIMATED_PROFILES_GLOB))
    title_reg = re.compile(rf"\({re.escape(reg)}\)")
    for path in paths:
        title = path.read_text().splitlines()[0]
        if title_reg.search(title):
            return path
    if not barn_name:
        return None
    for path in paths:
        title = path.read_text().splitlines()[0]
        if re.search(rf"\b{re.escape(barn_name)}\b", title, re.I):
            return path
    return None


def load_breeding_animals(
    *,
    breeding_roster: Path = BREEDING_ROSTER,
    herd_roster: Path = HERD_ROSTER,
    la_scores: Path = LA_SCORES,
) -> tuple[dict[str, dict | None], dict[str, dict]]:
    """
    Build doe and buck trait maps keyed by Barn Name.

    Does with incomplete LA → value None (BIS N/A).
    Bucks without usable LA → full Script inputs from estimated profile (`estimated=True`).
    Bucks with LA → official scores, then fill any blank traits (typically mammary)
    from a matching `profiles/estimated-buck-profile-*.md` when present.
    """
    does_list, bucks_list = parse_breeding_roster(breeding_roster)
    meta = parse_herd_roster_meta(herd_roster)
    scores = parse_la_scores(la_scores)

    does: dict[str, dict | None] = {}
    for barn, reg in does_list:
        animal_meta = meta.get(reg, {})
        row = scores.get(reg)
        if row is None or row.get("incomplete"):
            does[barn] = None
            continue
        ra = row["ra"]
        band = load_preferred_ra_band()
        protect_above = band[1] if band else None
        does[barn] = {
            **{k: row[k] for k in TRAIT_KEYS},
            # Protect from further flattening when already above GOALS preferred upper bound
            "protect_ra": (
                protect_above is not None and ra is not None and ra > protect_above
            ),
            "fs": row["fs"],
            "reg": reg,
            "estimated": False,
            "estimated_traits": set(),
            "owner_height_in": animal_meta.get("owner_height_in"),
            "registered_name": animal_meta.get("registered_name"),
        }

    bucks: dict[str, dict] = {}
    for barn, reg in bucks_list:
        row = scores.get(reg)
        profile = find_estimated_profile(reg, barn)
        profile_values = parse_estimated_bis_inputs(profile) if profile else None

        if row and not row.get("incomplete"):
            traits = {k: row[k] for k in TRAIT_KEYS}
            estimated_traits: set[str] = set()
            if profile_values is not None:
                traits, estimated_traits = merge_profile_fills(traits, profile_values)
            bucks[barn] = {
                **traits,
                "estimated": False,
                "estimated_traits": estimated_traits,
                "fs": row["fs"],
                "reg": reg,
                "profile": str(profile.relative_to(ROOT)) if profile else None,
            }
            continue

        if profile_values is None:
            raise FileNotFoundError(
                f"No LA scores and no estimated profile for buck {barn} ({reg}). "
                f"Add scores to {la_scores.name} or a profiles/estimated-buck-profile-*.md "
                f"with a ## Script inputs (BIS) table."
            )
        bucks[barn] = {
            **{k: profile_values[k] for k in TRAIT_KEYS},
            "estimated": bool(profile_values.get("estimated", True)),
            "estimated_traits": set(TRAIT_KEYS),
            "fs": profile_values.get("fs") or "estimated",
            "reg": reg,
            "profile": str(profile.relative_to(ROOT)),
        }

    return does, bucks


if __name__ == "__main__":
    does, bucks = load_breeding_animals()
    print("Does:")
    for name, data in does.items():
        print(f"  {name}: {'incomplete' if data is None else data}")
    print("Bucks:")
    for name, data in bucks.items():
        print(f"  {name}: {data}")
