#!/usr/bin/env python3
"""
Fetch Linear Appraisal history from ADGA Genetics for an animal's
parents and siblings, and upsert into LA_REFERENCE_SCORES.md.

Be polite: default 2.0s between requests, identifiable User-Agent,
small bursts only (parents + siblings — not whole-herd crawls).

Example:
  python3 scripts/fetch_adga_linear_refs.py D002277726
  python3 scripts/fetch_adga_linear_refs.py https://genetics.adga.org/GoatDetail.aspx?RegNumber=D002277726
  python3 scripts/fetch_adga_linear_refs.py D002277726 --half-sibs --dry-run

Source: https://genetics.adga.org/ (ADGA / CDCB public genetics site)
"""

from __future__ import annotations

import argparse
import html as htmllib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF_SCORES = ROOT / "LA_REFERENCE_SCORES.md"
BASE = "https://genetics.adga.org"
DETAIL = f"{BASE}/GoatDetail.aspx"

# ADGA Genetics returns 403 for non-browser User-Agents. Use a normal
# browser UA and stay polite via delay + small family-sized request sets.
# Contact / purpose for operators reading logs or this file:
#   Forged Farm / Brian Denton, ADGA member 1660541 — personal breeding research.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
)
DEFAULT_DELAY_S = 2.5
SUBMENU = "ctl00$BodyContentPlaceHolder$SubMenu1"


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------


def _request(url: str, data: bytes | None = None, referer: str | None = None) -> str:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    if data is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Origin"] = BASE
        headers["Referer"] = referer or url
    req = urllib.request.Request(url, data=data, headers=headers)
    last_err: Exception | None = None
    for attempt in range(1, 5):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            last_err = e
            # Retry transient gateway / rate-limit responses
            if e.code in (429, 502, 503, 504) and attempt < 4:
                time.sleep(DEFAULT_DELAY_S * attempt * 2)
                continue
            raise
        except urllib.error.URLError as e:
            last_err = e
            if attempt < 4:
                time.sleep(DEFAULT_DELAY_S * attempt * 2)
                continue
            raise
    raise RuntimeError(last_err)


