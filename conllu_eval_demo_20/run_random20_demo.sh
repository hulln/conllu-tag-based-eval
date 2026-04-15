#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
DEMO_DIR="$SCRIPT_DIR"
PYTHON="$ROOT_DIR/.venv/bin/python"
MODE="${1:-slice-existing}"

DATA_DIR="$DEMO_DIR/data"
PRED_DIR="$DEMO_DIR/predictions"
RESULTS_DIR="$DEMO_DIR/results"
DIAG_DIR="$DEMO_DIR/diagnostics"
TABLES_DIR="$DEMO_DIR/tables"

FULL_GOLD="$ROOT_DIR/data/gold/sl_ssj-ud-test.conllu"
FULL_CLASSLA_PRED="$ROOT_DIR/predictions/output/20260414-1819_sl-ssj-ud-test_full_classla_aligned_predicted.conllu"
FULL_TRANKIT_PRED="$ROOT_DIR/predictions/output/20260414-1819_sl-ssj-ud-test_full_trankit_aligned_predicted.conllu"

GOLD="$DATA_DIR/random20.gold.conllu"
SENT_IDS="$DATA_DIR/random20.sent_ids.txt"
CLASSLA_PRED="$PRED_DIR/classla_random20_aligned.conllu"
TRANKIT_PRED="$PRED_DIR/trankit_random20_aligned.conllu"

CLASSLA_EVAL="$RESULTS_DIR/classla_eval.txt"
TRANKIT_EVAL="$RESULTS_DIR/trankit_eval.txt"
CLASSLA_TAGGED="$DIAG_DIR/classla_eval_tagged.txt"
TRANKIT_TAGGED="$DIAG_DIR/trankit_eval_tagged.txt"
LOG="$RESULTS_DIR/run_random20_demo.log"

mkdir -p "$PRED_DIR" "$RESULTS_DIR" "$DIAG_DIR" "$TABLES_DIR"
: > "$LOG"

log() {
  printf '\n%s\n' "$*" | tee -a "$LOG"
}

run() {
  log "COMMAND: $*"
  "$@" 2>&1 | tee -a "$LOG"
}

run_save() {
  local out_file="$1"
  shift
  log "COMMAND: $*"
  "$@" 2>&1 | tee "$out_file" | tee -a "$LOG"
}

cd "$ROOT_DIR"

log "DEMO FOLDER"
log "$DEMO_DIR"
log "MODE"
log "$MODE"

log "STEP 1: The 20 selected sentence IDs"
nl -ba "$SENT_IDS" | tee -a "$LOG"

log "STEP 2: The first full gold example"
awk 'BEGIN { RS=""; ORS="\n\n" } NR == 1 { print; exit }' "$GOLD" | tee -a "$LOG"

if [[ "$MODE" == "live" ]]; then
  log "STEP 3: Run CLASSLA live on the 20 examples, forced to use the gold token boundaries"
  run "$PYTHON" scripts/predict_classla.py \
    --mode aligned \
    --aligned-gold "$GOLD" \
    --output "$CLASSLA_PRED" \
    --progress-every 1

  log "STEP 4: Run Trankit live on the 20 examples, forced to use the gold token boundaries"
  run "$PYTHON" scripts/predict_trankit.py \
    --mode aligned \
    --model-source clarin-11356-1997 \
    --cache-dir cache/trankit \
    --aligned-gold "$GOLD" \
    --output "$TRANKIT_PRED" \
    --progress-every 1
else
  log "STEP 3: Extract the same 20 examples from the already-created full-run gold/prediction files"
  run "$PYTHON" "$DEMO_DIR/extract_existing_predictions.py" \
    --sent-ids "$SENT_IDS" \
    --gold-source "$FULL_GOLD" \
    --classla-source "$FULL_CLASSLA_PRED" \
    --trankit-source "$FULL_TRANKIT_PRED" \
    --gold-out "$GOLD" \
    --classla-out "$CLASSLA_PRED" \
    --trankit-out "$TRANKIT_PRED"

  log "STEP 4: Prediction files are now local to the demo folder"
  ls -lh "$CLASSLA_PRED" "$TRANKIT_PRED" | tee -a "$LOG"
fi

log "STEP 5: Human-readable alignment check before trusting metrics"
run_save "$DIAG_DIR/alignment_check.txt" "$PYTHON" "$DEMO_DIR/verify_alignment_and_example.py" \
  --gold "$GOLD" \
  --classla "$CLASSLA_PRED" \
  --trankit "$TRANKIT_PRED"

log "STEP 6: Official eval output for CLASSLA"
run_save "$CLASSLA_EVAL" "$PYTHON" scripts/conll18_ud_eval_tag-based.py \
  -v "$GOLD" "$CLASSLA_PRED"

log "STEP 7: Official eval output for Trankit"
run_save "$TRANKIT_EVAL" "$PYTHON" scripts/conll18_ud_eval_tag-based.py \
  -v "$GOLD" "$TRANKIT_PRED"

log "STEP 8: Official eval output with per-tag breakdowns for CLASSLA"
run_save "$CLASSLA_TAGGED" "$PYTHON" scripts/conll18_ud_eval_tag-based.py \
  -v --upos ".*" --xpos ".*" --uas ".*" --las ".*" "$GOLD" "$CLASSLA_PRED"

log "STEP 9: Official eval output with per-tag breakdowns for Trankit"
run_save "$TRANKIT_TAGGED" "$PYTHON" scripts/conll18_ud_eval_tag-based.py \
  -v --upos ".*" --xpos ".*" --uas ".*" --las ".*" "$GOLD" "$TRANKIT_PRED"

log "STEP 10: Build Markdown error reports"
run "$PYTHON" scripts/analyze_errors.py \
  "$GOLD" "$CLASSLA_PRED" "$DIAG_DIR/classla_errors.md" \
  --model-name "CLASSLA random20" --top-n 20

run "$PYTHON" scripts/analyze_errors.py \
  "$GOLD" "$TRANKIT_PRED" "$DIAG_DIR/trankit_errors.md" \
  --model-name "Trankit random20" --top-n 20

run "$PYTHON" scripts/compare_models.py \
  "$GOLD" "$CLASSLA_PRED" "$TRANKIT_PRED" "$RESULTS_DIR/classla_vs_trankit.md" \
  --model-a "CLASSLA random20" --model-b "Trankit random20" --top-n 20

run "$PYTHON" scripts/content_comparison_table.py \
  "$GOLD" "$CLASSLA_PRED" "$TRANKIT_PRED" "$RESULTS_DIR/content_comparison.md" \
  --model-a "CLASSLA random20" --model-b "Trankit random20" --top-n 20 --examples-per-item 5

log "STEP 11: Build the interactive HTML comparison table"
run "$PYTHON" scripts/build_interactive_comparison_table.py \
  "$GOLD" "$CLASSLA_PRED" "$TRANKIT_PRED" \
  "$CLASSLA_TAGGED" "$TRANKIT_TAGGED" \
  "$TABLES_DIR/comparison_table.html" "$TABLES_DIR/comparison_table_data.js" \
  --run-id random20_demo --examples-per-item 5

log "STEP 12: Files now created inside the visible demo folder"
find "$DEMO_DIR" -maxdepth 2 -type f | sort | tee -a "$LOG"

log "DONE"
log "Open this table in a browser if you want the clickable example view:"
log "$TABLES_DIR/comparison_table.html"
