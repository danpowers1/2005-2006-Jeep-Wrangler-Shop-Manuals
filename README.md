# 2005–2006 Jeep Wrangler TJ Shop Manuals

Factory service manuals, diagnostic manuals, and parts lists for the 2005 and 2006 Jeep Wrangler TJ/LJ.

- 2006 manuals are the default reference; 2005 manuals are kept for cross-checking.
- `2006 TJ Service Manual .pdf` / `2005 TJ Service Manual.pdf` are the full factory service manuals.
- The `*_FSM_Part1/Part2` files are the 2005 service manual split into two halves.
- Body / Chassis / Powertrain PDFs are the factory diagnostic procedure manuals.

## Fast lookup (no full-manual download)

Every page of every manual is also stored on its own:
`pages/<manual>/pNNNN.pdf` (single page, ~30 KB) and `pages/<manual>/pNNNN.txt` (its text), where NNNN is the PDF page number.

```bash
# 1. Index only: about 10 seconds, no PDFs
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --filter=blob:none --no-checkout \
  https://github.com/danpowers1/2005-2006-jeep-wrangler-shop-manuals manuals
cd manuals && git checkout HEAD -- README.md INDEX.md index tools

# 2. Find the page (last column, page_pdf, is the per-page file)
grep -i "stabilizer bar" index/pages.tsv

# 3. Fetch + render just those pages
tools/page.sh pages/2006-service-manual/p0046.pdf pages/2006-parts-list/p0025.pdf
```

Full-text search when the index misses: `git checkout HEAD -- pages/2006-service-manual` pulls only that manual's pages, then `grep -il "<words>" pages/2006-service-manual/*.txt`.

## Finding things

See **[INDEX.md](INDEX.md)**: a page map of every manual (sections, figures, PDF page numbers).
- `index/pages.tsv`: one row per page (file, PDF page, printed page, header, section, figures, page_pdf). Grep it.
- `index/<manual>.md`: full outline and figure list for each manual.
- Rebuild after adding or replacing a manual: `pip install pymupdf && python3 tools/build_index.py && python3 tools/split_pages.py`