def _extract_form(page: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for m in re.finditer(r"<input[^>]+>", page, re.I):
        tag = m.group(0)
        name_m = re.search(r'name="([^"]+)"', tag, re.I)
        if not name_m:
            continue
        val_m = re.search(r'value="([^"]*)"', tag, re.I)
        fields[htmllib.unescape(name_m.group(1))] = (
            htmllib.unescape(val_m.group(1)) if val_m else ""
        )
    return fields


def _postback(url: str, page: str, target: str, argument: str = "") -> str:
    fields = _extract_form(page)
    fields["__EVENTTARGET"] = target
    fields["__EVENTARGUMENT"] = argument
    body = urllib.parse.urlencode(fields).encode()
    return _request(url, data=body, referer=url)


class PoliteClient:
    """Session-less client with mandatory delay between hits."""

    def __init__(self, delay_s: float = DEFAULT_DELAY_S):
        self.delay_s = max(0.5, float(delay_s))
        self._last = 0.0
        self.hits = 0

    def _wait(self) -> None:
        now = time.monotonic()
        wait = self.delay_s - (now - self._last)
        if wait > 0:
            time.sleep(wait)

    def get(self, url: str) -> str:
        self._wait()
        html = _request(url)
        self._last = time.monotonic()
        self.hits += 1
        return html

    def postback(self, url: str, page: str, target: str, argument: str = "") -> str:
        self._wait()
        html = _postback(url, page, target, argument)
        self._last = time.monotonic()
        self.hits += 1
        return html


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def normalize_reg(raw: str) -> str:
    """Accept URL, D00…, PD…, or bare digits → ADGA D######## form."""
    s = raw.strip()
    m = re.search(r"RegNumber=([DP]?\d+)", s, re.I)
    if m:
        s = m.group(1)
    s = s.upper().replace(" ", "")
    if s.startswith("PD"):
        digits = s[2:]
        return "D" + digits.zfill(9)
    if s.startswith("D"):
        return "D" + s[1:].zfill(9)
    if s.isdigit():
        return "D" + s.zfill(9)
    raise ValueError(f"Cannot parse registration number from: {raw!r}")


def adga_to_pd(reg: str) -> str:
    """D002277726 → PD2277726 (matches LA_REFERENCE_SCORES / herd style)."""
    reg = normalize_reg(reg)
    return "PD" + str(int(reg[1:]))


def detail_url(reg: str) -> str:
    return f"{DETAIL}?RegNumber={normalize_reg(reg)}"


def _cell_text(cell_html: str) -> str:
    t = re.sub(r"<br\s*/?>", " ", cell_html, flags=re.I)
    t = re.sub(r"<[^>]+>", "", t)
    t = htmllib.unescape(t).replace("\xa0", " ").strip()
    return t


def _parse_grid(page: str, grid_id_substr: str) -> list[dict[str, str]]:
    m = re.search(
        rf'<table[^>]*id="([^"]*{re.escape(grid_id_substr)}[^"]*)"[^>]*>([\s\S]*?)</table>',
        page,
        re.I,
    )
    if not m:
        return []
    table = m.group(2)
    headers: list[str] = []
    rows_out: list[dict[str, str]] = []
    for rm in re.finditer(r"<tr[^>]*>([\s\S]*?)</tr>", table, re.I):
        row = rm.group(1)
        ths = re.findall(r"<th[^>]*>([\s\S]*?)</th>", row, re.I)
        if ths and not headers:
            headers = [re.sub(r"\s+", " ", _cell_text(h)) for h in ths]
            continue
        tds = re.findall(r"<td[^>]*>([\s\S]*?)</td>", row, re.I)
        if not tds or not headers:
            continue
        vals = [_cell_text(c) for c in tds]
        # pad / trim
        if len(vals) < len(headers):
            vals += [""] * (len(headers) - len(vals))
        rows_out.append(dict(zip(headers, vals[: len(headers)])))
    return rows_out


def _menu_enabled(page: str, label: str) -> bool:
    # enabled: javascript postback link; disabled: <a disabled="true">Label</a>
    if re.search(
        rf"SubMenu1&#39;,&#39;{re.escape(label)}&#39;\)\">\s*{re.escape(label)}",
        page,
    ):
        return True
    return False


@dataclass
class GoatIdentity:
    reg: str  # ADGA D…
    name: str
    sex: str | None = None  # Male / Female
    dob: str | None = None  # ISO-ish
    breed_pct: str | None = None
    herdbook: str | None = None
    titles: str | None = None  # e.g. GCH from title attr
    sire_reg: str | None = None
    sire_name: str | None = None
    dam_reg: str | None = None
    dam_name: str | None = None


@dataclass
class LinearAppraisal:
    la_year: str
    age: str
    traits: dict[str, str] = field(default_factory=dict)
    structural: dict[str, str] = field(default_factory=dict)
    codes: list[str] = field(default_factory=list)


@dataclass
class GoatRecord:
    identity: GoatIdentity
    appraisals: list[LinearAppraisal] = field(default_factory=list)
    role: str = ""
    linear_available: bool = False


def parse_identity(page: str, reg: str) -> GoatIdentity:
    reg = normalize_reg(reg)
    title_m = re.search(r"Goat Detail:\s*([^<\n]+)", page)
    name = ""
    titles = None
    sex = None
    if title_m:
        # e.g. ILENESRASCALS MICHAEL DARLING - D002277726 (PB Buck)
        raw = htmllib.unescape(title_m.group(1)).strip()
        raw = re.sub(rf"\s*-\s*{reg}.*$", "", raw, flags=re.I).strip()
        # trailing (PB Buck) / (PB Doe GCH) — may remain if reg strip failed
        paren = re.search(r"\(([^)]*)\)\s*$", raw)
        if not paren:
            # title sometimes keeps "NAME - D00… (PB Doe GCH)" before strip
            paren = re.search(
                rf"{re.escape(reg)}\s*\(([^)]*)\)",
                htmllib.unescape(title_m.group(1)),
                re.I,
            )
        if paren:
            meta = paren.group(1)
            if raw.endswith(")"):
                raw = re.sub(r"\s*\([^)]*\)\s*$", "", raw).strip()
            if re.search(r"\bBuck\b", meta, re.I):
                sex = "Male"
            elif re.search(r"\bDoe\b", meta, re.I):
                sex = "Female"
            tm = re.search(r"\b(SGCH|GCH|SG|CH)\b", meta, re.I)
            if tm:
                titles = tm.group(1).upper()
        name = re.sub(r"\s*\([^)]*\)\s*$", "", raw).strip()

    dob = None
    m = re.search(r"DOB:\s*([0-9/]+)", page)
    if m:
        dob = _us_date_to_iso(m.group(1).strip())

    breed_pct = None
    m = re.search(r"Breed Percent:\s*([^<\n]+)", page)
    if m:
        breed_pct = m.group(1).strip()

    sire_reg = sire_name = dam_reg = dam_name = None
    for m in re.finditer(
        r'title="([^"]*)"\s+href="GoatDetail\.aspx\?RegNumber=(D\d+)">\s*([SD])\s*:\s*([^<]+?)\s*</a>',
        page,
    ):
        _title, preg, letter, pname = m.groups()
        pname = htmllib.unescape(pname).strip()
        if letter == "S":
            sire_reg, sire_name = normalize_reg(preg), pname
        elif letter == "D":
            dam_reg, dam_name = normalize_reg(preg), pname

    return GoatIdentity(
        reg=reg,
        name=name or reg,
        sex=sex,
        dob=dob,
        breed_pct=breed_pct,
        titles=titles,
        sire_reg=sire_reg,
        sire_name=sire_name,
        dam_reg=dam_reg,
        dam_name=dam_name,
    )


def _us_date_to_iso(s: str) -> str:
    # M/D/YYYY or YYYY.MM.DD
    s = s.strip()
    if re.match(r"\d{4}\.\d{2}\.\d{2}$", s):
        y, m, d = s.split(".")
        return f"{y}-{m}-{d}"
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})$", s)
    if m:
        mo, dy, y = m.groups()
        return f"{y}-{int(mo):02d}-{int(dy):02d}"
    return s


