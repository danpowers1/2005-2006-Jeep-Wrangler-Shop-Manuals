#!/usr/bin/env bash
# Fetch and render individual manual pages without downloading whole manuals.
#
# One-time per chat (about 10 s, index only, no PDFs):
#   GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --filter=blob:none --no-checkout \
#     https://github.com/danpowers1/2005-2006-jeep-wrangler-shop-manuals manuals
#   cd manuals && git checkout HEAD -- README.md INDEX.md index tools
#
# Then, from the repo root:
#   grep -i "stabilizer bar" index/pages.tsv          # last column = page_pdf
#   tools/page.sh pages/2006-service-manual/p0046.pdf [more pages...]
#
# For each page this pulls the ~30 KB PDF and its .txt, renders a 150 dpi PNG
# next to them, and prints the PNG and TXT paths.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
DPI="${DPI:-150}"
[ $# -gt 0 ] || { sed -n '2,15p' "$0"; exit 1; }
paths=()
for p in "$@"; do paths+=("$p" "${p%.pdf}.txt"); done
git checkout HEAD -- "${paths[@]}"
for p in "$@"; do
  out="${p%.pdf}"
  pdftoppm -r "$DPI" -png -singlefile "$p" "$out"
  echo "$out.png"
  echo "${p%.pdf}.txt"
done
