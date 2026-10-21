#!/usr/bin/env python3
"""Build the page index for the Jeep manuals in this repository.

Outputs:
  INDEX.md              overview, how to use, manual list, service-manual group map
  index/<manual>.md     full bookmark outline + every figure caption, with PDF page numbers
  index/pages.tsv       one row per page across all manuals (grep-friendly)

Run from the repo root:  python3 tools/build_index.py
Requires: pip install pymupdf
"""
import os
import re
import sys

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "index")

# file -> (slug, title, year, kind)
MANUALS = [
    ("2006 TJ Service Manual .pdf", "2006-service-manual", "2006 TJ/LJ Factory Service Manual", "2006", "fsm"),
    ("2006-TJ-Powertrain.pdf", "2006-powertrain-diagnostics", "2006 TJ Powertrain Diagnostic Procedures", "2006", "diag"),
    ("2006-TJ-Body.pdf", "2006-body-diagnostics", "2006 TJ Body Diagnostic Procedures", "2006", "diag"),
    ("2006-TJ-Chassis.pdf", "2006-chassis-diagnostics", "2006 TJ Chassis Diagnostic Procedures (ABS, axle lock)", "2006", "diag"),
    ("2006 TJ Parts List.pdf", "2006-parts-list", "2006 TJ Parts List", "2006", "parts"),
    ("2005 TJ Service Manual.pdf", "2005-service-manual", "2005 TJ/LJ Factory Service Manual", "2005", "fsm"),
    ("2005 Jeep Wrangler TJ Powertrain Manual.PDF", "2005-powertrain-diagnostics", "2005 TJ Powertrain Diagnostic Procedures", "2005", "diag"),
    ("2005 Jeep Wrangler TJ Body Manual.PDF", "2005-body-diagnostics", "2005 TJ Body Diagnostic Procedures", "2005", "diag"),
    ("2005 Jeep Wrangler TJ Chassis Manual.PDF", "2005-chassis-diagnostics", "2005 TJ Chassis Diagnostic Procedures (ABS, axle lock)", "2005", "diag"),
    ("2005 TJ Parts List.pdf", "2005-parts-list", "2005 TJ Parts List", "2005", "parts"),
    ("42RLE-AUTOMATIC-TRANSMISSION.pdf", "42rle-automatic-transmission", "42RLE Automatic Transmission (FSM excerpt)", "both", "excerpt"),
    ("NSG370-MANUAL-TRANSMISSION.pdf", "nsg370-manual-transmission", "NSG370 6-Speed Manual Transmission (FSM excerpt)", "both", "excerpt"),
]
# The 2005 FSM is also stored split in two halves; they are page-for-page copies of the full file.
SPLITS = [
    ("2005_TJ_FSM_Part1_p1-799_Chassis-Electrical-Wiring.pdf", "2005 TJ Service Manual.pdf", 0),
    ("2005_TJ_FSM_Part2_p800-1678_Engine-Driveline-Body.pdf", "2005 TJ Service Manual.pdf", 799),
]

PAGE_NO = re.compile(r"^(\d{1,2}[a-zA-Z]{0,2}|[a-zA-Z]{1,3}|\d{1,2}[a-zA-Z]{0,2}\s*[A-Z]?)\s+-\s+(\d{1,4})$")
FIG = re.compile(r"^Fig\.\s*(\d+)\s+(.*)$")
CALLOUT = re.compile(r"^\d+\s+-\s+")
SKIP_TOC = {"MAIN WELCOME PAGE", "INSTRUCTIONS", "FOREWORD", "COMMENTS"}