def parse_linear_history(page: str) -> list[LinearAppraisal]:
    linear_rows = _parse_grid(page, "LinearTraitHistoryGrid")
    struct_rows = _parse_grid(page, "StructuralTraitGrid")
    code_rows = _parse_grid(page, "LinearCodeGrid")

    by_year: dict[str, LinearAppraisal] = {}
    for row in linear_rows:
        year = row.get("LAYear", "").strip()
        if not year:
            continue
        traits = {k: v for k, v in row.items() if k not in ("LAYear", "Age")}
        by_year[year] = LinearAppraisal(
            la_year=year, age=row.get("Age", "").strip(), traits=traits
        )

    for row in struct_rows:
        year = row.get("LAYear", "").strip()
        if not year:
            continue
        structural = {k: v for k, v in row.items() if k not in ("LAYear", "Age")}
        if year in by_year:
            by_year[year].structural = structural
            if not by_year[year].age:
                by_year[year].age = row.get("Age", "").strip()
        else:
            by_year[year] = LinearAppraisal(
                la_year=year,
                age=row.get("Age", "").strip(),
                structural=structural,
            )

    for row in code_rows:
        year = row.get("LAYear", "").strip()
        if year not in by_year:
            continue
        bits = []
        for key in ("Code 1", "Code 2", "Code 3"):
            c = (row.get(key) or "").strip()
            if c:
                bits.append(c)
        by_year[year].codes = bits

    # newest first
    return [by_year[y] for y in sorted(by_year.keys(), reverse=True)]


@dataclass
class ProgenyRow:
    reg: str
    name: str
    sex: str  # M / F
    dob: str | None
    eval_code: str  # PT / T / P / NA / …


