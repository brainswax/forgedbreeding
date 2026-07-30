#!/usr/bin/env python3
"""
Build a static HTML site from reports/ and profiles/ for GitHub Pages (or local preview).

Usage:
  pip install -r requirements-pages.txt
  python3 scripts/publish_pages.py
  python3 scripts/publish_pages.py --out /tmp/forged-site --base-url /
  open _site/index.html
"""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "_site"

try:
    import markdown as md_lib
except ImportError as e:
    raise SystemExit(
        "Missing dependency: markdown\n"
        "  pip install -r requirements-pages.txt\n"
        f"({e})"
    ) from e


MD = md_lib.Markdown(
    extensions=[
        "tables",
        "fenced_code",
        "smarty",
        "sane_lists",
        "toc",
    ],
    extension_configs={"toc": {"permalink": False}},
)

REPORT_GROUPS = [
    ("Herd", re.compile(r"^herd-(?!breeding)")),
    ("Herd breeding", re.compile(r"^herd-breeding-")),
    ("Individual", re.compile(r"^individual-")),
    ("Breeding", re.compile(r"^breeding-")),
    ("Planning", re.compile(r"^planning-")),
]


def title_from_md(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def slug_label(stem: str) -> str:
    return stem.replace("-", " ").replace("_", " ").strip().title()


def rewrite_md_links(html: str, *, base: str) -> str:
    """Point in-repo .md links at generated .html pages when possible."""

    def repl(m: re.Match) -> str:
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        if href.endswith(".md"):
            name = Path(href).name[:-3] + ".html"
            parts = Path(href).parts
            if "profiles" in parts or href.startswith("../profiles") or href.startswith("profiles/"):
                return f'href="{base}profiles/{name}"'
            if "reports" in parts or href.startswith("../reports") or href.startswith("reports/"):
                return f'href="{base}reports/{name}"'
            # bare filename in same section — leave as sibling html
            return f'href="{name}"'
        return m.group(0)

    return re.sub(r'href="([^"]+)"', repl, html)


def render_markdown(text: str, *, base: str) -> str:
    MD.reset()
    return rewrite_md_links(MD.convert(text), base=base)


def page_shell(
    *,
    title: str,
    body: str,
    base: str,
    crumb: str | None = None,
    description: str = "Forged Farm Nigerian Dwarf LA breeding reports and profiles.",
) -> str:
    crumb_html = ""
    if crumb:
        crumb_html = f'<p class="crumb"><a href="{base}index.html">Home</a> · {crumb}</p>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_esc(title)} · Forged Farm</title>
  <meta name="description" content="{_esc(description)}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{base}assets/site.css" />
</head>
<body>
  <div class="atmosphere" aria-hidden="true"></div>
  <header class="site-header">
    <a class="brand" href="{base}index.html">
      <span class="brand-mark">Forged Farm</span>
      <span class="brand-sub">Breeding decisions</span>
    </a>
    <nav class="site-nav">
      <a href="{base}index.html#reports">Reports</a>
      <a href="{base}index.html#profiles">Profiles</a>
    </nav>
  </header>
  <main class="sheet">
    {crumb_html}
    <article class="prose">
{body}
    </article>
  </main>
  <footer class="site-footer">
    <p>Forged Farm · Brian Denton · ADGA 1660541</p>
    <p class="muted">Generated {date.today().isoformat()} from repo markdown</p>
  </footer>
</body>
</html>
"""


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def collect_md(folder: Path) -> list[tuple[Path, str, str]]:
    """Return (path, stem, title) sorted by stem."""
    rows = []
    for path in sorted(folder.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        rows.append((path, path.stem, title_from_md(text, slug_label(path.stem))))
    return rows


def write_doc_pages(
    items: list[tuple[Path, str, str]],
    out_dir: Path,
    *,
    section: str,
    base_prefix: str,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for path, stem, title in items:
        text = path.read_text(encoding="utf-8")
        body = render_markdown(text, base=base_prefix)
        html = page_shell(
            title=title,
            body=body,
            base=base_prefix,
            crumb=f'{section} · <span>{_esc(stem)}</span>',
        )
        (out_dir / f"{stem}.html").write_text(html, encoding="utf-8")


def index_group_html(label: str, items: list[tuple[Path, str, str]], href_dir: str) -> str:
    if not items:
        return ""
    lis = "\n".join(
        f'      <li><a href="{href_dir}/{stem}.html"><span class="link-title">{_esc(title)}</span>'
        f'<span class="link-slug">{_esc(stem)}</span></a></li>'
        for _path, stem, title in items
    )
    return f"""
    <section class="index-block">
      <h2>{_esc(label)}</h2>
      <ul class="doc-list">
{lis}
      </ul>
    </section>
"""


def build_index(
    reports: list[tuple[Path, str, str]],
    profiles: list[tuple[Path, str, str]],
    *,
    base: str,
) -> str:
    grouped: dict[str, list] = {label: [] for label, _ in REPORT_GROUPS}
    other: list = []
    for item in reports:
        stem = item[1]
        placed = False
        for label, pat in REPORT_GROUPS:
            if pat.search(stem):
                grouped[label].append(item)
                placed = True
                break
        if not placed:
            other.append(item)

    blocks = ['<div id="reports">']
    for label, _ in REPORT_GROUPS:
        blocks.append(index_group_html(label, grouped[label], f"{base}reports"))
    if other:
        blocks.append(index_group_html("Other reports", other, f"{base}reports"))
    blocks.append("</div>")
    blocks.append('<div id="profiles">')
    blocks.append(index_group_html("Estimated profiles", profiles, f"{base}profiles"))
    blocks.append("</div>")

    body = f"""
    <header class="hero">
      <p class="eyebrow">Linear Appraisal breeding desk</p>
      <h1>Forged Farm</h1>
      <p class="lede">Published reports and estimated profiles for the current breeding roster — ranked by Breeding Impact Score where applicable.</p>
    </header>
    {"".join(blocks)}
"""
    return page_shell(
        title="Reports & profiles",
        body=body,
        base=base,
        description="Forged Farm published LA breeding reports and estimated animal profiles.",
    )


CSS = """\
:root {
  --ink: #1c2430;
  --muted: #5a6574;
  --paper: #f3f6f8;
  --sheet: rgba(255, 255, 255, 0.78);
  --line: rgba(28, 36, 48, 0.12);
  --accent: #3f6f5a;
  --accent-deep: #2a4d3d;
  --ember: #9a5b2f;
  --display: "Fraunces", "Palatino Linotype", Palatino, serif;
  --body: "Source Sans 3", "Segoe UI", sans-serif;
}

* { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  min-height: 100vh;
  color: var(--ink);
  font-family: var(--body);
  font-size: 1.05rem;
  line-height: 1.55;
  background: var(--paper);
}

.atmosphere {
  position: fixed;
  inset: 0;
  z-index: -1;
  background:
    radial-gradient(ellipse 80% 50% at 10% -10%, rgba(63, 111, 90, 0.18), transparent 55%),
    radial-gradient(ellipse 70% 45% at 100% 0%, rgba(154, 91, 47, 0.12), transparent 50%),
    linear-gradient(165deg, #e7eef2 0%, #f5f3ef 45%, #dde5ea 100%);
}

.site-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1.5rem;
  max-width: 52rem;
  margin: 0 auto;
  padding: 1.75rem 1.25rem 0.5rem;
}

.brand {
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.brand-mark {
  font-family: var(--display);
  font-weight: 700;
  font-size: 1.55rem;
  letter-spacing: -0.02em;
  line-height: 1.1;
}

.brand-sub {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--muted);
}

.site-nav {
  display: flex;
  gap: 1.25rem;
  font-size: 0.95rem;
}

.site-nav a {
  color: var(--accent-deep);
  text-decoration: none;
  border-bottom: 1px solid transparent;
}

.site-nav a:hover {
  border-bottom-color: var(--accent);
}

.sheet {
  max-width: 52rem;
  margin: 1rem auto 3rem;
  padding: 1.75rem 1.4rem 2.25rem;
  background: var(--sheet);
  border: 1px solid var(--line);
  backdrop-filter: blur(8px);
}

.crumb {
  margin: 0 0 1.25rem;
  font-size: 0.9rem;
  color: var(--muted);
}

.crumb a { color: var(--accent-deep); }

.hero {
  margin-bottom: 2.25rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--line);
}

