#!/usr/bin/env python3
"""Split every manual into one small PDF + one text file per page.

  pages/<slug>/p0046.pdf   single page, vector (render with pdftoppm)
  pages/<slug>/p0046.txt   that page's text (pdftotext -layout)

Also adds a `page_pdf` column to index/pages.tsv pointing at each page's file,
so a chat can fetch one ~30 KB page instead of a 50 MB manual.

Needs qpdf and poppler-utils (pdftotext). Run from the repo root:
  python3 tools/split_pages.py
Re-run after tools/build_index.py (which rewrites pages.tsv).
"""
import csv, glob, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from build_index import MANUALS  # (file, slug, title, year, kind)

PAGES = os.path.join(ROOT, "pages")


def split(fname, slug):
    src = os.path.join(ROOT, fname)
    out = os.path.join(PAGES, slug)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    subprocess.run(["qpdf", "--split-pages", src, os.path.join(out, "tmp-%d.pdf")],
                   check=True, stderr=subprocess.DEVNULL)
    n = 0
    for p in glob.glob(os.path.join(out, "tmp-*.pdf")):
        num = int(os.path.basename(p)[4:-4])
        dst = os.path.join(out, f"p{num:04d}.pdf")
        os.rename(p, dst)
        subprocess.run(["pdftotext", "-layout", dst, dst[:-4] + ".txt"], check=True)
        n += 1
    return n


def main():
    slug_of = {}
    for fname, slug, *_ in MANUALS:
        n = split(fname, slug)
        slug_of[fname] = slug
        print(f"{slug}: {n} pages")

    tsv = os.path.join(ROOT, "index", "pages.tsv")
    with open(tsv, newline="") as f:
        rows = list(csv.reader(f, delimiter="\t"))
    head = rows[0]
    if "page_pdf" in head:
        col = head.index("page_pdf")
    else:
        head.append("page_pdf")
        col = None
    for r in rows[1:]:
        slug = slug_of.get(r[0])
        path = f"pages/{slug}/p{int(r[1]):04d}.pdf" if slug else ""
        if col is None:
            r.append(path)
        else:
            r[col] = path
    with open(tsv, "w", newline="") as f:
        csv.writer(f, delimiter="\t", lineterminator="\n").writerows(rows)


if __name__ == "__main__":
    main()