def parse_progeny(page: str) -> list[ProgenyRow]:
    # Progeny grid id varies; find table whose headers include Reg#
    tables = re.findall(r"<table[^>]*>([\s\S]*?)</table>", page, re.I)
    out: list[ProgenyRow] = []
    for table in tables:
        if "Reg#" not in table and "Reg#" not in _cell_text(table):
            # header may use Reg#
            if not re.search(r"<th[^>]*>\s*<[^>]*>Reg#", table, re.I):
                continue
        headers: list[str] = []
        for rm in re.finditer(r"<tr[^>]*>([\s\S]*?)</tr>", table, re.I):
            row = rm.group(1)
            ths = re.findall(r"<th[^>]*>([\s\S]*?)</th>", row, re.I)
            if ths and not headers:
                headers = [re.sub(r"\s+", " ", _cell_text(h)) for h in ths]
                continue
            if not headers:
                continue
            tds = re.findall(r"<td[^>]*>([\s\S]*?)</td>", row, re.I)
            if not tds:
                continue
            vals = [_cell_text(c) for c in tds]
            if len(vals) < len(headers):
                vals += [""] * (len(headers) - len(vals))
            data = dict(zip(headers, vals[: len(headers)]))
            reg = (data.get("Reg#") or "").strip()
            if not re.match(r"D\d+", reg):
                # try link
                lm = re.search(r"RegNumber=(D\d+)", row)
                if not lm:
                    continue
                reg = lm.group(1)
            name = (data.get("Name") or "").strip()
            if not name:
                nm = re.search(r"RegNumber=D\d+[^>]*>([^<]+)</a>", row)
                name = htmllib.unescape(nm.group(1)).strip() if nm else reg
            sex = (data.get("Sex") or "").strip().upper()[:1]
            dob_raw = (data.get("DOB") or "").strip()
            dob = _us_date_to_iso(dob_raw) if dob_raw else None
            eval_code = (data.get("Eval") or "").strip()
            out.append(
                ProgenyRow(
                    reg=normalize_reg(reg),
                    name=name,
                    sex=sex,
                    dob=dob,
                    eval_code=eval_code,
                )
            )
        if out:
            break
    return out


def has_type_eval(eval_code: str) -> bool:
    return "T" in (eval_code or "").upper()


# ---------------------------------------------------------------------------
# Fetch orchestration
# ---------------------------------------------------------------------------


def fetch_goat(
    client: PoliteClient, reg: str, role: str, fetch_linear: bool = True
) -> GoatRecord:
    reg = normalize_reg(reg)
    url = detail_url(reg)
    print(f"  GET  {reg} ({role}) …", flush=True)
    page = client.get(url)
    ident = parse_identity(page, reg)
    rec = GoatRecord(identity=ident, role=role)

    if not fetch_linear:
        return rec

    if not _menu_enabled(page, "Linear History"):
        print(f"       no Linear History link (skip)", flush=True)
        return rec

    print(f"  POST Linear History {reg} …", flush=True)
    lh = client.postback(url, page, SUBMENU, "Linear History")
    apps = parse_linear_history(lh)
    rec.appraisals = apps
    rec.linear_available = bool(apps)
    print(f"       {len(apps)} appraisal(s)", flush=True)
    return rec


def fetch_progeny(client: PoliteClient, reg: str) -> list[ProgenyRow]:
    reg = normalize_reg(reg)
    url = detail_url(reg)
    print(f"  GET  progeny of {reg} …", flush=True)
    page = client.get(url)
    if not _menu_enabled(page, "Progeny"):
        print(f"       Progeny menu disabled", flush=True)
        return []
    print(f"  POST Progeny {reg} …", flush=True)
    prog_page = client.postback(url, page, SUBMENU, "Progeny")
    rows = parse_progeny(prog_page)
    seen_pages = {1}
    # Paginate: __doPostBack('…ProgenyGrid','Page$N')
    while True:
        page_nums = sorted(
            {
                int(n)
                for n in re.findall(
                    r"ProgenyGrid&#39;,&#39;Page\$(\d+)&#39;",
                    prog_page,
                )
            }
        )
        next_pages = [n for n in page_nums if n not in seen_pages]
        if not next_pages:
            break
        n = next_pages[0]
        print(f"  POST Progeny page {n} …", flush=True)
        prog_page = client.postback(
            url, prog_page, "ctl00$BodyContentPlaceHolder$ProgenyGrid", f"Page${n}"
        )
        seen_pages.add(n)
        more = parse_progeny(prog_page)
        # de-dupe by reg
        have = {r.reg for r in rows}
        for r in more:
            if r.reg not in have:
                rows.append(r)
                have.add(r.reg)
    print(f"       {len(rows)} progeny row(s) across {len(seen_pages)} page(s)", flush=True)
    return rows


