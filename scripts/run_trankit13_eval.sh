#!/usr/bin/env bash
# Additional evaluation on the Trankit 1.3 model (CLARIN 11356/2201, which adds
# non-standard spoken Slovenian to SST training data), run the SAME way as the
# previous full runs: aligned mode, Trankit vs CLASSLA, on both the standard SSJ
# and the spoken/non-standard SST test sets.
#
# Designed to run inside the Docker container (see docker/README.md), but works
# on any host with the project venv active.
#
# Tunables via environment:
#   GPU=1            -> pass --trankit-gpu (only if preflight reports a GPU)
#   STAMP=...        -> run-stamp token (default: <date>-tk13, distinguishes 1.3 from the 1.2 runs)
#   MODEL_URL/MD5    -> override the CLARIN model (defaults to 11356/2201 below)
#   CACHE_DIR        -> fresh Trankit cache (default cache/trankit-11356-2201; do NOT reuse cache/trankit)
set -euo pipefail
cd "$(dirname "$0")/.."

MODEL_URL="${MODEL_URL:-https://www.clarin.si/repository/xmlui/bitstream/handle/11356/2201/trankit-sl-ssj%2bsststand%2bsstpog.zip}"
MODEL_MD5="${MODEL_MD5:-ff1f3b86a4996fd5944db14725c602d8}"
CACHE_DIR="${CACHE_DIR:-cache/trankit-11356-2201}"
STAMP="${STAMP:-$(date +%Y%m%d-%H%M)-tk13}"

GPU_FLAG=()
if [[ "${GPU:-0}" == "1" ]]; then
    GPU_FLAG=(--trankit-gpu)
fi

trankit_args=(
    --modes aligned
    --run-stamp "$STAMP"
    --trankit-model-source clarin-11356-1997
    --trankit-clarin-url "$MODEL_URL"
    --trankit-clarin-md5 "$MODEL_MD5"
    --trankit-cache-dir "$CACHE_DIR"
    --download-classla-models
    "${GPU_FLAG[@]}"
)

echo "### Trankit 1.3 eval | stamp=$STAMP | cache=$CACHE_DIR | gpu=${GPU:-0}"

echo ""
echo "=== [1/2] SSJ (standard) ==="
python scripts/run_pipeline.py \
    --gold data/gold/sl_ssj-ud-test.conllu \
    --classla-type default \
    "${trankit_args[@]}"

echo ""
echo "=== [2/2] SST (spoken / non-standard) ==="
python scripts/run_pipeline.py \
    --gold data/gold/sl_sst-ud-test.conllu \
    --classla-type spoken \
    "${trankit_args[@]}"

echo ""
echo "### Done. Predictions under predictions/output/ (stamp $STAMP), results under results/output/."