.eyebrow {
  margin: 0 0 0.5rem;
  font-size: 0.78rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--ember);
}

.hero h1 {
  margin: 0;
  font-family: var(--display);
  font-size: clamp(2.4rem, 6vw, 3.4rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.05;
}

.lede {
  margin: 0.85rem 0 0;
  max-width: 36rem;
  font-size: 1.12rem;
  color: var(--muted);
}

.index-block {
  margin: 0 0 2rem;
}

.index-block h2 {
  margin: 0 0 0.75rem;
  font-family: var(--display);
  font-size: 1.45rem;
  font-weight: 600;
}

.doc-list {
  list-style: none;
  margin: 0;
  padding: 0;
  border-top: 1px solid var(--line);
}

.doc-list li {
  border-bottom: 1px solid var(--line);
}

.doc-list a {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  padding: 0.85rem 0.15rem;
  text-decoration: none;
  color: inherit;
}

.doc-list a:hover .link-title {
  color: var(--accent-deep);
}

.link-title {
  font-weight: 600;
}

.link-slug {
  font-size: 0.82rem;
  color: var(--muted);
  font-variant-numeric: tabular-nums;
}

.prose h1 {
  margin: 0 0 1rem;
  font-family: var(--display);
  font-size: clamp(1.8rem, 4vw, 2.35rem);
  line-height: 1.15;
  letter-spacing: -0.02em;
}

.prose h2 {
  margin: 2rem 0 0.75rem;
  font-family: var(--display);
  font-size: 1.35rem;
  font-weight: 600;
}

.prose h3 {
  margin: 1.5rem 0 0.5rem;
  font-size: 1.08rem;
}

.prose p, .prose ul, .prose ol {
  margin: 0 0 1rem;
}

.prose a { color: var(--accent-deep); }

.prose table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.88rem;
  margin: 0 0 1.25rem;
  display: block;
  overflow-x: auto;
}