def collect_family(
    client: PoliteClient,
    subject_reg: str,
    *,
    include_half_sibs: bool = False,
    include_subject_linear: bool = True,
) -> list[GoatRecord]:
    subject_reg = normalize_reg(subject_reg)
    print(f"Subject {subject_reg}", flush=True)
    subject = fetch_goat(
        client, subject_reg, role="subject", fetch_linear=include_subject_linear
    )
    if not subject.identity.sire_reg or not subject.identity.dam_reg:
        raise RuntimeError(
            f"Could not parse sire/dam from pedigree for {subject_reg}"
        )

    sire_reg = subject.identity.sire_reg
    dam_reg = subject.identity.dam_reg
    print(
        f"Parents: sire {sire_reg} ({subject.identity.sire_name}); "
        f"dam {dam_reg} ({subject.identity.dam_name})",
        flush=True,
    )

    sire = fetch_goat(
        client,
        sire_reg,
        role=f"Sire of {subject.identity.name} ({adga_to_pd(subject_reg)})",
    )
    dam = fetch_goat(
        client,
        dam_reg,
        role=f"Dam of {subject.identity.name} ({adga_to_pd(subject_reg)})",
    )

    dam_prog = fetch_progeny(client, dam_reg)
    sire_prog = fetch_progeny(client, sire_reg)

    dam_regs = {p.reg for p in dam_prog}
    sire_regs = {p.reg for p in sire_prog}
    full_sib_regs = sorted((dam_regs & sire_regs) - {subject_reg})

    print(f"Full siblings: {len(full_sib_regs)}", flush=True)
    for r in full_sib_regs:
        name = next((p.name for p in dam_prog if p.reg == r), r)
        print(f"  - {r} {name}", flush=True)

    half_regs: list[str] = []
    if include_half_sibs:
        half_regs = sorted((dam_regs | sire_regs) - {subject_reg} - set(full_sib_regs))
        print(f"Half siblings: {len(half_regs)}", flush=True)

    # Prefer animals that ADGA marks as having type eval
    eval_by_reg = {p.reg: p.eval_code for p in dam_prog + sire_prog}

    records = [sire, dam]
    # Optionally keep subject if it has linear (Michael often won't on ADGA yet)
    if include_subject_linear and subject.linear_available:
        subject.role = (
            f"Subject / herd buck — ADGA Genetics linear history "
            f"(also in herd scores as {adga_to_pd(subject_reg)})"
        )
        records.insert(0, subject)

    for reg in full_sib_regs:
        ev = eval_by_reg.get(reg, "")
        role = (
            f"Full sibling of {subject.identity.name} ({adga_to_pd(subject_reg)})"
        )
        if not has_type_eval(ev):
            print(f"  skip {reg} (Eval={ev or 'NA'} — no type)", flush=True)
            # still record identity stub? skip to avoid empty sections
            continue
        rec = fetch_goat(client, reg, role=role)
        records.append(rec)

    for reg in half_regs:
        ev = eval_by_reg.get(reg, "")
        if not has_type_eval(ev):
            continue
        side = "maternal" if reg in dam_regs else "paternal"
        role = (
            f"{side.capitalize()} half-sibling of "
            f"{subject.identity.name} ({adga_to_pd(subject_reg)})"
        )
        rec = fetch_goat(client, reg, role=role)
        records.append(rec)

    return records


# ---------------------------------------------------------------------------
# Markdown emission
# ---------------------------------------------------------------------------

# Map ADGA Genetics linear headers → compact column keys used in LA_REFERENCE_SCORES
TRAIT_MAP = [
    ("Stature", "ST"),
    ("Strength", "STR"),
    ("Dairyness", "DY"),
    ("Rump Angle", "RA"),
    ("Rump Width", "RW"),
    ("Rear Leg Side View", "RL SV"),
    ("Fore Udder Attachment", "FA"),
    ("Rear Udder Height", "RH"),
    ("Rear Udder Arch", "RUA"),
    ("Medial", "MS"),
    ("Udder Depth", "UD"),
    ("Teat Placement", "TP"),
    ("Teat Diameter", "TD"),
    ("Teat Length", "TL"),
    ("Body Depth", "BD"),
    ("Rear Udder Side View", "RUSV"),
]

