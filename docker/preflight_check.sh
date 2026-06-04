#!/usr/bin/env bash
# Run INSIDE the container to resolve the two "not sure" questions:
#   1. Is an NVIDIA GPU visible to this container?
#   2. Can the container reach clarin.si / HuggingFace to download the model?
#
#   docker compose build
#   docker compose run --rm eval bash docker/preflight_check.sh
# (add `--gpus all` via `docker compose run --rm --gpus all eval ...` if you want
#  to test GPU visibility too.)
set -uo pipefail

echo "=== GPU ==="
if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi -L || true
else
    echo "nvidia-smi not found in container (CPU-only unless started with --gpus all + nvidia-container-toolkit)."
fi

python - <<'PY'
import torch
print(f"torch {torch.__version__} | CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"  device: {torch.cuda.get_device_name(0)}")
PY

echo ""
echo "=== Network (model download reachability) ==="
for url in \
    "https://www.clarin.si/repository/xmlui/handle/11356/2201" \
    "https://huggingface.co/xlm-roberta-base/resolve/main/config.json" ; do
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "$url" || echo "FAIL")
    echo "  $code  $url"
done

echo ""
echo "Done. GPU usable if CUDA available == True; network OK if HTTP codes are 200/30x."