def clean(s):
    s = s.replace(" ", " ").replace(" ", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s.replace("\t", " ").replace("|", "/")


def page_meta(text):
    """Return (printed page label, running header) from a page's text."""
    lines = [clean(l) for l in text.splitlines() if clean(l)]
    if not lines:
        return "", ""
    tail = lines[-6:] + lines[:4]
    label = ""
    for l in tail:
        if PAGE_NO.match(l):
            label = l
            break
    if not label:  # diagnostic manuals and parts lists print a bare page number
        for l in reversed(lines[-4:]):
            if re.fullmatch(r"\d{1,3}|[ivx]{1,4}", l):
                label = l
                break
    header = ""
    for l in lines[-6:]:
        if l == label or l in ("TJ", "LJ", "TJ/LJ") or "(Continued)" in l:
            continue
        if l.isupper() and 3 <= len(l) <= 60 and not CALLOUT.match(l) and not l.startswith("FIG"):
            header = l
    return label, header


def figures(text):
    lines = [clean(l) for l in text.splitlines()]
    out = []
    for i, l in enumerate(lines):
        m = FIG.match(l)
        if not m:
            continue
        num, cap = m.group(1), m.group(2)
        # captions sometimes wrap onto one or two more lines
        j = i + 1
        while j < len(lines) and j <= i + 2 and cap.endswith(("-", "/", ",", "&")):
            nxt = lines[j]
            if not nxt or FIG.match(nxt) or CALLOUT.match(nxt):
                break
            cap = (cap + " " + nxt).strip()
            j += 1
        cap = cap.rstrip(" -")
        if cap and not re.match(r"^\(|^\d", cap):  # skip in-text references like "(Fig. 4)."
            out.append((num, cap))
    return out


def section_paths(doc):
    """Map 1-based page -> list of bookmark titles (outermost first) in effect on that page."""
    toc = [e for e in doc.get_toc() if e[2] >= 1 and clean(e[1]) not in SKIP_TOC]
    paths = {}
    stack = []
    k = 0
    for pg in range(1, len(doc) + 1):
        while k < len(toc) and toc[k][2] <= pg:
            lvl, title = toc[k][0], clean(toc[k][1])
            stack = [s for s in stack if s[0] < lvl] + [(lvl, title)]
            k += 1
        paths[pg] = [t for _, t in stack]
    return toc, paths


def short_path(path, kind):
    # drop the manual-level root bookmark ("TJ Service Manual", "TJ Chassis", ...)
    p = path[1:] if path and path[0].startswith(("TJ ", "2005", "2006")) else path
    if kind == "fsm":
        # drop generic leaf headings so the path stays readable
        while len(p) > 2 and p[-1] in ("DESCRIPTION", "OPERATION"):
            p = p[:-1]
    return " > ".join(p[:5])


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    summary = []
    group_maps = {}
    for fname, slug, title, year, kind in MANUALS:
        path = os.path.join(ROOT, fname)
        doc = pymupdf.open(path)
        toc, paths = section_paths(doc)
        figs_all = []
        for i in range(len(doc)):
            pg = i + 1
            text = doc[i].get_text()
            label, header = page_meta(text)
            figs = figures(text)
            for n, cap in figs:
                figs_all.append((pg, label, header, n, cap))
            section = short_path(paths.get(pg, []), kind) if toc else header
            rows.append([
                fname, str(pg), label, header, section,
                "; ".join(f"Fig. {n} {c}" for n, c in figs),
            ])

        # per-manual markdown
        md = [f"# {title}", "", f"File: `{fname}` · {len(doc)} PDF pages", ""]
        md.append("Page numbers below are **PDF page numbers** (what `pdftoppm -f N -l N` expects), "
                  "not the printed page labels.")
        if fname == "2005 TJ Service Manual.pdf":
            md.append("")
            md.append("Also stored split in two: PDF pages 1–799 = `2005_TJ_FSM_Part1_...pdf` (same page numbers); "
                      "PDF pages 800–1678 = `2005_TJ_FSM_Part2_...pdf` (subtract 799).")
        md += ["", "## Contents (from the PDF bookmarks)", ""]
        if toc:
            for lvl, t, pg in toc:
                t = clean(t)
                if lvl == 1 and t.startswith("TJ "):
                    continue
                indent = "  " * max(0, lvl - 2)
                md.append(f"{indent}- {t} — p.{pg}")
        else:
            md.append("_This PDF has no bookmarks. Use the running headers in `pages.tsv` and the figure list below._")
            seen = None
            for r in rows:
                if r[0] == fname and r[3] and r[3] != seen:
                    md.append(f"- {r[3]} — p.{r[1]}")
                    seen = r[3]
        md += ["", "## Figures", ""]
        if figs_all:
            md.append("| PDF page | Printed page | Section header | Figure |")
            md.append("|---:|---|---|---|")
            for pg, label, header, n, cap in figs_all:
                md.append(f"| {pg} | {label} | {header} | Fig. {n} {cap} |")
        else:
            md.append("_No numbered figure captions in this manual (diagrams are unlabeled or in tables)._")
        with open(os.path.join(OUT, f"{slug}.md"), "w") as f:
            f.write("\n".join(md) + "\n")

        if kind == "fsm":
            groups = []
            lvl2 = [(clean(t), pg) for lvl, t, pg in toc if lvl == 2]
            for idx, (t, pg) in enumerate(lvl2):
                end = (lvl2[idx + 1][1] - 1) if idx + 1 < len(lvl2) else len(doc)
                groups.append((t, pg, max(pg, end)))
            group_maps[year] = groups
        summary.append((title, fname, slug, len(doc), len(toc), len(figs_all)))
        doc.close()

    with open(os.path.join(OUT, "pages.tsv"), "w") as f:
        f.write("file\tpdf_page\tprinted_page\theader\tsection\tfigures\n")
        for r in rows:
            f.write("\t".join(r) + "\n")

    # top-level INDEX.md
    md = ["# Manual index", "",
          "Map of every manual in this repository: what's in it and on which PDF page.", "",
          "## How to use", "",
          "1. Find the topic: `grep -i \"crankshaft oil seal\" index/pages.tsv` "
          "(columns: file, PDF page, printed page, running header, section path, figure captions, page_pdf).",
          "2. Or browse a manual's outline and figure list in `index/<manual>.md`.",
          "3. Show the page: `tools/page.sh <page_pdf>` fetches just that page (~30 KB) and renders a PNG. "
          "Every page is stored on its own as `pages/<manual>/pNNNN.pdf` + `.txt` (NNNN = PDF page), "
          "so you never need to download a whole manual. See README.md for the fast clone.", "",
          "Use the 2006 manuals by default; check the 2005 manuals to cross-check.",
          "The service manuals cover both the 2.4L and the 4.0L engine; check the running header "
          "(e.g. `ENGINE 4.0L`) before using a spec.", "",
          "## Manuals", "",
          "| Manual | File | PDF pages | Bookmarks | Figures | Index |",
          "|---|---|---:|---:|---:|---|"]
    for title, fname, slug, n, nt, nf in summary:
        md.append(f"| {title} | `{fname}` | {n} | {nt} | {nf} | [index/{slug}.md](index/{slug}.md) |")
    md += ["", "The 2005 service manual is also stored as two halves "
           "(`2005_TJ_FSM_Part1_p1-799...` and `2005_TJ_FSM_Part2_p800-1678...`). "
           "Part 2 page = full-manual page − 799.", ""]
    for year in ("2006", "2005"):
        if year not in group_maps:
            continue
        md += [f"## {year} service manual: groups", "", "| Group | PDF pages |", "|---|---|"]
        for t, a, b in group_maps[year]:
            md.append(f"| {t} | {a}–{b} |")
        md.append("")
    with open(os.path.join(ROOT, "INDEX.md"), "w") as f:
        f.write("\n".join(md))
    print(f"{len(rows)} pages indexed across {len(summary)} manuals")


if __name__ == "__main__":
    sys.exit(main())