STRUCT_MAP = [
    ("Head", "Head"),
    ("Shoulder Assembly", "Shldrs"),
    ("Front Legs", "LF"),
    ("Rear Legs", "LR"),
    ("Feet", "Feet"),
    ("Back", "Back"),
    ("Rump", "Rump"),
    ("Udder Texture", "Txt"),
    ("General Appearance", "GA"),
    ("Dairy Strength", "DS"),
    ("Body Capacity", "Body"),
    ("Mammary System", "MMY"),
    ("FS", "FS"),
]


def _dash(v: str | None) -> str:
    if v is None:
        return "—"
    v = v.strip()
    if v == "" or v.upper() == "NA":
        return "—"
    return v


def _fs_letters(app: LinearAppraisal) -> str:
    ga = _dash(app.structural.get("General Appearance"))
    ds = _dash(app.structural.get("Dairy Strength"))
    body = _dash(app.structural.get("Body Capacity"))
    mmy = app.structural.get("Mammary System", "").strip()
    fs = _dash(app.structural.get("FS"))
    letters = "".join(x for x in (ga, ds, body, mmy) if x and x != "—")
    # normalize + to +
    if letters and fs != "—":
        return f"`{letters} {fs}`"
    if fs != "—":
        return f"`{fs}`"
    return "—"


