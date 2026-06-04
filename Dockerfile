# Trankit/CLASSLA evaluation image for the CJVT server.
# Single image works on CPU or GPU: the pinned torch==2.0.1 wheel ships CUDA
# runtime libs, so it uses an NVIDIA GPU when the container is started with
# `--gpus all` (and predict gets --trankit-gpu), and falls back to CPU otherwise.
FROM python:3.10-slim

# ca-certificates: TLS for the clarin.si / HuggingFace model downloads.
# curl: used by docker/preflight_check.sh to probe outbound network.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /project

# Install deps in their own layer so code/data changes don't trigger a reinstall.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# The project (scripts, data/gold, cache/, predictions/, results/) is mounted at
# runtime via docker-compose, so nothing else is COPYed in. Default to a shell;
# the actual run command is documented in docker/README.md.
CMD ["bash"]
