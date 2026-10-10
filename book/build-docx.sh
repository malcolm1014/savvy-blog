#!/usr/bin/env bash
# Build Word (.docx) exports of A Hacker's Guide to Survive from the canonical HTML.
# Usage:  ./book/build-docx.sh            # build every chapter + a combined book
#         ./book/build-docx.sh ch01-...   # build one chapter directory
#
# Requires: pandoc (tested with 3.1.x). HTML is the source of truth; .docx files
# are build artifacts and are NOT committed to the repo (see .gitignore).
set -euo pipefail

# Force UTF-8 so pandoc never mangles em-dashes / curly quotes regardless of host locale.
export LANG=C.UTF-8 LC_ALL=C.UTF-8

BOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="${BOOK_DIR}/docx"
mkdir -p "${OUT_DIR}"

TITLE="A Hacker's Guide to Survive"
AUTHOR="Malcolm R. Smith — Savvy Security LLC"

build_one () {
  local dir="$1"
  local name
  name="$(basename "${dir}")"
  local src="${dir}/index.html"
  [ -f "${src}" ] || { echo "skip: no index.html in ${dir}"; return; }
  echo "building ${name}.docx"
  pandoc "${src}" \
    --from html --to docx \
    --metadata title="${TITLE}" \
    --metadata author="${AUTHOR}" \
    -o "${OUT_DIR}/${name}.docx"
}

if [ "$#" -ge 1 ]; then
  build_one "${BOOK_DIR}/$1"
  exit 0
fi

# All chapters
for d in "${BOOK_DIR}"/ch*/; do
  [ -d "${d}" ] && build_one "${d}"
done

# Appendices (separate from the ch* naming, built explicitly)
[ -d "${BOOK_DIR}/appendices" ] && build_one "${BOOK_DIR}/appendices"

# Combined full-book document (chapters in order, appendices last)
mapfile -t CHAPTERS < <(find "${BOOK_DIR}" -maxdepth 2 -name index.html -path '*/ch*' | sort)
[ -f "${BOOK_DIR}/appendices/index.html" ] && CHAPTERS+=("${BOOK_DIR}/appendices/index.html")
if [ "${#CHAPTERS[@]}" -gt 0 ]; then
  echo "building A-Hackers-Guide-to-Survive-full.docx"
  pandoc "${CHAPTERS[@]}" \
    --from html --to docx \
    --metadata title="${TITLE}" \
    --metadata author="${AUTHOR}" \
    --toc --toc-depth=2 \
    -o "${OUT_DIR}/A-Hackers-Guide-to-Survive-full.docx"
fi

echo "done -> ${OUT_DIR}"