def format_animal_markdown(rec: GoatRecord) -> str:
    ident = rec.identity
    pd = adga_to_pd(ident.reg)
    name = ident.name.upper()
    if ident.titles and not name.startswith(ident.titles):
        # keep GCH etc. only in prose notes; heading uses registered name
        pass

    lines: list[str] = []
    lines.append(f"## {name} ({pd})")
    lines.append("")
    lines.append(f"**Role:** {rec.role}")
    if ident.breed_pct:
        bp = ident.breed_pct.strip()
        compact = bp.replace(" ", "")
        if "100%D" in compact or compact == "100%D":
            lines.append("**Breed:** Purebred Nigerian Dwarf (100% D)")
        else:
            lines.append(f"**Breed:** {bp}")
    if ident.dob:
        lines.append(f"**DOB:** {ident.dob}")
    if ident.sex:
        lines.append(f"**Sex:** {ident.sex}")
    elif ident.name:
        # fallback: infer from goat-detail title already parsed; leave blank if unknown
        pass
    if ident.sire_name and ident.sire_reg:
        lines.append(
            f"**Sire:** {ident.sire_name.upper()} ({adga_to_pd(ident.sire_reg)})"
        )
    if ident.dam_name and ident.dam_reg:
        lines.append(
            f"**Dam:** {ident.dam_name.upper()} ({adga_to_pd(ident.dam_reg)})"
        )
    lines.append(f"**ADGA Genetics:** {detail_url(ident.reg)}")
    lines.append("")

    if not rec.appraisals:
        lines.append("_No Linear History available on ADGA Genetics (guest view)._")
        lines.append("")
        lines.append("---")
        lines.append("")
        return "\n".join(lines)

    # Header — doe-style full table (includes BD). Match existing reference file.
    header = (
        "| Date       | Age (ADGA) | ST | STR | DY | RA | RW | RL SV | FA | RH | RUA | MS | UD | TP | TD | TL | BD | RUSV | "
        "Head | Shldrs | LF | LR | Feet | Back | Rump | Txt | GA | DS | Body | MMY | FS |"
    )
    sep = (
        "|------------|------------|----|-----|----|----|----|-------|----|----|-----|----|----|----|----|----|----|------|"
        "------|--------|----|----|------|------|------|-----|----|----|------|-----|----|"
    )
    lines.append(header)
    lines.append(sep)

    for app in rec.appraisals:
        # Date: LA year only from this page
        date_s = f"{app.la_year}-??-??"
        cells = [date_s, _dash(app.age)]
        for src, _dst in TRAIT_MAP:
            cells.append(_dash(app.traits.get(src)))
        for src, _dst in STRUCT_MAP:
            if src == "FS":
                continue
            cells.append(_dash(app.structural.get(src)))
        cells.append(_dash(app.structural.get("FS")))
        lines.append("| " + " | ".join(cells) + " |")

    lines.append("")
    lines.append("**Notes**")
    lines.append(
        f"- Source: ADGA Genetics Linear History for {ident.reg} "
        f"(fetched {date.today().isoformat()})."
    )
    lines.append(
        "- Appraisal **Date** is LA year only (`YYYY-??-??`); exact calendar date is not shown on Linear History."
    )
    fs_bits = [_fs_letters(a) for a in rec.appraisals]
    fs_bits = [b for b in fs_bits if b != "—"]
    if fs_bits:
        lines.append(f"- Final Score format in reports: {', '.join(fs_bits)}.")
    # RUSV scale note
    rusvs = []
    for a in rec.appraisals:
        v = (a.traits.get("Rear Udder Side View") or "").strip()
        if v.isdigit():
            rusvs.append(int(v))
    if any(v > 4 for v in rusvs):
        lines.append(
            "- RUSV values >4 reflect the older 0–50-style field recording; "
            "current SOP uses a short 0–4 RUSV scale — do not mix scales casually."
        )
    if any(a.codes for a in rec.appraisals):
        for a in rec.appraisals:
            if a.codes:
                lines.append(f"- {a.la_year} codes: {'; '.join(a.codes)}.")
    if ident.sex == "Male":
        lines.append(
            "- Buck: mammary linears (FA, RH, MS, UD, TP, TD, TL, RUSV) often blank / unscored."
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def upsert_reference_scores(path: Path, records: list[GoatRecord], dry_run: bool) -> None:
    text = path.read_text() if path.exists() else ""
    if not text.strip():
        text = (
            "# LA Reference Scores\n"
            "**Herd breeding reference animals**\n"
            f"**Last updated:** {date.today().isoformat()}\n\n"
            "Full Linear Appraisal records. One row per evaluation.\n\n"
            "---\n\n"
        )

    # bump last updated
    text = re.sub(
        r"(\*\*Last updated:\*\*\s*)\d{4}-\d{2}-\d{2}",
        rf"\g<1>{date.today().isoformat()}",
        text,
        count=1,
    )

    for rec in records:
        if not rec.appraisals and "subject" in rec.role.lower():
            continue
        pd = adga_to_pd(rec.identity.reg)
        block = format_animal_markdown(rec)
        # Match existing section by (PDxxxxxxx) in heading
        pat = re.compile(
            rf"^## .+?\({re.escape(pd)}\)\s*\n[\s\S]*?(?=^## |\Z)",
            re.M,
        )
        if pat.search(text):
            text = pat.sub(block, text, count=1)
            print(f"Updated section {pd}", flush=True)
        else:
            # insert before final appendix note if present
            marker = "*(Additional reference animals will be appended below as data is provided.)*"
            if marker in text:
                text = text.replace(marker, block + marker)
            else:
                if not text.endswith("\n"):
                    text += "\n"
                text += block
            print(f"Appended section {pd}", flush=True)

    if dry_run:
        print("\n--- DRY RUN (first 4000 chars of would-be file tail) ---\n")
        print(text[-4000:])
        return

    path.write_text(text)
    print(f"Wrote {path}", flush=True)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "animal",
        help="ADGA reg (D002277726 / PD2277726) or GoatDetail URL",
    )
    ap.add_argument(
        "--half-sibs",
        action="store_true",
        help="Also fetch maternal/paternal half-siblings with type evals",
    )
    ap.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY_S,
        help=f"Seconds between HTTP requests (default {DEFAULT_DELAY_S})",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and print actions; do not write LA_REFERENCE_SCORES.md",
    )
    ap.add_argument(
        "--skip-subject-linear",
        action="store_true",
        help="Do not request Linear History for the subject animal itself",
    )
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        default=REF_SCORES,
        help="Markdown file to upsert (default LA_REFERENCE_SCORES.md)",
    )
    args = ap.parse_args(argv)

    try:
        reg = normalize_reg(args.animal)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2

    client = PoliteClient(delay_s=args.delay)
    print(
        f"Fetching family for {reg} from ADGA Genetics "
        f"(delay={args.delay}s, half_sibs={args.half_sibs})",
        flush=True,
    )
    print(f"User-Agent: {USER_AGENT}", flush=True)

    try:
        records = collect_family(
            client,
            reg,
            include_half_sibs=args.half_sibs,
            include_subject_linear=not args.skip_subject_linear,
        )
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    with_scores = [r for r in records if r.appraisals]
    print(
        f"\nDone: {client.hits} HTTP requests; "
        f"{len(with_scores)}/{len(records)} animals with linear rows",
        flush=True,
    )
    upsert_reference_scores(args.output, records, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
