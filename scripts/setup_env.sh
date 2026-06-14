#!/usr/bin/env bash
set -euo pipefail

CONDA_BIN="/home/nianxingyan/miniconda3/bin/conda"
ENV_NAME="nats-demo"

if "$CONDA_BIN" env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  "$CONDA_BIN" env update -n "$ENV_NAME" -f environment.yml --prune
else
  "$CONDA_BIN" env create -f environment.yml
fi

"$CONDA_BIN" run -n "$ENV_NAME" python -m pip install -e .

echo "Conda environment '$ENV_NAME' is ready."
