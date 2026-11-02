#!/usr/bin/env bash
# Copy the evaluation pages from tables/ into the eval/ folder of the wip repository
# (https://github.com/hulln/wip, published at https://wip.nhull.eu/eval/).
#
#   scripts/publish_to_wip.sh ~/Projekti/wip
#   cd ~/Projekti/wip && git add -A eval && git commit -m "Update eval" && git push
#
# Only files that git tracks, or untracked files that are not ignored, are copied.
# Ignored files, such as the unconfirmed Dutch spoken data in
# tables/am_benchmark_v2/data/{examples,layers}, never leave this repository.
# Not copied: README files, and tables/index.html (an old local start page).
# eval/ becomes an exact copy, so files deleted here are deleted there too.
set -euo pipefail

wip="${1:?usage: scripts/publish_to_wip.sh <path to the wip repository>}"
repo="$(cd "$(dirname "$0")/.." && pwd)"
[ -d "$wip/.git" ] || { echo "Not a git repository: $wip" >&2; exit 1; }

stage="$(mktemp -d)"
trap 'rm -rf -- "${stage:?}"' EXIT

cd "$repo"
git ls-files -z --cached --others --exclude-standard -- tables \
  | grep -z -v -E '(^tables/index\.html$|(^|/)README\.md$)' \
  | rsync -a --from0 --files-from=- ./ "$stage/"

mkdir -p "$wip/eval"
rsync -a --delete "$stage/tables/" "$wip/eval/"
echo "Copied $(find "$wip/eval" -type f | wc -l) files into $wip/eval"
git -C "$wip" status --short -- eval | head -20