.prose th, .prose td {
  border: 1px solid var(--line);
  padding: 0.4rem 0.55rem;
  text-align: left;
  vertical-align: top;
  white-space: nowrap;
}

.prose th {
  background: rgba(63, 111, 90, 0.08);
  font-weight: 600;
}

.prose tr:nth-child(even) td {
  background: rgba(28, 36, 48, 0.02);
}

.prose code {
  font-size: 0.92em;
  background: rgba(28, 36, 48, 0.06);
  padding: 0.1em 0.35em;
}

.prose strong { font-weight: 600; }

.site-footer {
  max-width: 52rem;
  margin: 0 auto 2.5rem;
  padding: 0 1.25rem;
  color: var(--muted);
  font-size: 0.88rem;
}

.site-footer p { margin: 0.2rem 0; }
.muted { opacity: 0.85; }

@media (max-width: 640px) {
  .site-header { flex-direction: column; align-items: flex-start; }
  .sheet { margin-top: 0.5rem; border-left: none; border-right: none; }
  .prose th, .prose td { white-space: normal; }
}
"""


def build(out: Path, base_url: str) -> None:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    assets = out / "assets"
    assets.mkdir()
    (assets / "site.css").write_text(CSS, encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")

    base = base_url if base_url.endswith("/") else base_url + "/"
    # Root-relative base for all pages (works for user site "/" or project "/repo/")
    asset_base = base

    reports = collect_md(ROOT / "reports")
    profiles = collect_md(ROOT / "profiles")

    write_doc_pages(
        reports,
        out / "reports",
        section="Reports",
        base_prefix=asset_base,
    )
    write_doc_pages(
        profiles,
        out / "profiles",
        section="Profiles",
        base_prefix=asset_base,
    )

    index_html = build_index(reports, profiles, base=asset_base)
    (out / "index.html").write_text(index_html, encoding="utf-8")

    print(f"Built {len(reports)} reports + {len(profiles)} profiles → {out}")
    print(f"Base URL: {asset_base}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output directory (default {DEFAULT_OUT.name}/)",
    )
    ap.add_argument(
        "--base-url",
        default="/",
        help="Base URL path for GitHub project Pages (e.g. /forgedbreeding/)",
    )
    args = ap.parse_args(argv)
    build(args.out, args.base_url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
