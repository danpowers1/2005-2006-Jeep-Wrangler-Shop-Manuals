# 2005–2006 Jeep Wrangler TJ Shop Manuals

Factory service manuals, diagnostic manuals, and parts lists for the 2005 and 2006 Jeep Wrangler TJ/LJ.

- 2006 manuals are the default reference; 2005 manuals are kept for cross-checking.
- `2006 TJ Service Manual .pdf` / `2005 TJ Service Manual.pdf` are the full factory service manuals.
- The `*_FSM_Part1/Part2` files are the 2005 service manual split into two halves.
- Body / Chassis / Powertrain PDFs are the factory diagnostic procedure manuals.

## Finding things fast

See **[INDEX.md](INDEX.md)**: a page map of every manual (sections, figures, PDF page numbers).
- `index/pages.tsv`: one row per page (file, PDF page, printed page, header, section, figures). Grep it.
- `index/<manual>.md`: full outline and figure list for each manual.
- Rebuild after adding or replacing a manual: `pip install pymupdf && python3 tools/build_index.py`
